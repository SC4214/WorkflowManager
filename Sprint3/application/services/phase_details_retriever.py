import sqlite3

def get_phase_details(phase_id):
    """
    Retrieves details for a specific phase, including the project title.

    Args:
        phase_id (int): The ID of the phase to retrieve.

    Returns:
        dict: A dictionary containing the phase details, or None if not found.
    """
    conn = sqlite3.connect('data/workflow_manager.db')
    cursor = conn.cursor()

    query = """
    SELECT
        p.projTitle,
        ph.phaseTitle,
        ph.phaseDueDate,
        ph.phaseDescription
    FROM Phases ph
    JOIN Projects p ON ph.projID = p.projID
    WHERE ph.phaseID = ?
    """

    cursor.execute(query, (phase_id,))
    details = cursor.fetchone()
    conn.close()

    if details:
        return {
            'project_title': details[0],
            'phase_title': details[1],
            'due_date': details[2],
            'description': details[3]
        }
    return None
