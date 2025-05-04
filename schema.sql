BEGIN;

-- Drop the old table (if any)
DROP TABLE IF EXISTS entries;

-- Recreate with an `id` column
CREATE TABLE entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  what_to_do TEXT NOT NULL,
  due_date   TEXT NOT NULL,
  status     TEXT    NOT NULL DEFAULT ''
);

COMMIT;