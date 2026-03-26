"""
init_db.py

This module is responsible for database initialization and connection
management for the Project Workflow Manager Application.

Functionality includes:
    - Establishing a connection to the SQLite database
    - Ensuring the database file and directory exist
    - Initialize required database tables using the defined schema

This is the data access entry point for other components to handle
database connection logic.

"""

import sqlite3
from pathlib import Path
from schema import USER_TABLE

#Path to the SQLite database file
DB_PATH = Path("data") / "workflow_manager.db"


"""
PRE:
    - The application has permission to create directores and files
      at the specified DB_PATH.
    - The sqlite3 module is available in the environment.

POST:
    - The database directory exists (created if necessary)
    - A connection to the SQLite database is established and returned.

Returns:
    - sqlite3.Connection object connected to the database file.
"""
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


"""
PRE:
    - The database connection can be established.
    - Tables contain valid SQL for table creation.

POST:
    - The Users table exists in the database
    - All schema changes committed to the database.

Returns:
    - None
"""
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        #Tables to create
        cursor.execute(USER_TABLE)

        conn.commit()
