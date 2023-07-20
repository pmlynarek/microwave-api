from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.error_handlers import register_error_handlers
from app.api.routes import api_router
from app.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=settings.API_PREFIX)
    register_error_handlers(application)

    return application
