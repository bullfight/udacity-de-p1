# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS times;"

# CREATE TABLES

songplay_table_create = ("""
  CREATE TABLE IF NOT EXISTS songplays (
    songplay_id serial PRIMARY KEY NOT NULL,
    start_time  timestamp,
    user_id     integer,
    song_id     varchar,
    artist_id   varchar,
    session_id  integer,
    location    varchar,
    user_agent  varchar
  )
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users (
      user_id    integer PRIMARY KEY NOT NULL,
      first_name varchar,
      last_name  varchar,
      gender     varchar,
      level      varchar
  )
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs
    (
        song_id   varchar PRIMARY KEY NOT NULL,
        artist_id varchar,
        title     varchar,
        year      varchar,
        duration  float
    )
""")

artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artists
  (
      artist_id varchar PRIMARY KEY NOT NULL,
      name      varchar,
      location  varchar,
      latitude  float,
      longitude float
  )
""")

time_table_create = ("""
  CREATE TABLE IF NOT EXISTS times
  (
    start_time timestamp,
    hour       integer,
    day        integer,
    week       integer,
    month      integer,
    year       integer,
    weekday    integer
  )
""")

# INSERT RECORDS
songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO NOTHING
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, artist_id, title, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING
""")

time_table_insert = ("""
    INSERT INTO times (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# Find sonds by title, name, and duration, return song_id and artist_id
song_select = ("""
    SELECT songs.song_id, artists.artist_id
        FROM songs
        INNER JOIN artists ON (songs.artist_id = artists.artist_id)
        WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s
""")


# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
