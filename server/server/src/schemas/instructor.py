from pydantic import BaseModel
from typing import List

from ..models import Subject
from .core import CoreResponseSchema, CoreUserCreateRequest, CoreUserUpdateRequest


class InstructorCreateRequest(CoreUserCreateRequest):
    subject_id: int | None


class InstructorUpdateRequest(CoreUserUpdateRequest):
    subject_id: int | None


class InstructorResponse(CoreResponseSchema, InstructorCreateRequest):
    subject_id: Subject | dict


class InstructorResponseList(BaseModel):
    querysets: List[InstructorResponse]


class InstructorRepositorySchemas(object):
    list = InstructorResponseList
    retrieve = InstructorResponse
