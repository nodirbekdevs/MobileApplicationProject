from fastapi import Request
from typing import List

from src.utils import ADMIN
from src.models import Feedback
from src.repositories import Storage, CoreRepository
from src.services import Pagination, SendResponse, Filter


class FeedbackController:
    def __init__(self):
        self.repo: CoreRepository = Storage.feedback
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        candidate_id, role = request.state.user['id'], request.state.user['role']

        feedback_query: dict = dict()

        if role != ADMIN:
            feedback_query.update(user_id=candidate_id, user_type=role)

        query = Filter(query=feedback_query).filtering_with_params(params=params)

        all_feedback: List[Feedback] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=all_feedback, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        feedback: Feedback = await self.repo.retrieve(query=query)

        if feedback is None:
            return self.response.failure(
                data=dict(message=f'Feedback with this {query} query does not exists'), status_code=404
            )

        feedback = self.repo.schemas.retrieve(feedback)

        return self.response.success(data=feedback, status_code=200)

    async def create(self, data: dict):
        feedback: Feedback = await self.repo.retrieve(query=data)

        if feedback:
            return self.response.failure(
                data=dict(message=f'Feedback with this {data} values already exists'), status_code=400
            )

        feedback: Feedback = await self.repo.create(data=data)

        return self.response.success(data=feedback, status_code=201)

    async def update(self, query: dict, data: dict):
        feedback: Feedback = await self.repo.retrieve(query=query)

        if feedback is None:
            return self.response.failure(
                data=dict(message=f'Feedback with this {query} query does not exists'), status_code=404
            )

        feedback: Feedback = await self.repo.update(query=query, data=data)

        return self.response.success(data=feedback, status_code=200)

    async def delete(self, query):
        feedback: Feedback = await self.repo.retrieve(query=query)

        if feedback is None:
            return self.response.failure(
                data=dict(message=f'Feedback with this {query} query does not exists'), status_code=404
            )

        await self.repo.destroy(queryset=feedback)

        return self.response.success(data=dict(message=f"Feedback with this {query} has deleted"), status_code=204)
