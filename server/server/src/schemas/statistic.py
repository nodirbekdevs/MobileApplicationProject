from pydantic import BaseModel
from typing import List
from datetime import datetime

from .core import CoreResponseSchema
from ..models import Instructor, Student, Subject, Section


class StatisticCreateRequest(BaseModel):
    instructor: int
    subject: int
    student: int
    section: int
    checked_tests: str | dict
    total_tests: int
    right_count: int
    wrong_count: int
    percentage: float
    solved_time: datetime


class StatisticResponse(CoreResponseSchema, StatisticCreateRequest):
    instructor_id: Instructor | dict
    student_id: Student | dict
    subject_id: Subject | dict
    section_id: Section | dict
    checked_tests: str | dict
    solved_time: datetime | str


class StatisticResponseList(BaseModel):
    querysets: List[StatisticResponse]


class StatisticRepositorySchemas(object):
    list = StatisticResponseList
    retrieve = StatisticResponse
