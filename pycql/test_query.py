from uuid import uuid4

from pycql.query import Query


def _insert():
    # Insert Test
    uuid = uuid4().hex
    data = dict({'user__uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data)
    assert query.execute(renderOnly=True).strip() == "INSERT INTO Hollywood.NerdMovies ( user__uuid, fan ) " \
                                                     "VALUES ( " + uuid + ", 'johndoe' )"

    uuid = uuid4().hex
    data = dict({'user__uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data).ttl(1, 'day')
    assert query.execute(renderOnly=True).strip() == "INSERT INTO Hollywood.NerdMovies ( user__uuid, fan ) " \
                                                     "VALUES ( " + uuid + ", 'johndoe' ) " \
                                                                          "USING TTL 86400"

    data = {'user_id': 'frodo',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
            'emails': {'f@baggins.com', 'baggins@gmail.com'}}
    query = Query('users').insert(data)
    assert query.execute(renderOnly=True).strip() == "INSERT INTO users ( first_name, last_name, user_id, emails ) " \
                                                     "VALUES ( 'Frodo', 'Baggins', 'frodo', {'baggins@gmail.com', 'f@baggins.com'} )"

    data = {'user_id': 'frodo',
            'todo': {'2012-10-2 12:10': 'die'}}
    query = Query('users').insert(data)
    assert query.execute(renderOnly=True).strip() == "INSERT INTO users ( todo, user_id ) " \
                                                     "VALUES ( {'2012-10-2 12:10': 'die'}, 'frodo' )"

    data = {'id__uuid': '62c36092-82a1-3a00-93d1-46196ee77204',
            'song_order': 1,
            'song_id__uuid': 'a3e64f8f-bd44-4f28-b8d9-6938726e34d4',
            'title': 'La Grange',
            'artist': 'ZZ Top',
            'album': 'Tres Hombres',
    }
    query = Query('playlists').insert(data)
    assert query.execute(
        renderOnly=True).strip() == "INSERT INTO playlists ( id__uuid, album, song_order, artist, title, song_id__uuid ) " \
                                    "VALUES ( 62c36092-82a1-3a00-93d1-46196ee77204, 'Tres Hombres', 1, 'ZZ Top', 'La Grange', " \
                                    "a3e64f8f-bd44-4f28-b8d9-6938726e34d4 )"

    "INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 1, a3e64f8f-bd44-4f28-b8d9-6938726e34d4, 'La Grange', 'ZZ Top', 'Tres; Hombres')"
    "INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 2, 8a172618-b121-4136-bb10-f665cfc469eb, 'Moving in Stereo', 'Fu Manchu', 'We Must Obey')"
    "INSERT INTO playlists (id, song_order, song_id, title, artist, album) VALUES (62c36092-82a1-3a00-93d1-46196ee77204, 3, 2b09185b-fb5a-4734-9b56-49077de9edbf, 'Outside Woman Blues', 'Back Door; Slam', 'Roll Away')"
    '''
    INSERT INTO emp (empID, deptID, first_name, last_name) VALUES (104, 15, 'jane', 'smith')
    INSERT INTO Music.songs (id, title, artist, album) VALUES (a3e64f8f-bd44-4f28-b8d9-6938726e34d4, 'La Grange', 'ZZ Top', 'Tres Hombres')
    INSERT INTO excelsior.clicks ( userid, url, date, name) VALUES ( 3715e600-2eb0-11e2-81c1-0800200c9a66, 'http://apache.org', '2013-10-09', 'Mary') USING TTL 86400
    INSERT INTO excelsior.clicks ( userid, url, date, name) VALUES ( cfd66ccc-d857-4e90-b1e5-df98a3d40cd6, 'http://google.com', '2013-10-11', 'Bob' )
    INSERT INTO users (user_name, password) VALUES ('cbrown', 'ch@ngem4a') USING TTL 86400
    INSERT INTO users (todo) VALUES ( { '2013-9-22 12:01' : 'birthday wishes to Bilbo', '2013-10-1 18:00' : 'Check into Inn of Prancing Pony' })
    INSERT INTO test (id, value_float, value_double) VALUES ('test1', -2.6034345E+38, -2.6034345E+38)



    '''


def _select():
    query = Query('peers').select()
    assert query.execute(renderOnly=True).strip() == "SELECT * FROM peers"

    query = Query('users').select().compare('first_name', 'jane').compare('last_name', 'smith', '=')
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM users WHERE first_name = 'jane' AND last_name = 'smith'"

    query = Query('clicks', 'excelsior').select().ttl('name').compare('url', 'http://apache.org')
    assert query.execute(
        renderOnly=True).strip() == "SELECT TTL (name) FROM excelsior.clicks WHERE url = 'http://apache.org'"

    query = Query('clicks', 'excelsior').select().writetime('name').compare('url', 'http://apache.org')
    assert query.execute(
        renderOnly=True).strip() == "SELECT WRITETIME (name) FROM excelsior.clicks WHERE url = 'http://apache.org'"

    query = Query('clicks', 'excelsior').select().writetime('date').compare('url', 'http://google.org')
    assert query.execute(
        renderOnly=True).strip() == "SELECT WRITETIME (date) FROM excelsior.clicks WHERE url = 'http://google.org'"

    query = Query('users').select().compare('gender', 'f').compare('state', 'TX').compare('birth_year', 1968, '>')
    query.allowFiltering()
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM users WHERE gender = 'f' AND state = 'TX' AND birth_year > 1968 " \
                                    "ALLOW FILTERING"

    query = Query('test').select().compareToken('k', 42, '>')
    assert query.execute(renderOnly=True).strip() == "SELECT * FROM test WHERE TOKEN (k) > TOKEN (42)"

    query = Query('myTable').select().compare('t', "maxTimeuuid('2013-01-01 00:05+0000')", '>', True)
    query.compare('t', "minTimeuuid('2013-02-02 10:00+0000')", '<', True)
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM myTable WHERE t > maxTimeuuid('2013-01-01 00:05+0000') " \
                                    "AND t < minTimeuuid('2013-02-02 10:00+0000')"

    query = Query('People').select('Name', 'Occupation').compare('empID', (199, 200, 207), 'IN')
    assert query.execute(
        renderOnly=True).strip() == "SELECT Name, Occupation FROM People WHERE empID IN (199, 200, 207)"

    query = Query('users').select('COUNT(*)')
    assert query.execute(renderOnly=True).strip() == "SELECT COUNT(*) FROM users"

    query = Query('users').select().count()
    assert query.execute(renderOnly=True).strip() == "SELECT COUNT(*) FROM users"

    query = Query('big_table').select().count().limit(50000)
    assert query.execute(renderOnly=True).strip() == "SELECT COUNT(*) FROM big_table LIMIT 50000"

    query = Query('Migrations', 'system').select().count()
    assert query.execute(renderOnly=True).strip() == "SELECT COUNT(*) FROM system.Migrations"

    query = Query('ruling_stewards').select().compare('king', 'Brego', '=').compare('reign_start', 2450, '>=')
    query.compare('reign_start', 2500, '<').allowFiltering()
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM ruling_stewards WHERE king = 'Brego' AND reign_start >= 2450 " \
                                    "AND reign_start < 2500 ALLOW FILTERING"

    query = Query('ruling_stewards').select().compare('king', 'none').compare('reign_start', 1500, '>=')
    query.compare('reign_start', 3000, '<').allowFiltering().limit(10)
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM ruling_stewards WHERE king = 'none' AND reign_start >= 1500 " \
                                    "AND reign_start < 3000 LIMIT 10 ALLOW FILTERING"

    query = Query('periods').select().compareToken('period_name', 'Third Age', '>')
    query.compareToken('period_name', 'Fourth Age', '<')
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM periods WHERE TOKEN (period_name) > TOKEN ('Third Age') " \
                                    "AND TOKEN (period_name) < TOKEN ('Fourth Age')"

    query = Query('playlists').select().compare('id__uuid', '62c36092-82a1-3a00-93d1-46196ee77204')
    query.limit(50).orderBy('song_order', 'desc')
    assert query.execute(
        renderOnly=True).strip() == "SELECT * FROM playlists WHERE id__uuid = 62c36092-82a1-3a00-93d1-46196ee77204 " \
                                    "ORDER BY song_order DESC LIMIT 50"

    query = Query('playlists').select('title').compare('artist', 'Fu Manchu')
    assert query.execute(renderOnly=True).strip() == "SELECT title FROM playlists WHERE artist = 'Fu Manchu'"

    """
    SELECT * from People
    SELECT COUNT(*) FROM users
    SELECT COUNT(*) FROM big_table LIMIT 200000
    SELECT * FROM ruling_stewards WHERE king = 'Brego' AND reign_start >= 2450 AND reign_start < 2500 ALLOW FILTERING
    Select * FROM ruling_stewards WHERE king = 'none' AND reign_start >= 1500 AND reign_start < 3000 LIMIT 10 ALLOW FILTERING
    SELECT * FROM periods WHERE TOKEN(period_name) > TOKEN('Third Age') AND TOKEN(period_name) < TOKEN('Fourth Age')
    SELECT * FROM playlists WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 ORDER BY song_order DESC LIMIT 50
    SELECT user_id, emails FROM users WHERE user_id = 'frodo'
    SELECT WRITETIME (first_name) FROM users WHERE last_name = 'Jones'
    SELECT * from system.schema_keyspaces
    SELECT user_id, emails FROM users WHERE user_id = 'frodo'
    SELECT user_id, top_places FROM users WHERE user_id = 'frodo'
    SELECT user_id, todo FROM users WHERE user_id = 'frodo'
    SELECT * FROM users WHERE gender = 'f' AND state = 'TX' AND birth_year > 1968 ALLOW FILTERING
    SELECT * FROM test WHERE k > 42
    SELECT * FROM test WHERE token(k) > token(42)
    SELECT * FROM counterks.page_view_counts
    SELECT * FROM MyTable
    SELECT * FROM test

    """


def _delete():
    query = Query('Planeteers').delete('col1', 'col2', 'col3').where('userID', 'Captain')
    assert query.execute(renderOnly=True).strip() == "DELETE col1, col2, col3 FROM Planeteers WHERE userID = 'Captain'"

    query = Query('MastersOfTheUniverse').delete().where('mastersID', ('Man-At-Arms', 'Teela'), 'IN')
    assert query.execute(
        renderOnly=True).strip() == "DELETE FROM MastersOfTheUniverse WHERE mastersID IN ('Man-At-Arms', 'Teela')"

    query = Query('users').delete('email', 'phone').using(1318452291034).where('user_name', 'jsmith')
    assert query.execute(renderOnly=True).strip() == "DELETE email, phone FROM users USING TIMESTAMP 1318452291034 " \
                                                     "WHERE user_name = 'jsmith'"

    query = Query('SomeTable').delete('col1').where('userID', 'some_key_value')
    assert query.execute(renderOnly=True).strip() == "DELETE col1 FROM SomeTable WHERE userID = 'some_key_value'"

    query = Query('SomeTable').delete('col1').where('userID', '(key1, key2)', 'IN', True)
    assert query.execute(renderOnly=True).strip() == "DELETE col1 FROM SomeTable WHERE userID IN (key1, key2)"

    query = Query('users').delete('phone').where('user_name', ('jdoe', 'jsmith'), 'IN')
    assert query.execute(renderOnly=True).strip() == "DELETE phone FROM users WHERE user_name IN ('jdoe', 'jsmith')"

    query = Query('users').delete("todo ['2012-9-24']").where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == "DELETE todo ['2012-9-24'] FROM users WHERE user_id = 'frodo'"

    query = Query('users').delete("top_places[3]").where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == "DELETE top_places[3] FROM users WHERE user_id = 'frodo'"

    query = Query('users').delete("emails").where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == "DELETE emails FROM users WHERE user_id = 'frodo'"

    query = Query('users').delete("name").where('userID', 'user2')
    assert query.execute(renderOnly=True).strip() == "DELETE name FROM users WHERE userID = 'user2'"

    """
    DELETE session_token FROM users where pk = 'jsmith'
    DELETE FROM users where pk = 'jsmith'
    """


def test_update():
    """
    - UPDATE UserActionCounts SET total = total + 2 WHERE keyalias = 523
    - UPDATE excelsior.clicks USING TTL 432000 SET user_name = 'bob' WHERE userid=cfd66ccc-d857-4e90-b1e5-df98a3d40cd6 AND url='http://google.com'
    - UPDATE Movies SET col1 = val1, col2 = val2 WHERE movieID = key1
    - UPDATE Movies SET col3 = val3 WHERE movieID IN (key1, key2, key3)
    - UPDATE Movies SET col4 = 22 WHERE movieID = key4
    - UPDATE users SET state = 'TX' WHERE user_uuid IN (88b8fd18-b1ed-4e96-bf79-4280797cba80, 06a8913c-c0d6-477c-937d-6c1b69a95d43, bc108776-7cb5-477f-917d-869c12dfffa8)
    - UPDATE users SET name = 'John Smith', email = 'jsmith@cassie.com' WHERE user_uuid = 88b8fd18-b1ed-4e96-bf79-4280797cba80
    - UPDATE counterks.page_view_counts SET counter_value = counter_value + 2 WHERE url_name='www.datastax.com' AND page_name='home'
    - UPDATE users SET emails = emails + {'fb@friendsofmordor.org'} WHERE user_id = 'frodo'
    - UPDATE users SET emails = emails - {'fb@friendsofmordor.org'} WHERE user_id = 'frodo'
    - UPDATE users SET emails = {} WHERE user_id = 'frodo'
    - UPDATE users SET todo = { '2012-9-24' : 'enter mordor', '2012-10-2 12:00' : 'throw ring into mount doom' } WHERE user_id = 'frodo'
    - UPDATE users SET todo['2012-10-2 12:10'] = 'die' WHERE user_id = 'frodo'
    - UPDATE users USING TTL <ttl value> SET todo['2012-10-1'] = 'find water' WHERE user_id = 'frodo'
    - UPDATE users SET top_places = [ 'rivendell', 'rohan' ] WHERE user_id = 'frodo'
    - UPDATE users SET top_places = [ 'the shire' ] + top_places WHERE user_id = 'frodo'
    - UPDATE users SET top_places = top_places + [ 'mordor' ] WHERE user_id = 'frodo'
    - UPDATE users SET top_places[2] = 'riddermark' WHERE user_id = 'frodo'
    - UPDATE users SET top_places = top_places - ['riddermark'] WHERE user_id = 'frodo'
    - UPDATE users USING TTL 432000 SET 'password' = 'ch@ngem4a' WHERE user_name = 'cbrown'
    - UPDATE users SET todo['2012-10-2 12:00'] = 'throw my precious into mount doom' WHERE user_id = 'frodo'
    - UPDATE users USING TTL <computed_ttl>
    UPDATE counterks.page_view_counts SET counter_value = counter_value + 1 WHERE url_name='www.datastax.com' AND page_name='home'
    UPDATE counterks.page_view_counts SET counter_value = counter_value + 2 WHERE url_name='www.datastax.com' AND page_name='home'
    UPDATE MyTable SET SomeColumn = 'SomeValue' WHERE columnName = B70DE1D0-9908-4AE3-BE34-5573E5B09F14

    """

    # update can receive dictionary as parameter as key, value pair
    # key should be in string or in unicode
    # value can be in any cql_type. Values which are in cql_type that python don't support,
    # enclose them with quote. and pass the parameter no_string=True eg. uuid, timestamp
    data = {u'col1': u'val1',
            'col2': u'val2', }
    query = Query('Movies').update(data, no_string=True).where('movieID', 'key1', '=', no_string=True)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE Movies SET col2 = val2, col1 = val1 WHERE movieID = key1"

    data = {'user_name': 'bob'}
    query = Query('clicks', 'excelsior').update(data).where('userid', 'cfd66ccc-d857', '=', no_string=True).ttl(432000)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE excelsior.clicks USING TTL 432000 SET user_name = 'bob' WHERE userid = cfd66ccc-d857"

    data = ('total', 2, '+=')
    query = Query('userActionCounts').update(data).where('keyalias', 523)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE userActionCounts SET total = total + 2 WHERE keyalias = 523"

    data = {'user_name': 'bob'}
    query = Query('clicks', 'excelsior').update(data).ttl(432000)
    query.where('userid__uuid', 'cfd66ccc-d857-4e90-b1e5-df98a3d40cd6')
    query.where('url', 'http://google.com')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE excelsior.clicks USING TTL 432000 SET user_name = 'bob' " \
           "WHERE userid__uuid = cfd66ccc-d857-4e90-b1e5-df98a3d40cd6 AND url = 'http://google.com'"

    query = Query('Movies').update({'col4': 22}).where('movieID', 'key4', '=', no_string=True)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE Movies SET col4 = 22 WHERE movieID = key4"

    query = Query('movies').update({'col3': 'val3'}, no_string=True).where('movieID', '(key1, key2, key3)', 'IN', no_string=True)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE movies SET col3 = val3 WHERE movieID IN (key1, key2, key3)"

    query = Query('users').update({'state': 'TX'}).where('user_uuid', '(88b8fd18-b1ed-4e96-bf79-4280797cba80, '
                                                                      '06a8913c-c0d6-477c-937d-6c1b69a95d43, '
                                                                      'bc108776-7cb5-477f-917d-869c12dfffa8)', 'IN',
                                                         no_string=True)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET state = 'TX' WHERE user_uuid IN (88b8fd18-b1ed-4e96-bf79-4280797cba80, " \
           "06a8913c-c0d6-477c-937d-6c1b69a95d43, bc108776-7cb5-477f-917d-869c12dfffa8)"

    data = {'name': 'John Smith',
            'email': 'jsmith@cassie.com'}
    query = Query('users').update(data).where('user_uuid', '88b8fd18-b1ed-4e96-bf79-4280797cba80', no_string=True)
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET name = 'John Smith', email = 'jsmith@cassie.com' " \
           "WHERE user_uuid = 88b8fd18-b1ed-4e96-bf79-4280797cba80"

    query = Query('page_view_counts', 'counterks').update(('counter_value', 2, '+='))
    query.where('url_name', 'www.datastax.com')
    query.where('page_name', 'home')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE counterks.page_view_counts SET counter_value = counter_value + 2 " \
           "WHERE url_name = 'www.datastax.com' AND page_name = 'home'"

    emails = {'fb@friendsofmordor.org'}
    query = Query('users').update(('emails', emails, '+=')).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET emails = emails + {'fb@friendsofmordor.org'} WHERE user_id = 'frodo'"

    emails = {'fb@friendsofmordor.org'}
    query = Query('users').update(('emails', emails, '-=')).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET emails = emails - {'fb@friendsofmordor.org'} WHERE user_id = 'frodo'"

    emails = {}
    query = Query('users').update({'emails': emails}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET emails = {} WHERE user_id = 'frodo'"

    data_map = {'2012-9-24': 'enter mordor', '2012-10-2 12:00': 'throw ring into mount doom'}
    query = Query('users').update({'todo': data_map}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET todo = {'2012-9-24': 'enter mordor', '2012-10-2 12:00': 'throw ring into mount doom'} " \
           "WHERE user_id = 'frodo'"

    query = Query('users').update({"todo['2012-10-2 12:10']": 'die'}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET todo['2012-10-2 12:10'] = 'die' WHERE user_id = 'frodo'"

    query = Query('users').update({"todo['2012-10-1']": 'find water'}).ttl(1, 'hr').where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users USING TTL 3600 SET todo['2012-10-1'] = 'find water' WHERE user_id = 'frodo'"

    top_places = ['rivendell', 'rohan']
    query = Query('users').update({'top_places': top_places}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET top_places = ['rivendell', 'rohan'] WHERE user_id = 'frodo'"

    # =+ means prepend
    top_places = ['the shire']
    query = Query('users').update(('top_places', top_places, '=+')).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET top_places = ['the shire'] + top_places WHERE user_id = 'frodo'"

    top_places = ['mordor']
    query = Query('users').update(('top_places', top_places, '+=')).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET top_places = top_places + ['mordor'] WHERE user_id = 'frodo'"

    query = Query('users').update({'top_places[2]': 'riddermark'}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET top_places[2] = 'riddermark' WHERE user_id = 'frodo'"

    query = Query('users').update(('top_places', ['riddermark'], '-=')).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET top_places = top_places - ['riddermark'] WHERE user_id = 'frodo'"

    query = Query('users').update({'password': 'ch@ngem4a'}).where('user_name', 'cbrown').ttl(5, 'day')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users USING TTL 432000 SET password = 'ch@ngem4a' WHERE user_name = 'cbrown'"

    query = Query('users').update({"todo['2012-10-2 12:00']": 'throw my precious into mount doom'}).where('user_id', 'frodo')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users SET todo['2012-10-2 12:00'] = 'throw my precious into mount doom' WHERE user_id = 'frodo'"

    query = Query('users').update().ttl(2, 'hr')
    assert query.execute(renderOnly=True).strip() == \
           "UPDATE users USING TTL 7200"