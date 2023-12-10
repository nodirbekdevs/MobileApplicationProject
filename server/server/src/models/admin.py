from ormar.fields import String

from ..utils import BaseMeta
from .core import CustomUser


class Admin(CustomUser):
    class Meta(BaseMeta):
        tablename = "management_admin"

    type: str = String(max_length=255, choices=["ADMIN", "SUPER_ADMIN"], nullable=False)
