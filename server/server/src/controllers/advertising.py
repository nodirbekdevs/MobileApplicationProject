from io import BytesIO

from fastapi import Request, File, UploadFile
from typing import List
from asyncio import to_thread
from base64 import b64decode

from ..utils import ADVERTISING, uploads_file_path
from ..models import Advertising
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, File, Filter


class AdvertisingController:
    def __init__(self):
        self.repo: CoreRepository = Storage.advertising
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        query: dict = Filter().filtering_with_params(params=params)

        advertisements: List[Advertising] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=advertisements, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        advertising: Advertising = await self.repo.retrieve(query=query)

        if advertising is None:
            return self.response.failure(
                data=dict(message=f'Advertising with this {query} query does not exists'), status_code=404
            )

        advertising = self.repo.schemas.retrieve(advertising)

        return self.response.success(data=advertising, status_code=200)

    async def create(self, data: dict, file):
        advertising: Advertising = await self.repo.retrieve(query=data)

        if advertising:
            return self.response.failure(
                data=dict(message=f'Advertising with this {data} values already exists'), status_code=400
            )

        if file:
            decoded_bytes = await to_thread(b64decode, file)

            image = UploadFile(BytesIO(decoded_bytes))

            file_path: str = await File(file=image).save(
                file_model_type=ADVERTISING, path=uploads_file_path, title=data['title']
            )

            data.update(image=file_path)

        advertising: Advertising = await self.repo.create(data=data)

        return self.response.success(data=advertising, status_code=201)

    async def update(self, query: dict, data: dict, file):
        advertising: Advertising = await self.repo.retrieve(query=query)

        if advertising is None:
            return self.response.failure(
                data=dict(message=f'Advertising with this {query} query does not exists'), status_code=404
            )

        if file:
            if advertising.image:
                await File.remove(file_path=advertising.image)

            decoded_bytes = await to_thread(b64decode, file)

            image = UploadFile(BytesIO(decoded_bytes))

            file_path: str = await File(file=image).save(
                file_model_type=ADVERTISING, path=uploads_file_path, title=data['title'] if data.get('title') else advertising.title
            )

            data.update(image=file_path)

        advertising: Advertising = await self.repo.update(query=query, data=data)

        return self.response.success(data=advertising, status_code=200)

    async def delete(self, query):
        advertising: Advertising = await self.repo.retrieve(query=query)

        if advertising is None:
            return self.response.failure(
                data=dict(message=f'Advertising with this {query} query does not exists'), status_code=404
            )

        if advertising.image:
            await File.remove(file_path=advertising.image)

        await self.repo.destroy(queryset=advertising)

        return self.response.success(data=dict(message=f"Advertising with this {query} has deleted"), status_code=204)
