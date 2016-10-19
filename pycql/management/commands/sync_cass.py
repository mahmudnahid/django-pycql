from pycql.manager import Table
from django.core.management.base import NoArgsCommand
from django.db.models import get_apps
from pycql import query
from pycql import manager




def listTables(keyspace):
    q = query.Query('schema_columnfamilies', 'system').select('columnfamily_name')
    q.where('keyspace_name', keyspace)
    tables = q.execute()
    table_list = []
    for table in tables:
        table_list.append(table['columnfamily_name'])
    return table_list

def dropTable(keyspace, table):
    q = manager.Table(keyspace+'.'+table).drop()
    q.execute()
    try:
        pass
    except:
        raise Exception("Error dropping keyspace {}".format(keyspace))
    return True



class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        apps = get_apps()

        for app in apps:
            for obj in dir(app):
                obj = getattr(app, obj)
                if hasattr(obj, '_meta'):
                    meta = obj._meta
                    print listTables(meta.keyspace)
                    if meta.table_name in listTables(meta.keyspace):
                        msg = ''.join((
                            'Looks like you already have a `', meta.table_name,
                            '` column family in keyspace `', meta.keyspace,
                            '`. Do you want to delete and recreate it? ',
                            'All current data will be deleted! (y/n): ',
                        ))
                        resp = raw_input(msg)
                        if not resp or resp[0] != 'y':
                            print "Ok, then we're done here."
                            continue
                        dropTable(meta.keyspace, meta.table_name)

                    table = Table(meta.table_name, meta.keyspace)
                    table.create()
                    table.createColumn(meta.columns)
                    table.setPrimaryKey(meta.PRIMARY_KEY)
                    table.execute()
                    for index_column in meta.index_list:
                        table = Table(meta.table_name, meta.keyspace)
                        table.createIndex(index_column, index_column)
                        table.execute()

        print('All Done')





