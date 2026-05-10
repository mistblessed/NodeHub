from app.db.connection import fetch_all, fetch_one
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.test import Test

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