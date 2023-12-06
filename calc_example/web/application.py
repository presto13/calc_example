from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from calc_example.web.api.router import api_router
from calc_example.web.lifetime import register_shutdown_event, register_startup_event
from calc_example.web.web_app.route_web_app import router as web_app_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="calc_example",
        version=metadata.version("calc_example"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.mount("/static", StaticFiles(directory="calc_example/static"), name="static")

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=web_app_router, prefix="")

    return app
