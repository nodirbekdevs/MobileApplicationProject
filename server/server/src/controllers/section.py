from fastapi import Request
from typing import List

from .user import UserController
from ..models import Section, Test
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Translator, Populate
from ..utils import INSTRUCTOR


class SectionController:
    def __init__(self):
        self.repo: CoreRepository = Storage.section
        self.response = SendResponse

    async def get_all(self, request: Request):
        params, user = request.query_params, request.state.user

        filter = dict()

        if user['role'] == INSTRUCTOR:
            filter.update(instructor_id=user['id'])

        query: dict = Filter(query=filter).filtering_with_params(params=params)

        sections: List[Section] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=sections, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        section: Section = await self.repo.retrieve(query=query, populate=Populate.section)

        if section is None:
            return self.response.failure(
                data=dict(message=f'Section with this {query} query does not exists'), status_code=404
            )

        section = self.repo.schemas.retrieve(section)

        return self.response.success(data=section, status_code=200)

    async def create(self, user, data: dict):
        instructor = await Storage.instructor.retrieve(query=dict(id=data['instructor_id']))

        if instructor is None:
            return self.response.failure(data=dict(message="Instructor does not exist"), status_code=404)

        subject = await Storage.subject.retrieve(query=dict(id=data['subject_id']))

        if subject is None:
            return self.response.failure(data=dict(message="Subject does not exist"), status_code=404)

        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        translated_title = await Translator(language=language).translate(data['title'])
        translated_description = await Translator(language=language).translate(data['description'])

        section_data = dict(instructor_id=data['instructor_id'], subject_id=data['subject_id'])

        section_query = dict(title_uz=data['title']) if language == 'ru' else dict(title_ru=translated_title)

        section_data.update(
            title_uz=translated_title, title_ru=data['title'],
            description_uz=translated_description, description_ru=data['description']
        ) if language == 'uz' else section_data.update(
            title_uz=data['title'], title_ru=translated_title,
            description_uz=data['description'], description_ru=translated_description
        )

        section: Section = await self.repo.retrieve(query=section_query)

        if section:
            return self.response.failure(
                data=dict(message=f'Section with this {section_query} values already exists'), status_code=400
            )

        section: Section = await self.repo.create(data=section_data, populate=Populate.section)

        return self.response.success(data=section, status_code=201)

    async def update(self, user, query: dict, data: dict):
        section: Section = await self.repo.retrieve(query=query)

        if section is None:
            return self.response.failure(
                data=dict(message=f'Section with this {query} query does not exists'), status_code=404
            )

        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        instructor = await Storage.instructor.retrieve(query=dict(id=section.instructor_id.id))

        section_query, section_data = dict(instructor_id=instructor.id), dict()

        if data.get('title') is not None:
            translated_title = await Translator(language=language).translate(data['title'])

            section_query = dict(title_uz=data['title']) if language == 'ru' else dict(title_ru=translated_title)

            section_data.update(
                title_uz=translated_title, title_ru=data['title']
            ) if language == 'uz' else section_data.update(
                title_uz=data['title'], title_ru=translated_title
            )

        if section_query:
            section: Section = await self.repo.retrieve(query=section_query)

            if section:
                return self.response.failure(
                    status_code=400, data=dict(message="Section with this title already exists!")
                )

        if data.get('description') is not None:
            translated_description = await Translator(language=language).translate(data['description'])

            section_data.update(
                description_uz=translated_description, description_ru=data['description']
            ) if language == 'uz' else section_data.update(
                description_uz=data['description'], description_ru=translated_description
            )

        section: Section = await self.repo.update(query=query, data=section_data)

        return self.response.success(data=section, status_code=200)

    async def delete(self, query):
        section: Section = await self.repo.retrieve(query=query)

        if section is None:
            return self.response.failure(
                data=dict(message=f'Section with this {query} query does not exists'), status_code=404
            )

        tests: List[Test] = await Storage.test.list(query=dict(section_id=section.id, is_testing=True))

        if tests is not []:
            return self.response.failure(data=dict(message="This sections test is solving"), status_code=400)

        tests: List[Test] = await Storage.test.list(query=dict(section_id=section.id))

        if tests:
            for test in tests:
                await test.delete()

        await self.repo.destroy(queryset=section)

        return self.response.success(data=dict(message=f"Section with this {query} has deleted"), status_code=204)
