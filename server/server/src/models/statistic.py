from ormar import ForeignKey, Integer, Float, Text, Date, String
from datetime import datetime

from ..utils import BaseMeta
from .core import IsActiveCreatedUpdatedAtAbstract
from .instructor import Instructor
from .section import Section
from .student import Student
from .subject import Subject


class Statistic(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = "testing_statistics"

    instructor_id = ForeignKey(to=Instructor, ondelete="NO ACTION", nullable=False)
    student_id = ForeignKey(to=Student, ondelete="NO ACTION", nullable=False)
    subject_id = ForeignKey(to=Subject, ondelete="NO ACTION", nullable=False)
    section_id = ForeignKey(to=Section, ondelete="NO ACTION", nullable=False)
    checked_tests: str = Text(nullable=False)
    total_tests: int = Integer(default=0)
    right_count: int = Integer(default=0)
    wrong_count: int = Integer(default=0)
    percentage: float = Float(default=0.0)
    solved_time: str = String(max_length=255, nullable=False)
