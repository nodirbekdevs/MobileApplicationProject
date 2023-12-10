from ormar.fields import ForeignKey, Integer

from .core import CustomUser
from .subject import Subject
from ..utils import BaseMeta


class Instructor(CustomUser):
    class Meta(BaseMeta):
        tablename = 'management_instructor'

    subject_id = ForeignKey(to=Subject, ondelete='NO ACTION', nullable=True)
    solving_test_number = Integer(default=30)
