from app.db.connection import fetch_all, fetch_one, execute_insert, execute_query
from app.models.feedback import Feedback

def submit_feedback(user_id, name, email, subject, message):
    """Создаёт новое обращение."""
    return execute_insert(
        "INSERT INTO feedback (user_id, name, email, subject, message) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (user_id, name, email, subject, message)
    )

def get_all_feedback(status=None):
    """Возвращает список обращений, опционально фильтруя по статусу."""
    if status:
        rows = fetch_all("SELECT * FROM feedback WHERE status = %s ORDER BY created_at DESC", (status,))
    else:
        rows = fetch_all("SELECT * FROM feedback ORDER BY created_at DESC")
    return [Feedback.from_dict(r) for r in rows]

def get_feedback_by_id(feedback_id):
    row = fetch_one("SELECT * FROM feedback WHERE id = %s", (feedback_id,))
    if row:
        return Feedback.from_dict(row)
    return None

def update_feedback_status(feedback_id, new_status):
    execute_query("UPDATE feedback SET status = %s WHERE id = %s", (new_status, feedback_id))

def delete_feedback(feedback_id):
    execute_query("DELETE FROM feedback WHERE id = %s", (feedback_id,))