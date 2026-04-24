from init_db import get_connection

def check_user(email, password):
    email = email.strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM Users WHERE email = ?", (email,))
        result = cursor.fetchone()

    if result and result[1] == password:
        return result[0]
    
    return None
