from init_db import get_connection

def check_user(email, password):
    email = email.strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Users WHERE email = ?", (email,))
        result = cursor.fetchone()

    if result:
        return result[0] == password

    return False
