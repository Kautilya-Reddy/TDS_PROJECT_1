import sqlite3
from contextlib import contextmanager

DB_PATH = "eval.db"

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db() as conn:
        conn.executescript(open("schema.sql", "r", encoding="utf-8").read())
