# Implementation roadmap and milestone gates

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Delivery rules

Source: Document 04 section 20. Preserve M00-M23 and their original gates. At the original baseline all milestones were unstarted and M00 was in preparation. The current execution status appears in the M01 foundation update below. Dependency order is sequential by default; parallel documentation or isolated probes may proceed only where no unresolved dependency exists. No feature code before its specification; no simulated dispatch before M02, M04-M06 and applicable authority, accounting and independent evidence gates. All milestone PRs require scope, explicit requirement IDs, test plan, actual verification, migration/recovery implications, evidence and approval before merging. Financial and security controls are continuous.

## 2. Original milestone catalogue

### M00

Discovery and design baseline. Approve Documents 01 to 04 with recorded gaps, establish the requirements, assumptions and decision registers, finalise the detailed architecture and financial contracts necessary for the initial slice. Gate: traceability crosswalk reviewed; unresolved decisions have an owner and approval condition.

Status: ACCEPTED for M01 foundation implementation by the maintainer.

### M01

Foundation. Create repository boundaries, pinned dependencies, local Compose environment, CI, separate databases, identity skeleton and test fixtures. Gate: clean build, migration, seed, smoke tests and verified separation of service credentials.

Status: IN PROGRESS. Dependency: M00 accepted. Final M01 acceptance depends on the recorded verification and maintainer review.

### M02

Financial model and persistence. Implement canonical identities, exact monetary representation, event provenance, transaction constraints, journal posting primitive and outbox/inbox foundation. Gate: balance, concurrency and duplicate tests pass before external money movement is enabled.

Status: NOT STARTED. Dependency: M01 accepted, unless a documented dependency review approves independent work.

### M03

PAS vertical slice. Implement policy and product versions, billing obligations, claims approval and financial result intake. Gate: independent bill run, adjustment and idempotent consumption, with no reliance on the hub's database.

Status: NOT STARTED. Dependency: M02 accepted, unless a documented dependency review approves independent work.

### M04

Integration gateway. Implement canonical contracts, REST, durable messaging and actual SFTP exchange with receipts. Gate: cross-transport equivalence, partial-file, duplicate and broker recovery tests.

Status: NOT STARTED. Dependency: M03 accepted, unless a documented dependency review approves independent work.

### M05

Mandate and beneficiary controls. Implement channel-specific authority, versions, approvals and sensitive identity changes. Gate: negative authorisation and lifecycle cases pass.

Status: NOT STARTED. Dependency: M04 accepted, unless a documented dependency review approves independent work.

### M06

Banking simulator and adapter. Implement independent provider records, simulated accounts, authority outcomes, status enquiry and settlement generation. Gate: provider idempotency, lost acknowledgement and independent statement evidence.

Status: NOT STARTED. Dependency: M05 accepted, unless a documented dependency review approves independent work.

### M07

Collections engine. Implement scheduling, attempt identity, route eligibility, amount reservation and bank collection processing. Gate: first complete bill-to-reconciled-result vertical slice using the minimal journal and reconciliation primitives; no unsafe resubmission.

Status: NOT STARTED. Dependency: M06 accepted, unless a documented dependency review approves independent work.

### M08

Payroll simulator and collections. Implement employer configuration, authority, deduction and remittance contracts. Gate: partial deduction, affordability and aggregated remittance evidence.

Status: NOT STARTED. Dependency: M07 accepted, unless a documented dependency review approves independent work.

### M09

Disbursements. Implement approved claims and refund execution, beneficiary checks and return handling. Gate: authorised credit, duplicate rejection and controlled return recovery.

Status: NOT STARTED. Dependency: M08 accepted, unless a documented dependency review approves independent work.

### M10

Ledger and accounting controls. Complete the dedicated ledger design, operational control accounts, posting policy, reversal and period controls. Gate: immutable balanced entries, source-purpose uniqueness and independent reconciliation of journal totals. The primitive introduced in M02 remains mandatory throughout.

Status: NOT STARTED. Dependency: M09 accepted, unless a documented dependency review approves independent work.

### M11

Settlement management. Complete independent statement and settlement batch import, gross/net fees, revisions and delayed evidence. Gate: execution and settlement states remain separate.

Status: NOT STARTED. Dependency: M10 accepted, unless a documented dependency review approves independent work.

### M12

Reconciliation and allocation. Complete three-way reconciliation, partial and aggregate matching, exceptions and return-to-PAS results. Gate: worked cases and property-based allocation controls pass with independent sources.

Status: NOT STARTED. Dependency: M11 accepted, unless a documented dependency review approves independent work.

### M13

Configurable rules. Implement versioned declarative policies, approval and evaluation trace. Gate: historical reproducibility and safe rule changes, with simulation isolated from dispatch.

Status: NOT STARTED. Dependency: M12 accepted, unless a documented dependency review approves independent work.

### M14

Operational exceptions and recovery. Complete case workflow, enquiry, approved correction, replay and support procedures. Gate: crash, retry, late-result and contradictory evidence scenarios pass.

Status: NOT STARTED. Dependency: M13 accepted, unless a documented dependency review approves independent work.

### M15

Operational interfaces. Complete four independent application experiences and inspection workflows. Gate: browser-tested end-to-end journeys using actual backend data.

Status: NOT STARTED. Dependency: M14 accepted, unless a documented dependency review approves independent work.

### M16

Security and governance assessment. Deepen tenant isolation, least privilege, threat modelling, audit, secret handling and negative tests. Gate: no unresolved critical security defect. Baseline access and integrity controls remain in all earlier milestones.

Status: NOT STARTED. Dependency: M15 accepted, unless a documented dependency review approves independent work.

### M17

Data engineering and reporting. Complete operational metrics, incremental exports, data lake, lineage and curated BI model. Gate: source-to-report reconciliation and pipeline recovery, with Power BI execution status recorded.

Status: NOT STARTED. Dependency: M16 accepted, unless a documented dependency review approves independent work.

### M18

Legacy migration and enterprise onboarding. Implement import, shadow runs, cutover, rollback and partner certification. Gate: exclusive execution, opening balance verification and traceable acceptance evidence.

Status: NOT STARTED. Dependency: M17 accepted, unless a documented dependency review approves independent work.

### M19

Payment and value-added service extension. Add selected simulated instant credit, request-to-pay and service adapter capabilities. Gate: new integration works without regressions or changes to unrelated core logic.

Status: NOT STARTED. Dependency: M18 accepted, unless a documented dependency review approves independent work.

### M20

Reliability, performance and recovery. Run the approved load and disaster recovery programme, tune measured bottlenecks and retain results. Gate: financial correctness maintained under workload and faults; quantitative target deviations explicitly reviewed.

Status: NOT STARTED. Dependency: M19 accepted, unless a documented dependency review approves independent work.

### M21

Optional AI feasibility. Evaluate narrow intelligence use cases only after reliable curated data is available. Gate: baseline comparison, evidence of improvement and non-authoritative decision support, or documented deferral.

Status: NOT STARTED. Dependency: M20 accepted, unless a documented dependency review approves independent work.

### M22

Independent engineering review. Inspect code, contracts, security, financial correctness, performance and evidence; remediate findings. Gate: reproducible independent review with remaining limitations and risks explicitly recorded.

Status: NOT STARTED. Dependency: M21 accepted, unless a documented dependency review approves independent work.

### M23

Final delivery. Complete release package, local runbook, verified demonstration, final technical and executive documentation, portfolio case study and walkthrough materials. Gate: a separate engineer can reproduce and inspect the claimed results. Hosted deployment is recorded as verified, deferred or blocked, not assumed.

Status: NOT STARTED. Dependency: M22 accepted, unless a documented dependency review approves independent work.

## 3. M00 work package (next action)

1. Confirm the approved discovery PDF hashes and stable IDs with `python3 scripts/validate_baseline.py`. Review each crosswalk and record exceptions.
2. Establish repository and canonical local checkout for documentation and isolated feasibility probes only. No scaffold is represented as functioning financial software. Record actual hardware, OS/architecture, available RAM/storage, Docker and Git versions, supported dependency versions and licensing.
3. Resolve ADR-P01 through P09 for the initial architecture. Evaluate actual PostgreSQL, RabbitMQ and SFTP interoperability and local resource use; record failed or skipped checks. Confirm identity and independent credentials. Power BI and cloud deployment remain explicit feasibility work, not blockers to core local correctness unless scope changes.
4. Draft the detailed Volume 02 business/functional/non-functional specifications, initial architecture, financial identities and authority/ledger rules needed for the foundation and first slice. Freeze test fixture expectations and contract versioning; approve dependent specifications before each later milestone. Preserve original FR/NFR identifiers and explicit owners.
5. Produce M01 Codex instructions after M00 review. Define exact scope, paths, dependency pins, health checks, CI, negative credential tests, migration/seed procedures, acceptance evidence and rollback. Do not claim an M00 pass based on this bundle alone.
6. Maintainer approves the selected stack and M00 exit record, including unresolved decisions with responsible owner and blocking condition. Then authorise M01.

## 4. First financial vertical slice (M02-M07)

The early slice proves a real PAS obligation through ESB intake, mandate validation, independent simulated bank execution, separate settlement, matched allocation and PAS acknowledgement. M02 provides journal primitive and idempotency before any dispatch; M03 creates the obligation; M04 transports equivalent commands; M05 authority; M06 independent bank; M07 collections and minimal reconciliation. Test normal success, duplicate submissions, lost acknowledgement, mandate revocation and independent statement evidence. Complete detailed ledger and reconciliation capabilities at M10-M12 without weakening earlier invariants. Payroll, claims and data engineering remain required at their original milestones.

## 5. Milestone record template

Milestone ID and title; baseline revision; authorised scope; explicit exclusions; dependencies and reviewed specifications; linked FR/NFR/FI/ADR/SC; paths changed; migration and backward compatibility; test commands and actual pass/fail/skip/blocked counts; evidence files and commit; unresolved risks; release gate decision; approval date and owner. Do not proceed past a failed financial or security gate. A hosted deployment blocker is distinct from local verification; record both honestly.

## 6. M00 execution status

The [M00 completion report](milestones/m00/M00_COMPLETION_REPORT.md) records historical local blockers and subsequent hosted verification. The maintainer accepted M00 for foundation implementation and authorized M01. The [M01 preparation](milestones/m00/M00_M01_IMPLEMENTATION_PREPARATION.md) records foundation sequencing and proof obligations.

## 7. M01 foundation execution

The maintainer accepted M00 for M01 on 26 November 2026. M01 implementation and evidence are recorded in the [M01 report](milestones/m01/M01_IMPLEMENTATION_REPORT.md) and [completion report](milestones/m01/M01_COMPLETION_REPORT.md). M02 remains unstarted and requires explicit authorization. Financial policy choices concerning fees, rounding, control accounts, settlement adjustments and accounting periods remain gates for their dependent work.
