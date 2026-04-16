from init_db import get_connection


def get_phases_for_project(project_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT phaseID, projID, phaseTitle, phaseDueDate, phaseDescription
            FROM Phases
            WHERE projID = ?
            """,
            (project_id,)
        )
        rows = cursor.fetchall()

    return rows