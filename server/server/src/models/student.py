from .core import CustomUser
from ..utils import BaseMeta


class Student(CustomUser):
    class Meta(BaseMeta):
        tablename = 'management_student'

    pass
