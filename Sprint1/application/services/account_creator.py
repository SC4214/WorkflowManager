"""
account_creator.py

This module handles account creation logic for the Workflow manager application.

Responsibilities:
    - Validate whether a new account can be created
    - Ensure email uniqueness within the database
    - Inserting new user records into the database

"""

from init_db import get_connection

"""
PRE:
    - email and password are provided as non-empty strings
    - The data base connection can be established.
    - The Users table exists in the database.

POST:
    - If the email already exists, no new account is created
      and the database remains unchanged
    - If the email does not exist, a new user record is inserted
      into the Users table
    - A tuple indicating success or failure is returned

Returns:
    - (bool, str):
        - True and success message if account creation is successful
        - False and error message if account creation fails
"""
def create_account(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if email exists
        cursor.execute("SELECT id FROM Users WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, "An account with that email already exists."

        # Insert new account
        cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, password))

    return True, "Account created successfully"
