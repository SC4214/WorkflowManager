from init_db import get_connection

def create_project(title, dueDate, manager_id, description):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if project exists
        cursor.execute("SELECT projID FROM Projects WHERE projTitle = ?", (title,))
        if cursor.fetchone():
            return False, "A project with this title already exists."

        # Insert new account
        cursor.execute("INSERT INTO Projects (projTitle, projDueDate, projManagerID, projDescription) VALUES (?, ?, ?, ?)", (title, dueDate, manager_id, description))

    return True, "Project created successfully"

    
