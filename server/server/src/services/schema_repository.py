class SchemaRepository(object):
    def __init__(self, schemas):
        self.schemas = schemas

    def list(self, data):
        return self.schemas.list(querysets=[self.schemas.retrieve(**item.dict()).dict() for item in data]).dict()

    def retrieve(self, data):
        return self.schemas.retrieve(**data.dict()).dict()
