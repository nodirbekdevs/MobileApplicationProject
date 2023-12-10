from pydantic import BaseModel
from typing import List

from .core import CoreResponseSchema
from ..models import Instructor, Subject


class SectionCreateRequest(BaseModel):
    instructor_id: int
    subject_id: int
    title: str
    description: str


class SectionUpdateRequest(BaseModel):
    title: str | None
    description: str | None


class SectionResponse(CoreResponseSchema):
    instructor_id: Instructor | dict
    subject_id: Subject | dict
    total_tests: int
    title_uz: str
    title_ru: str
    description_uz: str
    description_ru: str


class SectionResponseList(BaseModel):
    querysets: List[SectionResponse]


class SectionRepositorySchemas(object):
    list = SectionResponseList
    retrieve = SectionResponse
