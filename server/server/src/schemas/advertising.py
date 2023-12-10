from fastapi import UploadFile, File, Form, Body
from io import BytesIO
from pydantic import BaseModel
from typing import List, Union

from .core import CoreResponseSchema


class AdvertisingCreateRequest(BaseModel):
    title: str
    description: str | None
    image: bytes | None


class AdvertisingUpdateRequest(BaseModel):
    title: str | None
    description: str | None
    image: bytes | None


class AdvertisingResponse(CoreResponseSchema, AdvertisingCreateRequest):
    image: str | None


class AdvertisingResponseList(BaseModel):
    querysets: List[AdvertisingResponse]


class AdvertisingRepositorySchemas(object):
    list = AdvertisingResponseList
    retrieve = AdvertisingResponse
