# M00 architecture verification

Revision 0.1 | 26 November 2026 | EPI 0.1.0 | Partial evidence.

## Executed local verification

Run `python3.12 -m unittest discover -s scripts/m00 -p test_local_probes.py -v` from the repository root. Three tests passed, zero failed and zero skipped. The [execution record](../../../evidence/m00/local-verification.txt) records exact commands and results. The environment is macOS arm64 with CPython 3.12.15 and OpenSSH 10.3p1. There is no Git commit identifier.

- Exact arithmetic (FR-020, FI-01, NFR-001). Independent expected value was 75,031 cents for the three rate-independent decimal amounts. The observed sum matched. This check uses Python Decimal. The PostgreSQL exact-value check is separate.
- Provider operation identity (FR-010/015/019/025, FI-03/04, SC-03). A separate process committed 75,000 cents then exited before emitting an acknowledgement. Enquiry and identical replay returned the expected persisted operation. Changed replay was rejected. A direct independent fixture database count confirmed one row and 75,000 cents. This uses a local CLI boundary and SQLite. HTTP transport, provider orchestration, settlement and actual Hub recovery remain unverified.
- SFTP transfer and file readiness (FR-008, SC-08, NFR-004). The OpenSSH client invoked the actual SFTP subsystem through standard input and output. Uploaded bytes, staging suffix filtering, remote rename, re-download, CSV row and digest matched the expected fixture. Two transfers yielded a single digest. SSH public-key authentication, chroot isolation and network custody are separate requirements.

`python3 scripts/validate_baseline.py` verified the four PDF fingerprints, catalogue and source text, format and links. `python3.12 -m compileall -q scripts` checked Python syntax. `bash -n scripts/m00/probe_sftp_ssh.sh` checked the networked SFTP script syntax. Compose configuration parsing succeeded. These checks carry no claim of service execution.

## Pending execution and expected outcomes

- PostgreSQL probe (FR-010/020/024, FI-01/05/06/09, NFR-001/003). Expect exact 75,031 cents, denial of a writer against another database, rollback of both posting and outbox on injected failure, rejection of imbalance, a missing parent, duplicate posting and direct update, then one durable posting/outbox pair. Two concurrent reservations of 80 against capacity 100 must leave 20 available after the serialization retry rejects the losing reservation.
- RabbitMQ probe (FR-007/010, FI-03/10, SC-08, NFR-002). Expect confirms for persistent publications, redelivery of an unacknowledged committed operation after connection loss, one durable fixture inbox effect after duplicate delivery, explicit consumer acknowledgement, then one bounded poison-message retry and a single dead-letter record. The inbox is a SQLite fixture. Postgres-backed inbox and broker restart/recovery require the later integration gates.
- Networked SFTP probe (FR-008, FI-09, SC-08/09). Expect OpenSSH transfer with verified host key, independently generated partner keys, failed cross-account authentication, unavailable peer and out-of-chroot paths, and identical downloaded bytes. Create only scratch credentials. Invalid, changed and partially imported manifest recovery remains an M04 integration test.
- Analytical replay probe (FR-031/032/033, FI-11, SC-10, NFR-008). Expect two immutable Parquet batches, one suppressed repeated batch, an overlapping event with two source hashes, lineage and a late negative adjustment. The replay query should report three unique events totalling 90,000 cents. Object-store policies and incremental publication recovery are deferred to the analytics milestone.
- Infrastructure (ADR-P01/03/08, NFR-006/009). Expect a clean pull and health start on ARM64 and AMD64. Capture distro and digest, CPU, memory, disk and cold-start time for each active service. Dependency packages and images are candidates until verified. Power BI runtime is a separate Windows check.

## Reproduce on a network-enabled host

Run only against newly provisioned disposable services. From the repository root, use a fresh shell:

```bash
set -e
scratch="$(mktemp -d)"
python3.12 -m venv "$scratch/venv"
"$scratch/venv/bin/python" -m pip install -r scripts/m00/requirements.txt
export EPI_M00_POSTGRES_PASSWORD="$(openssl rand -hex 20)"
export EPI_M00_AMQP_PASSWORD="$(openssl rand -hex 20)"
export EPI_M00_POSTGRES_DSN="postgresql://epi_probe:$EPI_M00_POSTGRES_PASSWORD@127.0.0.1:55432/epi_probe"
export EPI_M00_AMQP_URL="amqp://epi_probe:$EPI_M00_AMQP_PASSWORD@127.0.0.1:55672/%2F"
trap 'docker compose -p epi-m00 -f scripts/m00/compose.yaml down -v' EXIT
docker compose -p epi-m00 -f scripts/m00/compose.yaml up -d --wait
"$scratch/venv/bin/python" -m unittest discover -s scripts/m00 -p test_service_probes.py -v
bash scripts/m00/probe_sftp_ssh.sh
```

The [GitHub Actions workflow](../../../.github/workflows/m00-verification.yml) includes a GNU/Linux runner path. The host network and daemon blocked the service test run here. The tests are kept enabled in CI. Record the resolved image digests and runtime results against the final commit before accepting architecture and release gates.
