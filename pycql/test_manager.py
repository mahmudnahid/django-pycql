from pycql import manager


def test_create_table():
#
#     ###
#     ### Add column test
#     ###
#
#     # Create table
#     user = manager.Table('user').create()
#     # assert str(user)[:42] == '<pycql.object_mapper.CreateTable object at'
#
#     # Add column Tuple
#     user.createColumn('uid', 'uuid')
#     # assert user._placeholder['_COLUMNDEF_']['uid'] == 'uuid'
#
#     # Add column Dictionary
#     user._placeholder['_COLUMNDEF_'] = ''
#     user.createColumn({'uid': 'uuid', 'email': 'text'})
#     assert user._placeholder['_COLUMNDEF_']['uid'] is 'uuid' and user._placeholder['_COLUMNDEF_']['email'] is 'text'
#
#     # Add column as type
#     user._placeholder['_COLUMNDEF_'] = ''
#     user.createColumn().type_ascii('char')
#     assert user._placeholder['_COLUMNDEF_']['char'] == 'ascii'
#
#     user.createColumn().type_varchar('username')
#     assert user._placeholder['_COLUMNDEF_']['username'] == 'varchar'
#
#     # Add column with collection as type
#     user._placeholder['_COLUMNDEF_'] = 0
#     user.createColumn().type_text('email', 'set')
#     assert user._placeholder['_COLUMNDEF_']['email'] == 'set<text>'
#
#     # Add column as collection
#     user._placeholder['_COLUMNDEF_'] = {}
#     user.createColumn().type_list('fav_post', 'varchar')
#     assert user._placeholder['_COLUMNDEF_']['fav_post'] == 'list<varchar>'
#
#     # Add column as map
#     user._placeholder['_COLUMNDEF_'] = {}
#     user.createColumn().type_map('todo', ('timestamp', 'text'))
#     assert user._placeholder['_COLUMNDEF_']['todo'] == 'map<timestamp, text>'
#
#     # Add column as type with primary key
#     user._placeholder['_COLUMNDEF_'] = {}
#     user.createColumn({'name': 'varchar', 'email': 'text'})
#     user.createColumn().type_uuid('uid', True)
#     assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
#
    # Set primary key
    user = manager.Table('timeseries', 'demodb').create()
    user.createColumn({'event_type': 'text', 'insertion_time': 'timestamp', 'event': 'blob'})
    user.setPrimaryKey([['event_type', 'event'], 'insertion_time'])
    print user._placeholder
    assert user.execute(renderOnly=True) == "CREATE TABLE demodb.timeseries ( insertion_time timestamp, event_type text, event blob, PRIMARY KEY ((event_type, event), insertion_time) ) "

#
#     # Set compound primary key
#     user._placeholder['_COLUMNDEF_'] = {}
#     user.createColumn({'name': 'varchar', 'email': 'text'})
#     user.createColumn().type_uuid('uid')
#     user.setPrimaryKey('uid', 'email')
#     assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
#     assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['email']
#
#     # Set compound primary key with multiple clustering key
#     user.setPrimaryKey('uid', 'username', 'phone')
#     assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
#     assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['username', 'phone']
#
#     # Set composite primary key with multiple composite key and multiple clustering key
#     user.setPrimaryKey(('uid', 'timezone'), 'username', 'phone')
#     assert user._placeholder['_PRIMARY-KEY_']['composite'] == ['uid', 'timezone']
#     assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['username', 'phone']
#     user.options(compact=True)
#
#     ###
#     ###  Render Functions test
#     ###
#     renderUser = user
#     renderUser.createColumn('username', 'text')
#     renderUser.createColumn('phone', 'text')
#     renderUser.setPrimaryKey('uid', 'username', 'phone')
#     render = renderUser.execute(renderOnly=True)
#     assert 'PRIMARY KEY (uid, username, phone)' in render
#
#     renderUser.createColumn().type_timeuuid('timezone')
#     renderUser.setPrimaryKey(('uid', 'timezone'), 'username', 'phone')
#     render = renderUser.execute(renderOnly=True)
#     assert 'PRIMARY KEY ((uid, timezone), username, phone)' in render (((uid, date), sdfe, sdfle ))
#
#     renderUser.setPrimaryKey('uid')
#     render = renderUser.execute(renderOnly=True)
#     assert 'PRIMARY KEY (uid)' in render
#
#     ###
#     ### Table Options test
#     ###
#     user = manager.Table('user').create()
#     user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
#     render = user.execute(renderOnly=True)
#     assert "WITH compression = {'hi': 'guys', 'hello': 'guys'} " \
#            "AND compaction = {'class': 'sdf'}" in render
#
#     user = manager.Table('user').create()
#     user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
#     user.options(caching='hellow', comment='hou mou')
#     render = user.execute(renderOnly=True)
#     assert "WITH caching = hellow AND comment = hou mou AND compression = {'hi': 'guys', 'hello': 'guys'} " \
#            "AND compaction = {'class': 'sdf'}" in render
#
#     user = manager.Table('user').create()
#     user.createColumn('uid', 'uuid')
#     user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
#     user.options(caching='hellow', comment='hou mou')
#     user.options(compact=True)
#     render = user.execute(renderOnly=True)
#     assert "WITH COMPACT STORAGE AND comment = hou mou AND compression = {'hi': 'guys', 'hello': 'guys'} " \
#            "AND compaction = {'class': 'sdf'} AND caching = hellow" in render
#
#
#     "CREATE TABLE users (user_name varchar PRIMARY KEY,password varchar,gender varchar,session_token varchar,state varchar,birth_year bigint)"
#     "CREATE TABLE emp (empID int,deptID int,first_name varchar,last_name varchar,PRIMARY KEY (empID, deptID))"
#     "CREATE TABLE Cats (block_id uuid,breed text,color text,short_hair boolean,PRIMARY KEY ((block_id, breed), color, short_hair))"
#     "CREATE TABLE users (; userid text PRIMARY KEY,; first_name text,; last_name text,; emails set<text>,; top_scores list<int>,; todo map<timestamp, text>)"
#     "CREATE TABLE MonkeyTypes ( block_id uuid, species text, alias text, population varint, PRIMARY KEY (block_id)) WITH comment='Important biological records' AND read_repair_chance = 1.0;"
#     "CREATE TABLE DogTypes ( block_id uuid, species text, alias text, population varint, PRIMARY KEY (block_id)) WITH compression = { 'sstable_compression' : 'DeflateCompressor', 'chunk_length_kb' : 64 } AND compaction = { 'class' : 'SizeTieredCompactionStrategy', 'min_threshold' : 6 }"
#     "CREATE TABLE sblocks ( block_id uuid, subblock_id uuid, data blob, PRIMARY KEY (block_id, subblock_id)) WITH COMPACT STORAGE"
#     "create table timeseries ( event_type text, insertion_time timestamp, event blob, PRIMARY KEY (event_type, insertion_time)) WITH CLUSTERING ORDER BY (insertion_time DESC)"
#     ""
#
#     "CREATE TABLE users (user_name varchar PRIMARY KEY,password varchar,gender varchar,session_token varchar,state varchar,birth_year bigint)"
#     "CREATE TABLE emp (empID int,deptID int,first_name varchar,last_name varchar,PRIMARY KEY (empID, deptID))"
#     "CREATE TABLE Cats (block_id uuid,breed text,color text,short_hair boolean,PRIMARY KEY ((block_id, breed), color, short_hair))"
#     "CREATE TABLE users (; userid text PRIMARY KEY,; first_name text,; last_name text,; emails set<text>,; top_scores list<int>,; todo map<timestamp, text>)"
#     "CREATE TABLE MonkeyTypes (; block_id uuid,; species text,; alias text,; population varint,; PRIMARY KEY (block_id)); WITH comment='Important biological records'; AND read_repair_chance = 1.0;"
#     "CREATE TABLE DogTypes (; block_id uuid,; species text,; alias text,; population varint,; PRIMARY KEY (block_id)) WITH compression =; { 'sstable_compression' : 'DeflateCompressor', 'chunk_length_kb' : 64 }; AND compaction =; { 'class' : 'SizeTieredCompactionStrategy', 'min_threshold' : 6 };"
#     "CREATE TABLE sblocks (; block_id uuid,; subblock_id uuid,; data blob,; PRIMARY KEY (block_id, subblock_id)); WITH COMPACT STORAGE;"
#     "create table timeseries (; event_type text,; insertion_time timestamp,; event blob,; PRIMARY KEY (event_type, insertion_time)); WITH CLUSTERING ORDER BY (insertion_time DESC);"
#     ""
#
#     """
#     CREATE TABLE ruling_stewards ( steward_name text, king text, reign_start int, event text, PRIMARY KEY (steward_name, king, reign_start) )
#     CREATE TABLE periods ( period_name text, event_name text, event_date timestamp, weak_race text, strong_race text, PRIMARY KEY (period_name, event_name, event_date)
#     CREATE TABLE users ( user_name varchar, password varchar, gender varchar, session_token varchar, state varchar, birth_year bigint, PRIMARY KEY (user_name))
#     CREATE TABLE excelsior.clicks ( userid uuid, url text, date timestamp, //unrelated to WRITETIME discussed in the next section name text, PRIMARY KEY (userid, url) )
#     CREATE TABLE users ( user_id text PRIMARY KEY, first_name text, last_name text, emails set<text> )
#     CREATE TABLE test ( k int PRIMARY KEY, v1 int, v2 int )
#     CREATE TABLE counterks.page_view_counts (counter_value counter, url_name varchar, page_name varchar, PRIMARY KEY (url_name, page_name) )
#     CREATE TABLE test ( Foo int PRIMARY KEY, "Bar" int )
#     CREATE TABLE test( id varchar PRIMARY KEY, value_double double, value_float float )
#     CREATE TABLE myschema.users ( userID uuid, fname text, lname text, email text,address text, zip int, state text, PRIMARY KEY (userID) )
#     CREATE TABLE timeline ( user_id varchar, email_id uuid, author varchar, body varchar, PRIMARY KEY (user_id, email_id) )
#
#
#
#     """
#
#
# def test_alter_table():
#     ###
#     ### Table Alter Test
#     ###
#
#     # Alter Column
#     """
#
#
#     """
#     user = manager.Table('adamsFamily', 'monsters').alter()
#     user.alterColumn('lastKnownLocation', 'uuid')
#     user.options(compact=True)
#     render = user.execute(renderOnly=True)
#     assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE uuid WITH COMPACT STORAGE'
#
#     # Alter Column with type syntax
#     user = manager.Table('adamsFamily', 'monsters').alter()
#     user.alterColumn().type_uuid('lastKnownLocation')
#     user.options(compact=True)
#     render = user.execute(renderOnly=True)
#     assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE uuid WITH COMPACT STORAGE'
#
#     # Alter column with map type
#     user = manager.Table('adamsFamily', 'monsters').alter()
#     user.alterColumn().type_map('lastKnownLocation', ('uuid', 'text'))
#     user.options(compact=True)
#     render = user.execute(renderOnly=True)
#     assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE map<uuid, text> ' \
#                      'WITH COMPACT STORAGE'
#
#     # Add column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.addColumn('gravesite', 'varchar')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily ADD gravesite varchar'
#
#     # Add column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.addColumn('top_places', 'list<text>')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily ADD top_places list<text>'
#
#     # Add column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.addColumn().type_text('top_places', 'list')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily ADD top_places list<text>'
#
#     # Add column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.addColumn().type_list('top_places', 'text')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily ADD top_places list<text>'
#
#     # Drop column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.dropColumn('gender')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily DROP gender'
#
#     # Rename column
#     user = manager.Table('addamsFamily', 'monsters').alter()
#     user.renameColumn('gender', 'gonder')
#     render = user.execute(renderOnly=True)
#     assert render.strip() == 'ALTER TABLE monsters.addamsFamily RENAME gender TO gonder'
#
#     # TEST BY GIASH
#     # Alter column
#     user = manager.Table('addamsFamily').alter()
#     user.alterColumn('plot_number', 'uuid')
#     render = user.execute(renderOnly=True)
#     assert render.strip() =='ALTER TABLE addamsFamily ALTER plot_number TYPE uuid'
#
#
#
#     """
#     ALTER TABLE users ADD coupon_code varchar;
#     ALTER TABLE users ALTER coupon_code TYPE int;
#     ALTER TABLE users ADD top_places list<text>
#     ALTER TABLE users ADD todo map<timestamp, text>
#     ALTER TABLE addamsFamily ADD gravesite varchar
#     ALTER TABLE users ADD top_places list<text>
#     ALTER TABLE addamsFamily DROP gender
#     ALTER TABLE addamsFamily WITH comment = 'A most excellent and useful table' AND read_repair_chance = 0.2
#     ALTER TABLE addamsFamily WITH compression = { 'sstable_compression' : 'DeflateCompressor', 'chunk_length_kb' : 64 }
#     ALTER TABLE users WITH compaction = { 'class' : 'SizeTieredCompactionStrategy', 'min_threshold' : 6 }
#     ALTER USER moss WITH PASSWORD 'bestReceiver'
#     """
#
# def test_drop_table():
#
#     node = manager.Table('worldSeriesAttendees').drop()
#     assert node.execute(renderOnly=True) == "DROP TABLE worldSeriesAttendees"
#
#
#     """
#     DROP TABLE users
#     DROP KEYSPACE demodb
#     """
#
#
# def test_create_keyspace():
#
#     excelsior = manager.Keyspace('Excelsior').create().replication({'class': 'SimpleStrategy', 'replication_factor': 3})
#     assert excelsior.execute(renderOnly=True).strip() == "CREATE KEYSPACE Excelsior " \
#                                          "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3}"
#
#     replication = {'class': 'NetworkTopologyStrategy', 'dc1': 3, 'dc2': 2}
#     excalibur = manager.Keyspace("'Excalibur'").create().replication(replication)
#     assert excalibur.execute(renderOnly=True).strip() == "CREATE KEYSPACE 'Excalibur' " \
#                                          "WITH REPLICATION = {'dc2': 2, 'class': 'NetworkTopologyStrategy', 'dc1': 3}"
#
#     replication = {'class': 'NetworkTopologyStrategy', 'dc1': 1}
#     excalibur = manager.Keyspace("Risky").create().replication(replication).durableWrites(False)
#     assert excalibur.execute(renderOnly=True) == "CREATE KEYSPACE Risky " \
#                                  "WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'dc1': 1} " \
#                                  "AND DURABLE_WRITES = false"
#
#     # test by gias
#     demodb = manager.Keyspace('demodb').create().replication({'class': 'SimpleStrategy', 'replication_factor': 3})
#     assert demodb.execute(renderOnly=True).strip() == "CREATE KEYSPACE demodb WITH REPLICATION = " \
#                               "{'class': 'SimpleStrategy', 'replication_factor': 3}"
#
#
#     """
#     CREATE KEYSPACE counterks WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }
#     ALTER KEYSPACE "Excalibur" WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }
#     CREATE KEYSPACE "Excalibur" WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc1' : 3, 'dc2' : 2};
#
#     """
#
#
# def test_create_user():
#     ''
#     "CREATE USER spillman WITH PASSWORD 'Niner27';"
#     "CREATE USER akers WITH PASSWORD 'Niner2' SUPERUSER;"
#     "CREATE USER boone WITH PASSWORD 'Niner75' NOSUPERUSER;"
#     "CREATE USER test NOSUPERUSER;"
#
#
#
# def test_grant():
#     ''
#     "GRANT SELECT ON ALL KEYSPACES TO spillman;"
#     "GRANT MODIFY ON KEYSPACE field TO akers;"
#     "GRANT ALTER ON KEYSPACE forty9ers TO boone;"
#     "GRANT ALL PERMISSIONS ON ravens.plays TO boone;"
#     "GRANT ALL ON KEYSPACE keyspace_name TO user_name"
#
#
# def test_create_user():
#     """
#     "CREATE USER spillman WITH PASSWORD 'Niner27';"
#     "CREATE USER akers WITH PASSWORD 'Niner2' SUPERUSER;"
#     "CREATE USER boone WITH PASSWORD 'Niner75' NOSUPERUSER;"
#     "CREATE USER test NOSUPERUSER;"
#     """
#
#
# def test_grant():
#     """
#     "GRANT SELECT ON ALL KEYSPACES TO spillman;"
#     "GRANT MODIFY ON KEYSPACE field TO akers;"
#     "GRANT ALTER ON KEYSPACE forty9ers TO boone;"
#     "GRANT ALL PERMISSIONS ON ravens.plays TO boone;"
#     "GRANT ALL ON KEYSPACE keyspace_name TO user_name"
#     """
#
#
# def test_index():
#
#     """
#     CREATE INDEX state_key ON users (state);
#     CREATE INDEX birth_year_key ON users (birth_year)
#     CREATE INDEX user_state ON myschema.users (state)
#     CREATE INDEX ON myschema.users (zip)
#
#     "DROP INDEX user_state;"
#     "DROP INDEX users_zip_idx;"
#     """
#     index = manager.Table('users', 'myschema').createIndex('user_state', 'state')
#     assert index.execute(renderOnly=True) == "CREATE INDEX user_state ON myschema.users (state)"
#
#     index = manager.Table('users', 'myschema').createIndex('', 'zip')
#     assert index.execute(renderOnly=True) == "CREATE INDEX ON myschema.users (zip)"
#
#     index = manager.Table('users', 'myschema').dropIndex('user_state')
#     assert index.execute(renderOnly=True) == "DROP INDEX user_state"
#
#     index = manager.Table('users', 'myschema').dropIndex('users_zip_idx')
#     assert index.execute(renderOnly=True) == "DROP INDEX users_zip_idx"
#
#
# def test_alter_keyspace():
#
#     excelsior = manager.Keyspace('Excelsior').alter().replication({'class': 'SimpleStrategy', 'replication_factor': 3})
#     assert excelsior.execute(renderOnly=True).strip() == "ALTER KEYSPACE Excelsior " \
#                                          "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3}"
#
#     replication = {'class': 'NetworkTopologyStrategy', 'dc1': 3, 'dc2': 2}
#     excalibur = manager.Keyspace("'Excalibur'").alter().replication(replication)
#     assert excalibur.execute(renderOnly=True).strip() == "ALTER KEYSPACE 'Excalibur' " \
#                                          "WITH REPLICATION = {'dc2': 2, 'class': 'NetworkTopologyStrategy', 'dc1': 3}"
#
#     replication = {'class': 'NetworkTopologyStrategy', 'dc1': 1}
#     excalibur = manager.Keyspace("Risky").alter().replication(replication).durableWrites(False)
#     exhabibur = manager.Keyspace("dangerous").alter().replication(replication).durableWrites()
#     assert excalibur.execute(renderOnly=True) == "ALTER KEYSPACE Risky " \
#                                  "WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'dc1': 1} " \
#                                  "AND DURABLE_WRITES = false"
#     assert exhabibur.execute(renderOnly=True) == "ALTER KEYSPACE dangerous " \
#                                  "WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'dc1': 1} " \
#                                  "AND DURABLE_WRITES = true"
#
#     replication = {'class': 'SimpleStrategy', 'replication_factor': 3}
#     excalibur = manager.Keyspace("Excalibur").alter().replication(replication)
#     assert excalibur.execute(renderOnly=True) == "ALTER KEYSPACE Excalibur " \
#                                   "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3}"
#
#     excalibur = manager.Keyspace("Excalibur").alter().durableWrites(False)
#     assert excalibur.execute(renderOnly=True) == "ALTER KEYSPACE Excalibur " \
#                                   "WITH DURABLE_WRITES = false"
#
#
# def test_drop_keyspace():
#     twitter = manager.Keyspace('MyTwitterClone').drop()
#     assert twitter.execute(renderOnly=True) == "DROP KEYSPACE MyTwitterClone"
#
