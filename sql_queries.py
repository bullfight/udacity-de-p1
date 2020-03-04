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
    start_time  timestamp NOT NULL,
    user_id     integer NOT NULL,
    song_id     varchar,
    artist_id   varchar,
    session_id  integer NOT NULL,
    location    varchar NOT NULL,
    user_agent  varchar NOT NULL
  )
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users (
      user_id    integer PRIMARY KEY NOT NULL,
      first_name varchar NOT NULL,
      last_name  varchar NOT NULL,
      gender     varchar NOT NULL,
      level      varchar NOT NULL
  )
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs
    (
        song_id   varchar PRIMARY KEY NOT NULL,
        artist_id varchar NOT NULL,
        title     varchar NOT NULL,
        year      varchar NOT NULL,
        duration  float NOT NULL
    )
""")

artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artists
  (
      artist_id varchar PRIMARY KEY NOT NULL,
      name      varchar NOT NULL,
      location  varchar NOT NULL,
      latitude  float,
      longitude float
  )
""")

time_table_create = ("""
  CREATE TABLE IF NOT EXISTS times
  (
    start_time timestamp PRIMARY KEY,
    hour       integer NOT NULL,
    day        integer NOT NULL,
    week       integer NOT NULL,
    month      integer NOT NULL,
    year       integer NOT NULL,
    weekday    integer NOT NULL
  )
""")

# INSERT RECORDS
songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%(user_id)s, %(first_name)s, %(last_name)s, %(gender)s, %(level)s)
    ON CONFLICT (user_id) DO UPDATE SET level = %(level)s
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
    ON CONFLICT (start_time) DO NOTHING
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
