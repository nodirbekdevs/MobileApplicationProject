from ormar.fields import String, Text

from .core import IsActiveCreatedUpdatedAtAbstract
from ..utils import BaseMeta


class Subject(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = 'testing_subject'

    title_uz: str = String(max_length=255, nullable=False)
    title_ru: str = String(max_length=255, nullable=False)
    description_uz: str = Text(nullable=False)
    description_ru: str = Text(nullable=False)
