from os.path import join
from .base import BASE_DIR

STATIC_URL = "/static/"
STATIC_ROOT = join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = join(BASE_DIR, "media")
STATIC_FILES_DIRS = [
    BASE_DIR / 'static'
]
