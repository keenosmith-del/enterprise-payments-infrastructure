"""Run only with four disposable PostgreSQL databases supplied by the caller."""
import os
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from packages.epi_foundation.app import Settings, create_app

ROOT = Path(__file__).resolve().parents[2]
APPS = ("policy-administration", "payments-hub", "banking-simulator", "payroll-simulator")


@pytest.mark.parametrize("app", APPS)
def test_repeatable_migration_and_readiness(app: str) -> None:
    url = os.environ["EPI_TEST_BASE_URL"] + "/" + app.replace("-", "_")
    env = dict(os.environ, EPI_DATABASE_URL=url)
    command = ["alembic", "-c", str(ROOT / "apps" / app / "backend" / "alembic.ini"), "upgrade", "head"]
    subprocess.run(command, env=env, check=True, cwd=ROOT)
    subprocess.run(command, env=env, check=True, cwd=ROOT)
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            assert conn.execute(text("select version_num from alembic_version")).scalar_one() == "m01_principals"
            assert conn.execute(text("select count(*) from tenant")).scalar_one() == 0
    finally:
        engine.dispose()
    client = TestClient(create_app(app, Settings(database_url=url)))
    # Identity is intentionally absent in this database-only test.
    assert client.get("/health/ready").status_code == 503
