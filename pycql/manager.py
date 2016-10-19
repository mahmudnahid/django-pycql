
from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
from cassandra import decoder
from pycql.render import RenderManagers

class Keyspace(object):
    def __init__(self, keyspace):

        self._placeholder = dict()

        self._placeholder['_KEYSPACE_'] = keyspace
        self._main_query = ""

    def replication(self, map):
        if not isinstance(map, dict):
            raise TypeError("Datatype mismatch. Dictionary expected")
        elif 'class' in map and map['class'] not in ('SimpleStrategy', 'NetworkTopologyStrategy'):
            raise ValueError("Replication factor 'class' contains unsupported value")
        elif 'replication_factor' in map and not isinstance(map['replication_factor'], int):
            raise ValueError("Replication factor must be integer")

        self._placeholder['_REPLICATION_'] = map

        return self

    def durableWrites(self, value=True):
        self._placeholder['_DURABLE-WRITES_'] = str(value).lower()
        return self

    def create(self):
        self._main_query = "CREATE KEYSPACE %(_KEYSPACE_)s WITH %(_REPLICATION_)s%(_DURABLE-WRITES_)s"
        return self

    def alter(self):
        self._main_query = "ALTER KEYSPACE %(_KEYSPACE_)s WITH %(_REPLICATION_)s%(_DURABLE-WRITES_)s"
        return self

    def drop(self):
        self._main_query = "DROP KEYSPACE %(_KEYSPACE_)s"
        return self

    def execute(self, return_type='dict', renderOnly=False):
        rendered = RenderManagers().render(self)
        if renderOnly:
            return rendered

        cluster = Cluster()
        cluster.connection_class = LibevConnection
        connection = cluster.connect()
        connection.row_factory = getattr(decoder, return_type + '_factory', 'dict_factory')

        return connection.execute(rendered)

class Table(object):
    def __init__(self, table_name, keyspace=None):

        # __default_keyspace = 'demodb'
        # keyspace = keyspace if keyspace is not None else __default_keyspace
        # self._placeholder['_TABLE_'] = keyspace + '.' + table_name

        self.__table = keyspace + '.' + table_name if keyspace else table_name

    def _init(self):
        self._placeholder = dict()
        self._placeholder['_TABLE_'] = self.__table

    def createIndex(self, name, col_name):
        self._init()
        self._main_query = 'CREATE INDEX %(_INDEX_)sON %(_TABLE_)s (%(_COLUMN_)s)'
        self._placeholder['_INDEX_'] = str(name) + ' ' if name else ''
        self._placeholder['_COLUMN_'] = str(col_name)
        return self

    def dropIndex(self, name):
        self._init()
        self._main_query = 'DROP INDEX %(_INDEX_)s'
        self._placeholder['_INDEX_'] = str(name)
        return self

    def drop(self):
        self._init()
        self._main_query = 'DROP TABLE %(_TABLE_)s'
        return self

    def execute(self, return_type='dict', renderOnly=False):
        rendered = RenderManagers().render(self)
        if renderOnly:
            return rendered

        cluster = Cluster()
        cluster.connection_class = LibevConnection
        connection = cluster.connect()
        connection.row_factory = getattr(decoder, return_type + '_factory', 'dict_factory')

        return connection.execute(rendered)

    # after alter()
    def dropColumn(self, column):
        self._placeholder['_DROP-COLUMN_'] = column

    # after alter()
    def renameColumn(self, *columns):
        if columns:
            self._placeholder['_RENAME-COLUMN_'] = columns

    # after alter()
    def alterColumn(self, *columns):
        """
        These changes to a column type are not allowed:
            * Changing the type of a clustering column.
            * Changing columns on which an index is defined.

        :param columns:
        :return: :raise:
        """
        self._placeholder['cql-type'] = '_ALTER-COLUMN_'
        if columns and len(columns) == 2:
            self._placeholder['_ALTER-COLUMN_'] = columns
            # Todo validate cql-type and string
        return self

    # after alter()
    def addColumn(self, *columns):
        """
        These additions to a table are not allowed:
            * Adding a column having the same name as an existing column.
            * Adding columns to tables defined with COMPACT STORAGE.
        """
        self._placeholder['cql-type'] = '_ADD-COLUMN_'
        if columns and len(columns) == 2:
            self._placeholder['_ADD-COLUMN_'] = columns
            # Todo validate cql-type and string
        return self
    ######################################################################

    def options(self, *args, **kwargs):
        self.optionsList = ('compression', 'compaction', 'compact', 'bloom_filter_fp_chance', 'caching', 'comment',
                            'dclocal_read_repair_chance', 'gc_grace_seconds', 'read_repair_chance', 'replicate_on_write')


        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                if k not in self.optionsList:
                    raise Exception('Invalid option')
        elif kwargs:
            for k, v in kwargs.items():
                if k not in self.optionsList:
                    raise Exception('Invalid option')

            if '_OPTIONS_' in self._placeholder:
                self._placeholder['_OPTIONS_'].update(kwargs)
            else:
                self._placeholder['_OPTIONS_'] = kwargs

        return self

    def _setPlaceholderKey(self, key, value_type):
        if key not in self._placeholder or not self._placeholder[key]:
            # if provided key is not available or if the value is empty
            self._placeholder[key] = value_type

    def createColumn(self, *columns):
        """
        Add columns to dictionary. All key and values will be rendered when execute is called.

        :param columns:
        :return: :raise:
        """
        if columns:
            self._setPlaceholderKey('_COLUMNDEF_', dict())

            if isinstance(columns[0], str) and len(columns) == 2:
                self._placeholder['_COLUMNDEF_'].update({columns[0]: columns[1]})
                # print(self._placeholder)
            elif isinstance(columns[0], str) and columns[2] is True:
                self._placeholder['_COLUMNDEF_'].update({columns[0]: columns[1]})
                self.setPrimaryKey(columns[0])
            elif isinstance(columns[0], dict) and len(columns) == 1:
                self._placeholder['_COLUMNDEF_'].update(columns[0])
                # print(self._placeholder)
            else:
                raise Exception("Invalid Column Definition")

        return self

    def setPrimaryKey(self, keys):
        self._placeholder['_PRIMARY-KEY_'] = dict()

        first = True

        for key in keys:
            if first:
                first = False
                if isinstance(key, (str, tuple, list)):
                    self._placeholder['_PRIMARY-KEY_']['composite'] = key
                else:
                    raise Exception("Invalid Primary Key")
            else:
                if 'clustering' not in self._placeholder['_PRIMARY-KEY_'] or not self._placeholder['_PRIMARY-KEY_']['clustering']:
                    self._placeholder['_PRIMARY-KEY_']['clustering'] = list()
                self._placeholder['_PRIMARY-KEY_']['clustering'].append(key)

    def create(self):
        self._init()
        self._main_query = 'CREATE TABLE %(_TABLE_)s ( %(_COLUMNDEF_)s, %(_PRIMARY-KEY_)s ) %(_OPTIONS_)s'
        return self


    def alter(self):
        self._init()
        self._main_query = 'ALTER TABLE %(_TABLE_)s %(_ALTER_)s %(_OPTIONS_)s'
        return self







# class Column(object):
#
#     def __init__(self, obj):
#         self._main_query = obj._main_query
#         self._placeholder = obj._placeholder
#
#     def _setCqlType(self, name, cql_type, collection=None):
#         pass
#
#     def type_ascii(self, name, collection=None):
#         self._setCqlType(name, 'ascii', collection)
#
#     def type_bigint(self, name, collection=None):
#         self._setCqlType(name, 'bigint', collection)
#
#     def type_blob(self, name, collection=None):
#         self._setCqlType(name, 'blob', collection)
#
#     def type_boolean(self, name, collection=None):
#         self._setCqlType(name, 'boolean', collection)
#
#     def type_counter(self, name, collection=None):
#         self._setCqlType(name, 'counter', collection)
#
#     def type_decimal(self, name, collection=None):
#         self._setCqlType(name, 'decimal', collection)
#
#     def type_double(self, name, collection=None):
#         self._setCqlType(name, 'double', collection)
#
#     def type_float(self, name, collection=None):
#         self._setCqlType(name, 'float', collection)
#
#     def type_inet(self, name, collection=None):
#         self._setCqlType(name, 'inet', collection)
#
#     def type_int(self, name, collection=None):
#         self._setCqlType(name, 'int', collection)
#
#     def type_text(self, name, collection=None):
#         self._setCqlType(name, 'text', collection)
#
#     def type_timestamp(self, name, collection=None):
#         self._setCqlType(name, 'timestamp', collection)
#
#     def type_uuid(self, name, collection=None):
#         self._setCqlType(name, 'uuid', collection)
#
#     def type_timeuuid(self, name, collection=None):
#         self._setCqlType(name, 'timeuuid', collection)
#
#     def type_varchar(self, name, collection=None):
#         self._setCqlType(name, 'varchar', collection)
#
#     def type_varint(self, name, collection=None):
#         self._setCqlType(name, 'varint', collection)
#
#     # Method for set, list and map
#     def type_list(self, name, cql_type):
#         self._setCqlType(name, cql_type, 'list')
#
#     def type_set(self, name, cql_type):
#         self._setCqlType(name, cql_type, 'set')
#
#     def type_map(self, name, cql_type):
#         self._setCqlType(name, cql_type, 'map')
#
#     def addColumn(self, *columns):
#         return self
#
#
# class CreateColumn(Column):
#
#     def _setPlaceholderKey(self, key, value_type):
#         if key not in self._placeholder or not self._placeholder[key]:
#             # if provided key is not available or if the value is empty
#             self._placeholder[key] = value_type
#
#     def _setCqlType(self, name, cql_type, collection=None):
#         """
#         Type function to set cql data type of Columns
#
#         :param name: String
#         :param cql_type: String (general) or Tuple (if collection == 'map')
#         :param collection: 'set' | 'list'
#         """
#         self._setPlaceholderKey('_COLUMNDEF_', dict())
#
#         if collection in ('set', 'list'):
#             cql_type = str(collection) + '<' + str(cql_type) + '>'
#         elif collection is True:
#             self.setPrimaryKey(name)
#         elif collection == 'map' and isinstance(cql_type, tuple):
#             cql_type = collection + '<' + ', '.join(cql_type) + '>'
#
#         self._placeholder['_COLUMNDEF_'].update({name: cql_type})
#
#
#
# class AlterColumn(Column):
#
#     def _setCqlType(self, name, cql_type, collection=None):
#
#         if collection in ('set', 'list'):
#             cql_type = str(collection) + '<' + str(cql_type) + '>'
#         elif collection == 'map' and isinstance(cql_type, tuple):
#             cql_type = collection + '<' + ', '.join(cql_type) + '>'
#
#         self._placeholder[self._placeholder['cql-type']] = (name, cql_type)





