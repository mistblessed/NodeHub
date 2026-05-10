from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, role, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data['role'],
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }