def test_register_page_loads(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert 'Регистрация' in response.data.decode('utf-8')

def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert 'Вход' in response.data.decode('utf-8')

def test_register_new_user(client, app):
    with app.app_context():
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }, follow_redirects=True)
        assert 'Регистрация прошла успешно' in response.data.decode('utf-8')
        
        from app.db.connection import fetch_one
        user = fetch_one("SELECT * FROM users WHERE username = 'newuser'")
        assert user is not None

def test_login_with_valid_credentials(client):
    response = client.post('/auth/login', data={
        'username': 'student',
        'password': 'student123',
    }, follow_redirects=True)
    assert 'Вы успешно вошли' in response.data.decode('utf-8')

def test_login_with_invalid_credentials(client):
    response = client.post('/auth/login', data={
        'username': 'student',
        'password': 'wrongpass',
    }, follow_redirects=True)
    assert 'Неверный логин или пароль' in response.data.decode('utf-8')

def test_logout(client, auth):
    auth.login()
    response = auth.logout()
    assert 'Вы вышли из системы' in response.data.decode('utf-8')