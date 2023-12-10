from ormar.fields import ForeignKey, Boolean, Text, String
from ormar_postgres_extensions.fields.array import ARRAY
from sqlalchemy import String as AlchemyString

from ..utils import BaseMeta
from .core import IsActiveCreatedUpdatedAtAbstract
from .instructor import Instructor
from .section import Section
from .subject import Subject


class Test(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = "testing_test"

    instructor_id: Instructor = ForeignKey(to=Instructor, ondelete="NO ACTION", nullable=False)
    subject_id: Subject = ForeignKey(to=Subject, ondelete="NO ACTION", nullable=False)
    section_id: Section = ForeignKey(to=Section, ondelete="NO ACTION", nullable=False)
    image: str = String(max_length=255, nullable=True)
    question_uz: str = String(max_length=1000, nullable=False)
    question_ru: str = String(max_length=1000, nullable=False)
    variants_uz: list = ARRAY(item_type=AlchemyString())
    variants_ru: list = ARRAY(item_type=AlchemyString())
    correct_answer_uz: str = Text(nullable=False)
    correct_answer_ru: str = Text(nullable=False)
    is_testing: bool = Boolean(default=False)
