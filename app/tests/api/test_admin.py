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

    # Изменяем роль student на admin
    response = client.post('/admin/users/2/role', data={'role': 'admin'}, follow_redirects=True)
    assert 'Роль обновлена' in response.data.decode('utf-8')

    # Возвращаем обратно
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