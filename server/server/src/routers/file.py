from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..controllers import FileController
from ..middlewares import Authentication

file_routes = APIRouter(prefix='/file', tags=['File'], dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])


@file_routes.get('/')
async def one_file(request: Request):
    return await FileController().get_one(request=request)
