"""Shared HTTP foundation. Identity and tenant access are not yet implemented."""

import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EPI_")
    environment: str = "development"
    database_url: str = ""


def create_app(name: str, settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    logger = logging.getLogger("epi.request")
    engine: Engine | None = None
    if config.database_url.startswith("postgresql+psycopg://"):
        try:
            engine = create_engine(config.database_url, pool_pre_ping=True,
                                   connect_args={"connect_timeout": 3})
        except (SQLAlchemyError, ValueError, ImportError):
            logger.error("database configuration invalid")
    slug = name.lower().replace(" ", "-")
    alembic_ini = Path(__file__).resolve().parents[2] / "apps" / slug / "backend" / "alembic.ini"
    try:
        heads = set(ScriptDirectory.from_config(Config(str(alembic_ini))).get_heads()) if alembic_ini.is_file() else set()
    except (OSError, KeyError, ValueError):
        heads = set()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        yield
        if engine is not None:
            engine.dispose()

    app = FastAPI(title=name, docs_url="/docs" if config.environment == "development" else None,
                  redoc_url=None, lifespan=lifespan)

    @app.middleware("http")
    async def request_context(request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        started = time.monotonic()
        try:
            correlation_id = str(uuid.UUID(request.headers.get("X-Correlation-ID", request_id)))
        except ValueError:
            correlation_id = request_id
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info(json.dumps({"application": name, "environment": config.environment,
                               "request_id": request_id, "correlation_id": correlation_id,
                               "method": request.method, "status": response.status_code,
                               "duration_ms": round((time.monotonic() - started) * 1000, 2)}))
        return response

    @app.exception_handler(HTTPException)
    async def technical_error(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": "request_failed",
                            "request_id": request.state.request_id}, headers=exc.headers)

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", response_model=None)
    def ready() -> dict[str, str] | JSONResponse:
        if engine is None or not heads:
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        try:
            with engine.connect() as conn:
                revisions = set(conn.execute(text("SELECT version_num FROM foundation_schema_revision")).scalars())
                if revisions != heads:
                    return JSONResponse(status_code=503, content={"status": "not_ready"})
        except SQLAlchemyError:
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return {"status": "ready"}

    @app.get("/info")
    def info() -> dict[str, str]:
        return {"application": name, "environment": config.environment, "stage": "foundation-in-progress"}

    return app
