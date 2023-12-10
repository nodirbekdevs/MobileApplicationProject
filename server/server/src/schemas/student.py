from pydantic import BaseModel
from typing import List

from .core import CoreResponseSchema, CoreUserCreateRequest, CoreUserUpdateRequest


class StudentCreateRequest(CoreUserCreateRequest):
    pass


class StudentUpdateRequest(CoreUserUpdateRequest):
    pass


class StudentResponse(CoreResponseSchema, StudentCreateRequest):
    pass


class StudentResponseList(BaseModel):
    querysets: List[StudentResponse]


class StudentRepositorySchemas(object):
    list = StudentResponseList
    retrieve = StudentResponse
