import re
import sys

from django.utils import six

from pycql.query import Query


TRANSIT_NAMES = ('bloom_filter_fp_chance', 'caching',
                 'comment', 'compaction', 'compression',
                 'dclocal_read_repair_chance', 'gc_grace_seconds',
                 'read_repair_chance', 'replicate_on_write' , 'columns',
                 'PRIMARY_KEY', 'keyspace', 'index_list',
)


class Options(object):

    def __init__(self, attr_meta, table_name, app_label=None):

        self.meta = attr_meta
        self.table_name = table_name
        self.app_label = app_label
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in TRANSIT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))



class ModelMetaClass(type):
    """
    Meta class for all models
    """
    def __new__(cls, name, bases, attrs):

        super_new = super(ModelMetaClass, cls).__new__

        # Ignore Model itself when creating class with six.with_metaclass()
        if name == 'Model' or name == 'NewBase':
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        # Get Meta inner class
        if not attr_meta:
            raise AttributeError(
                "Meta class not found. Please define atleast the PRIMARY_KEY for your table"
            )

        if getattr(attr_meta, 'app_label', None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            model_module = sys.modules[new_class.__module__]
            kwargs = {'app_label': model_module.__name__.split('.')[-2]}
        else:
            kwargs = {}

        verbose_name = lambda class_name: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '\\1', class_name).lower().strip()
        table_name = verbose_name(new_class.__name__)

        # Set all the Meta data as attributes of the object
        setattr(new_class, '_meta', Options(attr_meta, table_name, **kwargs))


        #prepare interface for the Query class by adding a objects attribute
        # which will be accessible for using the query methods
        query = attrs.pop('objects', None)
        table = verbose_name(new_class.__name__)
        query_object = Query(table, attr_meta.keyspace)

        setattr(new_class, 'objects', query_object)


        return new_class


class Model(six.with_metaclass(ModelMetaClass)):

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

    def insert(self, data):
        return self.__class__.objects.insert(data)

    def select(self, *args):
        return self.__class__.objects.select(*args)

    def delete(self, *args):
        return self.__class__.objects.delete(*args)

    def update(self, data):
        return self.__class__.objects.update(data)


