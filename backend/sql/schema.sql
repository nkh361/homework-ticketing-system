DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS team;

CREATE TABLE user(
	userID VARCHAR(255) PRIMARY KEY,
	username VARCHAR(128) NOT NULL UNIQUE,
	email VARCHAR(128) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL
);

CREATE TABLE project (
	projectID VARCHAR(255) PRIMARY KEY,
	owner VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  teamID VARCHAR(255),
  INDEX (projectID)
);

CREATE TABLE ticket (
  ticketID VARCHAR(255) PRIMARY KEY,
  projectID VARCHAR(255),
  userID VARCHAR(255) NOT NULL,
  name VARCHAR(128) NOT NULL,
  created_at VARCHAR(128) NOT NULL,
  due_date VARCHAR(128) NOT NULL,
  priority INT,
  status TEXT
);

CREATE TABLE role (
  	roleID VARCHAR(255) PRIMARY KEY,
  	name VARCHAR(128),
  	description TEXT
);

CREATE TABLE team (
  teamID VARCHAR(255) PRIMARY KEY,
  projectID VARCHAR(255),
  userID VARCHAR(255),
  roleID VARCHAR(255)
);

ALTER TABLE project
ADD CONSTRAINT fk_project_user
FOREIGN KEY (owner) REFERENCES user(userID);

ALTER TABLE project
ADD CONSTRAINT fk_project_team
FOREIGN KEY (teamID) REFERENCES team(teamID);

ALTER TABLE project
ADD CONSTRAINT fk_ticket_project
FOREIGN KEY (projectID) REFERENCES project(projectID);

ALTER TABLE ticket
ADD CONSTRAINT fk_ticket_user
FOREIGN KEY (userID) REFERENCES user(userID);

ALTER TABLE team
ADD CONSTRAINT fk_team_project
FOREIGN KEY (projectID) REFERENCES project(projectID);