import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """Process song_data and load songs and artists tables

    Arguments:
    cur -- The database cursor (psycopg2.extensions.cursor)
    filepath - The filepath to be read (str)
    """

    # open song file
    df = pd.read_json(filepath, typ='series', convert_dates=False)

    # insert song record
    song_data = df.loc[['song_id', 'artist_id', 'title', 'year', 'duration']].values.tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.loc[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Process log_data and Load times, users and songplays tables

    Arguments:
    cur -- The database cursor (psycopg2.extensions.cursor)
    filepath - The filepath to be read (str)
    """

    # open log file
    df = pd.read_json(filepath, lines=True)
    df = df.astype({'ts': 'datetime64[ms]'})

    # filter by NextSong action
    df = df[df.page.eq('NextSong')]

    # insert time data records
    ts = df.ts
    time_data = (ts, ts.dt.hour, ts.dt.day, ts.dt.weekofyear, ts.dt.month, ts.dt.year, ts.dt.dayofweek )
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].dropna(subset=['userId'])

    # insert user records
    for i, row in user_df.iterrows():
        user_labels = ('user_id', 'first_name', 'last_name', 'gender', 'level')
        user_dict = dict(zip(user_labels, row))
        cur.execute(user_table_insert, user_dict)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, songid, artistid, row.sessionId, row.location, row.userAgent )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Iterate over each file in a filepath add pass the file to a function

    Arguments:
    cur -- The database cursor (psycopg2.extensions.cursor)
    conn -- The database connection (psycopg2.extensions.connection)
    filepath - The filepath to be read (str)
    func - The function to be applied to the given filepath
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
