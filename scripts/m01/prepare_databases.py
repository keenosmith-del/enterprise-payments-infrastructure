"""Bootstrap and migrate four databases using separate provisioner and migration roles."""
import os
import subprocess
from urllib.parse import quote

from bootstrap_databases import APPS, bootstrap
from seed import seed

bootstrap()
for app in APPS:
    migration_password = quote(os.environ[f"EPI_{app.upper()}_MIGRATION_PASSWORD"], safe="")
    migration_url = f"postgresql+psycopg://{app}_migration:{migration_password}@postgres:5432/{app}"
    env = dict(os.environ, EPI_DATABASE_URL=migration_url)
    subprocess.run(["alembic", "-c", f"apps/{app.replace('_', '-')}/backend/alembic.ini", "upgrade", "head"], check=True, env=env)
    seed(f"postgresql://{app}_migration:{migration_password}@postgres:5432/{app}")
