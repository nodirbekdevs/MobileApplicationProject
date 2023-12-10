from pydantic import BaseModel
from typing import List

from .core import CoreResponseSchema


class FeedbackCreateRequest(BaseModel):
    user_id: str
    user_type: str
    is_read: bool | None
    reason: str
    status: str | None


class FeedbackUpdateRequest(BaseModel):
    reason: str | None
    status: str | None


class FeedbackResponse(CoreResponseSchema, FeedbackCreateRequest):
    pass


class FeedbackResponseList(BaseModel):
    querysets: List[FeedbackResponse]


class FeedbackRepositorySchemas(object):
    list = FeedbackResponseList
    retrieve = FeedbackResponse
