from ormar import ModelMeta, String, Text

from ..utils import BaseMeta
from .core import IsActiveCreatedUpdatedAtAbstract


class Advertising(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = "marketing_advertising"

    title: str = String(max_length=255, nullable=False)
    description: str = Text(nullable=True)
    image: str = String(max_length=1000, nullable=True)
