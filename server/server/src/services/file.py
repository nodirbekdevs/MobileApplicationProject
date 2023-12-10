from fastapi import UploadFile
from aiofiles import open
from os import mkdir, remove
from os.path import exists, splitext, join
from asyncio import to_thread
from uuid import uuid4
from re import sub

from ..utils import TEST
from .response import SendResponse


class File(object):
    def __init__(self, file):
        self.file = file
        self.response = SendResponse

    async def write(self, file_name: str):
        async with open(file_name, "wb") as file:
            await file.write(self.file.file.read())

    @classmethod
    async def check_exists(cls, file_path):
        return await to_thread(exists, file_path)

    @classmethod
    async def check_or_create_folder(cls, file_path):
        file_exists = await cls.check_exists(file_path)

        if file_exists is False:
            await to_thread(mkdir, file_path)

    @classmethod
    async def remove(cls, file_path):
        file_exists = await cls.check_exists(file_path)

        if file_exists:
            await to_thread(remove, path=file_path)

    # @staticmethod
    # async def get_file(file_path):
    #     async with open(file_path, 'rb') as file:
    #
    #     pass

    async def save(self, file_model_type: str, path: str, user=None, title=None):
        await self.check_or_create_folder(file_path=path)

        model_type = "test" if file_model_type == TEST else 'advertising'

        file_model_path = f"{path}/{model_type}_images"

        await self.check_or_create_folder(file_path=file_model_path)

        name = f'{self.file.filename}' if self.file.filename else title

        file_name = f"{'_'.join(name.split(' '))}_{uuid4()}.jpg"

        if title:
            file_name = f"{'_'.join(name.lower().replace('?', '').split(' '))}_{uuid4()}.jpg"

        if user:
            file_name = f'{user.id}_{file_name}'

        file_path = f'{file_model_path}/{file_name}'

        await self.write(file_path)

        return file_path
