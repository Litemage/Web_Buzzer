/*if table exists, delete it*/

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;

/*Create our table*/

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL
);

CREATE TABLE questions (
  id INTEGER PRIMARY KEY,
  question_name TEXT NOT NULL,
  answer_id INTEGER,
  FOREIGN KEY (answer_id) REFERENCES users (id)
);
