# M00 preparation for M01 foundation

Revision 0.1 | 26 November 2026 | EPI 0.1.0 | Design only. Start after acceptance of M00 and explicit maintainer authorisation.

## Repository path plan

- `apps/`: `policy-administration/`, `payments-hub/`, `banking-simulator/`, `payroll-simulator/`.
- `services/`: `enterprise-integration/`, `data-engineering/`.
- `packages/`: `financial-types/`, `integration-contracts/`, `observability/`, `ui-components/`.
- `contracts/`: `openapi/`, `asyncapi/`, `events/`, `files/`.
- `infrastructure/`: `docker/`, `postgres/`, `rabbitmq/`, `sftp/`, `identity/`, `observability/`.
- `analytics/`: `pipelines/`, `transformations/`, `semantic-models/`, `power-bi/`.
- `tests/`: `integration/`, `contracts/`, `financial-integrity/`, `end-to-end/`, `performance/`, `recovery/`.
- `simulations/`, `evidence/`, `scripts/`, `docs/` and `.github/workflows/` for simulation inputs, evidence and verification.

The future directories are introduced with their first exercised contents. `scripts/m00` contains disposable probes. App code and app migrations start at the relevant milestone.

## Sequence and acceptance evidence

1. Platform owner locks Python and Node dependencies using reviewed resolvers and version provenance, records image digests by architecture and documents install from clean checkout. Confirm license review for distributed packages and scan dependencies and images. Queue the latest safe releases within each approved compatibility line.
2. Create independent app databases. Apply roles, connection denials, schema ownership and migrations using separate identities. Seed repeatably using synthetic fixtures and explicit tenant and legal entity IDs. In integration tests prove each application cannot connect to, read or modify other application stores. Verify a second migration invocation is safe, and test upgrade and forward repair without accessing another application. Capture schema and credential test evidence for ADR-P01, NFR-003 and NFR-009.
3. Configure the local core profile for database, broker and four app health surfaces. Add isolated identity and integration profiles for Keycloak and SFTP. Set health checks for liveness versus readiness and observe late service availability. Expose ports only to the host loopback when needed. Use profile-scoped Compose project names, named volumes and explicit teardown scope. Define secret injection via ignored files or a local environment, distinct runtime passwords, constrained broker accounts and per-partner SSH keys. Keep sample values inert and ephemeral credentials out of logs.
4. Establish a synthetic tenant and role model for human and service principals. Verify token issuer and audience, tenant enforcement, wrong-scope denial and safe identity outages. Approvals remain independently exercised in their dependent milestones. Document safe local credential rotation and reset paths.
5. Build repeatably and run the milestone baseline, lint, type, dependency, migration, seed, smoke and privilege tests both locally and in CI. Record OS, architecture, image digests, exact commands, counts, branch SHA and workflow URL. Require a clean re-run from a fresh Git checkout. Keep broker, SFTP and DB denial tests real. Do not use demo UI or generated data as verification of application persistence.
6. Require signed review of the M01 build, migration, seed and credential gate before M02 financial primitives. Subsequent implementation preserves short transactions across external I/O, independent provider evidence, synthetic-only rails and dispatch controls. Validate M02 and M04-M06 prerequisites before any dispatch.

Outstanding M00 gates are listed in the [completion report](M00_COMPLETION_REPORT.md). Owners are platform for environment and release, integration for real transports, finance for worked expectations, security for cross-tenant and principal controls, data for analytical lineage, and the maintainer for decision approval.
