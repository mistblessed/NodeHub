import bcrypt
from app.db.connection import fetch_one, execute_insert
from app.models.user import User

def get_user_by_username(username):
    row = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
    return User.from_dict(row) if row else None

def get_user_by_email(email):
    row = fetch_one("SELECT * FROM users WHERE email = %s", (email,))
    return User.from_dict(row) if row else None

def create_user(username, email, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = execute_insert(
        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, 'student') RETURNING id",
        (username, email, password_hash)
    )
    return get_user_by_username(username)

def verify_password(user, password):
    if user is None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))