def test_profile_requires_login(client):
    response = client.get('/profile/', follow_redirects=True)
    assert 'Пожалуйста, войдите' in response.data.decode('utf-8')

def test_profile_shows_progress(client, auth):
    auth.login()
    response = client.get('/profile/')
    decoded = response.data.decode('utf-8')
    # Должен быть заголовок "Прогресс по модулям" и блок "Последние действия"
    assert 'Прогресс по модулям' in decoded
    assert 'Последние действия' in decoded