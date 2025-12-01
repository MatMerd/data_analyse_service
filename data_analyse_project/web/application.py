from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from data_analyse_project.di import build_container
from data_analyse_project.features.logline.api import router as logline_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Tools",
        version="1.0.0",
        default_response_class=ORJSONResponse,
        lifespan=build_container,
    )
    app.include_router(logline_router)
    return app
