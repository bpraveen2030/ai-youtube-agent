import sqlite3
from pathlib import Path


DB_PATH = Path("data/news.db")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT UNIQUE,
                source TEXT,
                summary TEXT,
                published TEXT,
                score INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_stories(stories):
    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        for story in stories:
            conn.execute(
                """
                INSERT OR IGNORE INTO stories
                (title, url, source, summary, published, score)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    story["title"],
                    story["url"],
                    story["source"],
                    story["summary"],
                    story["published"],
                    story["score"],
                )
            )
