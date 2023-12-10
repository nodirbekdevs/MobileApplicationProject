from fastapi import Request
from typing import List

from ..controllers.user import UserController
from ..models import Student
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Bcrypt


class StudentController:
    def __init__(self):
        self.repo: CoreRepository = Storage.student
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        query: dict = Filter().filtering_with_params(params=params)

        students: List[Student] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=students, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        student: Student = await self.repo.retrieve(query=query)

        if student is None:
            return self.response.failure(
                data=dict(message=f'Student with this {query} query does not exists'), status_code=404
            )

        student = self.repo.schemas.retrieve(student)

        return self.response.success(data=student, status_code=200)

    async def create(self, data: dict):
        exist_student_query = dict(phone_number=data['phone_number'])

        student = await UserController.check_exist(query=exist_student_query)

        if student:
            return self.response.failure(
                data=dict(message=f'Student with this {exist_student_query} values already exists'), status_code=400
            )

        if data.get('password') is None:
            password = await Bcrypt.hash(data['phone_number'])
            data.update(password=password)

        student: Student = await self.repo.create(data=data)

        return self.response.success(data=student, status_code=201)

    async def update(self, query: dict, data: dict):
        student: Student = await self.repo.retrieve(query=query)

        if student is None:
            return self.response.failure(
                data=dict(message=f'Student with this {query} query does not exists'), status_code=404
            )

        if data.get('phone_number'):
            exist_student = await UserController.check_exist(query=dict(phone_number=data.get('phone_number')))

            if exist_student:
                return self.response.failure(
                    data=dict(message=f"Student with this {data['phone_number']} phone number already exists"),
                    status_code=400
                )

        student: Student = await self.repo.update(query=query, data=data)

        return self.response.success(data=student, status_code=200)

    async def delete(self, query):
        student: Student = await self.repo.retrieve(query=query)

        if student is None:
            return self.response.failure(
                data=dict(message=f'Student with this {query} query does not exists'), status_code=404
            )

        await self.repo.destroy(queryset=student)

        return self.response.success(data=dict(message=f"Student with this {query} has deleted"), status_code=204)
