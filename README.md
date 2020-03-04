# Sparkify Songplays

## Problem

Sparkify a music streaming startup is seeking to analyze songplays by users of a
new application. The app generates two artifacts:

* Song Data - JSON Metadata about songs available for streaming in the app
* Log Data - JSON logs of user songplays
*Song Data*

The Song Data files include JSON Metadata about songs available for streaming in the app.

Example Song Data:

```json
{ "num_songs": 1,
  "artist_id": "ARD7TVE1187B99BFB1",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "California - LA",
  "artist_name": "Casual", "song_id":
  "SOMZWCG12A8C13C480",
  "title": "I Didn't Mean To",
  "duration": 218.93179,
  "year": 0
}
```

*Log Data*

Newline delimited JSON logs of user songplays.

Example Log Data:

```json
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
{"artist":null,"auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":0,"lastName":"Summers","length":null,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"GET","page":"Home","registration":1540344794796.0,"sessionId":139,"song":null,"status":200,"ts":1541106106796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}
```

A songplay table is built from these artifacts and answers questions like the
following:

* How many songs were streamed on each of the past 5 days?
* Who are the most active listening users?
* What metro region has the most active users?

## Solution

Build the following dimension tables to provide easy access to details about songplays by primary key.

* `artists`
* `users`
* `songs`
* `times`

Build a `songplays` fact table against which example analytical questions around
songplays are quickly and easily queried.

# Building Sparkify Database

The Sparkify Database with associated tables is built by executing the following scripts

```
python create_tables.py
python etl.py
```

## Example Queries

*How many songs were streamed on each of the past 5 days?*
```sql
SELECT DATE(songplays.start_time) as date, count(*) as counts
  FROM songplays
  WHERE songplays.start_time > (DATE '2018-11-29' - INTERVAL '5 days')
  GROUP BY date
  ORDER BY date DESC;
```

*Who are the most active paid, users in the past 5 days?*
```sql
SELECT songplays.user_id, count(*) as count
  FROM songplays
  INNER JOIN users ON (songplays.user_id = users.user_id) \
  WHERE
    songplays.start_time > (DATE '2018-11-29' - INTERVAL '5 days') AND
    users.level = 'paid'
  GROUP BY songplays.user_id
  ORDER BY count desc
  LIMIT 5;
```

*What metro region has the most active users?*
```sql
SELECT location, count(*) as count
  FROM songplays
  GROUP BY songplays.location
  ORDER BY count desc
  LIMIT 5;
```

## Tables

A sample selection of tables available in the Sparify Database:

*songplays*

```sql
sparkifydb=# select * from songplays limit 5;
 songplay_id |       start_time        | user_id | song_id | artist_id | session_id |          location           |                                                   user_agent
-------------+-------------------------+---------+---------+-----------+------------+-----------------------------+-----------------------------------------------------------------------------------------------------------------
           1 | 2018-11-01 21:01:46.796 |       8 |         |           |        139 | Phoenix-Mesa-Scottsdale, AZ | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
           2 | 2018-11-01 21:05:52.796 |       8 |         |           |        139 | Phoenix-Mesa-Scottsdale, AZ | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
           3 | 2018-11-01 21:08:16.796 |       8 |         |           |        139 | Phoenix-Mesa-Scottsdale, AZ | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
           4 | 2018-11-01 21:11:13.796 |       8 |         |           |        139 | Phoenix-Mesa-Scottsdale, AZ | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
           5 | 2018-11-01 21:17:33.796 |       8 |         |           |        139 | Phoenix-Mesa-Scottsdale, AZ | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
```

*users*

```sql
sparkifydb=# select * from users limit 5;
 user_id | first_name | last_name | gender | level
---------+------------+-----------+--------+-------
     100 | Adler      | Barrera   | M      | free
      53 | Celeste    | Williams  | F      | free
      69 | Anabelle   | Simpson   | F      | free
       8 | Kaylee     | Summers   | F      | free
      62 | Connar     | Moreno    | M      | free
```

*artists*

```sql
sparkifydb=# select * from artists limit 5;
     artist_id      |         name          |          location           | latitude | longitude
--------------------+-----------------------+-----------------------------+----------+-----------
 AR7G5I41187FB4CE6C | Adam Ant              | London, England             |          |
 AR8ZCNI1187B9A069B | Planet P Project      |                             |          |
 ARXR32B1187FB57099 | Gob                   |                             |          |
 AR10USD1187B99F3F1 | Tweeterfriendly Music | Burlington, Ontario, Canada |          |
 ARGSJW91187B9B1D6B | JennyAnyKind          | North Carolina              | 35.21962 | -80.01955
```

*songs*

```sql
sparkifydb=# select * from songs limit 5;
      song_id       |     artist_id      |      title      | year | duration
--------------------+--------------------+-----------------+------+-----------
 SONHOTT12A8C13493C | AR7G5I41187FB4CE6C | Something Girls | 1982 | 233.40363
 SOIAZJW12AB01853F1 | AR8ZCNI1187B9A069B | Pink World      | 1984 | 269.81832
 SOFSOCN12A8C143F5D | ARXR32B1187FB57099 | Face the Ashes  | 2007 | 209.60608
 SOHKNRJ12A6701D1F8 | AR10USD1187B99F3F1 | Drop of Rain    | 0    | 189.57016
 SOQHXMF12AB0182363 | ARGSJW91187B9B1D6B | Young Boy Blues | 0    | 218.77506
```

*times*

```sql
sparkifydb=# select * from times limit 5;
       start_time        | hour | day | week | month | year | weekday
-------------------------+------+-----+------+-------+------+---------
 2018-11-01 21:01:46.796 |   21 |   1 |   44 |    11 | 2018 |       3
 2018-11-01 21:05:52.796 |   21 |   1 |   44 |    11 | 2018 |       3
 2018-11-01 21:08:16.796 |   21 |   1 |   44 |    11 | 2018 |       3
 2018-11-01 21:11:13.796 |   21 |   1 |   44 |    11 | 2018 |       3
 2018-11-01 21:17:33.796 |   21 |   1 |   44 |    11 | 2018 |       3
```

