class Lesson:
    def __init__(self, id, title, theoretical_content, order, module_id):
        self.id = id
        self.title = title
        self.theoretical_content = theoretical_content
        self.order = order
        self.module_id = module_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            title=data['title'],
            theoretical_content=data['theoretical_content'],
            order=data['order'],
            module_id=data['module_id']
        )