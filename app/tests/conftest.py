import os
import bcrypt
import pytest
from app import create_app
from app.db.connection import get_pool, get_connection, return_connection

@pytest.fixture(scope='session')
def app():
    os.environ['DB_NAME'] = 'nodehub_test_db'
    os.environ['WTF_CSRF_ENABLED'] = 'False'
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    
    # Генерируем хеши паролей именно здесь
    admin_hash = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode()
    student_hash = bcrypt.hashpw('student123'.encode(), bcrypt.gensalt()).decode()
    
    with app.app_context():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Создание таблиц
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id              SERIAL          PRIMARY KEY,
                    username        VARCHAR(50)     NOT NULL UNIQUE,
                    email           VARCHAR(120)    NOT NULL UNIQUE,
                    password_hash   VARCHAR(255)    NOT NULL,
                    role            VARCHAR(20)     NOT NULL DEFAULT 'student'
                                    CHECK (role IN ('student', 'admin')),
                    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS modules (
                    id              SERIAL          PRIMARY KEY,
                    title           VARCHAR(200)    NOT NULL,
                    description     TEXT,
                    "order"         INTEGER         NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS lessons (
                    id                  SERIAL          PRIMARY KEY,
                    title               VARCHAR(200)    NOT NULL,
                    theoretical_content TEXT            NOT NULL,
                    "order"             INTEGER         NOT NULL DEFAULT 0,
                    module_id           INTEGER         NOT NULL REFERENCES modules(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS tests (
                    id          SERIAL          PRIMARY KEY,
                    title       VARCHAR(200)    NOT NULL,
                    module_id   INTEGER         NOT NULL REFERENCES modules(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS questions (
                    id              SERIAL          PRIMARY KEY,
                    text            TEXT            NOT NULL,
                    question_type   VARCHAR(30)     NOT NULL
                                    CHECK (question_type IN ('single_choice', 'multiple_choice', 'text_input')),
                    options         JSONB,
                    correct_answer  TEXT            NOT NULL,
                    test_id         INTEGER         NOT NULL REFERENCES tests(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS user_progress (
                    id              SERIAL          PRIMARY KEY,
                    user_id         INTEGER         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    lesson_id       INTEGER         REFERENCES lessons(id) ON DELETE SET NULL,
                    test_id         INTEGER         REFERENCES tests(id) ON DELETE SET NULL,
                    status          VARCHAR(30)     NOT NULL DEFAULT 'in_progress'
                                    CHECK (status IN ('in_progress', 'completed', 'failed')),
                    score           REAL,
                    completed_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    CONSTRAINT chk_progress_object CHECK (
                        (lesson_id IS NOT NULL AND test_id IS NULL) OR
                        (lesson_id IS NULL AND test_id IS NOT NULL)
                    )
                );
                CREATE TABLE IF NOT EXISTS user_answers (
                    id              SERIAL          PRIMARY KEY,
                    user_id         INTEGER         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    question_id     INTEGER         NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
                    given_answer    TEXT            NOT NULL,
                    is_correct      BOOLEAN         NOT NULL,
                    answered_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                """)
                
                # Очистка и наполнение
                cur.execute("TRUNCATE TABLE user_answers, user_progress, questions, tests, lessons, modules, users RESTART IDENTITY CASCADE;")
                
                cur.execute("""
                INSERT INTO users (username, email, password_hash, role) VALUES
                ('admin',   'admin@nodehub.ru',   %s, 'admin'),
                ('student', 'student@nodehub.ru', %s, 'student')
                """, (admin_hash, student_hash))
                
                cur.execute("""
                INSERT INTO modules (title, description, "order") VALUES
                ('Основы Node.js', 'Введение', 1),
                ('Модули и NPM', 'Система модулей', 2)
                """)
                
                cur.execute("""
                INSERT INTO lessons (title, theoretical_content, "order", module_id) VALUES
                ('Что такое Node.js?', 'Контент урока 1', 1, 1),
                ('Установка', 'Контент урока 2', 2, 1)
                """)
                
                cur.execute("""
                INSERT INTO tests (title, module_id) VALUES
                ('Тест: Основы', 1)
                """)
                
                cur.execute("""
                INSERT INTO questions (text, question_type, options, correct_answer, test_id) VALUES
                ('На каком движке работает Node.js?', 'single_choice', '["V8", "SpiderMonkey"]', 'V8', 1),
                ('Что делает process?', 'multiple_choice', '["Информация о процессе", "DOM-дерево"]', '["Информация о процессе"]', 1),
                ('Введите команду для проверки версии Node.js', 'text_input', NULL, 'node -v', 1)
                """)
                
                # Прогресс студента
                cur.execute("""
                INSERT INTO user_progress (user_id, lesson_id, status) VALUES
                (2, 1, 'completed')
                """)
                
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            return_connection(conn)
    
    yield app
    
    # Очистка после всех тестов
    with app.app_context():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS user_answers CASCADE")
                cur.execute("DROP TABLE IF EXISTS user_progress CASCADE")
                cur.execute("DROP TABLE IF EXISTS questions CASCADE")
                cur.execute("DROP TABLE IF EXISTS tests CASCADE")
                cur.execute("DROP TABLE IF EXISTS lessons CASCADE")
                cur.execute("DROP TABLE IF EXISTS modules CASCADE")
                cur.execute("DROP TABLE IF EXISTS users CASCADE")
                conn.commit()
        finally:
            return_connection(conn)
    del os.environ['DB_NAME']

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth(client):
    class AuthActions:
        def login(self, username='student', password='student123'):
            return client.post('/auth/login', data={
                'username': username,
                'password': password,
            }, follow_redirects=True)
        def logout(self):
            return client.get('/auth/logout', follow_redirects=True)
    return AuthActions()