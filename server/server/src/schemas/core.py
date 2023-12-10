from pydantic import BaseModel, constr, validator
from datetime import datetime


class CoreResponseSchema(BaseModel):
    id: int
    is_active: bool
    updated_at: datetime
    created_at: datetime


class CoreCollatedSchema(BaseModel):
    data: dict
    message: str
    status: bool


class CoreUserRequest(BaseModel):
    telegram_id: int
    name: str | None
    username: str | None
    password: str | None
    phone_number: str
    lang: str | None


class CoreUserCreateRequest(BaseModel):
    telegram_id: int
    name: str | None
    username: str | None
    password: str | None
    phone_number: str
    lang: str | None = 'ru'


class CoreUserUpdateRequest(BaseModel):
    name: str | None
    username: str | None
    old_password: constr(max_length=255) | None
    new_password: constr(max_length=255) | None
    phone_number: str | None
    lang: str | None

    @classmethod
    @validator('old_password', 'new_password', pre=True)
    def validate_not_none(cls, value):
        if value is None:
            raise ValueError("Field cannot be None")
        return value
