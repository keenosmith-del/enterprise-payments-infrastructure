"""Provision isolated development databases. Use only on a dedicated disposable cluster.

EPI_BOOTSTRAP_DSN is an administrative psycopg DSN. For each application,
EPI_<NAME>_MIGRATION_PASSWORD and EPI_<NAME>_RUNTIME_PASSWORD are required.
"""
import os

import psycopg
from psycopg import sql

APPS = ("policy_administration", "payments_hub", "banking_simulator", "payroll_simulator")


def required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"{name} must be supplied")
    return value


def bootstrap() -> None:
    dsn = required("EPI_BOOTSTRAP_DSN")
    passwords = {
        (app, role): required(f"EPI_{app.upper()}_{role.upper()}_PASSWORD")
        for app in APPS for role in ("migration", "runtime")
    }
    if len(set(passwords.values())) != len(passwords):
        raise RuntimeError("All application credentials must be distinct")
    with psycopg.connect(dsn, autocommit=True) as conn:
        for database in ("postgres", "template1"):
            conn.execute(sql.SQL("REVOKE CONNECT, TEMPORARY ON DATABASE {} FROM PUBLIC").format(sql.Identifier(database)))
        for app in APPS:
            owner, migration, runtime = (f"{app}_{suffix}" for suffix in ("owner", "migration", "runtime"))
            for role in (owner, migration, runtime):
                exists = conn.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (role,)).fetchone()
                if not exists:
                    conn.execute(sql.SQL("CREATE ROLE {} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS").format(sql.Identifier(role)))
                conn.execute(sql.SQL("ALTER ROLE {} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS").format(sql.Identifier(role)))
            for role, kind in ((migration, "migration"), (runtime, "runtime")):
                conn.execute(sql.SQL("ALTER ROLE {} LOGIN PASSWORD {}").format(sql.Identifier(role), sql.Literal(passwords[app, kind])))
            conn.execute(sql.SQL("GRANT {} TO {} WITH INHERIT FALSE, SET TRUE").format(sql.Identifier(owner), sql.Identifier(migration)))
            exists = conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (app,)).fetchone()
            if not exists:
                conn.execute(sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0").format(sql.Identifier(app), sql.Identifier(owner)))
            conn.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(sql.Identifier(app), sql.Identifier(owner)))
            conn.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(app)))
            conn.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}, {}").format(sql.Identifier(app), sql.Identifier(migration), sql.Identifier(runtime)))
    for app in APPS:
        # Connection parameters are inherited without exposing the password in logs.
        with psycopg.connect(dsn, dbname=app, autocommit=True) as conn:
            owner = f"{app}_owner"
            conn.execute(sql.SQL("ALTER SCHEMA public OWNER TO {}").format(sql.Identifier(owner)))
            conn.execute("REVOKE ALL ON SCHEMA public FROM PUBLIC")
            conn.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(sql.Identifier(f"{app}_runtime")))
            conn.execute(sql.SQL("ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA public REVOKE ALL ON TABLES FROM PUBLIC").format(sql.Identifier(owner)))


if __name__ == "__main__":
    bootstrap()
