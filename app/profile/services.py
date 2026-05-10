from app.db.connection import fetch_all, fetch_one
from app.models.user_progress import UserProgress

def get_user_progress(user_id):
    """Возвращает полный прогресс пользователя: уроки и тесты."""
    # Получаем все записи прогресса для данного пользователя
    rows = fetch_all(
        "SELECT * FROM user_progress WHERE user_id = %s ORDER BY completed_at DESC",
        (user_id,)
    )
    progress_list = [UserProgress.from_dict(r) for r in rows]
    return progress_list

def get_progress_with_names(user_id):
    """
    Возвращает прогресс в удобном для отображения виде:
    список словарей с названиями уроков/тестов и модулей.
    """
    progress = get_user_progress(user_id)
    result = []
    for p in progress:
        item = {'status': p.status, 'score': p.score, 'completed_at': p.completed_at}
        if p.lesson_id:
            # Это урок
            lesson = fetch_one("SELECT title, module_id FROM lessons WHERE id = %s", (p.lesson_id,))
            if lesson:
                item['type'] = 'lesson'
                item['title'] = lesson['title']
                item['module_id'] = lesson['module_id']
                module = fetch_one("SELECT title FROM modules WHERE id = %s", (lesson['module_id'],))
                item['module_title'] = module['title'] if module else 'Неизвестный модуль'
        elif p.test_id:
            # Это тест
            test = fetch_one("SELECT title, module_id FROM tests WHERE id = %s", (p.test_id,))
            if test:
                item['type'] = 'test'
                item['title'] = test['title']
                item['module_id'] = test['module_id']
                module = fetch_one("SELECT title FROM modules WHERE id = %s", (test['module_id'],))
                item['module_title'] = module['title'] if module else 'Неизвестный модуль'
        result.append(item)
    return result

def get_module_progress_summary(user_id):
    """
    Возвращает сводку по модулям: процент пройденных уроков и тестов.
    """
    modules = fetch_all("SELECT * FROM modules ORDER BY \"order\"")
    summary = []
    for mod in modules:
        # Считаем общее количество уроков в модуле
        total_lessons = fetch_one("SELECT COUNT(*) as cnt FROM lessons WHERE module_id = %s", (mod['id'],))['cnt']
        # Считаем завершенные уроки пользователем в этом модуле
        completed_lessons = fetch_one(
            "SELECT COUNT(*) as cnt FROM user_progress WHERE user_id = %s AND lesson_id IN "
            "(SELECT id FROM lessons WHERE module_id = %s) AND status = 'completed'",
            (user_id, mod['id'])
        )['cnt']
        
        # Тесты: есть ли тест в модуле и пройден ли он
        test = fetch_one("SELECT id FROM tests WHERE module_id = %s LIMIT 1", (mod['id'],))
        test_completed = False
        test_score = None
        if test:
            test_progress = fetch_one(
                "SELECT status, score FROM user_progress WHERE user_id = %s AND test_id = %s AND status = 'completed'",
                (user_id, test['id'])
            )
            if test_progress:
                test_completed = True
                test_score = test_progress['score']
        
        summary.append({
            'module_title': mod['title'],
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'lesson_percent': round(completed_lessons / total_lessons * 100) if total_lessons else 0,
            'test_completed': test_completed,
            'test_score': test_score
        })
    return summary