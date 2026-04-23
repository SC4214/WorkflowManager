"""
role_assigner.py

This module handles worker assignment logic for the Workflow Manager application.

Responsibilities:
    - Validate whether a worker can be assigned to a phase
    - Ensure the selected phase exists
    - Ensure the selected user exists
    - Prevent duplicate worker assignments for the same phase
    - Insert worker-role assignment records into the database
"""
from init_db import get_connection


def assign_role(userID, phaseID, role):
    """
    PRE:
        - userID is a valid user ID
        - phaseID is a valid phase ID
        - role is provided as a non-empty string
        - The database connection can be established
        - The Users, Phases, and Workers tables exist in the database

    POST:
        - If the selected phase does not exist, no assignment is created
        - If the selected user does not exist, no assignment is created
        - If the user is already assigned to the selected phase,
          no duplicate assignment is created
        - Otherwise, a new worker assignment record is inserted
          into the Workers table
        - A tuple indicating success or failure is returned

    Returns:
        - (bool, str):
            - True and success message if assignment succeeds
            - False and error message if assignment fails
    """
    empID = userID
    phaseNum = phaseID
    empRole = role

    if not empID or not phaseNum or not empRole:
        return False, "Please provide a phase, role, and at least one employee to assign."

    with get_connection() as conn:
        cursor = conn.cursor()

        # Verify selected phase exists
        cursor.execute(
            "SELECT phaseID FROM Phases WHERE phaseID = ?",
            (phaseNum,)
        )
        if not cursor.fetchone():
            return False, "The selected phase does not exist."

        # Verify selected user exists
        cursor.execute(
            "SELECT id FROM Users WHERE id = ?",
            (empID,)
        )
        if not cursor.fetchone():
            return False, "The selected user does not exist."

        # Verify the user isn't already assigned to the phase
        cursor.execute(
            "SELECT userID FROM Workers WHERE phaseID = ? AND userID = ?",
            (phaseNum, empID)
        )
        if cursor.fetchone():
            return False, "One or more of the selected employees is already assigned to this phase."

        # Assign user to phase
        cursor.execute(
            """
            INSERT INTO Workers (userID, phaseID, role)
            VALUES (?, ?, ?)
            """,
            (empID, phaseNum, empRole)
        )

        conn.commit()

    return True, "Employee(s) successfully assigned."