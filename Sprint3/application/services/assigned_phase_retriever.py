from init_db import get_connection


def get_assigned_phases_for_user(user_id):
    """
    Retrieves all phases assigned to a specific user.

    Returns:
        List of tuples containing phase/project assignment information.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                Phases.phaseID,
                Phases.projID,
                Phases.phaseTitle,
                Phases.phaseDueDate,
                Phases.phaseDescription,
                Projects.projTitle,
                Workers.role
            FROM Workers
            JOIN Phases ON Workers.phaseID = Phases.phaseID
            JOIN Projects ON Phases.projID = Projects.projID
            WHERE Workers.userID = ?
            """,
            (user_id,)
        )

        return cursor.fetchall()