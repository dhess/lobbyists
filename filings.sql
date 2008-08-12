DROP TABLE IF EXISTS filing;
DROP TABLE IF EXISTS org;
DROP TABLE IF EXISTS lobbying_org;
DROP TABLE IF EXISTS lobbyist;
DROP TABLE IF EXISTS government_entity;
DROP TABLE IF EXISTS issue;
DROP TABLE IF EXISTS specific_issue;
DROP TABLE IF EXISTS url;

CREATE TABLE filing(
  id VARCHAR(36) PRIMARY KEY,
  type VARCHAR(64),
  year INTEGER,
  period VARCHAR(64),
  filing_date VARCHAR(20),      -- ISO 8601 extended date+time format
  amount INTEGER
);

CREATE TABLE org(
  name VARCHAR(256) PRIMARY KEY
);

CREATE TABLE lobbying_org(
  id INTEGER PRIMARY KEY,           -- Senate registration ID
  name VARCHAR(256) REFERENCES org
);

CREATE TABLE lobbyist(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  last_name VARCHAR(256),
  first_name VARCHAR(256),
  middle_name VARCHAR(256)
);

CREATE TABLE government_entity(
  name VARCHAR(256) PRIMARY KEY
);

CREATE TABLE issue(
  description VARCHAR(256) PRIMARY KEY
);

CREATE TABLE specific_issue(
  description VARCHAR(256) PRIMARY KEY
);

CREATE TABLE url(
  url VARCHAR(256) PRIMARY KEY
);

-- special values, usually for unspecified fields.
INSERT INTO org VALUES('unspecified');
INSERT INTO lobbying_org VALUES(0, 'unspecified');
INSERT INTO lobbyist VALUES(NULL, 'unspecified', 'unspecified', 'unspecified'); -- key is always 1
INSERT INTO government_entity VALUES('unspecified');
INSERT INTO issue VALUES('unspecified');
INSERT INTO specific_issue VALUES('unspecified');
INSERT INTO url VALUES('unspecified');
