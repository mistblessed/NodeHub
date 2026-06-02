from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from app.config import Config
from flask_login import LoginManager, current_user
from app.models.user import User
from app.db.connection import fetch_one
from flask_wtf.csrf import CSRFProtect
from app.feedback.services import submit_feedback

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf = CSRFProtect(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        row = fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        if row:
            return User.from_dict(row)
        return None

    # Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.courses.routes import courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    from app.quizzes.routes import quizzes_bp
    app.register_blueprint(quizzes_bp, url_prefix='/quizzes')

    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # --- Основные маршруты ---
    @app.route('/')
    def index():
        return render_template('index.html', page_title='Главная')

    @app.route('/about')
    def about():
        return render_template('about.html', page_title='О проекте')

    @app.route('/contacts', methods=['GET', 'POST'])
    def contacts():
        if request.method == 'POST':
            if current_user.is_authenticated:
                user_id = current_user.id
                name = current_user.username
                email = current_user.email
            else:
                user_id = None
                name = request.form.get('name', '').strip()
                email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            errors = []
            if not name:
                errors.append('Имя обязательно')
            if not email:
                errors.append('Email обязателен')
            if not subject:
                errors.append('Тема обязательна')
            if not message:
                errors.append('Сообщение обязательно')
            if errors:
                for err in errors:
                    flash(err, 'danger')
            else:
                try:
                    submit_feedback(user_id, name, email, subject, message)
                    flash('Сообщение отправлено! Мы свяжемся с вами.', 'success')
                except Exception as e:
                    flash('Не удалось отправить сообщение. Попробуйте позже.', 'danger')
                return redirect(url_for('contacts'))
        return render_template('contacts.html', page_title='Контакты')

    # --- Обработчики ошибок ---
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', page_title='Страница не найдена'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html', page_title='Ошибка сервера'), 500

    return app