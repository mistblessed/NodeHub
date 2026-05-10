from app.db.connection import fetch_all, fetch_one, execute_query, execute_insert
from app.models.user import User
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.test import Test
from app.models.question import Question
import json
from app.models.question import Question

# ------------------- ПОЛЬЗОВАТЕЛИ -------------------
def get_all_users():
    rows = fetch_all("SELECT * FROM users ORDER BY id")
    return [User.from_dict(r) for r in rows]

def update_user_role(user_id, new_role):
    execute_query("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))

def delete_user(user_id):
    execute_query("DELETE FROM users WHERE id = %s", (user_id,))

# ------------------- МОДУЛИ -------------------
def get_all_modules():
    rows = fetch_all("SELECT * FROM modules ORDER BY \"order\"")
    return [Module.from_dict(r) for r in rows]

def get_module_by_id(module_id):
    row = fetch_one("SELECT * FROM modules WHERE id = %s", (module_id,))
    return Module.from_dict(row) if row else None

def create_module(title, description, order):
    return execute_insert(
        "INSERT INTO modules (title, description, \"order\") VALUES (%s, %s, %s) RETURNING id",
        (title, description, order)
    )

def update_module(module_id, title, description, order):
    execute_query(
        "UPDATE modules SET title = %s, description = %s, \"order\" = %s WHERE id = %s",
        (title, description, order, module_id)
    )

def delete_module(module_id):
    execute_query("DELETE FROM modules WHERE id = %s", (module_id,))

# ------------------- УРОКИ -------------------
def get_lessons_for_module(module_id):
    rows = fetch_all(
        "SELECT * FROM lessons WHERE module_id = %s ORDER BY \"order\"",
        (module_id,)
    )
    return [Lesson.from_dict(r) for r in rows]

def get_lesson_by_id(lesson_id):
    row = fetch_one("SELECT * FROM lessons WHERE id = %s", (lesson_id,))
    return Lesson.from_dict(row) if row else None

def create_lesson(title, content, order, module_id):
    return execute_insert(
        "INSERT INTO lessons (title, theoretical_content, \"order\", module_id) VALUES (%s, %s, %s, %s) RETURNING id",
        (title, content, order, module_id)
    )

def update_lesson(lesson_id, title, content, order, module_id):
    execute_query(
        "UPDATE lessons SET title = %s, theoretical_content = %s, \"order\" = %s, module_id = %s WHERE id = %s",
        (title, content, order, module_id, lesson_id)
    )

def delete_lesson(lesson_id):
    # Удаляем прогресс по этому уроку
    execute_query("DELETE FROM user_progress WHERE lesson_id = %s", (lesson_id,))
    execute_query("DELETE FROM lessons WHERE id = %s", (lesson_id,))

# ------------------- ТЕСТЫ -------------------
def get_tests_for_module(module_id):
    rows = fetch_all("SELECT * FROM tests WHERE module_id = %s", (module_id,))
    return [Test.from_dict(r) for r in rows]

def get_test_by_id(test_id):
    row = fetch_one("SELECT * FROM tests WHERE id = %s", (test_id,))
    return Test.from_dict(row) if row else None

def create_test(title, module_id):
    return execute_insert(
        "INSERT INTO tests (title, module_id) VALUES (%s, %s) RETURNING id",
        (title, module_id)
    )

def update_test(test_id, title):
    execute_query("UPDATE tests SET title = %s WHERE id = %s", (title, test_id))

def delete_test(test_id):
    # Сначала удаляем ответы пользователей на вопросы этого теста
    execute_query(
        "DELETE FROM user_answers WHERE question_id IN (SELECT id FROM questions WHERE test_id = %s)",
        (test_id,)
    )
    # Удаляем прогресс по этому тесту
    execute_query("DELETE FROM user_progress WHERE test_id = %s", (test_id,))
    # Теперь можно удалить сам тест (каскадно удалятся вопросы)
    execute_query("DELETE FROM tests WHERE id = %s", (test_id,))

# ------------------- ВОПРОСЫ -------------------
def get_questions_for_test(test_id):
    rows = fetch_all("SELECT * FROM questions WHERE test_id = %s ORDER BY id", (test_id,))
    return [Question.from_dict(r) for r in rows]

def get_question_by_id(question_id):
    row = fetch_one("SELECT * FROM questions WHERE id = %s", (question_id,))
    if row:
        return Question.from_dict(row)
    return None

def create_question(text, question_type, options, correct_answer, test_id):
    # Если options не None, сериализуем в JSON-строку
    options_json = json.dumps(options) if options is not None else None
    return execute_insert(
        "INSERT INTO questions (text, question_type, options, correct_answer, test_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (text, question_type, options_json, correct_answer, test_id)
    )

def update_question(question_id, text, question_type, options, correct_answer):
    options_json = json.dumps(options) if options is not None else None
    execute_query(
        "UPDATE questions SET text = %s, question_type = %s, options = %s, correct_answer = %s WHERE id = %s",
        (text, question_type, options_json, correct_answer, question_id)
    )

def delete_question(question_id):
    execute_query("DELETE FROM questions WHERE id = %s", (question_id,))

# Дополнительные сервисы для вопросов понадобятся позже