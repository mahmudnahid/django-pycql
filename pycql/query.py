from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
from cassandra import decoder
from pycql.render import RenderQuery
from collections import namedtuple


class Query(object):
    def __init__(self, table_name, keyspace=None):
        self._main_query = ''
        self.__table = keyspace + '.' + table_name if keyspace else table_name

    def _init(self):
        self._placeholder = dict()
        self._placeholder['_TABLE_'] = self.__table

    def execute(self, return_type='dict', renderOnly=False):
        # print self._placeholder
        rendered = RenderQuery().render(self)
        if renderOnly:
            return rendered

        cluster = Cluster()
        cluster.connection_class = LibevConnection
        connection = cluster.connect()
        connection.row_factory = getattr(decoder, return_type + '_factory', 'dict_factory')

        return connection.execute(rendered)

    def select(self, *columns):
        self._init()
        self._main_query = "SELECT %(_EXPR_)sFROM %(_TABLE_)s " \
                           "%(_WHERE_)s%(_ORDER_)s" \
                           "%(_LIMIT_)s%(_ALLOW-FILTERING_)s"
        if not columns:
            self._placeholder['_EXPR_'] = '*'
        elif columns and isinstance(columns[0], str):
            self._placeholder['_EXPR_'] = ', '.join(columns)
            # print self._placeholder['_EXPR_']
        elif columns and isinstance(columns[0], (tuple, list, set)):
            self._placeholder['_EXPR_'] = ', '.join(columns[0])
        return self

    def allowFiltering(self):
        self._placeholder['_ALLOW-FILTERING_'] = True
        return self

    def limit(self, limit):
        if isinstance(limit, int):
            self._placeholder['_LIMIT_'] = str(limit)
        return self

    def count(self):
        self._placeholder['_EXPR_'] = 'COUNT(*)'
        return self

    def writetime(self, col_name):
        self._placeholder['_EXPR_'] = 'WRITETIME (' + col_name + ')'
        return self

    def orderBy(self, col_name, order='ASC'):
        self._placeholder['_ORDER_'] = (col_name, order)

    def compareToken(self, key, value, comparator='=', term_only=False):

        key = 'TOKEN (' + key + ')'
        if isinstance(value, str):
            value = "'" + value + "'"

        value = value if term_only else 'TOKEN (' + str(value) + ')'

        return self.compare(key, value, comparator, True)

    def insert(self, data):
        # Todo: Options

        self._main_query = "INSERT INTO %(_TABLE_)s ( %(_IDENTIFIER_)s ) VALUES ( %(_VALUES_)s ) %(_OPTIONS_)s"
        self._init()
        if not isinstance(data, dict):
            raise Exception("Dictionary type data expected for insert query")

        self._placeholder['_IDENTIFIER_'] = data

        return self

    def ttl_select(self, col_name):
        self._placeholder['_EXPR_'] = 'TTL (' + col_name + ')'
        return self

    # for update
    def ttl(self, duration, human_readable='sec'):
        """
        Set TTL (Time to Live) for a data

        :param duration:
        :param human_readable: [default 's'] calculate second from human readable time
        :return:
        """

        if human_readable == 'min':
            duration *= 60
        elif human_readable == 'hr':
            duration *= 3600
        elif human_readable == 'day':
            duration *= 86400

        self._placeholder['_OPTIONS_'] = dict({'_TTL_': duration})

        return self

    def delete(self, *columns):
        self._init()
        self._main_query = "DELETE %(_EXPR_)sFROM %(_TABLE_)s " \
                           "%(_USING_)s%(_WHERE_)s"

        if columns and isinstance(columns[0], str):
            self._placeholder['_EXPR_'] = ', '.join(columns)
        elif columns and isinstance(columns[0], (tuple, list, set)):
            self._placeholder['_EXPR_'] = ', '.join(columns[0])
        return self

    def where(self, key, value, comparator='=', no_string=False):
        if not isinstance(key, str):
            raise Exception("Compare key type mismatched")

        if '_WHERE_' not in self._placeholder:
            self._placeholder['_WHERE_'] = list()

        self._placeholder['_WHERE_'].append((key, value, comparator, no_string))

        return self

    def using(self, timestamp):
        timestamp = int(timestamp)

        self._placeholder['_USING_'] = timestamp

        return self

    def update(self, *args, **kwargs):
        """
        Update data with CQL
        Expected Format:
            update(key, value, operator, no_string)
                >> to update single row where value is string
            update({key: value, key: value, ... } # receives dictionary
                >> to update multiple value with '=' operator where value is string
            update([(key, value, operator, no_string), (key, value, operator, no_string), ...])
                >> to update multiple value with full control

            Here- key must be string
                  value can be any cql data type (dictionary format only except string value)

        """
        self._init()
        self._main_query = "UPDATE %(_TABLE_)s %(_OPTIONS_)s%(_SET_)s%(_WHERE_)s"

        operator = '=' if 'operator' not in kwargs else kwargs['operator']
        no_string = False if 'no_string' not in kwargs else kwargs['no_string']
        row = namedtuple('row', ['key', 'value', 'operator', 'no_string'])

        if '_SET_' not in self._placeholder:
            self._placeholder['_SET_'] = list()

        if not args and not kwargs:
            return self

        if isinstance(args[0], (str, unicode)) and (len(args) in (2, 3)):
            pass

        if isinstance(args[0], dict) and len(args) == 1:
            keyvalues = args[0]
            # print(keyvalues)

            for key, value in keyvalues.items():
                self._placeholder['_SET_'].append(row(key, value, operator, no_string))
                # print(self._placeholder['_SET_'])

        if isinstance(args[0], tuple) and len(args) == 1:
            keyvalues = args[0]
            operator = operator if len(keyvalues) < 3 else keyvalues[2]
            no_string = no_string if len(keyvalues) < 4 else keyvalues[3]

            key = keyvalues[0]
            value = keyvalues[1]

            self._placeholder['_SET_'].append(row(key, value, operator, no_string))

        return self


