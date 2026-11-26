"""Idempotently seed only the configured application database with synthetic records."""
import os
import psycopg

TENANTS = (("10000000-0000-4000-8000-000000000001", "Synthetic Tenant A"),
           ("10000000-0000-4000-8000-000000000002", "Synthetic Tenant B"))
ENTITIES = (("20000000-0000-4000-8000-000000000001", TENANTS[0][0], "Synthetic Entity A"),
            ("20000000-0000-4000-8000-000000000002", TENANTS[1][0], "Synthetic Entity B"))


def seed(dsn: str) -> None:
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO tenant (id, name) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name", TENANTS)
            cur.executemany("INSERT INTO legal_entity (id, tenant_id, name) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET tenant_id = EXCLUDED.tenant_id, name = EXCLUDED.name", ENTITIES)
            principals = (("30000000-0000-4000-8000-000000000001", TENANTS[0][0], "synthetic-user", "human"),
                          ("30000000-0000-4000-8000-000000000002", TENANTS[1][0], "synthetic-user-b", "human"),
                          ("30000000-0000-4000-8000-000000000003", TENANTS[0][0], "integration-service", "service"))
            cur.executemany("INSERT INTO foundation_principal (id, tenant_id, identity_reference, kind) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET tenant_id = EXCLUDED.tenant_id, identity_reference = EXCLUDED.identity_reference, kind = EXCLUDED.kind", principals)
            cur.executemany("INSERT INTO application_config (tenant_id, key, value) VALUES (%s, %s, %s) ON CONFLICT (tenant_id, key) DO UPDATE SET value = EXCLUDED.value", [(tenant[0], "environment", "synthetic-development") for tenant in TENANTS])


if __name__ == "__main__":
    seed(os.environ["EPI_SEED_DSN"])
