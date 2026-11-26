# Engineering decision register

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Decision status

The following nine ADRs reproduce Document 04 section 18. Status: PROPOSED pending M00 validation and maintainer approval. The approved four-system scope and synthetic-only boundary cannot be changed through a technology decision. Owner: project maintainer (approval), implementing engineer (assessment and proof). For each ADR capture date, alternatives, decision, consequences, validation command/results, affected requirements and commit. Keep the original identifier when changing a decision; add a revision or superseding ADR.

## 2. Original proposed decisions

### ADR-P01

Independent application boundaries. Keep four separate systems and prohibit shared domain writes. A single application with one database would reduce infrastructure effort but fail to exercise independent integration and reconciliation. Consequence: more explicit contracts, seed procedures and distributed recovery tests.

### ADR-P02

Modular hub before service extraction. Keep core financial operations in one transactional persistence boundary with separate workers. Reject premature service fragmentation; evaluate extraction after measurements reveal independent scaling or isolation needs. Consequence: module ownership must be enforced even in one process.

### ADR-P03

Python and PostgreSQL first. Prefer a familiar Python/SQL environment with transactional constraints. Java and .NET remain candidates if benchmarks or domain modelling requirements justify a change. Consequence: concurrency, exact monetary representation and transaction isolation must be demonstrated rather than presumed.

### ADR-P04

Durable at-least-once transport. Prefer outbox/inbox and stable operation IDs over claims of exactly-once message delivery. Consequence: every consumer and external adapter must specify retry and idempotency semantics; ambiguous outcomes require enquiry or hold.

### ADR-P05

Non-custodial financial boundary. Keep the insurer's receivable ledger separate from the hub's operational control journal. Consequence: settlement evidence must substantiate control postings; no claim of real custody or statutory accounting compliance.

### ADR-P06

Independent three-source reconciliation. Choose obligations/instructions, execution and settlement as the core model, with explicit subordinate payroll evidence. Consequence: simulator statements must be independent; exact MoneyHub matching internals are not required or claimed.

### ADR-P07

Analytics separate from operations. Use exported records, versioned transformations and a curated model. Consequence: analytics may lag and needs lineage and freshness metrics; financial processing does not depend on BI availability.

### ADR-P08

Real local integrations, synthetic financial rails. Use actual HTTP, broker and SFTP communication while simulating money movement and scheme rules. Consequence: tests exercise real transport behaviour without asserting bank certification or regulated activity.

### ADR-P09

AI after deterministic verification. Keep model-based assistance outside financial authority and posting. Consequence: optional models require meaningful baseline comparisons; a model can be excluded without compromising core completeness.

## 3. Technology assessment baseline

Python and SQL are the preferred direction from Document 01. The proposed core stack is Python with FastAPI for HTTP contracts, Pydantic for boundary validation, SQLAlchemy 2 and Alembic for persistence and migrations, and PostgreSQL for transactional state. Python supports exact decimal arithmetic, asynchronous I/O, testing and analytical libraries, while PostgreSQL provides transactional isolation, unique constraints and locking primitives. These choices are not claims about the actual MoneyHub implementation. Java/Spring Boot and C#/.NET remain credible alternatives; they offer mature typed enterprise ecosystems but add a separate language and tooling burden to this project. The initial choice should be tested with concurrent financial operations, replay and a representative ingestion workload before being formally approved.

RabbitMQ is the proposed first broker for durable commands, acknowledgements, routing and dead-letter handling. Kafka is an alternative where retained event streams and independent high-volume consumers are demonstrably necessary. Do not deploy both by default. PostgreSQL outbox and inbox records provide business durability independent of broker retention. Redis is not required for initial financial state and must never become an authoritative ledger or idempotency store without a separate approved design. OpenSSH SFTP provides a concrete transfer service; Python routing and transformation modules provide the ESB capabilities without requiring a proprietary ESB licence. Contract-first OpenAPI, AsyncAPI and independently versioned CSV/XML schemas provide interoperable interfaces.

Use React and TypeScript for the four operational interfaces, with a shared design library but separate routes and permissions. Keycloak or another standards-compatible OIDC provider is a candidate for identity; local test identities and integration tests must prove actual role boundaries. OpenTelemetry, Prometheus and Grafana are candidate

observability tools. For analytics, use S3-compatible object storage, Parquet, PyArrow/Polars and DuckDB for a reproducible local data platform. Start with a small incremental Python job runner and versioned SQL transformations; adopt Dagster or Airflow and dbt only if scheduling, dependency management and lineage requirements justify them. Evaluate Power BI as the reporting consumer separately from the pipeline.

The repository should contain separate applications for PAS, hub, banking and payroll, plus integration, analytics, infrastructure, contracts, test fixtures, documentation and evidence directories. Shared code is limited to contract types, observability helpers and common technical utilities; domain rules are owned by their applications. Docker Compose is the proposed local deployment with health checks, named volumes, per-service identities and reproducible seed scripts. GitHub Actions runs unit, integration, migration, security and browser verification. Use isolated test databases, real broker and SFTP integration tests, and independently generated provider evidence. A hosted environment is an optional deployment exercise rather than a dependency for local correctness. Do not claim cloud deployment or provider provisioning until verified.

Detailed architecture decision records must evaluate licensing, supported platforms, container resource use, maintenance, failure characteristics, testability and actual workloads. Version pins, dependency licences, migrations and build instructions belong in the repository. The chosen stack must run on the intended development hardware or have documented substitutes, including a route for Windows-only reporting tooling. The technology selection gate may refine frameworks without altering the agreed functional requirements.

## 4. M00 decision validation worklist

### ADR-P01 and ADR-P02: boundaries and transactional core

Compare separate logical PostgreSQL databases with separate instances; use distinct roles and explicit grants. Demonstrate one application cannot read or write another's data, including cross-database credentials. Compare modular hub with service-per-module complexity. Validate atomic posting/outbox and independent provider recovery in a thin local proof. Proposed ownership: application and platform engineering. Gate: ownership model, service identities, transactional interface and isolation test design reviewed.

### ADR-P03: Python and relational persistence

Candidate: Python, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL. Compare Java/Spring and .NET for typed modelling, operational complexity, exact arithmetic and transaction behaviour. Choose pinned supported versions after ARM64 compatibility and licence review. Prove integer minor units, exact decimal conversion, locked allocation, uniqueness and transactional rollback against real PostgreSQL. No performance claim until measured. Gate: compatibility, build, migration and representative contention probe recorded.

### ADR-P04 and ADR-P08: transport and integration

Candidate: RabbitMQ (not Kafka by default), actual OpenSSH SFTP, independent Python ESB service, HTTP/OpenAPI, AsyncAPI and versioned file contracts. Compare broker failure and delivery semantics, replay requirements, and local resource footprint. Prove confirms, redelivery, transactional outbox/inbox, partial file quarantine, transfer account isolation and status enquiry. No exactly-once transport assertion. Gate: reproducible transport proof, synthetic provider contract and recovery semantics.

### ADR-P05 and ADR-P06: financial authority

Compare operational control accounting with unsafe duplication of insurer ledger; document legal entity, currency, source-purpose identity and custody boundary. Draft chart of control accounts, posting events and approval matrix. Demonstrate worked gross/net/fee/reversal example, independent evidence and partial allocations. Gate: signed financial design review before simulated dispatch.

### ADR-P07: analytics and BI

Candidate: Python job runner, PyArrow/Polars, Parquet, S3-compatible storage, DuckDB, versioned SQL, curated reporting database. Compare local object storage implementations on licence, architecture support and reproducibility. Defer orchestration/dbt unless justified; use no operational DB direct reporting access. Evaluate Power BI licensing and Windows availability, with BI-compatible exports and browser fallback. Gate: extract contract and replay proof; explicitly record unverified Power BI runtime.

### ADR-P09: optional AI

No AI dependency in core. Compare deterministic baselines against narrowly scoped models only after trustworthy synthetic data and controls exist. Gate M21: frozen datasets, held-out periods, errors, relevant subgroup results and no financial authorisation. May defer without blocking core.

## 5. Supporting technology decisions to register after evaluation

Candidate React/TypeScript/Vite interfaces, Keycloak/OIDC, Docker Compose profiles, GitHub Actions, pytest/Hypothesis/Testcontainers, Playwright, Locust, OpenTelemetry/Prometheus/Grafana. Document actual version pins and licence status, image platform, resource limits, security defaults, build commands and test evidence. Do not enable Kafka, Redis or extra orchestrators without a decision. Cloud provider selection is deferred; local reproduction is mandatory. No probe or external validation has been executed in this bundle. The exact tool versions and supported environment remain open.

## 6. M00 assessment status

The [M00 architecture assessment](milestones/m00/M00_ARCHITECTURE_ASSESSMENT.md) records proposed dispositions and owners for ADR-P01 through ADR-P09, plus provisional decisions M00-D01 to M00-D03. The [M00 verification record](milestones/m00/M00_ARCHITECTURE_VERIFICATION.md) records passed local feasibility checks and pending runtime evidence. The original decisions remain proposed.
