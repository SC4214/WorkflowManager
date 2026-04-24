import sqlite3

def update_project_details(project_id, due_date, description):
    """
    Updates the due date and description for a specific project.

    Args:
        project_id (int): The ID of the project to update.
        due_date (str): The new due date in 'YYYY-MM-DD' format.
        description (str): The new description.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        conn = sqlite3.connect('data/workflow_manager.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Projects
            SET projDueDate = ?, projDescription = ?
            WHERE projID = ?
        """, (due_date, description, project_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()
