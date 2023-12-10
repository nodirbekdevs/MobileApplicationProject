from typing import Optional, List

from pydantic import BaseModel

from .core import CoreResponseSchema, CoreUserCreateRequest, CoreUserUpdateRequest


class AdminCreateRequest(CoreUserCreateRequest):
    type: str


class AdminUpdateRequest(CoreUserUpdateRequest):
    type: str | None


class AdminResponse(CoreResponseSchema, AdminCreateRequest):
    pass


class AdminResponseList(BaseModel):
    querysets: List[AdminResponse]


class AdminRepositorySchemas(object):
    list = AdminResponseList
    retrieve = AdminResponse
