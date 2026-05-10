from flask import Flask, render_template
from app.config import Config
from flask_login import LoginManager
from app.models.user import User
from app.db.connection import fetch_one
from flask_wtf.csrf import CSRFProtect


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

    @app.route('/')
    def index():
        return render_template('index.html')

    return app