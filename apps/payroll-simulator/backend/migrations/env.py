import os
from alembic import context
from sqlalchemy import create_engine, pool, text

url = os.environ.get("EPI_DATABASE_URL")
if not url or not url.startswith("postgresql+psycopg://"):
    raise RuntimeError("EPI_DATABASE_URL must use postgresql+psycopg")

if context.is_offline_mode():
    context.configure(url=url, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(url, poolclass=pool.NullPool)
    with engine.connect() as connection:
        # Migrations log in as a dedicated role and assume only this application's owner.
        connection.execute(text("SET ROLE payroll_simulator_owner"))
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
        # Readiness can inspect the revision without access to migration administration.
        connection.execute(text("CREATE OR REPLACE VIEW foundation_schema_revision AS SELECT version_num FROM alembic_version"))
        connection.execute(text("GRANT SELECT ON foundation_schema_revision TO payroll_simulator_runtime"))
        # Grant only application records, never Alembic's administration table.
        connection.execute(text("GRANT SELECT, INSERT, UPDATE, DELETE ON tenant, legal_entity, foundation_principal, application_config TO payroll_simulator_runtime"))
        connection.commit()
    engine.dispose()
