BEGIN;

DROP TABLE IF EXISTS entries;

CREATE TABLE entries (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  what_to_do TEXT    NOT NULL,
  due_date   TEXT    NOT NULL,
  status     TEXT    NOT NULL DEFAULT '',
  category   TEXT    NOT NULL DEFAULT 'miscellaneous'
);

COMMIT;;