import re
from collections import namedtuple


class Render(object):

    def validate(self):
        pass

    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_']}

        return functions

    def render(self, obj):

        self._placeholder = obj._placeholder
        self._main_query = obj._main_query

        render = self._main_query % self._placeholders()
        print (render)
        return str(render)


class RenderManagers(Render):

    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_'] if '_TABLE_' in self._placeholder else '',
                     '_KEYSPACE_': self._placeholder['_KEYSPACE_'] if '_KEYSPACE_' in self._placeholder else '',
                     '_COLUMNDEF_': self.__renderColumndef(),
                     '_PRIMARY-KEY_': self.__renderPK(),
                     '_OPTIONS_': self.__renderOptions(),
                     '_ALTER_': self.__renderAlter(),
                     '_REPLICATION_': self.__renderReplication(),
                     '_DURABLE-WRITES_': self.__renderDurableWrites(),
                     '_INDEX_': self._placeholder['_INDEX_'] if '_INDEX_' in self._placeholder else '',
                     '_COLUMN_': self._placeholder['_COLUMN_'] if '_COLUMN_' in self._placeholder else '',
                     }

        return functions

    def __renderReplication(self):
        if '_REPLICATION_' not in self._placeholder:
            return ''

        return 'REPLICATION = ' + str(self._placeholder['_REPLICATION_'])

    def __renderDurableWrites(self):
        if '_DURABLE-WRITES_' not in self._placeholder:
            return ''

        dw = ' AND ' if '_REPLICATION_' in self._placeholder else ''

        return dw + 'DURABLE_WRITES = ' + self._placeholder['_DURABLE-WRITES_']

    def __renderOptions(self):

        opt = ''
        if '_OPTIONS_' not in self._placeholder:
            return opt

        opt_dict = self._placeholder['_OPTIONS_']

        opt_dict['_PROPERTIES_'] = list()
        opt += 'WITH '

        compact = opt_dict.pop('compact', None)
        if compact:
            opt_dict['_PROPERTIES_'].append('COMPACT STORAGE')

        if opt_dict:
            opt_dict['_PROPERTIES_'] += (['{} = {}'.format(k, v) for (k, v) in opt_dict.items()
                                          if not re.search(r'_[A-Z-]*?_', k)])

        opt += ' AND '.join(opt_dict['_PROPERTIES_'])

        return opt

    def __renderColumndef(self):
        if '_COLUMNDEF_' in self._placeholder:
            return ', '.join(['%s %s' % (key, value) for (key, value) in self._placeholder['_COLUMNDEF_'].items()])
        else:
            return ''

    def __renderAlter(self):
        if '_ALTER-COLUMN_' in self._placeholder:
            column = self._placeholder['_ALTER-COLUMN_']
            return 'ALTER ' + column[0] + ' TYPE ' + column[1]
        if '_ADD-COLUMN_' in self._placeholder:
            column = self._placeholder['_ADD-COLUMN_']
            return 'ADD ' + column[0] + ' ' + column[1]
        if '_DROP-COLUMN_' in self._placeholder:
            return 'DROP ' + self._placeholder['_DROP-COLUMN_']
        if '_RENAME-COLUMN_' in self._placeholder:
            column = self._placeholder['_RENAME-COLUMN_']
            return 'RENAME ' + column[0] + ' TO ' + column[1]
        else:
            return ''

    def __validatePK(self):

        if '_PRIMARY-KEY_' not in self._placeholder or 'composite' not in self._placeholder['_PRIMARY-KEY_']:
            raise ValueError("Primary key must be defined")

        if '_COLUMNDEF_' not in self._placeholder:
            raise ValueError("No column found")

        pk_dict = self._placeholder['_PRIMARY-KEY_']

        for pk_type in pk_dict:
            if isinstance(pk_dict[pk_type], (tuple, list)):
                for pk in pk_dict[pk_type]:
                    if not pk in self._placeholder['_COLUMNDEF_']:
                        raise Exception('{} key {} is not a column'.format(pk_type.title(), pk))
            else:
                if not pk_dict[pk_type] in self._placeholder['_COLUMNDEF_']:
                    raise Exception('{} key {} is not a column'.format(pk_type.title(), pk_dict[pk_type]))

    def __renderPK(self):

        pk = ''

        if '_PRIMARY-KEY_' not in self._placeholder:
            return pk

        self.__validatePK()

        pk_dict = self._placeholder['_PRIMARY-KEY_']

        pk += 'PRIMARY KEY ('

        if isinstance(pk_dict['composite'], (list, tuple)):
            pk += '(' + ', '.join(pk_dict['composite']) + ')'
        else:
            pk += pk_dict['composite']

        if 'clustering' in pk_dict:
            pk += ', ' + ', '.join(pk_dict['clustering'])

        pk += ')'

        return pk


class RenderQuery(Render):
    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_'],
                     '_IDENTIFIER_': self.__renderIdentifier(),
                     '_VALUES_': self.__renderValues(),
                     '_OPTIONS_': self.__renderOptions(),
                     '_EXPR_': self.__renderExpr(),
                     '_WHERE_': self.__renderWhere(),
                     '_ORDER_': self.__renderOrder(),
                     '_LIMIT_': self.__renderLimit(),
                     '_ALLOW-FILTERING_': self.__renderAllowFiltering(),
                     '_USING_': self.__renderUsing(),
                     '_SET_': self.__renderSet(),
                     }

        return functions

    def __handleComplexOperator(self, key, value, operator):
        if operator in ('+=', '-='):
            value = str(key) + ' ' + operator[:1] + ' ' + str(value)
        elif operator == '=+':
            value = str(value) + ' + ' + str(key)

        operator = '='

        formatted = namedtuple('formatted', ['key', 'value', 'operator'])

        return formatted(key, value, operator)

    def __renderSet(self):
        if '_SET_' not in self._placeholder or not self._placeholder['_SET_']:
            return ''

        wrapStr = lambda string, wrapper: wrapper + str(string) + wrapper

        for n, row in enumerate(self._placeholder['_SET_']):
            if isinstance(row.value, (str, unicode)) and not row.no_string and row.key[-6:] != '__uuid':
                value = wrapStr(row.value, "'")
            elif isinstance(row.value, (set)):
                value = '{' + str(tuple(row.value))[1:-1].strip(',') + '}'
            else:
                value = str(row.value)

            formatted = self.__handleComplexOperator(row.key, value, row.operator)
            self._placeholder['_SET_'][n] = str(formatted.key) + wrapStr(str(formatted.operator), ' ') + formatted.value

        return 'SET ' + ', '.join(self._placeholder['_SET_']) + ' '

    def __renderUsing(self):
        if '_USING_' not in self._placeholder:
            return ''
        elif isinstance(self._placeholder['_USING_'], int):
            return "USING TIMESTAMP " + str(self._placeholder['_USING_']) + ' '

    def __renderExpr(self):
        if '_EXPR_' not in self._placeholder:
            return ''
        elif isinstance('_EXPR', str):
            return self._placeholder['_EXPR_'] + ' '

    def __renderWhere(self):
        if '_WHERE_' not in self._placeholder:
            return ''

        wrapStr = lambda string, wrapper: wrapper + str(string) + wrapper

        for n, tuples in enumerate(self._placeholder['_WHERE_']):

            if isinstance(tuples[1], (str, unicode)) and not tuples[3] and tuples[0][-6:] != '__uuid':
                value = wrapStr(tuples[1], "'")
            else:
                value = str(tuples[1])

            self._placeholder['_WHERE_'][n] = str(tuples[0]) + wrapStr(str(tuples[2]), ' ') + value

        return 'WHERE ' + ' AND '.join(self._placeholder['_WHERE_']) + ' '

    def __renderOrder(self):
        if '_ORDER_' not in self._placeholder:
            return ''

        order = self._placeholder['_ORDER_']

        return 'ORDER BY ' + order[0] + ' ' + order[1].upper() + ' '

    def __renderLimit(self):
        if '_LIMIT_' not in self._placeholder:
            return ''
        return 'LIMIT ' + self._placeholder['_LIMIT_'] + ' '

    def __renderAllowFiltering(self):
        if '_ALLOW-FILTERING_' not in self._placeholder:
            return ''
        else:
            return 'ALLOW FILTERING'

    def __renderIdentifier(self):
        if '_IDENTIFIER_' not in self._placeholder:
            # raise Exception('Identifier missing in query')
            return ''
        elif not isinstance(self._placeholder['_IDENTIFIER_'], dict):
            raise Exception('Dictonay type expected')

        identifier = self._placeholder['_IDENTIFIER_']
        key = list()
        value = list()
        wrapStr = lambda string, wrapper: wrapper + str(string) + wrapper

        for k, v in identifier.items():
            key.append(k)
            if not isinstance(v, (list, set, dict)):
                value.append(str(v) if k[-6:] == '__uuid' or not isinstance(v, str) else wrapStr(v, "'"))
            elif isinstance(v, set):
                v = '{' + ', '.join(list(v) if k[-6:] == '__uuid' else [wrapStr(item, "'") for item in v]) + '}'
                value.append(v)
            elif isinstance(v, list):
                v = '[' + ', '.join(list(v) if k[-6:] == '__uuid' else [wrapStr(item, "'") for item in v]) + ']'
                value.append(v)
            elif isinstance(v, dict):
                value.append(str(v))

        self._placeholder['_VALUES_'] = ', '.join(value)
        return ', '.join(key)

    def __renderValues(self):

        if '_VALUES_' not in self._placeholder:
            value = self.__renderIdentifier()
        else:
            value = self._placeholder['_VALUES_']

        return value

    def __renderOptions(self):
        if '_OPTIONS_' in self._placeholder and '_TTL_' in self._placeholder['_OPTIONS_']:
            return 'USING TTL ' + str(self._placeholder['_OPTIONS_']['_TTL_']) + ' '
        else:
            return ''
