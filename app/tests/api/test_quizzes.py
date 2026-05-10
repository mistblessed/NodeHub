def test_test_page_requires_login(client):
    response = client.get('/quizzes/test/1')
    assert response.status_code == 302

def test_test_page_after_login(client, auth):
    auth.login()
    response = client.get('/quizzes/test/1')
    decoded = response.data.decode('utf-8')
    assert 'На каком движке работает Node.js?' in decoded

def test_submit_test_and_see_results(client, auth):
    auth.login()
    response = client.post('/quizzes/test/1', data={
        'q_1': 'V8',
        'q_2': '["Информация о процессе"]',
        'q_3': 'node -v',
    }, follow_redirects=True)
    decoded = response.data.decode('utf-8')
    assert 'Результат' in decoded
    assert 'Правильных ответов' in decoded

def test_result_page_shows_percent(client, auth):
    auth.login()
    response = client.post('/quizzes/test/1', data={
        'q_1': 'V8',
        'q_2': '["Информация о процессе"]',
        'q_3': 'node -v',
    }, follow_redirects=True)
    assert '%' in response.data.decode('utf-8')

def test_can_retake_test(client, auth):
    auth.login()
    response = client.get('/quizzes/test/1')
    assert response.status_code == 200