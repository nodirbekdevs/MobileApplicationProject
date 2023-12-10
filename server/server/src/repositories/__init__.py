from .core import CoreRepository
from ..models import *
from ..schemas import *


class Storage:
    admin = CoreRepository(model=Admin, scope="admin", schemas=SchemaStorage.admin)
    advertising = CoreRepository(model=Advertising, scope="advertising", schemas=SchemaStorage.advertising)
    feedback = CoreRepository(model=Feedback, scope="feedback", schemas=SchemaStorage.feedback)
    instructor = CoreRepository(model=Instructor, scope="instructor", schemas=SchemaStorage.instructor)
    section = CoreRepository(model=Section, scope="section", schemas=SchemaStorage.section)
    statistics = CoreRepository(model=Statistic, scope="statistic", schemas=SchemaStorage.statistic)
    student = CoreRepository(model=Student, scope="student", schemas=SchemaStorage.student)
    subject = CoreRepository(model=Subject, scope="subject", schemas=SchemaStorage.subject)
    test = CoreRepository(model=Test, scope="test", schemas=SchemaStorage.test)
