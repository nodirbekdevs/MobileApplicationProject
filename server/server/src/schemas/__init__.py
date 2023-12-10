from .admin import *
from .advertising import *
from .authentication import *
from .feedback import *
from .instructor import *
from .section import *
from .statistic import *
from .student import *
from .subject import *
from .test import *

from ..services import SchemaRepository


class SchemaStorage(object):
    admin = SchemaRepository(schemas=AdminRepositorySchemas)
    advertising = SchemaRepository(schemas=AdvertisingRepositorySchemas)
    feedback = SchemaRepository(schemas=FeedbackRepositorySchemas)
    instructor = SchemaRepository(schemas=InstructorRepositorySchemas)
    section = SchemaRepository(schemas=SectionRepositorySchemas)
    statistic = SchemaRepository(schemas=StatisticRepositorySchemas)
    student = SchemaRepository(schemas=StudentRepositorySchemas)
    subject = SchemaRepository(schemas=SubjectRepositorySchemas)
    test = SchemaRepository(schemas=TestRepositorySchemas)
