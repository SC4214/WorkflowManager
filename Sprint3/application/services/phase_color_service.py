from datetime import datetime, date

def get_due_date_colors(due_date_str):
    """
    Determines the color for a phase based on its due date.

    Args:
        due_date_str (str): The due date in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary with colors for different states.
    """
    default_colors = {
        "background": "#666666",
        "hover": "#777777",
        "pressed": "#555555",
        "border": "#888888"
    }

    if not due_date_str:
        return default_colors

    try:
        due_date = datetime.strptime(due_date_str.strip(), '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        return default_colors

    today = date.today()
    delta = due_date - today

    if delta.days < 7:
        # Red
        return {
            "background": "#c94c4c",
            "hover": "#d96c6c",
            "pressed": "#b93c3c",
            "border": "#e08d8d"
        }
    elif 7 <= delta.days < 30:
        # Orange
        return {
            "background": "#e89f28",
            "hover": "#f8b040",
            "pressed": "#d88f18",
            "border": "#f0c880"
        }
    else:
        # Green
        return {
            "background": "#5a9a5a",
            "hover": "#6ab16a",
            "pressed": "#4a894a",
            "border": "#8bcd8b"
        }
