from fastapi import APIRouter, Request, Depends

from ..utils import SUPER_ADMIN, ADMIN
from ..controllers import AdvertisingController
from ..middlewares import Authentication
from ..schemas import AdvertisingCreateRequest, AdvertisingUpdateRequest

advertising_routes = APIRouter(
    prefix='/advertising', tags=['Advertising'], dependencies=[Depends(Authentication([SUPER_ADMIN, ADMIN]))]
)


@advertising_routes.get('/')
async def all_advertisements(request: Request):
    return await AdvertisingController().get_all(request=request)


@advertising_routes.get('/{pk}')
async def one_advertising(pk: int):
    return await AdvertisingController().get_one(query=dict(id=pk))


@advertising_routes.post('/')
async def create_advertising(advertisement_data: AdvertisingCreateRequest):
    return await AdvertisingController().create(data=advertisement_data.dict(exclude={'image'}), file=advertisement_data.image)


@advertising_routes.patch('/{pk}')
async def update_advertising(pk: int, advertisement_data: AdvertisingUpdateRequest):
    return await AdvertisingController().update(
        query=dict(id=pk), data=advertisement_data.dict(exclude={'image'}), file=advertisement_data.image
    )


@advertising_routes.delete('/{pk}')
async def delete_advertising(pk: int):
    return await AdvertisingController().delete(query=dict(id=pk))
