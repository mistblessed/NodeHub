from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.db.connection import fetch_one

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=3, max=50, message='От 3 до 50 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Обязательное поле'),
        Email(message='Некорректный email')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Обязательное поле'),
        Length(min=6, message='Минимум 6 символов')
    ])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(message='Обязательное поле'),
        EqualTo('password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = fetch_one("SELECT id FROM users WHERE username = %s", (username.data,))
        if user:
            raise ValidationError('Этот логин уже занят.')

    def validate_email(self, email):
        user = fetch_one("SELECT id FROM users WHERE email = %s", (email.data,))
        if user:
            raise ValidationError('Этот email уже используется.')

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(message='Введите логин')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])
    submit = SubmitField('Войти')