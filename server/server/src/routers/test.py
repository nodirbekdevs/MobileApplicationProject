from fastapi import APIRouter, Request, Depends, UploadFile, File

from ..utils import ADMIN, SUPER_ADMIN, INSTRUCTOR, STUDENT
from ..controllers import TestController
from ..middlewares import Authentication
from ..schemas import TestCreateRequest, TestUpdateRequest, SolvingTestRequest, TestCheckRequest

test_routes = APIRouter(prefix='/test', tags=['Test'])


@test_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_tests(request: Request):
    return await TestController().get_all(request=request, user=request.state.user)


@test_routes.get('/solving', dependencies=[Depends(Authentication([STUDENT]))])
async def get_for_solving_tests(request: Request):
    return await TestController().get_for_solving(query=request.query_params)


@test_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_test(pk: int):
    return await TestController().get_one(query=dict(id=pk))


@test_routes.post('/check', dependencies=[Depends(Authentication([STUDENT]))])
async def check(request: Request, test_data: TestCheckRequest):
    return await TestController().check(user=request.state.user, data=test_data.dict())


@test_routes.post('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def create_test(request: Request, test_data: TestCreateRequest):
    return await TestController().create(user=request.state.user, data=test_data.dict(exclude={'image'}), file=test_data.image)


@test_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def update_test(request: Request, pk: int, test_data: TestUpdateRequest):
    return await TestController().update(
        user=request.state.user, query=dict(id=pk), data=test_data.dict(exclude={'image'}), file=test_data.image
    )


@test_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def delete_test(pk: int):
    return await TestController().delete(query=dict(id=pk))
