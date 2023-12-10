from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..repositories import Storage
from ..services import SendResponse
from ..schemas import SchemaStorage


class UserController:
    def __init__(self, user_id, user_type):
        self.user_id = user_id
        self.user_type = user_type

    async def get_one(self):
        candidate, candidate_query = dict(), dict(id=self.user_id)

        if self.user_type in [SUPER_ADMIN, ADMIN]:
            candidate = await Storage.admin.retrieve(query=candidate_query)
        elif self.user_type == INSTRUCTOR:
            candidate = await Storage.instructor.retrieve(query=candidate_query)
        elif self.user_type == STUDENT:
            candidate = await Storage.student.retrieve(query=candidate_query)

        return candidate

    @staticmethod
    async def get_one_by_telegram_id(telegram_id):
        candidate, type = dict(), ''

        student = await Storage.student.retrieve(query=dict(telegram_id=telegram_id))
        admin = await Storage.admin.retrieve(query=dict(telegram_id=telegram_id))
        instructor = await Storage.instructor.retrieve(query=dict(telegram_id=telegram_id))

        if student:
            candidate = SchemaStorage.student.retrieve(student)
            type = STUDENT
        elif admin:
            candidate = SchemaStorage.admin.retrieve(admin)
            type = ADMIN
        elif instructor:
            candidate = SchemaStorage.instructor.retrieve(instructor)
            type = INSTRUCTOR

        return SendResponse.success(data=dict(candidate=candidate, type=type), status_code=200)

    @staticmethod
    async def check_exist(query):
        admin = await Storage.admin.retrieve(query=query)
        instructor = await Storage.instructor.retrieve(query=query)
        student = await Storage.student.retrieve(query=query)

        if admin or instructor or student:
            return True

        return False

    @staticmethod
    async def check_type(query):
        admin = await Storage.admin.retrieve(query=query)
        instructor = await Storage.instructor.retrieve(query=query)
        student = await Storage.student.retrieve(query=query)

        if admin:
            return SendResponse.success(data=dict(type=admin.type), status_code=200)
        elif instructor:
            return SendResponse.success(data=dict(type=INSTRUCTOR), status_code=200)

        return SendResponse.success(data=dict(type=STUDENT), status_code=200)

    @staticmethod
    async def get_by_role(query: dict):
        role = query['role']

        candidate, query = dict(), dict(id=query['id'])

        if role == ADMIN:
            candidate = await Storage.admin.retrieve(query=query)
        elif role == INSTRUCTOR:
            candidate = await Storage.instructor.retrieve(query=query)
        elif role == STUDENT:
            candidate = await Storage.student.retrieve(query=query)

        if not candidate:
            return

        return SendResponse.success(data=dict(data=candidate), status_code=200)