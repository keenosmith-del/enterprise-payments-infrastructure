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
        connection.execute(text("SET ROLE banking_simulator_owner"))
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
        # Grant only application records, never Alembic's administration table.
        connection.execute(text("GRANT SELECT, INSERT, UPDATE, DELETE ON tenant, legal_entity TO banking_simulator_runtime"))
        connection.commit()
    engine.dispose()
