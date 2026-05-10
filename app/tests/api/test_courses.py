def test_modules_list(client):
    """Страница со списком модулей должна содержать заголовок 'Структура курса'."""
    response = client.get('/courses/modules')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'Структура курса' in decoded

def test_module_detail(client):
    """Страница конкретного модуля содержит хлебные крошки и заголовок 'Уроки'."""
    response = client.get('/courses/modules/1')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'Уроки' in decoded
    assert 'breadcrumb' in decoded   # хлебные крошки всегда есть

def test_lesson_requires_login(client):
    response = client.get('/courses/lessons/1', follow_redirects=True)
    assert 'Пожалуйста, войдите' in response.data.decode('utf-8')

def test_lesson_accessible_after_login(client, auth):
    auth.login()
    response = client.get('/courses/lessons/1')
    decoded = response.data.decode('utf-8')
    # На странице урока есть кнопка "Отметить как пройденный" или сообщение "Урок пройден"
    assert 'Отметить как пройденный' in decoded or 'Урок пройден' in decoded

def test_about_page_loads(client):
    response = client.get('/about')
    assert response.status_code == 200