CREATE TABLE IF NOT EXISTS Tracks (
    id integer PRIMARY KEY AUTOINCREMENT,
    project_ID INTEGER,
    start_time datetime,
    end_time datetime,
    project_time integer
);

CREATE TABLE IF NOT EXISTS Projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)