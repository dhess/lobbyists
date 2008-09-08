DROP TABLE IF EXISTS filing;
DROP TABLE IF EXISTS org;
DROP TABLE IF EXISTS lobbyist;
DROP TABLE IF EXISTS government_entity;
DROP TABLE IF EXISTS issue;
DROP TABLE IF EXISTS specific_issue;
DROP TABLE IF EXISTS url;
DROP TABLE IF EXISTS registrant;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS filing_registrant;
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS client_status;
DROP TABLE IF EXISTS state_or_local_gov;
DROP TABLE IF EXISTS client;

CREATE TABLE filing(
  id VARCHAR(36) PRIMARY KEY,
  type VARCHAR(64),
  year INTEGER,
  period VARCHAR(64),
  filing_date VARCHAR(20),      -- ISO 8601 extended date+time format
  amount INTEGER,
  registrant REFERENCES registrant,  -- optional
  client REFERENCES client -- optional
);

CREATE TABLE org(
  name VARCHAR(256) PRIMARY KEY ON CONFLICT IGNORE
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

CREATE TABLE country(
  name VARCHAR(64) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE state(
  name VARCHAR(64) PRIMARY KEY ON CONFLICT IGNORE
);
  
CREATE TABLE registrant(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address VARCHAR(256),
  description VARCHAR(256),
  country REFERENCES country,
  senate_id INTEGER,
  name REFERENCES org,
  ppb_country REFERENCES country
);

CREATE TABLE client_status(
  status VARCHAR(32) PRIMARY KEY
);

CREATE TABLE state_or_local_gov(
  val VARCHAR(7) PRIMARY KEY
);
  
CREATE TABLE client(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  country REFERENCES country,
  senate_id INTEGER,
  name REFERENCES org,
  ppb_country REFERENCES country,
  state REFERENCES state,
  ppb_state REFERENCES state,
  status REFERENCES client_status,
  description VARCHAR(256),
  state_or_local_gov REFERENCES state_or_local_gov,
  contact_name VARCHAR(256)
);

-- 3 possible state/local govt values.
INSERT INTO state_or_local_gov VALUES('missing');
INSERT INTO state_or_local_gov VALUES('n');
INSERT INTO state_or_local_gov VALUES('y');

-- 3 possible client statuses.
INSERT INTO client_status VALUES('active');
INSERT INTO client_status VALUES('terminated');
INSERT INTO client_status VALUES('administratively terminated');

-- special values, usually for unspecified fields.
