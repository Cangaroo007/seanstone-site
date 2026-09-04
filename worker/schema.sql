-- seanstone.com — the record behind the site.
--
-- Two tables. `enquiries` is people who deliberately contacted Sean. `sessions`
-- is people who engaged hard enough to be worth knowing about but never said
-- anything — the ones a normal site loses entirely.
--
-- Apply with:  wrangler d1 execute seanstone --remote --file=./schema.sql

CREATE TABLE IF NOT EXISTS enquiries (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  ts         TEXT    NOT NULL,          -- ISO 8601, UTC
  sid        TEXT,                      -- joins to sessions.sid
  email      TEXT,                      -- blank when they chose not to give one
  subject    TEXT,
  body       TEXT,
  company    TEXT,
  city       TEXT,
  country    TEXT,
  network    TEXT,
  segment    TEXT,                      -- what they told the router they were
  score      INTEGER,
  depth      INTEGER,                   -- % of the page read
  weakzone   TEXT,                      -- weakest diagnostic zone, if completed
  scopehours INTEGER,                   -- hours of scope built, if any
  asked      TEXT,                      -- questions typed into the ask box
  referrer   TEXT,
  ua         TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  ts         TEXT    NOT NULL,
  sid        TEXT    NOT NULL UNIQUE,   -- one alert per session, enforced here
  company    TEXT,
  city       TEXT,
  country    TEXT,
  network    TEXT,
  segment    TEXT,
  score      INTEGER,
  depth      INTEGER,
  minutes    INTEGER,
  visits     INTEGER,                   -- their visit number, from their browser
  signals    TEXT,
  weakzone   TEXT,
  scopehours INTEGER,
  asked      TEXT,
  stage      TEXT,
  nba        TEXT,                      -- the next action the panel recommended
  referrer   TEXT,
  ua         TEXT
);

CREATE INDEX IF NOT EXISTS idx_enq_ts  ON enquiries(ts DESC);
CREATE INDEX IF NOT EXISTS idx_sess_ts ON sessions(ts DESC);
CREATE INDEX IF NOT EXISTS idx_enq_co  ON enquiries(company);
CREATE INDEX IF NOT EXISTS idx_sess_co ON sessions(company);
