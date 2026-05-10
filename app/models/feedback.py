class Feedback:
    def __init__(self, id, user_id, name, email, subject, message, status, created_at):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.status = status
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            user_id=data.get('user_id'),
            name=data.get('name'),
            email=data.get('email'),
            subject=data['subject'],
            message=data['message'],
            status=data['status'],
            created_at=data.get('created_at')
        )