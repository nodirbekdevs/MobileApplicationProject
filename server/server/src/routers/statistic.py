from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..controllers import StatisticController
from ..middlewares import Authentication
from ..schemas import StatisticCreateRequest

statistic_routes = APIRouter(prefix='/statistic', tags=['Statistic'])


@statistic_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR]))])
async def all_statistics(request: Request):
    return await StatisticController().get_all(request=request)


@statistic_routes.get('/report', dependencies=[Depends(Authentication(INSTRUCTOR))])
async def get_report_of_statistics(request: Request):
    return await StatisticController().get_report(user=request.state.user)


@statistic_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, STUDENT]))])
async def one_statistic(pk: int):
    return await StatisticController().get_one(query=dict(id=pk))


@statistic_routes.post('/', dependencies=[Depends(Authentication([STUDENT]))])
async def create_statistic(request: Request, statistic_data: StatisticCreateRequest):
    return await StatisticController().create(user=request.state.user, data=statistic_data.dict())
