"""Technical HTTP foundation. No business or authentication claims are made here."""

import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EPI_")
    environment: str = "development"
    database_url: str = ""


def create_app(name: str, settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    app = FastAPI(title=name, docs_url="/docs" if config.environment == "development" else None,
                  redoc_url=None)
    logger = logging.getLogger("epi.request")

    @app.middleware("http")
    async def request_context(request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        started = time.monotonic()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info("application=%s environment=%s request_id=%s method=%s status=%s duration_ms=%.2f",
                    name, config.environment, request_id, request.method, response.status_code,
                    (time.monotonic() - started) * 1000)
        return response

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", response_model=None)
    def ready() -> dict[str, str] | JSONResponse:
        if not config.database_url:
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        try:
            engine = create_engine(config.database_url, connect_args={"connect_timeout": 3})
            try:
                with engine.connect() as conn:
                    # Readiness fails closed until the initial application migration exists.
                    revision = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
                    if revision != "m01_initial":
                        return JSONResponse(status_code=503, content={"status": "not_ready"})
            finally:
                engine.dispose()
        except (SQLAlchemyError, ValueError, ImportError):
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return {"status": "ready"}

    @app.get("/info")
    def info() -> dict[str, str]:
        return {"application": name, "environment": config.environment, "stage": "foundation-in-progress"}

    return app
