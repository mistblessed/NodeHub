def test_guest_cannot_access_admin(client):
    response = client.get('/admin/', follow_redirects=True)
    assert 'Пожалуйста, войдите' in response.data.decode('utf-8')

def test_student_cannot_access_admin(client, auth):
    auth.login()
    response = client.get('/admin/', follow_redirects=True)
    assert 'Доступ запрещён' in response.data.decode('utf-8')

def test_admin_can_access_admin(client, auth):
    auth.login('admin', 'admin123')
    response = client.get('/admin/')
    assert 'Панель управления' in response.data.decode('utf-8')

def test_admin_can_manage_users(client, auth):
    auth.login('admin', 'admin123')
    response = client.get('/admin/users')
    decoded = response.data.decode('utf-8')
    assert 'student' in decoded

    # изменение роли student на admin
    response = client.post('/admin/users/2/role', data={'role': 'admin'}, follow_redirects=True)
    assert 'Роль обновлена' in response.data.decode('utf-8')

    # возвращаем обратно
    client.post('/admin/users/2/role', data={'role': 'student'}, follow_redirects=True)

def test_admin_can_create_module(client, auth):
    auth.login('admin', 'admin123')
    response = client.post('/admin/modules/new', data={
        'title': 'Новый модуль',
        'description': 'Описание',
        'order': 4
    }, follow_redirects=True)
    assert 'Модуль создан' in response.data.decode('utf-8')
    response = client.get('/admin/modules')
    assert 'Новый модуль' in response.data.decode('utf-8')

def test_admin_can_edit_module(client, auth):
    auth.login('admin', 'admin123')
    # Редактируем модуль с id=1 (точно существует)
    response = client.post('/admin/modules/1/edit', data={
        'title': 'Изменённое название',
        'description': 'Новое описание',
        'order': 1
    }, follow_redirects=True)
    assert 'Модуль обновлён' in response.data.decode('utf-8')

def test_admin_can_create_lesson(client, auth):
    auth.login('admin', 'admin123')
    response = client.post('/admin/modules/1/lessons/new', data={
        'title': 'Новый урок',
        'content': 'Контент',
        'order': 10
    }, follow_redirects=True)
    assert 'Урок создан' in response.data.decode('utf-8')

def test_admin_can_edit_lesson(client, auth):
    auth.login('admin', 'admin123')
    # Редактируем урок с id=1 (точно существует)
    response = client.post('/admin/lessons/1/edit', data={
        'title': 'Изменённый урок',
        'content': 'Обновлённый контент',
        'order': 1
    }, follow_redirects=True)
    assert 'Урок обновлён' in response.data.decode('utf-8')

def test_admin_can_create_test(client, auth):
    auth.login('admin', 'admin123')
    response = client.post('/admin/modules/1/tests/new', data={
        'title': 'Новый тест'
    }, follow_redirects=True)
    assert 'Тест создан' in response.data.decode('utf-8')

def test_admin_can_edit_test(client, auth):
    auth.login('admin', 'admin123')
    # Редактируем тест с id=1 (точно существует)
    response = client.post('/admin/tests/1/edit', data={
        'title': 'Изменённый тест'
    }, follow_redirects=True)
    assert 'Тест обновлён' in response.data.decode('utf-8')

def test_admin_can_view_lessons_and_tests(client, auth):
    auth.login('admin', 'admin123')
    response = client.get('/admin/modules/1/lessons')
    assert response.status_code == 200
    assert 'Уроки модуля' in response.data.decode('utf-8')
    response = client.get('/admin/modules/1/tests')
    assert response.status_code == 200
    assert 'Тесты модуля' in response.data.decode('utf-8')