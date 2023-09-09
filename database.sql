DROP TABLE IF EXISTS history;

CREATE TABLE history (
  id TEXT PRIMARY KEY,
  price CURRENCY,
  quantity TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
