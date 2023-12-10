from fastapi import APIRouter

from ..utils import ROUTE_PREFIX
# from .handlers import *

from .admin import admin_routes
from .advertising import advertising_routes
from .authentication import authentication_routes
from .feedback import feedback_routes
from .file import file_routes
from .instructor import instructor_routes
from .section import section_routes
from .statistic import statistic_routes
from .student import student_routes
from .subject import subject_routes
from .test import test_routes
from .user import user_routes

router = APIRouter(prefix=ROUTE_PREFIX)

router.include_router(router=admin_routes)
router.include_router(router=advertising_routes)
router.include_router(router=authentication_routes)
router.include_router(router=feedback_routes)
router.include_router(router=file_routes)
router.include_router(router=instructor_routes)
router.include_router(router=section_routes)
router.include_router(router=statistic_routes)
router.include_router(router=student_routes)
router.include_router(router=subject_routes)
router.include_router(router=test_routes)
router.include_router(router=user_routes)
