from ormar import ModelMeta
from ormar import Model, Boolean, DateTime, BigInteger, String
from datetime import datetime

from . import tashkent_timezone


class IsActiveAbstract(Model):
    class Meta:
        abstract = True

    is_active: bool = Boolean(
        name="is_active", default=True, help_text="Enable/Disable access to"
    )


class CreatedAtAbstract(Model):
    class Meta:
        abstract = True

    created_at: datetime = DateTime(default=datetime.now(tashkent_timezone))


class UpdatedAtAbstract(Model):
    class Meta:
        abstract = True

    updated_at: datetime = DateTime(default=datetime.now(tashkent_timezone))


class IdAbstract(Model):
    class Meta:
        abstract = True

    id = BigInteger(primary_key=True)


class IsActiveCreatedUpdatedAtAbstract(IdAbstract, IsActiveAbstract, CreatedAtAbstract, UpdatedAtAbstract):
    class Meta(ModelMeta):
        abstract = True


class CustomUser(IsActiveCreatedUpdatedAtAbstract):
    class Meta:
        abstract = True

    telegram_id: int = BigInteger(nullable=False)
    name: str = String(max_length=255, nullable=False)
    username: str = String(max_length=255, nullable=True)
    password: str = String(max_length=450, nullable=True)
    phone_number: str = String(max_length=255, nullable=False, unique=True)
    lang: str = String(max_length=255, default='uz')

    def __str__(self) -> str:
        return str(self.phone_number)
