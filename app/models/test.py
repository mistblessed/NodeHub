class Test:
    def __init__(self, id, title, module_id):
        self.id = id
        self.title = title
        self.module_id = module_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            title=data['title'],
            module_id=data['module_id']
        )