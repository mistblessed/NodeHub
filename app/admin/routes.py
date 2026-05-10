from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from functools import wraps
import json
from app.admin.services import (
    get_all_users, update_user_role,
    get_all_modules, get_module_by_id, create_module, update_module, delete_module,
    get_lessons_for_module, get_lesson_by_id, create_lesson, update_lesson, delete_lesson,
    get_tests_for_module, get_test_by_id, create_test, update_test, delete_test,
    get_questions_for_test, delete_user, create_question, update_question, delete_question, get_question_by_id)
from app.feedback.services import get_all_feedback, get_feedback_by_id, update_feedback_status, delete_feedback


admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Декоратор для ограничения доступа только администраторам."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Доступ запрещён. Требуются права администратора.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ------------------- ГЛАВНАЯ АДМИНКИ -------------------
@admin_bp.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

# ------------------- ПОЛЬЗОВАТЕЛИ -------------------
@admin_bp.route('/users')
@admin_required
def list_users():
    users = get_all_users()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@admin_required
def change_role(user_id):
    new_role = request.form.get('role')
    if new_role in ('student', 'admin'):
        update_user_role(user_id, new_role)
        flash('Роль обновлена.', 'success')
    else:
        flash('Недопустимая роль.', 'danger')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user_view(user_id):
    if current_user.id == user_id:
        flash('Нельзя удалить самого себя.', 'danger')
    else:
        delete_user(user_id)
        flash('Пользователь удалён.', 'success')
    return redirect(url_for('admin.list_users'))

# ------------------- МОДУЛИ -------------------
@admin_bp.route('/modules')
@admin_required
def list_modules():
    modules = get_all_modules()
    return render_template('admin/modules.html', modules=modules)

@admin_bp.route('/modules/new', methods=['GET', 'POST'])
@admin_required
def create_module_view():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        order = request.form.get('order', 0)
        create_module(title, description, order)
        flash('Модуль создан.', 'success')
        return redirect(url_for('admin.list_modules'))
    return render_template('admin/module_form.html', module=None)

@admin_bp.route('/modules/<int:module_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_module(module_id):
    module = get_module_by_id(module_id)
    if not module:
        abort(404)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        order = request.form.get('order', 0)
        update_module(module_id, title, description, order)
        flash('Модуль обновлён.', 'success')
        return redirect(url_for('admin.list_modules'))
    return render_template('admin/module_form.html', module=module)

@admin_bp.route('/modules/<int:module_id>/delete', methods=['POST'])
@admin_required
def delete_module_view(module_id):
    delete_module(module_id)
    flash('Модуль удалён.', 'success')
    return redirect(url_for('admin.list_modules'))

# ------------------- УРОКИ (внутри модуля) -------------------
@admin_bp.route('/modules/<int:module_id>/lessons')
@admin_required
def list_lessons(module_id):
    module = get_module_by_id(module_id)
    if not module:
        abort(404)
    lessons = get_lessons_for_module(module_id)
    return render_template('admin/lessons.html', module=module, lessons=lessons)

@admin_bp.route('/modules/<int:module_id>/lessons/new', methods=['GET', 'POST'])
@admin_required
def create_lesson_view(module_id):
    module = get_module_by_id(module_id)
    if not module:
        abort(404)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        order = request.form.get('order', 0)
        create_lesson(title, content, order, module_id)
        flash('Урок создан.', 'success')
        return redirect(url_for('admin.list_lessons', module_id=module_id))
    return render_template('admin/lesson_form.html', module=module, lesson=None)

@admin_bp.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_lesson(lesson_id):
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        abort(404)
    module = get_module_by_id(lesson.module_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        order = request.form.get('order', 0)
        update_lesson(lesson_id, title, content, order, lesson.module_id)
        flash('Урок обновлён.', 'success')
        return redirect(url_for('admin.list_lessons', module_id=lesson.module_id))
    return render_template('admin/lesson_form.html', module=module, lesson=lesson)

@admin_bp.route('/lessons/<int:lesson_id>/delete', methods=['POST'])
@admin_required
def delete_lesson_view(lesson_id):
    lesson = get_lesson_by_id(lesson_id)
    if lesson:
        delete_lesson(lesson_id)
        flash('Урок удалён.', 'success')
        return redirect(url_for('admin.list_lessons', module_id=lesson.module_id))
    abort(404)


# ------------------- ВОПРОСЫ -------------------
@admin_bp.route('/tests/<int:test_id>/questions/new', methods=['GET', 'POST'])
@admin_required
def add_question(test_id):
    test = get_test_by_id(test_id)
    if not test:
        abort(404)
    if request.method == 'POST':
        text = request.form['text'].strip()
        qtype = request.form['question_type']
        options = None
        errors = []
        
        # Валидация текста вопроса
        if not text:
            errors.append('Текст вопроса обязателен.')
        
        # Обработка вариантов в зависимости от типа
        if qtype in ('single_choice', 'multiple_choice'):
            options_str = request.form.get('options', '').strip()
            if not options_str:
                errors.append('Для этого типа вопроса необходимо указать варианты ответов.')
            else:
                try:
                    options = json.loads(options_str)
                    if not isinstance(options, list) or len(options) == 0:
                        errors.append('Варианты должны быть непустым JSON-массивом.')
                except json.JSONDecodeError:
                    errors.append('Неверный формат вариантов. Введите JSON-массив, например: ["Ответ 1", "Ответ 2"].')
        elif qtype == 'text_input':
            options = None  # явно убираем
        else:
            errors.append('Неизвестный тип вопроса.')
        
        correct = request.form.get('correct_answer', '').strip()
        if not correct:
            errors.append('Правильный ответ обязателен.')
        
        if errors:
            for err in errors:
                flash(err, 'danger')
            # Вернуть форму с введёнными данными
            return render_template('admin/question_form.html', test=test, question=None, form_data=request.form)
        
        create_question(text, qtype, options, correct, test_id)
        flash('Вопрос добавлен.', 'success')
        return redirect(url_for('admin.edit_test', test_id=test_id))
    return render_template('admin/question_form.html', test=test, question=None, form_data=None)

@admin_bp.route('/tests/<int:test_id>/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(test_id, question_id):
    test = get_test_by_id(test_id)
    if not test:
        abort(404)
    question = get_question_by_id(question_id)
    if not question:
        abort(404)
    if request.method == 'POST':
        text = request.form['text'].strip()
        qtype = request.form['question_type']
        options = None
        errors = []
        
        if not text:
            errors.append('Текст вопроса обязателен.')
        
        if qtype in ('single_choice', 'multiple_choice'):
            options_str = request.form.get('options', '').strip()
            if not options_str:
                errors.append('Варианты ответов обязательны.')
            else:
                try:
                    options = json.loads(options_str)
                    if not isinstance(options, list) or len(options) == 0:
                        errors.append('Варианты должны быть непустым JSON-массивом.')
                except json.JSONDecodeError:
                    errors.append('Неверный формат вариантов.')
        elif qtype == 'text_input':
            options = None
        
        correct = request.form.get('correct_answer', '').strip()
        if not correct:
            errors.append('Правильный ответ обязателен.')
        
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('admin/question_form.html', test=test, question=question, form_data=request.form)
        
        update_question(question_id, text, qtype, options, correct)
        flash('Вопрос обновлён.', 'success')
        return redirect(url_for('admin.edit_test', test_id=test_id))
    # GET: отображаем форму с текущими данными вопроса
    return render_template('admin/question_form.html', test=test, question=question, form_data=None)

@admin_bp.route('/tests/<int:test_id>/questions/<int:question_id>/delete', methods=['POST'])
@admin_required
def delete_question_view(test_id, question_id):
    delete_question(question_id)
    flash('Вопрос удалён.', 'success')
    return redirect(url_for('admin.edit_test', test_id=test_id))

# ------------------- ОБРАТНАЯ СВЯЗЬ -------------------
@admin_bp.route('/feedback')
@admin_required
def feedback_list():
    status_filter = request.args.get('status')
    feedbacks = get_all_feedback(status_filter)
    return render_template('admin/feedback_list.html', feedbacks=feedbacks, current_filter=status_filter)

@admin_bp.route('/feedback/<int:feedback_id>')
@admin_required
def feedback_detail(feedback_id):
    fb = get_feedback_by_id(feedback_id)
    if not fb:
        abort(404)
    return render_template('admin/feedback_detail.html', feedback=fb)

@admin_bp.route('/feedback/<int:feedback_id>/status', methods=['POST'])
@admin_required
def feedback_change_status(feedback_id):
    new_status = request.form.get('status')
    if new_status in ('new', 'read', 'replied'):
        update_feedback_status(feedback_id, new_status)
        flash('Статус обновлён.', 'success')
    return redirect(url_for('admin.feedback_detail', feedback_id=feedback_id))

@admin_bp.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
@admin_required
def feedback_delete(feedback_id):
    delete_feedback(feedback_id)
    flash('Обращение удалено.', 'success')
    return redirect(url_for('admin.feedback_list'))

# ------------------- ТЕСТЫ (внутри модуля) -------------------
@admin_bp.route('/modules/<int:module_id>/tests')
@admin_required
def list_tests(module_id):
    module = get_module_by_id(module_id)
    if not module:
        abort(404)
    tests = get_tests_for_module(module_id)
    return render_template('admin/tests.html', module=module, tests=tests)

@admin_bp.route('/modules/<int:module_id>/tests/new', methods=['GET', 'POST'])
@admin_required
def create_test_view(module_id):
    module = get_module_by_id(module_id)
    if not module:
        abort(404)
    if request.method == 'POST':
        title = request.form['title']
        create_test(title, module_id)
        flash('Тест создан.', 'success')
        return redirect(url_for('admin.list_tests', module_id=module_id))
    return render_template('admin/test_form.html', module=module, test=None)

@admin_bp.route('/tests/<int:test_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_test(test_id):
    test = get_test_by_id(test_id)
    if not test:
        abort(404)
    module = get_module_by_id(test.module_id)
    if request.method == 'POST':
        title = request.form['title']
        update_test(test_id, title)
        flash('Тест обновлён.', 'success')
        return redirect(url_for('admin.list_tests', module_id=test.module_id))
    questions = get_questions_for_test(test_id)
    return render_template('admin/test_edit.html', module=module, test=test, questions=questions)

@admin_bp.route('/tests/<int:test_id>/delete', methods=['POST'])
@admin_required
def delete_test_view(test_id):
    test = get_test_by_id(test_id)
    if test:
        delete_test(test_id)
        flash('Тест удалён.', 'success')
        return redirect(url_for('admin.list_tests', module_id=test.module_id))
    abort(404)