from fastapi import HTTPException
from fastapi.responses import FileResponse


class SendResponse(object):
    @staticmethod
    def success(status_code: int, data):
        return dict(data=data, message="Успешно", status=True, status_code=status_code)

    @staticmethod
    def failure(status_code: int, data):
        raise HTTPException(detail=dict(data=data, message="Не успешно", status=False), status_code=status_code)

    @staticmethod
    def file(file_path: str):
        return FileResponse(path=file_path, media_type="image/jpeg")
