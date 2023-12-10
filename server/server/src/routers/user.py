from fastapi import APIRouter, Depends, Request

from ..utils import ADMIN, SUPER_ADMIN, INSTRUCTOR, STUDENT
from ..controllers import UserController
from ..middlewares import Authentication

user_routes = APIRouter(prefix='/user', tags=['User'])


@user_routes.get('/check/{telegram_id}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def check_type(telegram_id: int):
    return await UserController.check_type(query=dict(telegram_id=telegram_id))


@user_routes.get('/role/{user_id}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def get_by_role(request: Request, user_id: int):
    return await UserController.get_by_role(query=dict(id=user_id, role=request.query_params['role']))


@user_routes.get('/telegram_id/{telegram_id}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def get_one_by_telegram_id(telegram_id: int):
    return await UserController.get_one_by_telegram_id(telegram_id=telegram_id)
