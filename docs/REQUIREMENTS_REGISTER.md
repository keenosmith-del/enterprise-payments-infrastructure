# Master requirements register

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Register conventions

Source: Document 04 sections 15-17. The catalogue below retains the parent IDs, source wording and acceptance criteria (PDF line wrapping normalised). All entries are approved as scope baseline, not implemented or verified. C, E and O are preserved from the source. Owners are the system(s) specified in the entries; NFRs apply to all relevant components, with detailed owners to be assigned at design. Acceptance evidence status for every entry is NOT RUN; no test path or commit has yet been assigned. Each implementation PR must add requirement-linked test locations and results; use a child identifier for extra detail. The crosswalk preserves namespaces and avoids the previous MH identifier collision.

## 2. Functional requirements

### FR-001

Policy and product administration (C; PAS). Maintain synthetic policyholder, beneficiary, product, policy and effective-dated coverage records. Support creation, amendment, cancellation and reinstatement under explicit configurable rules. Acceptance: independently create a policy, change a product prospectively, and demonstrate that a historical bill retains its original product and coverage context.

### FR-002

Premium obligations and billing cycles (C; PAS). Generate unique, immutable premium obligations per policy and billing period; support adjustments and recurring schedules. Maintain receivable and account history. Acceptance: rerun a bill cycle concurrently and show one obligation per eligible policy and period; demonstrate a backdated adjustment without mutation of the prior obligation.

### FR-003

Claims and refunds (C; PAS, hub). Manage synthetic claims approvals and eligible refund authorisations with amount limits and stable payable references. The PAS originates approved payables; the hub must not create an insurance entitlement. Acceptance: reject unapproved claims, duplicate approvals and excess refunds; execute an approved payment and reconcile a returned payment without losing the payable history.

### FR-004

Financial result consumption (C; PAS). Receive immutable payment, allocation and reversal events, validate the referenced obligation, apply once and acknowledge consumption. Separate arrears and grace policy decisions from collection failures. Acceptance: deliver an allocation twice, then a late reversal; demonstrate correct outstanding amount and documented policy-state decisions, including an unknown obligation quarantine.

### FR-005

Canonical instruction intake (C; hub, integration). Accept versioned collection and disbursement commands, retain source provenance, validate canonical fields and issue durable receipts. Acceptance: equivalent API and batch inputs create the same domain representation; invalid amount, currency or tenant claims are rejected without dispatch.

### FR-006

REST integration (C; integration, all systems). Provide independently documented inbound and outbound APIs with scoped authentication, stable source IDs, receipt/status enquiry and compatible schema evolution. Acceptance: run positive, malformed, unauthenticated, duplicate and incompatible-version contract tests across at least two independent application boundaries.

### FR-007

Message integration (C; integration, all systems). Implement durable commands and events, transactional outbox/inbox, acknowledgement, bounded retry and quarantined failure handling. Acceptance: stop the broker, restart relay and consumer, duplicate delivery and reorder events; demonstrate eventual delivery of eligible commands without duplicate effects or stale state replacement.

### FR-008

Secure file exchange (C; integration). Operate a real SFTP exchange with segregated partner accounts, manifest validation, atomic file readiness, controlled imports, acknowledgement and outcome exports. Acceptance: exchange a valid batch end to end; test partial upload, invalid digest, total mismatch, malformed record, duplicate file and changed duplicate; verify exactly which records were accepted or rejected.

### FR-009

Enterprise adapter and mapping framework (C; integration, hub). Provide versioned transport and provider mappings, canonical error taxonomy and capability declarations. Preserve raw external codes and source records. Acceptance: add a second synthetic provider using a different schema; run the same financial contract tests without changing the core collections state model.

### FR-010

Instruction and attempt identity (C; hub). Enforce stable source IDs, material payload comparison, separate attempt identities and durable provider operation references across transports. Acceptance: send the same instruction concurrently through REST and SFTP; one instruction is accepted and only one eligible financial execution occurs. Reuse its identity with changed amount and confirm a conflict without execution.

### FR-011

Mandate lifecycle (C; hub, bank/payroll). Maintain channel-specific authority, external references, authentication evidence, effective dates, amendment, revocation and expiration. Acceptance: exercise authenticated, rejected, expired, amended and revoked authority; no new attempt may dispatch under invalid or superseded terms.

### FR-012

Account and beneficiary management (C; hub, bank). Verify synthetic account references and manage effective-dated beneficiary records with controlled changes. Treat verification as distinct from consent. Acceptance: reject a mismatched or unapproved beneficiary version, prevent self-approval of sensitive changes and demonstrate that verified account status alone cannot authorise a deduction.

### FR-013

Scheduling and channel selection (C; hub). Evaluate business dates, cut-offs, amount constraints, permitted channel, attempt limits and rule version before dispatch. Acceptance: test holiday/cut-off boundaries, cancelled mandates, in-flight amount reservations and an authorised alternative channel; unresolved earlier execution prevents fallback.

### FR-014

Bank collections (C; hub, bank). Process once-off and recurring EFT debit, DebiCheck and Registered Mandate collections using distinct simulated authorisation and outcome contracts. Acceptance: independently execute a full, partial, unpaid and returned collection; each channel rejects invalid authority under its own rules and produces a provider-side record.

### FR-015

Banking and payment simulation (C; bank). Maintain independent account balances, mandate responses, provider operations, outcome enquiry, statement and settlement generation. Acceptance: prove bank evidence is generated from independent persisted execution; inject delayed, duplicate, lost, conflicting and returned outcomes while preserving provider accounting and duplicate controls.

### FR-016

Payroll administration and deductions (C; payroll). Represent employer configuration, employee references, authority, payroll cycle, eligible deduction capacity and deduction/remittance history. Acceptance: process two employers with different file mappings and cut-offs, including termination, partial deductions, affordability rejection and cycle closure; no fictitious HR system is required.

### FR-017

Payroll collection integration (C; hub, payroll). Submit eligible salary deductions, process item results and remittances and distinguish acceptance, actual deduction and bank receipt. Acceptance: reconcile an aggregated remittance with constituent deductions, identify a missing remittance and trace a corrected remittance without repeated allocation.

### FR-018

Outbound disbursements (C; hub, bank). Process approved claims and refunds as synthetic EFT credits, support applicable batch windows and track returns. Acceptance: submit a valid approved payable, reject duplicate and insufficient approval, independently observe settlement and account for a return before authorised replacement.

### FR-019

Transaction outcome and recovery (C; hub, providers). Record independent execution, settlement and allocation states; handle ambiguity through enquiry and late evidence. Acceptance: interrupt a worker before commit, after local commit, and after provider execution before acknowledgement; recover without losing an instruction or producing another financial movement. Unresolvable status remains on hold.

### FR-020

Immutable financial-control journal (C; hub, PAS). Enforce balanced exact-value postings, unique source-purpose keys, authorisation, immutable posting and compensating correction. Respect separate PAS and non-custodial hub accounting boundaries. Acceptance: property-based and concurrent tests prove zero posted imbalances, duplicate postings and unauthorised mutations; reversals and closed-period adjustments remain independently traceable.

### FR-021

Settlement ingestion and tracking (C; hub, bank/payroll). Import independent settlement, statement and remittance evidence with batches, item references, gross/net values, fees and dates. Acceptance: process delayed, duplicated and revised files; retain the original records and prove that a reported execution success is not automatically treated as settled.

### FR-022

Payment and cash-deposit matching (C; hub). Match known references and eligible deterministic candidates; support unidentified deposits, partial receipts and ambiguous cases. Acceptance: match a referenced deposit, hold a duplicate-amount ambiguous deposit, resolve a reviewed match and prevent allocation over the available balance.

### FR-023

Three-way reconciliation (C; hub). Compare obligations/instructions, execution results and independent settlement evidence, including aggregate and partial matching, fees, late results and returns. Acceptance: reproduce the worked control totals from independent datasets; introduce a missing fee, duplicated settlement, delayed receipt and conflicting reference; every discrepancy is explained or retained as an unresolved exception.

### FR-024

Allocation and result delivery (C; hub, PAS). Allocate only eligible matched funds, retain posting and source links, issue immutable results and await consumer receipt. Acceptance: apply one receipt across multiple obligations and multiple receipts to one obligation, reject over-allocation under concurrent workers, and demonstrate late reversal and repeated delivery without a second PAS effect.

### FR-025

Exception management and correction (C; hub). Create actionable cases from validation, execution and reconciliation failures, with assignment, status, reason, evidence, approvals and correction history. Acceptance: resolve an ambiguous candidate through authorised review, reject self-approval and reproduce the original and corrected financial views. Never delete discrepancies to achieve a balanced report.

### FR-026

Versioned business rules (C; hub, PAS). Define and evaluate restricted declarative policies for processing, schedules, approvals and product integration. Rules must not override financial or authority invariants. Acceptance: activate a future-dated version, reproduce a prior decision, reject an invalid rule and prove the result records inputs and rule version.

### FR-027

Rules simulation and optimisation (E; hub). Compare prospective collection rules against a frozen synthetic cohort with measurable eligibility, collections, returns and cost indicators. Acceptance: publish reproducible baseline and candidate results with control totals, identify adverse cases and demonstrate no live-mode execution from the simulation environment.

### FR-028

Tenant and identity administration (C; all systems). Configure enterprise tenants, legal entities, users, service identities, roles and partner permissions. Acceptance: use two tenants with overlapping external references; negative tests prove cross-tenant reads, writes, exports, object access and processing are rejected. Verify distinct maker and approver principals.

### FR-029

Audit and evidence inspection (C; all systems). Record source receipts, material decisions, actor identities, approvals and historical changes and support authorised evidence exports. Acceptance: independently reconstruct an instruction from obligation through provider execution, settlement, journal and allocation, including a correction; verify exported hashes and access boundaries.

### FR-030

Operational user interfaces (C; all systems). Expose role-appropriate business actions, accurate states, transaction inspection and system administration. Acceptance: browser tests execute a complete bill-to-allocation and claim-to-settlement journey, including a failure case; all displayed amounts originate from persisted records and restricted actions are enforced by the backend.

### FR-031

Operational reporting and metric definitions (C; hub, PAS). Publish financial and operational metrics from actual processed records with explicit grain, period, denominator and freshness. Acceptance: independently recompute expected, collected, settled, outstanding, returned and allocated values from source records; pending and unknown are not counted as successful.

### FR-032

Analytical exports and data lake (E; analytics). Extract committed records to immutable raw objects, transform validated and business-ready Parquet datasets, preserve manifests, lineage and checkpoints. Acceptance: interrupt and rerun a pipeline, replay duplicate exports and ingest a late reversal; the resulting aggregates match independent source queries and no pipeline failure alters operational state.

### FR-033

Business intelligence model (E; analytics). Provide a documented semantic model, analytical measures and role-appropriate reports, including Power BI integration subject to supported environment and licensing. Acceptance: reproduce report values from the curated dataset, verify drill-through and freshness, and record actual Power BI execution or its explicit environment blocker with a working alternative reporting path.

### FR-034

Partner onboarding and integration certification (E; integration). Configure a new representative partner through credentials, mappings, contracts, validation and test exchange. Acceptance: onboard a second synthetic insurer or integration profile without a core-code fork, pass its compatibility suite and document activation and rollback.

### FR-035

Digital services and payment expansion (E; hub, bank). Extend the adapter model with simulated instant credit and request-to-pay flows and a documented value-added service such as account verification. Acceptance: execute each supported new flow with separate authority, outcome and settlement semantics, verify unsupported capability rejection and run regression tests for baseline channels.

### FR-036

Legacy migration and shadow processing (E; PAS, hub, integration). Import historical obligations and authority references, compare parallel decisions without financial execution, enforce exclusive cutover ownership and support safe rollback. Acceptance: reconcile imported opening balances, prove shadow mode cannot dispatch, verify one owner at cutover and resolve prior submitted operations before rollback routing resumes.

### FR-037

Replay and engineering evidence environment (E; all systems). Provide deterministic scenario seeds, fault schedules, receipt lineage, controlled replay and downloadable machine-readable evidence. Acceptance: reproduce an incident from captured inputs and rule versions in an isolated environment and prove replay does not change the original financial records or create repeated external effects.

### FR-038

Optional intelligence evaluation (O; analytics). Evaluate one or two narrowly scoped models for prediction, anomaly detection or matching assistance. Acceptance: use held-out synthetic periods, compare against deterministic baselines, report errors, coverage and relevant subgroup outcomes; no model may autonomously authorise, execute or post a financial operation. If not pursued, record the decision without blocking core acceptance.

## 3. Non-functional requirements

### NFR-001

Financial integrity. Zero unbalanced posted journals, duplicate financial effects, unauthorised execution and over-allocation across the defined correctness suite, including concurrent workloads and replay. Assert database constraints, source-to-posting counts and independent provider records. Any failure is a release blocker.

### NFR-002

Durability and delivery. No loss of durably accepted instructions within the tested process-crash and broker-outage scenarios. Deliver eligible work after recovery, or retain an explicit unresolved/quarantined state. Measure recovery time from fault removal to resumed processing and backlog clearance. Full disaster recovery is separately tested; the durability requirement does not imply zero loss after an untested storage catastrophe.

### NFR-003

Isolation and authorisation. Zero successful unauthorised operations in the defined negative test suite. Enforce role and tenant boundaries for API, broker, file, database, object storage and BI interfaces; include privileged actions and stale or conflicting authority. Critical unresolved security findings block release.

### NFR-004

Interoperability. All published core API, event and file fixtures pass schema, version, negative and cross-transport equivalence tests. An unsupported version results in an attributable rejection or quarantine. Connector change must not alter unrelated transaction outcomes.

### NFR-005

Scale and repeatability. Preserve Document 01's target dataset of 100,000 synthetic policyholders and up to one million financial events. Define event mix, number of actual instructions, attempts and postings separately; count only committed or independently observed operations. Complete a smaller correctness cohort first, then progressively increase load. Report throughput, p50/p95/p99 latency, error counts, database growth, CPU/memory and recovery. Proposed first benchmark: sustained 100 accepted instructions per second for ten minutes with p95 durable intake latency at or below 500 ms on documented hardware, excluding provider settlement latency. These numbers require calibration and approval before becoming fixed service objectives.

### NFR-006

Availability and recovery. Demonstrate recovery from worker termination, unavailable broker, unavailable provider, delayed file and database restart. Proposed local recovery target: resume eligible worker processing within five minutes of dependency restoration, subject to measured environment conditions. Demonstrate database and evidence-store backup/restore, record actual recovery point and recovery time, and reconcile independent provider effects before enabling dispatch. Do not claim high availability from a single-host Compose environment.

### NFR-007

Auditability and explainability. Every accepted financial instruction retains source identity and evidence; every dispatch, posting, rule decision and manual correction is attributable. Produce a trace export covering all records involved in selected scenarios. Verify that source references, monetary totals and timestamps can be independently followed without requiring developer-only database access.

### NFR-008

Analytical integrity. Reconcile all published financial measures to versioned source snapshots for the defined cohort; late events and duplicate imports must not distort totals. Show last successful publication time and explicit stale-data warnings. Proposed local freshness objective: a completed small batch appears in the analytical layer within five minutes of pipeline invocation, not a claim of continuous real-time processing.

### NFR-009

Maintainability and reproducibility. A clean checkout with documented prerequisites must build, migrate, seed and run the core ecosystem. CI executes the same critical verification used locally. Keep versioned schemas, migrations, dependency pins, configuration examples and a documented upgrade path. No secret, proprietary asset or real customer record may be required for reproduction.

### NFR-010

Operational and interface quality. Provide meaningful errors, accessible keyboard navigation, labelled controls, readable transaction detail and actionable operational status. Test key workflows at supported desktop viewport sizes; avoid client-side monetary calculations as the authoritative source. Operator recovery procedures must be documented and exercised.

### NFR-011

Data protection and compliance boundaries. Use synthetic identities only; enforce least privilege, retention, secret handling, redaction and controlled exports. Complete a threat model and data inventory. Evidence must state that the simulation is not licensed, certified, connected to live payment rails or verified for production compliance. Review current legal obligations separately before any commercial use.

## 4. Document 02 consolidated capability definitions

### D02.MH-01

Financial and PAS integration. Connect to an existing policy administration system and financial environment. Interpret as separate inbound instructions and outbound financial results.

### D02.MH-02

External interface abstraction. Absorb bank-interface changes outside client business logic. Interpret as replaceable protocol and payment-channel adapters.

### D02.MH-03

Collections and disbursements. Manage inbound and outbound money movement. Interpret as separate instruction types with shared control and settlement mechanisms.

### D02.MH-04

Mandates. Support payment authorisation management. Interpret as a distinct lifecycle with channel-specific validation.

### D02.MH-05

Matching. Automate allocation of payments and cash deposits. Interpret as deterministic matching supported by controlled exception review.

### D02.MH-06

Three-way reconciliation. Reconcile receipts and disbursements. The precise three sources and algorithms are not disclosed; define a defensible independent model.

### D02.MH-07

Configurable automation and product change. Enable trigger-driven actions and changes to financial products. Interpret as versioned configuration with controlled activation.

### D02.MH-08

Transaction insight and data usage. Make financial activity visible and useful for operational decisions. Interpret as traceable reporting and transaction-level inspection.

### D02.MH-09

Digital value-added services. Accommodate additional services around payments. Specific integrations are unresolved; investigate an extensible adapter framework.

These groups will be expanded into atomic requirements in Document 04. A claim of full proprietary feature parity is not supported by the available public material.

## 5. Cross-document traceability (Document 04 section 17)

### INIT.MH-01

Financial system integration. D02.MH-01; FR-005 to FR-009, FR-020, FR-024. Financial intake, accounting and outbound results.

### INIT.MH-02

Policy administration integration. D02.MH-01; FR-001 to FR-006, FR-024. Independent PAS obligations and result consumption.

### INIT.MH-03

External banking interface abstraction. D02.MH-02; FR-009, FR-015, FR-034, FR-035. Replaceable provider contracts.

### INIT.MH-04

Collections management. D02.MH-03; FR-010, FR-013 to FR-017, FR-019. Bank and payroll collections.

### INIT.MH-05

Disbursement management. D02.MH-03; FR-003, FR-012, FR-018, FR-019. Approved claims and refunds.

### INIT.MH-06

Automated payment matching. D02.MH-05; FR-022, FR-024. Deterministic matching and allocation.

### INIT.MH-07

Cash-deposit matching. D02.MH-05; FR-015, FR-021, FR-022. Independent deposit evidence and unresolved cash.

### INIT.MH-08

Three-way reconciliation. D02.MH-06; FR-020, FR-021, FR-023 to FR-025. Financial control and exception resolution.

### INIT.MH-09

Configurable automation. D02.MH-07; FR-013, FR-026, FR-027. Versioned processing rules and simulation.

### INIT.MH-10

Mandate management. D02.MH-04; FR-011, FR-012, FR-014, FR-016. Distinct authorisation models.

### INIT.MH-11

Data-driven decision-making. D02.MH-08; FR-027, FR-031 to FR-033; optionally FR-038. Verified analytics without requiring AI.

### INIT.MH-12

Rapid product changes. D02.MH-07; FR-001, FR-002, FR-026, FR-027. Effective-dated product and processing policy changes.

### INIT.MH-13

Transaction visibility. D02.MH-08; FR-019, FR-025, FR-029 to FR-033. Traceable state and reporting.

### INIT.MH-14

Digital value-added services. D02.MH-09; FR-009, FR-012, FR-034, FR-035. Independent integration and service expansion; actual proprietary service details remain unresolved.

### D02.BASE-01

Integration and abstraction. D02.MH-01/02; FR-005 to FR-010, FR-034; NFR-004. Equivalent outcomes across transport mechanisms.

### D02.BASE-02

Payment processing. D02.MH-03/04; FR-003, FR-010 to FR-019; NFR-001/002. Authority, execution and recovery.

### D02.BASE-03

Financial correctness. D02.MH-05/06; FR-020 to FR-025; NFR-001/007. Matching and independent settlement evidence.

### D02.BASE-04

Configurable operations. D02.MH-07; FR-026/027; NFR-003/007. Controlled activation and historical reproducibility.

### D02.BASE-05

Insight and extensibility. D02.MH-08/09; FR-029 to FR-035; NFR-004/008. Traceable metrics and adapter extension.

### D02.EXT-01

Enterprise delivery. FR-034/036; NFR-002/004. Import, parallel evaluation and controlled cutover.

### D02.EXT-02

Engineering assurance. FR-029/037; NFR-001 to NFR-010. Evidence, replay, monitoring and performance.

### D02.EXT-03

Financial intelligence. FR-038; optional, contingent on verified controls and data quality.

### D03.DOM-01

Separate obligations, authority and attempts. FR-002, FR-005, FR-010, FR-011, FR-019; NFR-001. Verify domain ownership and negative authority cases.

### D03.DOM-02

Distinct EFT debit, DebiCheck, RM and payroll. FR-011, FR-014 to FR-017. Independent channel contracts and tests.

### D03.DOM-03

Approved credit payments and refunds. FR-003, FR-012, FR-018. Approval and refund limits.

### D03.DOM-04

Distinct outcome, settlement and allocation. FR-019, FR-021, FR-024. Delayed and conflicting observations.

### D03.DOM-05

Exact amounts and immutable balanced postings. FR-020; NFR-001. Constraints, reversals and replay.

### D03.DOM-06

Three-way reconciliation, net settlement and partial receipts. FR-021 to FR-025. Reproducible control totals and exceptions.

### D03.DOM-07

REST, messaging and SFTP. FR-005 to FR-010; NFR-004. End-to-end contract and batch tests.

### D03.DOM-08

Tenant, account and approval boundaries. FR-011/012, FR-025, FR-028/029; NFR-003/011. Negative access and segregation tests.

### D03.DOM-09

Controlled recovery from ambiguity. FR-010, FR-015, FR-019, FR-037; NFR-002/006. Lost acknowledgement and crash scenarios.

### D03.DOM-10

Arrears and grace handling. FR-001/002/004. Policy lifecycle remains independent of a failed deduction.

### D03.DOM-11

Analytical export and lineage. FR-029, FR-031 to FR-033; NFR-008. Source-to-report checks.

### D03.DOM-12

Migration, extension and authorised rule changes. FR-026/027, FR-034 to FR-036; NFR-003/004. Simulation, cutover and rollback tests.

## 6. Original source definitions for baseline, extensions and domain obligations

The following preserve the original Document 02 section 21 and Document 03 section 21 wording independently of the abbreviated crosswalk. Classification D = documented; E = ecosystem evidence; I = interpretation; P = proposed. These classification letters are distinct from the C/E/O release priorities.

**D02.BASE-01 (original definition).** Integration and abstraction (D). MH-01 and MH-02. Demonstrate a representative PAS exchanging instructions and results through lab-owned contracts. Verify equivalent outcomes across API and file transports.

**D02.BASE-02 (original definition).** Payment processing (D/E). MH-03 and MH-04. Cover collections, disbursements, mandates and relevant bank and payroll channel workflows. Verify repeated and ambiguous submissions, authorisation changes and failed transactions.

**D02.BASE-03 (original definition).** Financial correctness (D/I). MH-05 and MH-06. Implement payment matching and an independent three-source reconciliation model. Verify unmatched cash, partial allocation, duplicate settlement data and reversal handling.

**D02.BASE-04 (original definition).** Configurable operations (D). MH-07. Implement controlled, versioned automation and rules. Verify effective-date changes, historical reproducibility and prevention of unauthorised processing.

**D02.BASE-05 (original definition).** Insight and extensibility (D/P). MH-08 and MH-09. Demonstrate transaction inspection, financial reporting, analytical lineage and addition of an adapter without altering unrelated core logic.

**D02.EXT-01 (original definition).** Enterprise delivery (P). Investigate onboarding, legacy data import, shadow processing, controlled cutover and recovery. Compare actual results without executing duplicate payments.

**D02.EXT-02 (original definition).** Engineering assurance (P). Investigate trace exports, replay, integration certification, observability and performance under controlled workloads.

**D02.EXT-03 (original definition).** Financial intelligence (P). Assess AI or machine learning only after deterministic controls and data quality have passed verification.

**D03.DOM-01 (original definition).** Separate PAS obligations, mandate authority and execution attempts. Acceptance evidence: Billing and execution contracts; invalid authority rejected.

**D03.DOM-02 (original definition).** Represent EFT debit, DebiCheck, RM and payroll independently. Acceptance evidence: Channel-specific simulator and negative tests.

**D03.DOM-03 (original definition).** Process credit payments and refunds against approved payable records. Acceptance evidence: Approval, duplicate and refund-limit tests.

**D03.DOM-04 (original definition).** Maintain distinct outcome, settlement and allocation states. Acceptance evidence: Delayed and conflicting event scenarios.

**D03.DOM-05 (original definition).** Preserve exact amounts and balanced immutable postings. Acceptance evidence: Constraint, reversal and replay tests.

**D03.DOM-06 (original definition).** Perform three-way reconciliation, including net settlement and partial receipts. Acceptance evidence: Reproducible control totals and exception evidence.

**D03.DOM-07 (original definition).** Support REST, durable messaging and working SFTP exchange. Acceptance evidence: Contract tests and end-to-end batch results.

**D03.DOM-08 (original definition).** Protect tenant, account and approval boundaries. Acceptance evidence: Negative authorisation and isolation tests.

**D03.DOM-09 (original definition).** Implement controlled recovery from ambiguous external results. Acceptance evidence: Crash and lost-acknowledgement verification.

**D03.DOM-10 (original definition).** Model policy arrears and grace handling without automatic lapse on failure. Acceptance evidence: PAS lifecycle and late-allocation scenarios.

**D03.DOM-11 (original definition).** Export verified data to analytical layers and report metric lineage. Acceptance evidence: Source-to-report reconciliation and freshness checks.

**D03.DOM-12 (original definition).** Support migration, extension and authorised rule changes. Acceptance evidence: Shadow run, rollback and configuration version tests.

## 7. Verification linkage

See `VERIFICATION_STRATEGY.md` for SC-01 to SC-12 with original coverage references. A scenario is not a substitute for a specific test for every requirement; M00 and milestone design must enumerate uncovered subcases, exact expected values, negative tests and evidence paths. Each FR/NFR will receive a disposition of not started, designed, implemented, verified, blocked or (only with approval) deferred. A verification record must link requirement ID, scenario/test ID, commit, environment, result, evidence path and limitations. Mandatory financial and isolation failures block acceptance.
