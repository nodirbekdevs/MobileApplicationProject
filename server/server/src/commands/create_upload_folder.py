from ..utils import uploads_file_path
from os import mkdir
from os.path import exists


def make_uploads_file():
    if exists(uploads_file_path):
        return

    mkdir(uploads_file_path)

    return
