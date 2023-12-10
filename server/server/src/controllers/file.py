from fastapi import Request

from ..services import SendResponse, File


class FileController(object):
    def __init__(self):
        self.response = SendResponse

    async def get_one(self, request: Request):
        params = request.query_params

        file_path = params['file_path']

        file = await File.check_exists(file_path=file_path)

        if file is False:
            return self.response.failure(data=dict(message="Image does not exist"), status_code=404)

        return self.response.file(file_path=file_path)

