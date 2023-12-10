from fastapi import APIRouter, Request

from ..controllers import AuthenticationController
from ..schemas import AuthenticationSchema

authentication_routes = APIRouter(prefix='/authentication', tags=['Authentication'])


@authentication_routes.post('/login')
async def login(authentication_data: AuthenticationSchema):
    return await AuthenticationController().login(data=authentication_data.dict())


@authentication_routes.post('/refresh')
async def refresh_token(request: Request):
    return await AuthenticationController().refresh_token(token=request.headers.get('Authorization'))
