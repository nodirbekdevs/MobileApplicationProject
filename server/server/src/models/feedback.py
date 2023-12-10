from ormar import ModelMeta, String, Text, Boolean

from .core import IsActiveCreatedUpdatedAtAbstract
from ..utils import BaseMeta


class Feedback(IsActiveCreatedUpdatedAtAbstract):
    class Meta(BaseMeta):
        tablename = 'marketing_feedback'

    user_id = String(max_length=255, nullable=False)
    user_type = String(max_length=255, nullable=False)
    is_read = Boolean(default=False)
    reason = Text(nullable=False)
    status = String(max_length=255, nullable=True, default="")