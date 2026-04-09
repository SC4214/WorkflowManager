"""
phase_creator.py

This module handles phase creation logic for the Workflow Manager application.

Responsibilities:
    - Validate whether a new phase can be created
    - Ensure the parent project exists
    - Ensure phase title uniqueness within the selected project
    - Insert new phase records into the database
"""

from init_db import get_connection


def create_phase(proj_id, title, due_date, description):
    """
    PRE:
        - proj_id is a valid project ID
        - title and due_date are provided as non-empty strings
        - The database connection can be established
        - The Projects and Phases tables exist in the database

    POST:
        - If the parent project does not exist, no phase is created
        - If the phase title already exists within the same project,
          no phase is created
        - Otherwise, a new phase record is inserted into the Phases table
        - A tuple indicating success or failure is returned

    Returns:
        - (bool, str):
            - True and success message if phase creation succeeds
            - False and error message if phase creation fails
    """
    title = title.strip()
    due_date = due_date.strip()
    description = description.strip()

    if not title or not due_date:
        return False, "Phase title and due date are required."

    with get_connection() as conn:
        cursor = conn.cursor()

        # Verify parent project exists
        cursor.execute(
            "SELECT projID FROM Projects WHERE projID = ?",
            (proj_id,)
        )
        if not cursor.fetchone():
            return False, "Selected project does not exist."

        # Check for duplicate phase title within the same project
        cursor.execute(
            "SELECT phaseID FROM Phases WHERE projID = ? AND phaseTitle = ?",
            (proj_id, title)
        )
        if cursor.fetchone():
            return False, "A phase with this title already exists for that project."

        # Insert new phase
        cursor.execute(
            """
            INSERT INTO Phases (projID, phaseTitle, phaseDueDate, phaseDescription)
            VALUES (?, ?, ?, ?)
            """,
            (proj_id, title, due_date, description)
        )

        conn.commit()

    return True, "Phase created successfully."