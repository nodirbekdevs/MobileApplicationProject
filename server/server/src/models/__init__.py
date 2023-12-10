from pytz import timezone

tashkent_timezone = timezone('Asia/Tashkent')

from .admin import *
from .advertising import *
from .core import *
from .feedback import *
from .instructor import *
from .section import *
from .statistic import *
from .student import *
from .subject import *
from .test import *


# from ormar import pre_update
#
#
# @pre_update(Album)
# async def before_update(sender, instance, **kwargs):
#     if instance.play_count > 50 and not instance.is_best_seller:
#         instance.is_best_seller = True