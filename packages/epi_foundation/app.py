"""Shared HTTP foundation. Identity and tenant access are not yet implemented."""

import json
import logging
import time
import uuid
import urllib.error
import urllib.request
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator
from uuid import UUID

from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from packages.epi_foundation.identity import OIDCVerifier, Principal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EPI_")
    environment: str = "development"
    database_url: str = ""
    oidc_issuer: str = ""
    oidc_audience: str = ""
    oidc_jwks_url: str = ""


def create_app(name: str, settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    logger = logging.getLogger("epi.request")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    registry = CollectorRegistry()
    request_count = Counter("epi_http_requests_total", "HTTP requests", ["method", "status"], registry=registry)
    duration = Histogram("epi_http_request_duration_seconds", "HTTP request duration", registry=registry)
    provider = TracerProvider(resource=Resource.create({"service.name": name, "deployment.environment.name": config.environment}))
    tracer = provider.get_tracer("epi.foundation")
    verifier = (OIDCVerifier(config.oidc_issuer, config.oidc_audience, config.oidc_jwks_url)
                if config.oidc_issuer and config.oidc_audience and config.oidc_jwks_url else None)
    bearer = HTTPBearer(auto_error=False)
    engine: Engine | None = None
    if config.database_url.startswith("postgresql+psycopg://"):
        try:
            engine = create_engine(config.database_url, pool_pre_ping=True,
                                   connect_args={"connect_timeout": 3})
        except (SQLAlchemyError, ValueError, ImportError):
            logger.error(json.dumps({"application": name, "category": "configuration_error"}))
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
        provider.shutdown()

    app = FastAPI(title=name, docs_url="/docs" if config.environment == "development" else None,
                  redoc_url=None, lifespan=lifespan)

    app.state.tracer_provider = provider

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
        with tracer.start_as_current_span("http.request") as span:
            span.set_attribute("http.request.method", request.method)
            response = await call_next(request)
            span.set_attribute("http.response.status_code", response.status_code)
        elapsed = time.monotonic() - started
        request_count.labels(request.method, str(response.status_code)).inc()
        duration.observe(elapsed)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info(json.dumps({"application": name, "environment": config.environment,
                               "request_id": request_id, "correlation_id": correlation_id,
                               "method": request.method, "status": response.status_code,
                               "duration_ms": round(elapsed * 1000, 2)}))
        return response

    @app.exception_handler(StarletteHTTPException)
    async def technical_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": "request_failed",
                            "request_id": request.state.request_id}, headers=exc.headers)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, _exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"error": "invalid_request",
                            "request_id": request.state.request_id})

    @app.exception_handler(Exception)
    async def internal_error(request: Request, _exc: Exception) -> JSONResponse:
        logger.error(json.dumps({"application": name, "environment": config.environment,
                                 "request_id": getattr(request.state, "request_id", "unknown"),
                                 "category": "internal_error"}))
        return JSONResponse(status_code=500, content={"error": "internal_error",
                            "request_id": getattr(request.state, "request_id", "unknown")})

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", response_model=None)
    def ready() -> dict[str, str] | JSONResponse:
        if engine is None or not heads or verifier is None:
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        try:
            with engine.connect() as conn:
                revisions = set(conn.execute(text("SELECT version_num FROM foundation_schema_revision")).scalars())
                if revisions != heads:
                    return JSONResponse(status_code=503, content={"status": "not_ready"})
            with urllib.request.urlopen(config.oidc_jwks_url, timeout=3) as response:
                jwks = json.loads(response.read(1024 * 1024))
                if response.status != 200 or not isinstance(jwks.get("keys"), list) or not jwks["keys"]:
                    return JSONResponse(status_code=503, content={"status": "not_ready"})
        except (SQLAlchemyError, urllib.error.URLError, TimeoutError, ValueError, AttributeError):
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return {"status": "ready"}

    def authenticated(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> Principal:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Credentials required")
        if verifier is None:
            raise HTTPException(status_code=503, detail="Identity unavailable")
        return verifier.verify(credentials.credentials)

    @app.get("/me")
    def me(principal: Principal = Depends(authenticated)) -> dict[str, object]:
        return {"kind": principal.kind, "tenant_ids": sorted(str(value) for value in principal.tenants)}

    @app.get("/tenants/{tenant_id}/legal-entities")
    def legal_entities(tenant_id: UUID, principal: Principal = Depends(authenticated)) -> dict[str, object]:
        if principal.kind != "human" or "foundation-reader" not in principal.roles or "foundation.read" not in principal.scopes:
            raise HTTPException(status_code=403, detail="Forbidden")
        if tenant_id not in principal.tenants:
            raise HTTPException(status_code=403, detail="Forbidden")
        if engine is None:
            raise HTTPException(status_code=503, detail="Database unavailable")
        try:
            with engine.connect() as conn:
                rows = conn.execute(text("SELECT id, name FROM legal_entity WHERE tenant_id = :tenant_id ORDER BY id"),
                                    {"tenant_id": tenant_id}).all()
                return {"items": [{"id": str(row.id), "name": row.name} for row in rows]}
        except SQLAlchemyError:
            raise HTTPException(status_code=503, detail="Database unavailable") from None

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    @app.get("/info")
    def info() -> dict[str, str]:
        return {"application": name, "environment": config.environment, "stage": "foundation-in-progress"}

    return app
