from fastapi import Request
from typing import List

from .user import UserController
from ..models import Subject
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Translator


class SubjectController:
    def __init__(self):
        self.repo: CoreRepository = Storage.subject
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        query: dict = Filter().filtering_with_params(params=params)

        subjects: List[Subject] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=subjects, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        subject: Subject = await self.repo.retrieve(query=query)

        if subject is None:
            return self.response.failure(
                data=dict(message=f'Subject with this {query} query does not exists'), status_code=404
            )

        subject = self.repo.schemas.retrieve(subject)

        return self.response.success(data=subject, status_code=200)

    async def create(self, user, data: dict):
        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        translated_title = await Translator(language=language).translate(data['title'])
        translated_description = await Translator(language=language).translate(data['description'])

        subject_data = dict()

        subject_query = dict(title_uz=data['title']) if language == 'ru' else dict(title_ru=translated_title)

        subject_data.update(
            title_uz=translated_title, title_ru=data['title'],
            description_uz=translated_description, description_ru=data['description']
        ) if language == 'uz' else subject_data.update(
            title_uz=data['title'], title_ru=translated_title,
            description_uz=data['description'], description_ru=translated_description
        )

        subject: Subject = await self.repo.retrieve(query=subject_query)

        if subject:
            return self.response.failure(
                data=dict(message=f'Subject with this {data} values already exists'), status_code=400
            )

        subject: Subject = await self.repo.create(data=subject_data)

        return self.response.success(data=subject, status_code=201)

    async def update(self, user, query: dict, data: dict):
        subject: Subject = await Storage.subject.retrieve(query=query)

        if subject is None:
            return self.response.failure(
                data=dict(message=f'Subject with this {query} query does not exists'), status_code=404
            )

        user = await UserController(user_id=user['id'], user_type=user['role']).get_one()

        language = 'ru' if user.lang == 'uz' else 'uz'

        subject_query, subject_data = dict(), dict()

        if data.get('title'):
            translated_title = await Translator(language=language).translate(data['title'])

            subject_query = dict(title_uz=data['title']) if language == 'ru' else dict(title_ru=translated_title)

            subject_data.update(
                title_uz=translated_title, title_ru=data['title']
            ) if language == 'uz' else subject_data.update(
                title_uz=data['title'], title_ru=translated_title
            )

        if data.get('description'):
            translated_description = await Translator(language=language).translate(data['description'])

            subject_data.update(
                description_uz=translated_description, description_ru=data['description']
            ) if language == 'uz' else subject_data.update(
                description_uz=data['description'], description_ru=translated_description
            )

        if subject_query:
            subject: Subject = await self.repo.retrieve(query=subject_query)

            if subject:
                return self.response.failure(
                    status_code=400, data=dict(message="Subject with this title already exists!")
                )

        subject: Subject = await self.repo.update(query=query, data=subject_data)

        return self.response.success(data=subject, status_code=200)

    async def delete(self, query):
        subject: Subject = await self.repo.retrieve(query=query)

        if subject is None:
            return self.response.failure(
                data=dict(message=f'Subject with this {query} query does not exists'), status_code=404
            )

        query = dict(subject_id=subject.id)

        instructors = await Storage.instructor.list(query=query)
        sections = await Storage.section.list(query=query)

        if instructors or sections:
            return self.response.failure(
                data=dict(message="Instrucor has taken this subject"), status_code=403
            )

        await self.repo.destroy(queryset=subject)

        return self.response.success(data=dict(message=f"Subject with this {query} has deleted"), status_code=204)
