from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..controllers import SectionController
from ..middlewares import Authentication
from ..schemas import SectionCreateRequest, SectionUpdateRequest

section_routes = APIRouter(prefix='/section', tags=['Section'])


@section_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_sections(request: Request):
    return await SectionController().get_all(request=request)


@section_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_section(pk: int):
    return await SectionController().get_one(query=dict(id=pk))


@section_routes.post('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def create_section(request: Request, section_data: SectionCreateRequest):
    return await SectionController().create(user=request.state.user, data=section_data.dict())


@section_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def update_section(request: Request, pk: int, section_data: SectionUpdateRequest):
    return await SectionController().update(user=request.state.user, query=dict(id=pk), data=section_data.dict())


@section_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def delete_section(pk: int):
    return await SectionController().delete(query=dict(id=pk))
