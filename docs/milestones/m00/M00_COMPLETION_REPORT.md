# M00 completion report

Revision 0.2 | 26 November 2026 | EPI 0.1.0 | Status: verification passed on GitHub Actions; maintainer acceptance pending.

## 01. Repository status

The canonical checkout is at `/Users/keenosmith/Programming/Projects/qlink-moneyhub/enterprise-payments-infrastructure` and the authoritative remote is [GitHub](https://github.com/keenosmith-del/enterprise-payments-infrastructure). The M00 baseline was pushed to `main` at `b517aba5ae1ceaa105589bafd8c6693850beabcd`. The SFTP correction was pushed at `c96725c1ca22700b7d80d74c51efb5bf6a2bfcb7`. This report records the subsequent hosted verification; the original local environment observations below remain historical.

## 02. Engineering baseline integrity

Documentation validation passed. Counts were 38 functional requirements, 11 non-functional requirements, nine original decisions, 12 scenarios, 24 milestones, 34 traceability entries, nine MoneyHub capability groups and seven unresolved questions. Four original PDF hashes matched. The original catalogue and source wording remain intact. Documentation and local Markdown link checks passed.

## 03. Development environment

Observed an Apple Silicon M5 development Mac, macOS 27.0.1, arm64, 16 GB RAM and 282 GiB available at inspection. Python 3.12.15, Python 3.15.1, Node 24.21.0, npm 11.19.0, Git 2.56.0, Docker CLI 29.8.2 and Compose 5.5.1 were inspected. Docker daemon startup, host port binding and package resolution were blocked. No successful ARM64 image run or Power BI execution was recorded. See [host and tooling findings](M00_DEVELOPMENT_ENVIRONMENT.md).

## 04. Technology assessment

The [technology selection](M00_TECHNOLOGY_SELECTION.md) recommends Python and PostgreSQL for the transactional core, RabbitMQ and OpenSSH SFTP for local integration, React/TypeScript for independent interfaces, Keycloak for OIDC, and Parquet and curated SQL for analytical reporting. The assessment records alternatives, licences, compatibility checks, resource assumptions and adoption gates. Version candidates remain provisional until an actual dependency and image run. Kafka, Redis, extra orchestration and a hosted platform are deferred.

## 05. Architectural decisions

The [architecture assessment](M00_ARCHITECTURE_ASSESSMENT.md) assesses ADR-P01 through ADR-P09 and proposes M00-D01 to M00-D03 with owners and approval conditions. Four independently persisted business systems retain their separate authorities. The modular Hub has one financial consistency boundary and independent workers. ESB, messaging, SFTP, data engineering and reporting are shared infrastructure. Material decisions remain pending formal review.

## 06. Financial design

The [financial contract baseline](M00_FINANCIAL_CONTRACT_BASELINE.md) defines preliminary identities, monetary representation, exact posting, scope and maker/checker controls, independent status enquiry, settlement, allocations and reversals. It includes ten worked examples. Finance review remains open on control chart, rounding, fees and adjustment periods. No business feature, application migration or dispatch is in this milestone.

## 07. Verification evidence

The [successful GitHub Actions run](https://github.com/keenosmith-del/enterprise-payments-infrastructure/actions/runs/45741263995) tested correction commit `c96725c1ca22700b7d80d74c51efb5bf6a2bfcb7`. Baseline validation and Python compilation passed; the local probe suite ran three tests with zero failures and zero skips. The services job ran three infrastructure tests with zero failures and zero skips, including the PostgreSQL, RabbitMQ and Parquet probes. The networked SFTP job passed public-key authentication, host verification, transfer, directory separation and its negative checks. All three jobs exited successfully. The local `bash scripts/m00/probe_sftp_ssh.sh` attempt exited 1 because the Docker daemon was unavailable; it is not counted as a pass. The hosted Linux run does not establish an ARM64 image run or Power BI execution. See [verification and reproduction](M00_ARCHITECTURE_VERIFICATION.md) and [original local output](../../../evidence/m00/local-verification.txt).

## 08. GitHub Actions

The [first run](https://github.com/keenosmith-del/enterprise-payments-infrastructure/actions/runs/45739210577) passed baseline and services but failed networked SFTP because StrictModes rejected the ownership of the bind-mounted authorised key. The correction mounts generated keys read-only at `/probe-keys-input`, then copies the host private key and authorised public keys into root-owned `/probe-keys` with modes 0600 and 0644 respectively; the directory is 0755. StrictModes, host verification, public-key authentication, chroot isolation and negative tests remain in place. The replacement run linked above passed baseline, services and networked-sftp. GitHub reported a Node.js 20 deprecation annotation for the pinned checkout action; the runner used Node.js 24 and the jobs passed.

## 09. Documentation

Added seven M00 specifications and reports, reproducible probes, evidence and workflow. Updated README, AGENTS.md, changelog and the documentation register. The documentation register links the work to original Volume 02 and Volume 03 topics without renumbering the five-volume programme. The architecture and financial specifications link controls to requirements, baseline decisions, invariants and scenario IDs.

## 10. Milestone 01 readiness

The [M01 preparation](M00_M01_IMPLEMENTATION_PREPARATION.md) describes the application paths, dependency and migration plans, health and security expectations, test scope and prerequisites. Implementation remains gated on resolving design approvals, obtaining M00 acceptance, then receiving separate M01 authorisation.

## 11. Final delivery status

The M00 verification workflow passed on the correction commit. This report update follows that run and triggers a fresh workflow on its own commit. Formal design and finance reviews and maintainer acceptance remain open; M01 requires separate authorisation. No M01 implementation was started. No application migrations or production deployment were performed.
