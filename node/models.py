from pycql.base import Model


class Node(Model):

    class Meta:
        keyspace = 'blog'
        columns = { 'nid' : 'varchar',
                    'title': 'varchar',
                    'body': 'text',
                    'author': 'varchar',
                    'node_timestamp': 'bigint',
                    'revision_log' : 'text',
                    'is_front_page': 'boolean',
                    'is_sticky': 'boolean',
                    'is_published': 'boolean',
                    # 'tags': 'text',
                    'can_comment': 'boolean',
                    'node_type': 'varchar'
        }


        PRIMARY_KEY = ['nid', 'is_published', 'node_timestamp']


# class NodeCount(Model):
#
#     class Meta:
#         keyspace = 'blog'
#         columns = {'views' : 'counter',
#                    'nid' : 'uuid',
#                    'title': 'varchar'
#         }
#         PRIMARY_KEY = ['nid', 'title']


