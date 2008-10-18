DROP TABLE IF EXISTS filing;
DROP TABLE IF EXISTS org;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS government_entity;
DROP TABLE IF EXISTS url;
DROP TABLE IF EXISTS registrant;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS filing_registrant;
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS client_status;
DROP TABLE IF EXISTS state_or_local_gov;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS filing_client;
DROP TABLE IF EXISTS lobbyist_status;
DROP TABLE IF EXISTS lobbyist_indicator;
DROP TABLE IF EXISTS lobbyist;
DROP TABLE IF EXISTS filing_lobbyists;
DROP TABLE IF EXISTS govt_entity;
DROP TABLE IF EXISTS filing_govt_entities;
DROP TABLE IF EXISTS issue_code;
DROP TABLE IF EXISTS issue;
DROP TABLE IF EXISTS filing_issues;
DROP TABLE IF EXISTS affiliated_org;
DROP TABLE IF EXISTS affiliated_org_urls;
DROP TABLE IF EXISTS filing_affiliated_orgs;

DROP INDEX IF EXISTS lobbyist_index;
DROP INDEX IF EXISTS client_index;
DROP INDEX IF EXISTS registrant_index;
DROP INDEX IF EXISTS affiliated_org_index;

CREATE TABLE filing(
  id VARCHAR(36) PRIMARY KEY,
  type VARCHAR(64),
  year INTEGER,
  period VARCHAR(64),
  filing_date VARCHAR(20),      -- ISO 8601 extended date+time format
  amount INTEGER
);

CREATE TABLE org(
  name VARCHAR(256) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE person(
  name VARCHAR(256) PRIMARY KEY ON CONFLICT IGNORE
);

-- Unfortunately, this isn't always a valid URL. It may contain all
-- sorts of random text.
CREATE TABLE url(
  url VARCHAR(256) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE country(
  name VARCHAR(64) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE state(
  name VARCHAR(64) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE registrant(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  country REFERENCES country,
  senate_id INTEGER,
  name REFERENCES org,
  ppb_country REFERENCES country
);

CREATE TABLE filing_registrant(
  filing REFERENCES filing,
  registrant REFERENCES registrant,
  address VARCHAR(256),
  description VARCHAR(256),
  PRIMARY KEY(filing, registrant)
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
  name REFERENCES org,
  ppb_country REFERENCES country,
  state REFERENCES state,
  ppb_state REFERENCES state,
  state_or_local_gov REFERENCES state_or_local_gov
);

CREATE TABLE filing_client(
  filing REFERENCES filing,
  client REFERENCES client,
  senate_id INTEGER,
  status REFERENCES client_status,
  contact_name REFERENCES person,
  description VARCHAR(256),
  PRIMARY KEY(filing, client)
);

CREATE TABLE lobbyist_status(
  status VARCHAR(32) PRIMARY KEY
);

CREATE TABLE lobbyist_indicator(
  status VARCHAR(16) PRIMARY KEY
);

CREATE TABLE lobbyist(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name REFERENCES person,
  indicator REFERENCES lobbyist_indicator,
  official_position VARCHAR(256)
);

-- Lobbyists elements in the XML documents are badly broken. Among
-- other problems, filings sometimes list the exact same Lobbyist
-- element (with identical attribute values) more than once. When
-- these are encountered, just ignore any occurrences after the
-- first. (In the future, it might be nice to flag these records so
-- they can be reported to the Senate.)
CREATE TABLE filing_lobbyists(
  filing REFERENCES filing,
  lobbyist REFERENCES lobbyist,
  status REFERENCES lobbyist_status,
  PRIMARY KEY(filing, lobbyist, status) ON CONFLICT IGNORE
);

CREATE TABLE govt_entity(
  name VARCHAR(64) PRIMARY KEY ON CONFLICT IGNORE
);

-- Filings sometimes list the exact same GovernmentEntity more than
-- once. Just ignore any occurrences after the first. (In the future,
-- it might be nice to flag these records so they can be reported to
-- the Senate.)
CREATE TABLE filing_govt_entities(
  filing REFERENCES filing,
  govt_entity REFERENCES govt_entity,
  PRIMARY KEY(filing, govt_entity) ON CONFLICT IGNORE
);

CREATE TABLE issue_code(
  code VARCHAR(80) PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE issue(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code REFERENCES code,
  specific_issue VARCHAR
);

CREATE TABLE filing_issues(
  filing REFERENCES filing,
  issue REFERENCES issue,
  PRIMARY KEY(filing, issue)
);

CREATE TABLE affiliated_org(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name REFERENCES org,
  country REFERENCES country,
  ppb_country REFERENCES country
);

CREATE TABLE affiliated_org_urls(
  org REFERENCES affiliated_org,
  url REFERENCES url,
  PRIMARY KEY(org, url) ON CONFLICT IGNORE
);

CREATE TABLE filing_affiliated_orgs(
  filing REFERENCES filing,
  org REFERENCES affiliated_org,
  PRIMARY KEY(filing, org) ON CONFLICT IGNORE
);

-- Create indexes for tables that get looked up during import. They
-- make a HUGE difference in import performance.
CREATE UNIQUE INDEX lobbyist_index ON lobbyist(
  name,
  indicator,
  official_position
);

CREATE UNIQUE INDEX client_index ON client(
  country,
  name,
  ppb_country,
  state,
  ppb_state,
  state_or_local_gov
);

CREATE UNIQUE INDEX registrant_index ON registrant(
  country,
  senate_id,
  name,
  ppb_country
);

CREATE UNIQUE INDEX affiliated_org_index ON affiliated_org(
  name,
  country,
  ppb_country
);

-- 3 possible state/local govt values.
INSERT INTO state_or_local_gov VALUES('unspecified');
INSERT INTO state_or_local_gov VALUES('n');
INSERT INTO state_or_local_gov VALUES('y');

-- 3 possible client statuses.
INSERT INTO client_status VALUES('active');
INSERT INTO client_status VALUES('terminated');
INSERT INTO client_status VALUES('administratively terminated');

-- 4 possible lobbyist statuses.
INSERT INTO lobbyist_status VALUES('active');
INSERT INTO lobbyist_status VALUES('terminated');
INSERT INTO lobbyist_status VALUES('undetermined');

-- 3 possible lobbyist indicators
INSERT INTO lobbyist_indicator VALUES('not covered');
INSERT INTO lobbyist_indicator VALUES('covered');
INSERT INTO lobbyist_indicator VALUES('undetermined');
