# Engineering verification strategy

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Verification mandate

Source: Document 04 sections 16 and 19. All tests are planned, not run. A build is not a financial integrity result. Verify independent outcomes rather than using the implementation as the expected-results oracle. Use real PostgreSQL, broker and SFTP for critical interoperability checks; mock isolated fault boundaries only where justified. Run unit and property tests early, real integration and contract tests at every affected milestone, browser tests against persisted data, adversarial security and recovery tests before release. Explicitly report unexecuted or blocked tests.

Verification begins before the first payment workflow and continues through all milestones. Unit tests cover domain rules and transitions. Property-based tests generate monetary allocations, duplicate requests, rule changes and posting combinations. Integration tests use real PostgreSQL constraints, a real broker and local SFTP service rather than replacing all dependencies with mocks. Contract tests verify producer and consumer compatibility with independent fixtures. Browser tests verify the actual operator journeys against persisted results. Failure injection and load tests run under documented, reproducible conditions.

A scenario manifest identifies seed, input dataset, application versions, rules, calendar, fault settings and expected invariants. Each run retains a unique identifier, commit, dependency versions, execution timestamps, environment description and machine-readable results. Record passed, failed, skipped and blocked tests separately; a test skipped because infrastructure is unavailable is not a passed verification. A build or unit test alone cannot establish financial correctness across independent systems.

## 2. Mandatory scenario catalogue

### SC-01

Recurring premium cycle. Create policies with monthly obligations; submit EFT debit, DebiCheck, RM and payroll instructions through different transports. Verify authority, exact amounts, independent provider outcomes, settlement, allocation and updated PAS account. Include a payer-initiated deposit. Covers FR-001 to FR-002, FR-005 to FR-017 and FR-021 to FR-024.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-02

Duplicate and conflicting instructions. Submit concurrent equivalent messages through REST, broker and file; then reuse the identity with a materially changed amount. Prove one accepted obligation effect, one eligible execution, one posting set and an attributable conflict. Covers FR-007/008/010/020 and NFR-001.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-03

Ambiguous provider execution. Commit a provider operation then lose its acknowledgement. Crash the worker; recover via independent status enquiry or later settlement evidence. Prove no second debit and no unsafe fallback. Repeat with an unavailable status endpoint and verify hold. Covers FR-015/019/025 and NFR-002/006.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-04

Authority and schedule changes. Authenticate one mandate, reject another, amend a limit, cancel a third after scheduling and test a cut-off boundary. Verify that dispatch re-evaluates current authority and a previously submitted instruction remains traceable. Covers FR-011 to FR-014 and FR-026.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-05

Payroll discrepancy. Create two employer cycles with partial deductions and affordability rejections. Return aggregate remittance with one missing employee allocation and later bank receipt. Reconcile the remittance and retain the unresolved item without forcing balance. Covers FR-016/017/021/023/024.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-06

Claims, refunds and returns. Approve a synthetic claim, release via an independently verified beneficiary, settle, return and resolve. Attempt a duplicate and excessive refund; require separate sensitive approval. Covers FR-003/012/018/020/025/028.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-07

Settlement and allocation integrity. Exercise the Section 8 example with known fees, unknown execution and late settlement, then omit fee evidence and insert duplicates. Include partial matching, multiple obligations and a late reversal in a closed accounting period. Verify exact totals, immutable adjustments and controlled approval. Covers FR-020 to FR-025 and NFR-001/007.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-08

Integration failure and replay. Transfer a partial file, corrupt the manifest, submit an incompatible schema, stop the broker and replay a dead-letter after correction. Verify receipt state, atomic acceptance policy and no duplicate financial effect. Covers FR-005 to FR-010 and NFR-002/004.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-09

Tenant and operator controls. Use overlapping references in two tenants, attempt access through APIs, storage, exports and broker routing, and attempt self-approval. Verify rejection and attributable audit records. Covers FR-025/028/029/030 and NFR-003/011.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-10

Reporting correctness. Export a processed cycle, interrupt transformation, replay and add a late reversal. Recompute all selected measures from independent operational records; verify the same versioned cohort and stale-data display. Covers FR-031 to FR-033 and NFR-008.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-11

Extension and migration. Configure a second partner, add a simulated channel, import opening balances, run shadow processing, cut over and roll back with unresolved attempts. Compare outcomes and prove exclusive dispatch ownership. Covers FR-027/034 to FR-037 and NFR-004/006.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

### SC-12

Scale and disaster recovery. Run the approved progressive workload, interrupt dependencies, restore backups and reconcile against provider records. Capture throughput and latency distributions, financial invariants, resource use, recovery point, recovery time and residual exceptions. Covers NFR-001/002/005/006/009 and FR-037.

Status: NOT RUN. Test fixture, expected outputs and evidence path to be defined before implementation of affected capabilities.

## 3. Test layers and release rules

Unit: exact arithmetic, state guards, permissions, rules, mapping and rounding. Property: conservation, non-negative eligible allocations, repeated commands, reversal and allocation combinations. Database integration: unique source-purpose posting, balanced commit, rollback, row locking, cross-tenant negative access, migration from prior schema. Messaging and files: durable acceptance, publish/ack crash, redelivery, partial transfer, schema mismatch, content hash, quarantine and replay. Contract: independent producer/consumer fixtures and major version mismatch. E2E: four systems with real transport and authoritative records, including user-facing workflow verification. Fault and recovery: process termination pre/post commit, broker outage, lost acknowledgement, database restart, independent provider enquiry, backup restore and reconciliation before resume. Security: tenant and role denial across API, DB credentials, queues, SFTP, object store and exports. Analytics: source-to-report control totals, late events, deduplication and versioned lineage.

## 4. Proposed benchmark protocol

Use NFR-005 exactly as initial ambition: 100,000 synthetic policyholders and up to one million financial events. First run a small deterministic correctness cohort; increase gradually and document event mix, actual instructions/attempts/postings, hardware and container caps. Proposed first intake benchmark: 100 durable accepts/s for ten minutes and p95 <=500 ms; distinguish intake from provider and settlement latency. Capture p50/p95/p99, offered and accepted rate, errors/retries, CPU/RAM, DB growth, queue age and correctness invariants. Run recovery and backup scenarios separately; proposed recovery target per NFR-006 is five minutes after restoration, and NFR-008 analytical freshness target is five minutes after invocation for a small batch. Calibrate and obtain approval before treating as fixed SLOs. Do not exclude errors or skipped runs to manufacture a pass.

## 5. Evidence contract

A run manifest must identify commit, seed, input hashes, environment, dependency versions, rule and calendar versions, fault schedule, start/end UTC, expected independent results and actual outputs. Evidence should include machine-readable results, logs with secrets redacted, control totals, independent provider records, migrations and trace exports. Record precise command and exit code, tests passed/failed/skipped/blocked separately. Tie each result to FR/NFR/FI/SC and milestone. Store under `evidence/<milestone>/<run-id>/` (proposed). No actual evidence is supplied by this initial bundle.

Release blockers: any known unbalanced posting, duplicate effect, unauthorised execution, cross-tenant access, unsafe ambiguous retry, unexplained forced balancing or missing critical acceptance test. A deferred optional AI experiment is not a core blocker. A missed performance target requires explicit measured deviation and approval, not relabelling it as a pass.
