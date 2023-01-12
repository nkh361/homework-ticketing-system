DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
  user_id VARCHAR(255) NOT NULL,
  title VARCHAR(128) NOT NULL,
  priority INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  due_date VARCHAR(128) NOT NULL,
  status TEXT
);
-- users table
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id VARCHAR(255) PRIMARY KEY,
  username VARCHAR(128) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);



