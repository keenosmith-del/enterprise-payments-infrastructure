"""Real PostgreSQL tests. Only run against a dedicated disposable cluster."""
import os
import subprocess
from pathlib import Path

import psycopg
import pytest
from psycopg.conninfo import make_conninfo
from fastapi.testclient import TestClient

from packages.epi_foundation.app import Settings, create_app

from scripts.m01.bootstrap_databases import APPS, bootstrap
from scripts.m01.seed import seed

ROOT = Path(__file__).resolve().parents[2]
ADMIN = os.environ["EPI_BOOTSTRAP_DSN"]


def connection(app: str, role: str, db: str | None = None) -> str:
    return make_conninfo(ADMIN, dbname=db or app, user=f"{app}_{role}",
                         password=os.environ[f"EPI_{app.upper()}_{role.upper()}_PASSWORD"])


def test_bootstrap_migrate_seed_and_role_isolation() -> None:
    bootstrap()
    bootstrap()
    for app in APPS:
        migration = connection(app, "migration")
        url = "postgresql+psycopg://" + f"{app}_migration:" + os.environ[f"EPI_{app.upper()}_MIGRATION_PASSWORD"] + "@127.0.0.1:55433/" + app
        path = app.replace("_", "-")
        env = dict(os.environ, EPI_DATABASE_URL=url)
        for _ in range(2):
            subprocess.run(["alembic", "-c", str(ROOT / "apps" / path / "backend/alembic.ini"), "upgrade", "head"], env=env, cwd=ROOT, check=True)
        runtime = connection(app, "runtime")
        seed(runtime)
        seed(runtime)
        with psycopg.connect(runtime) as conn:
            assert conn.execute("SELECT count(*) FROM tenant").fetchone()[0] == 2
            assert conn.execute("SELECT count(*) FROM legal_entity").fetchone()[0] == 2
            assert conn.execute("SELECT version_num FROM foundation_schema_revision").fetchone()[0] == "m01_initial"
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                conn.execute("SELECT * FROM alembic_version")
        with psycopg.connect(runtime) as conn:
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                conn.execute("CREATE TABLE prohibited (id integer)")
        with psycopg.connect(runtime) as conn:
            with pytest.raises(psycopg.errors.ForeignKeyViolation):
                conn.execute("INSERT INTO legal_entity (id, tenant_id, name) VALUES (%s, %s, %s)",
                             ("30000000-0000-4000-8000-000000000001", "30000000-0000-4000-8000-000000000002", "Invalid"))
        runtime_url = url.replace(f"{app}_migration:", f"{app}_runtime:").replace(
            os.environ[f"EPI_{app.upper()}_MIGRATION_PASSWORD"], os.environ[f"EPI_{app.upper()}_RUNTIME_PASSWORD"])
        with TestClient(create_app(app.replace("_", "-"), Settings(database_url=runtime_url))) as client:
            assert client.get("/health/ready").status_code == 200
        with psycopg.connect(migration) as conn:
            assert conn.execute("SELECT tableowner FROM pg_tables WHERE schemaname='public' AND tablename='tenant'").fetchone()[0] == f"{app}_owner"
        for kind in ("runtime", "migration"):
            for other in (*[x for x in APPS if x != app], "postgres"):
                with pytest.raises(psycopg.OperationalError):
                    psycopg.connect(connection(app, kind, other), connect_timeout=3)
