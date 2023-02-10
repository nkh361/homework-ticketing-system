DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
  user_id VARCHAR(255) NOT NULL,
  title VARCHAR(128) NOT NULL,
  priority INT,
  created_at VARCHAR(128) NOT NULL,
  due_date VARCHAR(128) NOT NULL,
  time_remaining INT as (DATEDIFF(created_at, due_date)),
  status TEXT
);
-- users table
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id VARCHAR(255) PRIMARY KEY,
  username VARCHAR(128) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);