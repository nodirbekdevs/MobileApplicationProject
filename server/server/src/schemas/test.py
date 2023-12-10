from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List, Union

from .core import CoreResponseSchema
from ..models import Instructor, Section, Subject


class TestCreateRequest(BaseModel):
    instructor: int
    subject: int
    section: int
    question: str
    variants: list
    correct_answer: str
    image: bytes | None


class TestUpdateRequest(BaseModel):
    question: str | None
    variants: Union[list | dict] | None
    correct_answer: str | None
    is_testing: bool | None
    image: bytes | None


class TestUploadPhotoRequest(BaseModel):
    image: UploadFile = File(...)


class TestResponse(CoreResponseSchema):
    instructor_id: Instructor | dict
    section_id: Section | dict
    subject_id: Subject | dict
    image: str | None
    question_uz: str
    question_ru: str
    variants_uz: list
    variants_ru: list
    correct_answer_uz: str
    correct_answer_ru: str
    is_testing: bool


class TestCheckRequest(BaseModel):
    tests: list
    time: str


class SolvingTestRequest(BaseModel):
    section_id: int


class TestResponseList(BaseModel):
    querysets: List[TestResponse]


class TestRepositorySchemas(object):
    list = TestResponseList
    retrieve = TestResponse
