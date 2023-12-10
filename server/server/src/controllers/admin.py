from fastapi import Request
from typing import List

from ..controllers.user import UserController
from ..models import Admin
from ..repositories import Storage, CoreRepository
from ..services import Pagination, SendResponse, Filter, Bcrypt


class AdminController:
    def __init__(self):
        self.repo: CoreRepository = Storage.admin
        self.response = SendResponse

    async def get_all(self, request: Request):
        params = request.query_params

        query: dict = Filter().filtering_with_params(params=params)

        admins: List[Admin] = await self.repo.list(query=query)

        data = Pagination(params=params, datas=admins, schemas=self.repo.schemas).paginate()

        return self.response.success(data=data, status_code=200)

    async def get_one(self, query: dict):
        admin: Admin = await self.repo.retrieve(query=query)

        if admin is None:
            return self.response.failure(
                data=dict(message=f'Admin with this {query} query does not exists'), status_code=404
            )

        admin = self.repo.schemas.retrieve(admin)

        return self.response.success(data=admin, status_code=200)

    async def create(self, data: dict):
        exist_admin_query = dict(phone_number=data['phone_number'])

        checking_user = await UserController.check_exist(query=exist_admin_query)

        if checking_user:
            return self.response.failure(
                data=dict(message=f'Admin with this {data} values already exists'), status_code=400
            )

        if data.get('password') is None:
            password = await Bcrypt.hash(data['phone_number'])
            data.update(password=password)

        admin: Admin = await self.repo.create(data=data)

        return self.response.success(data=admin, status_code=201)

    async def update(self, query: dict, data: dict):
        admin: Admin = await self.repo.retrieve(query=query)

        if admin is None:
            return self.response.failure(
                data=dict(message=f'Admin with this {query} query does not exists'), status_code=404
            )

        if data.get('phone_number'):
            checking_user = await UserController.check_exist(query=dict(phone_number=data.get('phone_number')))

            if checking_user:
                return self.response.failure(
                    data=dict(message=f"Admin with this {data['phone_number']} phone number already exists"),
                    status_code=400
                )

        if data.get('old_password') and data.get('new_password') is None:
            return self.response.failure(data=dict(message="New password is required"), status_code=403)
        elif data.get('old_password') is None and data.get('new_password'):
            return self.response.failure(data=dict(message="Old password is required"), status_code=403)
        elif data.get('old_password') and data.get('new_password'):
            check = await Bcrypt.check(admin.password, data['old_password'])

            if not check:
                return self.response.failure(data=dict(message="Password does not matched"), status_code=403)

            password = await Bcrypt.hash(data['new_password'])

            del data['old_password']
            del data['new_password']
            data.update(password=password)

        admin: Admin = await self.repo.update(query=query, data=data)

        return self.response.success(data=admin, status_code=200)

    async def delete(self, query):
        admin: Admin = await self.repo.retrieve(query=query)

        if admin is None:
            return self.response.failure(
                data=dict(message=f'Admin with this {query} query does not exists'), status_code=404
            )

        await self.repo.destroy(queryset=admin)

        return self.response.success(data=dict(message=f"Admin with this {query} has deleted"), status_code=204)
