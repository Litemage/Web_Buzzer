/*if table exists, delete it*/

DROP TABLE IF EXISTS users;

/*Create our table*/

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL
);
