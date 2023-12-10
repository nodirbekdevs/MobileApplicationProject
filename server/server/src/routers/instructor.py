from fastapi import APIRouter, Request, Depends

from ..utils import ADMIN, SUPER_ADMIN, INSTRUCTOR, STUDENT
from ..controllers import InstructorController
from ..middlewares import Authentication
from ..schemas import InstructorCreateRequest, InstructorUpdateRequest

instructor_routes = APIRouter(prefix='/instructor', tags=['Instructor'])


@instructor_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_instructors(request: Request):
    return await InstructorController().get_all(request=request)


@instructor_routes.get('/profile', dependencies=[Depends(Authentication([INSTRUCTOR]))])
async def instructor_profile(request: Request):
    return await InstructorController().get_one(query=dict(id=request.state.user['id']))


@instructor_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_instructor(pk: int):
    return await InstructorController().get_one(query=dict(id=pk))


@instructor_routes.get('/telegram/{pk}', dependencies=[Depends(Authentication([INSTRUCTOR]))])
async def one_instructor_by_telegram_id(pk: int):
    return await InstructorController().get_one(query=dict(telegram_id=pk))


@instructor_routes.post('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def create_instructor(instructor_data: InstructorCreateRequest):
    return await InstructorController().create(data=instructor_data.dict())


@instructor_routes.patch('/profile', dependencies=[Depends(Authentication([INSTRUCTOR]))])
async def update_instructor_profile(request: Request, instructor_data: InstructorUpdateRequest):
    return await InstructorController().update(query=dict(id=request.state.user['id']), data=instructor_data.dict())


@instructor_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def update_instructor(pk: int, instructor_data: InstructorUpdateRequest):
    return await InstructorController().update(query=dict(id=pk), data=instructor_data.dict())


@instructor_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def delete_instructor(pk: int):
    return await InstructorController().delete(query=dict(id=pk))
