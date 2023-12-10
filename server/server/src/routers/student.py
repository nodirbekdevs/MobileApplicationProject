from fastapi import APIRouter, Request, Depends

from ..utils import ADMIN, SUPER_ADMIN, INSTRUCTOR, STUDENT
from ..controllers import StudentController
from ..middlewares import Authentication
from ..schemas import StudentCreateRequest, StudentUpdateRequest

student_routes = APIRouter(prefix='/student', tags=['Student'])


@student_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_students(request: Request):
    return await StudentController().get_all(request=request)


@student_routes.get('/profile', dependencies=[Depends(Authentication([STUDENT]))])
async def student_profile(request: Request):
    return await StudentController().get_one(query=dict(id=request.state.user['id']))


@student_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_student(pk: int):
    return await StudentController().get_one(query=dict(id=pk))


@student_routes.get('/telegram/{pk}', dependencies=[Depends(Authentication([STUDENT]))])
async def one_student_by_telegram_id(pk: int):
    return await StudentController().get_one(query=dict(telegram_id=pk))


@student_routes.post('/')
async def create_student(student_data: StudentCreateRequest):
    return await StudentController().create(data=student_data.dict())


@student_routes.patch('/profile', dependencies=[Depends(Authentication([STUDENT]))])
async def update_student_profile(request: Request, student_data: StudentUpdateRequest):
    return await StudentController().update(query=dict(id=request.state.user['id']), data=student_data.dict())


@student_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, STUDENT]))])
async def update_student(pk: int, student_data: StudentUpdateRequest):
    return await StudentController().update(query=dict(id=pk), data=student_data.dict())


@student_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def delete_student(pk: int):
    return await StudentController().delete(query=dict(id=pk))
