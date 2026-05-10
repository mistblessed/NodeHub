def test_contacts_page_loads(client):
    response = client.get('/contacts')
    assert response.status_code == 200
    assert 'Контакты' in response.data.decode('utf-8')

def test_submit_feedback_authenticated(client, auth):
    auth.login()
    response = client.post('/contacts', data={
        'subject': 'Тестовая тема',
        'message': 'Тестовое сообщение'
    }, follow_redirects=True)
    assert 'Сообщение отправлено' in response.data.decode('utf-8')

def test_submit_feedback_guest(client):
    response = client.post('/contacts', data={
        'name': 'Гость',
        'email': 'guest@example.com',
        'subject': 'Вопрос',
        'message': 'Текст вопроса'
    }, follow_redirects=True)
    assert 'Сообщение отправлено' in response.data.decode('utf-8')

def test_admin_feedback_list(client, auth):
    auth.login('admin', 'admin123')
    response = client.get('/admin/feedback')
    assert 'Обратная связь' in response.data.decode('utf-8')

def test_admin_feedback_detail(client, auth):
    # Создадим обращение от студента
    auth.login()
    client.post('/contacts', data={
        'subject': 'Для детализации',
        'message': 'Детали'
    })
    auth.logout()
    auth.login('admin', 'admin123')
    # Просмотрим детали обращения с id=1
    response = client.get('/admin/feedback/1')
    assert response.status_code == 200