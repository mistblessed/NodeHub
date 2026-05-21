from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.quizzes.services import (
    get_test_by_id, get_questions_for_test, calculate_score, 
    save_test_result, save_user_answers, get_user_rank, get_total_participants
)

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.route('/test/<int:test_id>', methods=['GET'])
@login_required
def show_test(test_id):
    test = get_test_by_id(test_id)
    if not test:
        abort(404)
    questions = get_questions_for_test(test_id)
    return render_template('quizzes/test.html', test=test, questions=questions, page_title=test.title)

@quizzes_bp.route('/test/<int:test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    test = get_test_by_id(test_id)
    if not test:
        abort(404)

    # Собираем ответы из формы
    answers = {}
    for key, value in request.form.items():
        if key.startswith('q_'):
            q_id = key[2:]  # убираем префикс "q_"
            # Если value список (для multiple choice), объединяем в JSON-строку
            if isinstance(value, list):
                answers[q_id] = json.dumps(value)
            else:
                answers[q_id] = value

    # Вычисляем результат
    correct, total, percent = calculate_score(test_id, answers)
    # Сохраняем результат и ответы
    save_test_result(current_user.id, test_id, percent)
    save_user_answers(current_user.id, answers)

    rank = get_user_rank(test_id, current_user.id)
    total_participants = get_total_participants(test_id)

    return render_template('quizzes/result.html',
                           test=test, correct=correct, total=total, percent=percent,
                           rank=rank, total_participants=total_participants, page_title=f'{test.title} — Результат')

# Для JSON
import json