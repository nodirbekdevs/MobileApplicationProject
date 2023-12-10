from fastapi import Request
from typing import List

from ..controllers.user import UserController
from ..models import Instructor
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Populate, Bcrypt


class InstructorController:
    def __init__(self):
        self.repo: CoreRepository = Storage.instructor
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        query = Filter(query=dict()).filtering_with_params(params=params)

        instructors: List[Instructor] = await self.repo.list(query=query, populate=Populate.instructor)

        data = Pagination(params=params, datas=instructors, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        instructor: Instructor = await self.repo.retrieve(query=query, populate=Populate.instructor)

        if instructor is None:
            return self.response.failure(
                data=dict(message=f'Instructor with this {query} query does not exists'), status_code=404
            )

        instructor = self.repo.schemas.retrieve(instructor)

        return self.response.success(data=instructor, status_code=200)

    async def create(self, data: dict):
        exist_instructor_query = dict(phone_number=data['phone_number'])

        instructor = await UserController.check_exist(query=exist_instructor_query)

        if instructor:
            return self.response.failure(
                data=dict(message=f'Instructor with this {data} values already exists'), status_code=400
            )

        if data.get('subject'):
            subject = await Storage.subject.retrieve(query=dict(id=data['subject']))

            data.update(subject_id=subject)

        if data.get('password') is None:
            password = await Bcrypt.hash(data['phone_number'])
            data.update(password=password)

        instructor: Instructor = await self.repo.create(data=data, populate=Populate.instructor)

        return self.response.success(data=instructor, status_code=201)

    async def update(self, query: dict, data: dict):
        instructor: Instructor = await self.repo.retrieve(query=query)

        if instructor is None:
            return self.response.failure(
                data=dict(message=f'Instructor with this {query} query does not exists'), status_code=404
            )

        if data.get('phone_number'):
            instructor = await UserController.check_exist(query=dict(phone_number=data.get('phone_number')))

            if instructor:
                return self.response.failure(
                    data=dict(message=f"Instructor with this {data['phone_number']} phone number already exists"),
                    status_code=400
                )

        if data.get('subject'):
            subject = await Storage.subject.retrieve(query=dict(id=data['subject']))

            if subject is None:
                return self.response.failure(
                    data=dict(message=f"Subject with this does not exist"),
                    status_code=400
                )

            data.update(subject_id=subject.id)

        instructor: Instructor = await self.repo.update(query=query, data=data)

        return self.response.success(data=instructor, status_code=200)

    async def delete(self, query):
        instructor: Instructor = await self.repo.retrieve(query=query)

        if instructor is None:
            return self.response.failure(
                data=dict(message=f'Instructor with this {query} query does not exists'), status_code=404
            )

        query = dict(is_active=True, instructor_id=instructor.id)

        sections = await Storage.section.list(query=query)
        tests = await Storage.test.list(query=query)

        if sections or tests:
            return self.response.failure(
                status_code=400,
                data=dict(message="You can not delete this instructor. The reason is that instructor has active tests and sections")
            )

        await self.repo.destroy(queryset=instructor)

        return self.response.success(data=dict(message=f"Employee with this {query} has deleted"), status_code=204)
