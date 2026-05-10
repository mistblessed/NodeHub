from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.courses.services import get_all_modules, get_lesson_by_id, get_lessons_by_module, get_tests_by_module, complete_lesson
from app.quizzes.services import get_test_by_id
from app.db.connection import fetch_one

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/modules')
def modules_list():
    """Страница со списком всех модулей курса."""
    modules = get_all_modules()
    return render_template('courses/modules.html', modules=modules)

@courses_bp.route('/modules/<int:module_id>')
def module_detail(module_id):
    modules = get_all_modules()
    selected_module = next((m for m in modules if m.id == module_id), None)
    if not selected_module:
        abort(404)
    lessons = get_lessons_by_module(module_id)
    tests = get_tests_by_module(module_id)  # список тестов
    return render_template('courses/module_detail.html',
                           modules=modules,
                           selected_module=selected_module,
                           lessons=lessons,
                           tests=tests)  

@courses_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson_view(lesson_id):
    complete_lesson(current_user.id, lesson_id)
    flash('Урок отмечен как пройденный!', 'success')
    # Перенаправим обратно на страницу урока
    return redirect(url_for('courses.lesson_detail', lesson_id=lesson_id))


@courses_bp.route('/lessons/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        abort(404)
    modules = get_all_modules()
    module = next((m for m in modules if m.id == lesson.module_id), None)
    # Проверим, завершён ли урок
    from app.db.connection import fetch_one
    progress = fetch_one(
        "SELECT status FROM user_progress WHERE user_id = %s AND lesson_id = %s",
        (current_user.id, lesson_id)
    )
    completed = progress and progress['status'] == 'completed'
    return render_template('courses/lesson.html', lesson=lesson, module=module, completed=completed)