class Question:
    def __init__(self, id, text, question_type, options, correct_answer, test_id):
        self.id = id
        self.text = text
        self.question_type = question_type  # single_choice, multiple_choice, text_input
        self.options = options              # список или dict (из JSONB)
        self.correct_answer = correct_answer
        self.test_id = test_id

    @classmethod
    def from_dict(cls, data: dict):
        # psycopg2 автоматически преобразует JSONB в Python-объект (list/dict)
        return cls(
            id=data['id'],
            text=data['text'],
            question_type=data['question_type'],
            options=data['options'],
            correct_answer=data['correct_answer'],
            test_id=data['test_id']
        )