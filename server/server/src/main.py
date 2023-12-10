from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sys import argv

from .commands import make_uploads_file
from .utils import database, API_PREFIX, ORIGINS, HOST, uploads_file_path
from .routers import router


def get_application() -> FastAPI:
    application = FastAPI(
        docs_url='/api/v1/docs',
        redoc_url='/api/v1/redocs',
        title='TMI Test System API',
        version='1.0',
        openapi_url='/api/v1/openapi.json'
    )

    # application.mount("/uploads", StaticFiles(directory=uploads_file_path), name="images")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=['*']
    )

    application.state.database = database

    database_ = application.state.database

    @application.on_event("startup")
    async def startup() -> None:
        if not database_.is_connected:
            await database_.connect()

    @application.on_event("shutdown")
    async def shutdown() -> None:
        if database_.is_connected:
            await database_.disconnect()

    application.include_router(router=router, prefix=API_PREFIX)

    return application


if __name__ == '__main__':
    from uvicorn import run

    if len(argv) > 1 and argv[1] == 'createuploadsfile':
        make_uploads_file()
    else:
        app = get_application()

        # run("src.main:app", host="127.0.0.1", port=8250, reload=True)
        run(app=app, host=HOST, port=8002)
