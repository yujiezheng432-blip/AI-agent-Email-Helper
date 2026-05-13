import sqlite3
from pathlib import Path

DB_PATH = Path("data/email_agent.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT UNIQUE,
        sender TEXT,
        subject TEXT,
        body TEXT,
        summary TEXT,
        category TEXT,
        need_reply INTEGER,
        importance_score INTEGER,
        draft_reply TEXT,
        status TEXT DEFAULT 'raw',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()