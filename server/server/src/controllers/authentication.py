from ..utils import ADMIN, INSTRUCTOR, STUDENT
from ..models import Admin, Instructor, Student
from ..repositories import Storage
from ..services import SendResponse, Bcrypt, Token


class AuthenticationController:
    def __init__(self):
        self.response = SendResponse

    async def login(self, data: dict):
        query = dict(phone_number=data['phone_number'])

        admin: Admin = await Storage.admin.retrieve(query=query)
        instructor: Instructor = await Storage.instructor.retrieve(query=query)
        student: Student = await Storage.student.retrieve(query=query)

        if admin:
            candidate = admin
            role = ADMIN
        elif instructor:
            candidate = instructor
            role = INSTRUCTOR
        elif student:
            candidate = student
            role = STUDENT
        else:
            return self.response.failure(status_code=404, data=dict(message="You have not registered yet"))

        checking = await Bcrypt.check(hashed_password=candidate.password, password=data['password'])

        if not checking:
            return self.response.failure(status_code=400, data=dict(message="Password have not matched"))

        token_data = dict(id=candidate.id, role=role)

        token = await Token.encode_jwt(data=token_data)

        return self.response.success(data=dict(candidate=candidate, role=role, **token), status_code=200)

    async def refresh_token(self, token: str):
        token = token.split(' ')

        decoded_token = await Token.decode(token=token[1])

        candidate_query, role = dict(id=decoded_token['id']), decoded_token['role']

        candidate = dict()

        if role == ADMIN:
            candidate = await Storage.admin.retrieve(query=candidate_query)
        elif role == INSTRUCTOR:
            candidate = await Storage.instructor.retrieve(query=candidate_query)
        elif role == STUDENT:
            candidate = await Storage.student.retrieve(query=candidate_query)

        if candidate is None:
            return self.response.failure(status_code=403, data=dict(message='You have not exists in database'))

        token = await Token.encode_jwt(data=decoded_token)

        return self.response.success(data=token, status_code=200)
