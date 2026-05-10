class UserAnswer:
    def __init__(self, id, user_id, question_id, given_answer, is_correct, answered_at):
        self.id = id
        self.user_id = user_id
        self.question_id = question_id
        self.given_answer = given_answer
        self.is_correct = is_correct
        self.answered_at = answered_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            question_id=data['question_id'],
            given_answer=data['given_answer'],
            is_correct=data['is_correct'],
            answered_at=data.get('answered_at')
        )