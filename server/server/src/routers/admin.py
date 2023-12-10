from fastapi import APIRouter, Request, Depends

from ..utils import ADMIN, SUPER_ADMIN
from ..controllers import AdminController
from ..middlewares import Authentication
from ..schemas import AdminCreateRequest, AdminUpdateRequest

admin_routes = APIRouter(prefix='/admin', tags=['Admin'])


@admin_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def all_admins(request: Request):
    return await AdminController().get_all(request=request)


@admin_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def one_admin(pk: int):
    return await AdminController().get_one(query=dict(id=pk))


@admin_routes.get('/telegram/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def one_admin_by_telegram_id(pk: int):
    print("Keldi")
    return await AdminController().get_one(query=dict(telegram_id=pk))


@admin_routes.get('/profile', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def admin_profile(request: Request):
    return await AdminController().get_one(query=dict(id=request.state.user['id']))


@admin_routes.post('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def create_admin(admin_data: AdminCreateRequest):
    return await AdminController().create(data=admin_data.dict())


@admin_routes.patch('/profile', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def update_admin_profile(request: Request, admin_data: AdminUpdateRequest):
    return await AdminController().update(query=dict(id=request.state.user['id']), data=admin_data.dict())


@admin_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def update_admin(pk: int, admin_data: AdminUpdateRequest):
    return await AdminController().update(query=dict(id=pk), data=admin_data.dict())


@admin_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def delete_admin(pk: int):
    return await AdminController().delete(query=dict(id=pk))
