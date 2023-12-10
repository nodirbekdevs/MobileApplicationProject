from pydantic import BaseModel
from typing import List

from .core import CoreResponseSchema


class SubjectCreateRequest(BaseModel):
    title: str
    description: str


class SubjectUpdateRequest(BaseModel):
    title: str | None
    description: str | None


class SubjectResponse(CoreResponseSchema):
    title_uz: str
    title_ru: str
    description_uz: str
    description_ru: str


class SubjectResponseList(BaseModel):
    querysets: List[SubjectResponse]


class SubjectRepositorySchemas(object):
    list = SubjectResponseList
    retrieve = SubjectResponse
