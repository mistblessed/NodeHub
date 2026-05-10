from app.db.connection import fetch_all, fetch_one
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.test import Test
from app.db.connection import fetch_one, execute_insert, execute_query

def get_tests_by_module(module_id):
    rows = fetch_all("SELECT * FROM tests WHERE module_id = %s ORDER BY id", (module_id,))
    return [Test.from_dict(r) for r in rows]

def get_all_modules():
    rows = fetch_all("SELECT * FROM modules ORDER BY \"order\"")
    return [Module.from_dict(r) for r in rows]

def get_lesson_by_id(lesson_id):
    row = fetch_one("SELECT * FROM lessons WHERE id = %s", (lesson_id,))
    if row:
        return Lesson.from_dict(row)
    return None

def get_lessons_by_module(module_id):
    rows = fetch_all("SELECT * FROM lessons WHERE module_id = %s ORDER BY \"order\"", (module_id,))
    return [Lesson.from_dict(r) for r in rows]

def complete_lesson(user_id, lesson_id):
    # Проверим, есть ли уже запись
    existing = fetch_one(
        "SELECT id FROM user_progress WHERE user_id = %s AND lesson_id = %s",
        (user_id, lesson_id)
    )
    if existing:
        execute_query(
            "UPDATE user_progress SET status = 'completed', completed_at = NOW() WHERE id = %s",
            (existing['id'],)
        )
        return existing['id']
    else:
        return execute_insert(
            "INSERT INTO user_progress (user_id, lesson_id, status) VALUES (%s, %s, 'completed') RETURNING id",
            (user_id, lesson_id)
        )