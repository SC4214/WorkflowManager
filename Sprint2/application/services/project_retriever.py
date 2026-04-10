from init_db import get_connection
from services.project_object import ProjectNode

def get_projects_for_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT projID, projTitle, projDueDate, projManagerID, projDescription
            FROM Projects
            WHERE projManagerID = ?
            """,
            (user_id,)
        )
        rows = cursor.fetchall()

    projects = []
    for row in rows:
        project = ProjectNode(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
        )
        projects.append(project)

    return projects