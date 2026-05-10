def test_modules_list(client):
    response = client.get('/courses/modules')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'Основы Node.js' in decoded

def test_module_detail(client):
    response = client.get('/courses/modules/1')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'Основы Node.js' in decoded
    assert 'Что такое Node.js?' in decoded

def test_lesson_requires_login(client):
    response = client.get('/courses/lessons/1', follow_redirects=True)
    decoded = response.data.decode('utf-8')
    assert 'Пожалуйста, войдите' in decoded

def test_lesson_accessible_after_login(client, auth):
    auth.login()
    response = client.get('/courses/lessons/1')
    decoded = response.data.decode('utf-8')
    assert 'Контент урока 1' in decoded