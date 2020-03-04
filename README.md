# Sparkify Songplays

## Problem

Sparkify a music streaming startup is seeking to analyze songplays by users of a
new application. The app generates two artifacts:

* Song Data - JSON Metadata about songs available for streaming in the app
* Log Data - JSON logs of user songplays

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
