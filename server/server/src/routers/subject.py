from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..controllers import SubjectController
from ..middlewares import Authentication
from ..schemas import SubjectCreateRequest, SubjectUpdateRequest

subject_routes = APIRouter(prefix='/subject', tags=['Subject'])


@subject_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_subjects(request: Request):
    return await SubjectController().get_all(request=request)


@subject_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_subject(pk: int):
    return await SubjectController().get_one(query=dict(id=pk))


@subject_routes.post('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def create_subject(request: Request, subject_data: SubjectCreateRequest):
    return await SubjectController().create(user=request.state.user, data=subject_data.dict())


@subject_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def update_subject(request: Request, pk: int, subject_data: SubjectUpdateRequest):
    return await SubjectController().update(user=request.state.user, query=dict(id=pk), data=subject_data.dict())


@subject_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def delete_subject(pk: int):
    return await SubjectController().delete(query=dict(id=pk))
