import sqlite3
from pathlib import Path
from schema import USER_TABLE

DB_PATH = Path("data") / "workflow_manager.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(USER_TABLE)

        conn.commit()
