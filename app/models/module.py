class Module:
    def __init__(self, id, title, description, order):
        self.id = id
        self.title = title
        self.description = description
        self.order = order

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            order=data['order']
        )