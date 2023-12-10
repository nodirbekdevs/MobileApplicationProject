from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT
from ..controllers import FeedbackController
from ..middlewares import Authentication
from ..schemas import FeedbackCreateRequest, FeedbackUpdateRequest

feedback_routes = APIRouter(prefix='/feedback', tags=['Feedback'])


@feedback_routes.get('/', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def all_feedback(request: Request):
    return await FeedbackController().get_all(request=request)


@feedback_routes.get('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def one_feedback(pk: int):
    return await FeedbackController().get_one(query=dict(id=pk))


@feedback_routes.post('/', dependencies=[Depends(Authentication([INSTRUCTOR, STUDENT]))])
async def create_feedback(feedback_data: FeedbackCreateRequest):
    return await FeedbackController().create(data=feedback_data.dict())


@feedback_routes.patch('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))])
async def update_feedback(pk: int, feedback_data: FeedbackUpdateRequest):
    return await FeedbackController().update(query=dict(id=pk), data=feedback_data.dict())


@feedback_routes.delete('/{pk}', dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN, INSTRUCTOR, STUDENT]))])
async def delete_feedback(pk: int):
    return await FeedbackController().delete(query=dict(id=pk))
