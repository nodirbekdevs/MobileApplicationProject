from ormar import ModelMeta
from ormar.fields import ForeignKey, Integer, String, Text

from ..utils import BaseMeta
from .core import IsActiveCreatedUpdatedAtAbstract
from .instructor import Instructor
from .subject import Subject


class Section(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = "testing_section"

    instructor_id = ForeignKey(to=Instructor, ondelete="NO ACTION", nullable=False)
    subject_id = ForeignKey(to=Subject, ondelete="NO ACTION", nullable=False)
    title_uz: str = String(max_length=1000, nullable=False)
    title_ru: str = String(max_length=1000, nullable=False)
    description_uz: str = Text(nullable=False)
    description_ru: str = Text(nullable=False)
    total_tests: int = Integer(default=0)
