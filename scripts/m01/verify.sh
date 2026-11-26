#!/usr/bin/env bash
# Explicit full local verification. Uses disposable infrastructure for destructive probes.
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH="$PWD/.venv/bin:$PATH"
make lint typecheck test
python scripts/validate_baseline.py
.venv-security/bin/pip-audit --cache-dir .local/pip-audit-cache --disable-pip --no-deps -r requirements.lock
npm audit --audit-level=moderate
npm run typecheck
npm run build
make up
set -a
# This file is generated locally and contains synthetic development credentials.
source .local/epi.env
set +a
python -m pytest tests/integration/test_keycloak.py tests/integration/test_stack_authorization.py -v
npx playwright test tests/browser --workers=1
python -m pytest tests/integration/test_rabbit_permissions.py -v
docker compose --env-file .local/epi.env --profile integration build enterprise-integration
python scripts/m01/publish_probe.py
message="$(docker compose --env-file .local/epi.env --profile integration run --rm -T --no-deps enterprise-integration | tr -d '\r')"
test "$message" = synthetic-technical-probe
scripts/m01/create_sftp_keys.sh
docker compose --env-file .local/epi.env --profile sftp up -d --build --wait sftp
scripts/m01/probe_dev_sftp.sh
bash scripts/m00/probe_sftp_ssh.sh
docker compose --env-file .local/epi.env --profile analytics run --rm data-engineering
docker compose --env-file .local/epi.env --profile observability up -d --wait prometheus grafana
curl --retry 15 --retry-delay 2 --retry-all-errors -fsS "http://127.0.0.1:${EPI_PROMETHEUS_PORT:-9090}/-/ready" >/dev/null
curl --retry 15 --retry-delay 2 --retry-all-errors -fsS "http://127.0.0.1:${EPI_GRAFANA_PORT:-3000}/api/health" >/dev/null
python -m unittest discover -s scripts/m00 -p test_local_probes.py -v

# The database privilege suite creates and alters roles, so isolate it from the core cluster.
container="epi-m01-verify-$$"
m00_database="epi-m00-db-$$"
m00_broker="epi-m00-broker-$$"
cleanup() { docker rm -f "$container" "$m00_database" "$m00_broker" >/dev/null 2>&1 || true; }
trap cleanup EXIT
password="$(openssl rand -hex 24)"
mask() { if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then printf '::add-mask::%s\n' "$1"; fi; }
mask "$password"
docker run -d --name "$container" -e POSTGRES_PASSWORD="$password" -p 127.0.0.1:55433:5432 \
  postgres:17@sha256:87c8b42f423b45d5247e6aa8fdb2e7762fec164c68a50fe3eb07e7bfcaf4dbcf >/dev/null
for attempt in $(seq 1 30); do
  if docker exec "$container" pg_isready -U postgres >/dev/null; then break; fi
  if [[ "$attempt" == 30 ]]; then exit 1; fi
  sleep 1
done
export EPI_BOOTSTRAP_DSN="host=127.0.0.1 port=55433 dbname=postgres user=postgres password=$password"
for app in POLICY_ADMINISTRATION PAYMENTS_HUB BANKING_SIMULATOR PAYROLL_SIMULATOR; do
  for role in MIGRATION RUNTIME; do
    value="$(openssl rand -hex 24)"
    mask "$value"
    export "EPI_${app}_${role}_PASSWORD=$value"
  done
done
python -m pytest tests/integration/test_database_boundaries.py -v

# Preserve the original M00 service probes on isolated disposable endpoints.
export EPI_M00_POSTGRES_PASSWORD="$(openssl rand -hex 24)"
export EPI_M00_AMQP_PASSWORD="$(openssl rand -hex 24)"
mask "$EPI_M00_POSTGRES_PASSWORD"
mask "$EPI_M00_AMQP_PASSWORD"
docker run -d --name "$m00_database" -e POSTGRES_USER=epi_probe -e POSTGRES_PASSWORD="$EPI_M00_POSTGRES_PASSWORD" -p 127.0.0.1:55434:5432 postgres:17-bookworm >/dev/null
docker run -d --name "$m00_broker" -e RABBITMQ_DEFAULT_USER=epi_probe -e RABBITMQ_DEFAULT_PASS="$EPI_M00_AMQP_PASSWORD" -e 'RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS=+S 2:2 +A 2' -p 127.0.0.1:55672:5672 rabbitmq:4.2 >/dev/null
for attempt in $(seq 1 60); do
  if docker exec "$m00_database" pg_isready -U epi_probe >/dev/null 2>&1 && python -c 'import os,pika; c=pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 55672, "/", pika.PlainCredentials("epi_probe", os.environ["EPI_M00_AMQP_PASSWORD"]), socket_timeout=2)); c.close()' >/dev/null 2>&1; then break; fi
  if [[ "$attempt" == 60 ]]; then
    docker logs --tail 40 "$m00_database" >&2
    docker logs --tail 40 "$m00_broker" >&2
    exit 1
  fi
  sleep 2
done
export EPI_M00_POSTGRES_DSN="postgresql://epi_probe:$EPI_M00_POSTGRES_PASSWORD@127.0.0.1:55434/epi_probe"
export EPI_M00_AMQP_URL="amqp://epi_probe:$EPI_M00_AMQP_PASSWORD@127.0.0.1:55672/%2F"
python -m unittest discover -s scripts/m00 -p test_service_probes.py -v
