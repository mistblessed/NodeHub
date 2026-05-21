import json
from app.db.connection import fetch_one, fetch_all, execute_insert, execute_query
from app.models.test import Test
from app.models.question import Question

def get_test_by_id(test_id):
    """Получить тест по ID."""
    row = fetch_one("SELECT * FROM tests WHERE id = %s", (test_id,))
    if row:
        return Test.from_dict(row)
    return None

def get_questions_for_test(test_id):
    """Получить все вопросы теста."""
    rows = fetch_all("SELECT * FROM questions WHERE test_id = %s ORDER BY id", (test_id,))
    return [Question.from_dict(r) for r in rows]

def check_answer(question, user_answer):
    """
    Проверяет ответ пользователя на вопрос.
    Возвращает True, если ответ правильный.
    """
    if question.question_type == 'single_choice':
        # Простое сравнение строки
        return user_answer.strip() == question.correct_answer.strip()
    elif question.question_type == 'multiple_choice':
        # Ожидаем, что correct_answer - это строка с JSON-массивом выбранных вариантов
        # user_answer - тоже строка, полученная из формы (список через запятую или JSON)
        try:
            correct = set(json.loads(question.correct_answer))
            user = set(json.loads(user_answer))
        except (json.JSONDecodeError, TypeError):
            # Если не JSON, пробуем разбить по запятой
            correct = set(question.correct_answer.split(','))
            user = set(user_answer.split(','))
        return correct == user
    elif question.question_type == 'text_input':
        # Сравнение без учёта регистра и пробелов
        return user_answer.strip().lower() == question.correct_answer.strip().lower()
    return False

def calculate_score(test_id, user_answers_dict):
    """
    Вычисляет процент правильных ответов.
    user_answers_dict: словарь {question_id: ответ_пользователя}
    Возвращает (количество_правильных, общее_количество, процент).
    """
    questions = get_questions_for_test(test_id)
    total = len(questions)
    if total == 0:
        return 0, 0, 0.0
    correct_count = 0
    for q in questions:
        user_ans = user_answers_dict.get(str(q.id))
        if user_ans and check_answer(q, user_ans):
            correct_count += 1
    percent = round((correct_count / total) * 100, 1)
    return correct_count, total, percent

def save_test_result(user_id, test_id, score):
    """Сохраняет результат теста в user_progress (завершённый)."""
    # Проверим, есть ли уже запись (может, обновить?)
    existing = fetch_one(
        "SELECT id FROM user_progress WHERE user_id = %s AND test_id = %s",
        (user_id, test_id)
    )
    if existing:
        execute_query(
            "UPDATE user_progress SET status = 'completed', score = %s, completed_at = NOW() WHERE id = %s",
            (score, existing['id'])
        )
        return existing['id']
    else:
        return execute_insert(
            "INSERT INTO user_progress (user_id, test_id, status, score) VALUES (%s, %s, 'completed', %s) RETURNING id",
            (user_id, test_id, score)
        )

def save_user_answers(user_id, answers_dict):
    """Сохраняет детальные ответы пользователя на каждый вопрос."""
    for question_id, user_answer in answers_dict.items():
        # Получаем вопрос для проверки is_correct
        q = fetch_one("SELECT * FROM questions WHERE id = %s", (int(question_id),))
        if q:
            question = Question.from_dict(q)
            is_correct = check_answer(question, user_answer)
            # Вставляем запись
            execute_insert(
                "INSERT INTO user_answers (user_id, question_id, given_answer, is_correct) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, int(question_id), user_answer, is_correct)
            )

def get_user_rank(test_id, user_id):
    """Возвращает место пользователя по конкретному тесту (лучшая попытка)."""
    query = """
        WITH best_scores AS (
            SELECT user_id, MAX(score) as best_score
            FROM user_progress
            WHERE test_id = %s AND status = 'completed' AND score IS NOT NULL
            GROUP BY user_id
        ),
        ranked AS (
            SELECT user_id, best_score,
                   RANK() OVER (ORDER BY best_score DESC) as rank
            FROM best_scores
        )
        SELECT rank FROM ranked WHERE user_id = %s
    """
    row = fetch_one(query, (test_id, user_id))
    return row['rank'] if row else None

def get_total_participants(test_id):
    """Количество уникальных участников, завершивших тест."""
    query = """
        SELECT COUNT(DISTINCT user_id) as cnt
        FROM user_progress
        WHERE test_id = %s AND status = 'completed' AND score IS NOT NULL
    """
    row = fetch_one(query, (test_id,))
    return row['cnt'] if row else 0