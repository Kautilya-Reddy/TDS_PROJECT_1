CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    email TEXT NOT NULL,
    task TEXT NOT NULL,
    round INTEGER NOT NULL,
    nonce TEXT NOT NULL,
    brief TEXT NOT NULL,
    attachments TEXT NOT NULL,
    checks TEXT NOT NULL,
    evaluation_url TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    statuscode INTEGER,
    secret TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    email TEXT NOT NULL,
    task TEXT NOT NULL,
    round INTEGER NOT NULL,
    nonce TEXT NOT NULL,
    repo_url TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    pages_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    email TEXT NOT NULL,
    task TEXT NOT NULL,
    round INTEGER NOT NULL,
    repo_url TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    pages_url TEXT NOT NULL,
    check_name TEXT NOT NULL,
    score REAL NOT NULL,
    reason TEXT,
    logs TEXT
);
