class UserProgress:
    def __init__(self, id, user_id, lesson_id, test_id, status, score, completed_at):
        self.id = id
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.test_id = test_id
        self.status = status          # in_progress, completed, failed
        self.score = score            # float или None
        self.completed_at = completed_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            lesson_id=data.get('lesson_id'),
            test_id=data.get('test_id'),
            status=data['status'],
            score=data.get('score'),
            completed_at=data.get('completed_at')
        )