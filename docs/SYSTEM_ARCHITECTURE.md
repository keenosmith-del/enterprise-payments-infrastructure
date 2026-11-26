# System architecture baseline

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Architecture status and source

Source: Document 04 sections 4-6, 9-14. This is the design baseline for M00, not the final detailed System Architecture and Design deliverable. The four systems are independent ownership and deployment boundaries. Shared services do not constitute additional business systems. The hub begins as a modular monolith with durable workers. Proposed implementation topology and contract definitions need explicit approval before dependent code.

## 2. Application boundaries

Each application owns its database, migrations, validation and public integration boundary. A local infrastructure deployment may share a PostgreSQL server or broker instance to control resource consumption, but separate databases or schemas with distinct service credentials and enforced grants must prevent cross-system writes. A shared deployment does not create shared record ownership. Each system must be testable with an independently specified peer contract and capable of operating when other components are temporarily unavailable, within documented limits.

### 4.1 System 01: Policy Administration System (PAS)

The PAS owns policyholders, beneficiaries, products, policy versions, coverage status, premium schedules, billing periods, receivables, approved claims, refund eligibility and the allocation history of each policy account. A bill run creates immutable obligations with stable identifiers and a product/rule version. A rerun for the same policy and period cannot create an additional obligation. Amendments create adjustments or replacements with effective dates; cancellation and reinstatement must follow configurable synthetic insurance rules rather than a generic status toggle.

The PAS sends collection and approved disbursement instructions using the published contract. It does not call a bank adapter directly during normal operation. A financial outcome is consumed through a versioned inbound interface, with its own receipt, duplicate control and validation. A result with an unknown obligation reference is quarantined for review. Policy accounts reflect authorised allocation events, not the arrival of a provider acknowledgement. Arrears, grace periods and policy status are evaluated separately and must not transition to lapse merely because one deduction fails.

The PAS supports an operational interface for bill runs, payment instructions, claims approvals, policy account inspection and integration status. It must demonstrate a legacy scheduled batch interface alongside REST and asynchronous event integration. Financial and coverage decisions remain insurer-side, even when payment processing moves to the hub.

### 4.2 System 02: Enterprise Payments and Collections Hub

The hub is the main deliverable. It owns intake receipts, canonical instructions, payment authority records, execution attempts, channel routing, rule evaluations, scheduling, operational journal entries, provider observations, settlement allocations, reconciliation cases, approved exception actions and outgoing financial result messages. It accepts financial obligations from a PAS but does not redefine the premium, approve a claim or change an insurance contract.

Internally, modules separate instruction intake, mandate control, payment scheduling, channel orchestration, provider adapters, beneficiary administration, ledger, settlement, reconciliation, rules, exception management, integration administration, audit and reporting. Each module has an explicit application interface and owns its writes; uncontrolled modification of another module's financial records is prohibited. Financial operations requiring atomicity, such as recording a posting and its outbox event, may occur in one database transaction. Cross-system operations use durable messages and reconciliation, not a distributed database transaction.

A modular monolith with separate worker processes is the proposed starting point for the hub. It provides a practical financial consistency boundary while allowing workers to scale independently and modules to be extracted later if measurements justify it. This does not preclude separately deployed integration, reporting or simulation components. The hub must expose actual processing state and evidence to operational users, not calculate financial truth in the frontend.

### 4.3 System 03: Banking and Payment Network Simulator

The simulator represents fictitious banks and TPPP-facing providers. It owns synthetic account records, provider-side mandate authentication, execution receipts, independent transaction histories, bank balances and settlement files. It supports EFT debit, authenticated DebiCheck, Registered Mandate, EFT credit and direct deposit evidence. Additional simulated instant credit and request-to-pay are extension channels. No interface claims compatibility with a real bank or scheme.

The simulator independently validates instruction identity, authorisation where applicable, amount and provider capabilities. Its execution records and balance mutations occur within its own transaction boundary. Duplicate provider operation identifiers return the existing result if the payload is identical, and conflict if it differs. A configurable fault engine can delay, reject, duplicate or reorder responses, lose acknowledgements after execution, interrupt delivery, return unpaid items, and produce settlement differences. Scenario controls must not bypass accounting or create unexplained records. Explicit fault settings and seeds are captured in the test evidence.

Bank statements and settlement batches are generated from the simulator's own committed records, not copied from the hub's expected transactions. It must be possible for a provider to commit an operation while its response is unavailable, and for the hub to discover that fact through an independent enquiry or later evidence. The simulator also supports scheduled cut-offs and separate execution and settlement times.

### 4.4 System 04: Employer and Payroll Simulator

The payroll simulator owns synthetic employment relationships, payroll periods, deduction authority, employer-specific file formats, permissible deductions, available deduction capacity, actual payroll deductions and remittance records. It applies independent synthetic employment eligibility and affordability rules. The hub cannot assume that an accepted payroll instruction represents a deduction or that a deduction represents cash remitted.

For each payroll cycle, the simulator validates references and authorisations, determines full, partial or rejected deductions according to configured policy, closes the cycle, and generates deduction results and remittance evidence. It supports termination, changed employee identifiers, missed cut-offs, conflicting duplicates, partial payroll files, deductions without remittance and remittance discrepancies. A remittance may aggregate many employees; the system retains the item-level relationship needed for reconciliation. A separate financial receipt from the bank simulator can substantiate the remittance.

The simulator does not implement an entire HR, payroll tax or salary calculation product. Its boundary is the minimum independent payroll behaviour necessary to establish credible third-party collection and reconciliation workflows.

## 3. Shared infrastructure

The enterprise integration layer provides ESB capabilities: protocol translation, validation, routing, correlation, durable delivery, partner configuration and receipt management. It does not determine whether a premium is owed or authorise a financial transaction. An integration receipt proves transport and intake status only. The hub applies business authorisation and duplicate controls even when an upstream connector has already validated a message.

The broker transports durable work and outcome events; it is not the authoritative source of financial state. SFTP supplies secure partner-specific file exchange. Object storage retains raw files and analytical datasets with a metadata catalogue. The identity service provides authentication and token issuance, while each application enforces its own tenant and business permissions. Observability infrastructure receives operational signals without storing unnecessary sensitive account or mandate data.

The analytical pipeline extracts committed events and controlled snapshots into raw, validated and business-ready datasets. It consumes outcomes from the PAS, hub, bank and payroll interfaces under explicit data contracts. It must not access other databases as an ungoverned integration mechanism. An analytical outage may delay reports but must not block a valid payment or change a transaction outcome. A reporting dashboard is not a financial system of record.

Normal flow: the PAS creates an obligation and originates an instruction; the integration layer validates and routes it to the hub; the hub validates authority and dispatches an eligible attempt; the independent provider executes and returns evidence; the hub reconciles observations with independent settlement records; a controlled allocation or disbursement result is returned to the PAS. The data platform receives committed records for reporting. Every boundary crossing carries an immutable source identifier and correlation metadata.

## 4. Domain identity, amount and time

### 6.1 Identity and reference hierarchy

A tenant represents an enterprise customer and controls its business configuration. A legal entity within that tenant may have separate accounts, settlement arrangements and approval policies. A policy, billing obligation, mandate, payment instruction, attempt, provider operation, settlement item, journal entry, allocation and exception each has its own identity. None is interchangeable with a correlation identifier or a bank reference. An obligation may produce several legitimate attempts, a settlement may cover many attempts and an allocation may satisfy several obligations. These relationships must be explicit and auditable.

Every inter-system identifier is namespaced by source system and tenant. Internal IDs are immutable and opaque; external references are retained as received and normalised only in separate searchable fields. A unique constraint on tenant, source, operation type and source instruction identifier enforces intake idempotency. An instruction's payload hash is derived from a documented canonical representation, including material authorisation and monetary fields; volatile timestamps or correlation metadata do not cause false conflicts. An identical replay returns the recorded receipt; a materially different replay under the same key is a conflict requiring investigation.

A provider operation identifier belongs to a single execution attempt. The same identifier is reused for retries of uncertain transport, provided the provider contract guarantees idempotency or equivalent enquiry. A new attempt requires a resolved prior outcome or an explicitly approved correction, not merely a retry counter increment. The original obligation identity remains stable across attempts and channel changes.

### 6.2 Amounts, time and provenance

Use ZAR as the initial currency. Represent amounts as integer minor units in interchange contracts, with explicit currency and non-negative amounts where direction is separately encoded. The database uses bounded integer or exact numeric representations; binary floating point is prohibited for monetary calculations. Decimal arithmetic and documented rounding are required at calculation boundaries. Reject invalid scale, overflow, ambiguous currency and mismatched amount totals. Fees, gross amounts, net amounts, adjustments and reversals remain separate values.

Store timestamps as UTC instants plus source time and zone where relevant. Business processing dates, payroll periods, value dates, settlement dates, effective dates and accounting periods are distinct fields. A South African business calendar governs scheduling and synthetic processing windows. Use versioned calendar fixtures and explicitly define behaviour at cut-off boundaries, holidays and late arrivals. Record both event occurrence and ingestion times so an old observation does not overwrite newer authoritative state simply because it arrives later.

Source evidence includes source identity, schema version, event or file ID, record locator, integrity digest, received time, provider reference, validation outcome and responsible service or actor. Retention and access policies apply to

original payloads. A digest establishes content integrity, not authenticity by itself; source authentication and controlled storage are additional controls.

## 5. Enterprise integration contracts

### 9.1 Canonical message model

The integration layer accepts provider- or client-specific schemas and translates them into versioned internal message types. A canonical envelope contains schema version, message type, source, tenant, unique message ID, correlation and causation IDs, event time, payload and integrity metadata where applicable. A collection payload includes obligation ID, source instruction ID, mandate reference and version, amount in minor units, currency, requested business date, eligible channel and product rule context. A disbursement adds payable and approval references and beneficiary version. Responses distinguish receipt, validation, execution outcome, settlement, allocation and exception events.

The hub must validate material fields independently of the ESB. Contract compatibility rules permit additive optional fields within a compatible version but require a new major version for changes to monetary units, required fields or semantics. Unknown versions and unmappable provider codes are quarantined. Contract fixtures will cover backward compatibility, invalid records and provider-specific transformations. No raw payload is interpreted as trusted configuration or executable code.

### 9.2 REST and asynchronous messages

The proposed REST resources include collection instructions, disbursement instructions, mandates, operations, receipts, settlement imports, reconciliation cases and results. A successful asynchronous submission returns an intake receipt and a queryable identifier, for example HTTP 202 after durable acceptance. It is not a promise of collection or settlement. Structural errors return an explicit validation result; duplicate payload conflicts return HTTP 409. External clients authenticate with scoped service credentials and use stable idempotency keys. Endpoints support bounded pagination, correlation IDs, safe error messages and rate controls.

Commands and events have different contracts. A command requests a specific action; an event records a committed fact. A transactional outbox writes messages in the same commit as the owning state change. A relay publishes durable messages to the broker and marks delivery after broker confirmation. A crash between publish and marking may cause

duplicates. The receiver stores an inbox receipt and the local effect in a single database transaction before acknowledging delivery. Retryable transport failures use bounded backoff with jitter; non-retryable contract failures enter a quarantined or dead-letter workflow. Redelivery and event replay must not create new financial effects. Per-entity sequence/version guards prevent stale events from replacing authoritative state; unresolved contradictions are escalated.

### 9.3 SFTP and batch instructions

A real local SFTP service will expose segregated partner accounts and inbound, processing, archive, rejected and outbound locations, with restricted key-based authentication. A sender transfers a temporary file and atomically renames it or supplies a manifest-ready marker; the importer does not process a partially uploaded file. The manifest specifies file type, schema version, batch identity, source, declared record count, monetary control totals, encoding and content digest. Each row carries a unique source instruction identity. Inbound bytes are retained before parsing with recorded integrity and provenance.

The importer validates file structure, schema, expected sender, counts and totals before releasing instructions. Policy distinguishes whole-file rejection from explicitly permitted row-level rejection. A batch with invalid control totals cannot silently release a subset. Receipt messages communicate file acceptance, duplicate or conflict status, record-level rejection and processing progress. A results file is generated from committed outcomes using a stable batch identity and a deterministic export version; it is published atomically, and retransmission does not trigger execution. The same business instruction received through API and SFTP must resolve to one instruction when its source identity and canonical content agree.

Partner onboarding includes contract fixtures, credential provisioning, directory permissions, test delivery, acknowledgement handling, mapping version approval, cut-off configuration and controlled activation. The integration layer exposes queue age, transfer failures, receipt history and replay options. Replays are permissioned and always reuse source identities unless a separate corrective business instruction is explicitly authorised.

## 6. Rules and operational interfaces

Rules must be declarative, deterministic and versioned, with a restricted expression vocabulary rather than arbitrary uploaded Python. A rule set has tenant, scope, priority, conditions, actions, effective date, version and approval history. Conflicting or incomplete rules default to a safe hold or rejection. Rules cannot override authority limits, ledger invariants or tenant boundaries. Historical decisions retain the evaluated rule version, material inputs, result and explanation. An operator may propose a new version and simulate it on a frozen dataset before another authorised operator activates it.

Collection optimisation uses approved business rules to choose permitted processing windows or eligible routes. It must not infer authorisation from a predicted success probability or apply repeated attempts that violate limits. Compare the proposed strategy against a fixed baseline with the same synthetic cohort, tracking collection rates, fees, affordability rejections, returns and customer-impact indicators. Changes to product configuration originate in the appropriate owning system and are applied through versioned contracts; the hub does not override the PAS premium calculation.

The value-added services framework exposes explicit adapter capabilities and independent service contracts for account verification, deposit matching and proposed additional payment channels. An adapter advertises supported

command types, authority constraints, status enquiry, idempotency semantics, processing windows, settlement format and error taxonomy. Extending the system means implementing an adapter, registering configuration and running compatibility tests rather than changing the main transaction model. Unsupported capabilities fail closed. Instant credit and request-to-pay are independent extension paths; a request-to-pay request or acceptance is not itself proof of settled credit.

Operational interfaces provide task-oriented views for finance, integration, collections, risk, administration and review. The primary hub interface includes queues, instructions, mandates, beneficiaries, attempts, settlement files, reconciliations, exceptions, rule versions, partner health, journal inspection, audit and reports. Each detail view links to original source evidence and chronological events, shows distinct states and displays actual processing data. Actions such as retries, overrides, approvals, rule activation and reconciliation adjustments invoke authorised backend commands. The PAS and simulators have independent administrative views for their respective responsibilities. Fault controls are visibly restricted to simulation administration.

## 7. Analytical architecture

The analytical pipeline is a planned supporting platform, not a parallel operational ledger. Committed event exports and controlled incremental extracts populate immutable raw objects in S3-compatible storage. Each object has source, partition, schema version, checksum and extract cursor; batches have manifests and source counts. Source exports use durable sequence checkpoints or explicit high-water marks with an overlap/deduplication strategy, not a timestamp-only cursor that may miss late commits. Pipeline jobs must be restartable and track successful publication separately from extraction.

The raw layer retains original records and ingestion metadata. The validated layer normalises schema, identities, financial amounts and timestamps, deduplicates source records, and quarantines invalid records with reasons. The business-ready layer publishes versioned fact and dimension models for obligations, attempts, outcomes, settlement items, allocations, mandates, policy accounts and exceptions. Preserve a bridge between aggregated settlement and item-level execution records. Avoid joining one-to-many tables in a way that duplicates amounts. Historical dimension changes retain effective dates where needed for reproducible reports. Use Parquet and SQL transformations, with lineage from report rows back to source events and batch manifests.

Define every metric by grain, time basis, currency, eligibility population and denominator. Collection success by amount equals successful execution amount divided by eligible attempted amount for a defined cohort and observation cut-off; obligation-level recovery uses a different denominator and must not be conflated. Unknown and pending results are separately reported. Net cash settled excludes fees only when those fees are substantiated; gross and net values remain distinguishable. Reconciliation coverage may be reported as matched eligible amount divided by expected amount, accompanied by unmatched reasons and reporting freshness. A metric revision must preserve the previous definition and identify its effective version.

Business intelligence will expose a semantic model suitable for Power BI, including explicit measures, date dimensions, tenant and product filters, settlement ageing and drill-through references. The report dataset is published through a supported analytical SQL or extract interface, not a direct uncontrolled query into the operational database. Power BI Desktop availability on the development platform and service licensing must be checked at the technology selection gate. A reproducible browser-based report and exported model/dataset provide a fallback when Microsoft tooling is

unavailable; Power BI integration remains a planned deliverable and any uncompleted verification is recorded explicitly.

## 8. Security and recovery

Tenant membership and service identity are server-derived, never trusted from a user-supplied tenant header alone. Enforce tenant-scoped access at application and persistence boundaries, including indexes, queries, object paths, broker routing, logs, exports and analytical access. Use resource-level checks for every privileged action. Distinguish finance maker, approver, reconciliation reviewer, integration operator, tenant administrator, read-only auditor and simulation administrator; no principal approves their own sensitive proposal. Authorisation is evaluated again at execution for queued sensitive actions whose permissions may have changed.

Use scoped service credentials, short-lived tokens where supported, encrypted transport, securely stored secrets, segregated SFTP keys and key rotation procedures. Store synthetic account tokens rather than unnecessary bank details. Redact credentials, account identifiers and personal data from operational traces. Validate payload sizes, schemas and file names; isolate untrusted file parsing and prevent path traversal, decompression abuse and formula injection in exported CSV. Establish retention and deletion policies for each data class. Use synthetic identities only; document the legal and regulatory exclusions in the user interface and README.

Append-only audit records capture actor, tenant, action, object identity, time, request ID, before/after references and approval chain. Audit records must be access-controlled and exportable for independent verification; optional digest chaining can support integrity checks but does not establish tamper-proof storage if the database administrator can modify all records. Changes to financial rules, privileges, bank references, settlement matches and journal corrections require attributable evidence. Security tests cover unauthorised object access, cross-tenant attempts, stale tokens, forged messages, duplicate approvals and privilege escalation.

Reliability relies on durable local state, explicit unknown outcomes, transaction constraints and independent evidence. A worker interrupted before commit leaves no posted effect. A worker interrupted after commit but before acknowledgement causes a replay, not a second posting. A provider that accepts execution but loses its response leaves the attempt unknown; query the provider by stable reference, consume later evidence and block unsafe resubmission. If provider status cannot be established, hold the operation for manual resolution. Timeouts are not payment failures. A broker outage may defer work; committed outbox records remain recoverable. A failed data pipeline must not affect financial state.

Observability includes structured logs, correlation tracing and metrics for instruction intake, queue age, dispatch latency, unknown outcomes, retries, duplicate conflicts, settlement ageing, unbalanced posting attempts, failed access checks and analytical freshness. Alerts must describe a measurable condition and route to a documented operational action. Backups include financial databases, retained evidence and configuration; restore tests verify journal balances, source counts, unresolved attempts and replay safety. External simulated providers are not rolled back with the hub. After recovery, reconcile against their independent evidence before resuming uncertain execution.

## 9. Migration

The legacy PAS integration will support a reproducible pre-migration workflow using scheduled files and a simulated legacy executor. Import historical obligations, mandate references, outstanding amounts, prior attempts, unmatched deposits and opening control balances from versioned migration files. Validate identities, counts, monetary totals and mapping errors; keep source-to-target lineage. Imported authority references do not imply that real mandates have been authenticated. Migration fixtures must capture stale or missing records and explicit exclusions.

During shadow processing, the hub receives equivalent instructions and evaluates routing, validation, accounting projections and expected outcomes without sending executable payment commands. Compare decisions and reconciled values to the legacy results on a fixed cohort; record unexplained discrepancies and approved differences. Shadow mode must be enforced by backend dispatch controls and provider-side rejection of shadow credentials, not just a UI switch.

Cutover requires explicit ownership of execution by tenant, channel and effective period. Freeze or drain legacy work, verify unresolved attempts, reconcile opening balances and obtain dual approval before granting the new path authority. A durable execution lease or equivalent mutually exclusive ownership control must prevent simultaneous live-mode dispatch in the simulation. Rollback restores routing responsibility only after identifying instructions already submitted by the new hub, preserving provider operation identities and reconciling their outcomes. Rollback is not restoration of an old database snapshot followed by re-execution. Document preconditions, exceptions, acceptance evidence and operational responsibility at every step.

## 10. Proposed repository topology

```text
apps/{policy-administration,payments-hub,banking-simulator,payroll-simulator}/
  backend/   frontend/
services/{enterprise-integration,data-engineering}/
packages/{financial-types,integration-contracts,observability,ui-components}/
contracts/{openapi,asyncapi,events,files}/
infrastructure/{docker,postgres,rabbitmq,sftp,identity,observability}/
analytics/{pipelines,transformations,semantic-models,power-bi}/
tests/{integration,contracts,financial-integrity,end-to-end,performance,recovery}/
simulations/   evidence/   scripts/   docs/   .github/workflows/
AGENTS.md   README.md   CHANGELOG.md   compose.yaml   .env.example
```

These are proposed paths, not existing software. Each application has own migrations, database credentials, domain and application services, API contracts, tests and deployment definition. Use distinct service identities and restrict network paths. Shared types cannot grant domain write access. One local PostgreSQL instance with separate logical databases may be used if credential separation passes. Core profile includes four systems, ESB, broker, database, SFTP and identity; analytics and observability profiles add supporting components as justified. M01 should start only the minimum necessary services, add the remainder incrementally. Pin image versions after M00 feasibility checks.

## 11. Design prerequisites

Before M02, approve domain identity, exact monetary and posting primitives, version transitions and migration/rollback. Before M04, approve canonical envelope, OpenAPI, message and file schemas, compatibility, receipt and quarantine policies. Before M05-M07, approve mandate authority, approval matrix, attempt state machine, provider idempotency/enquiry, settlement evidence and allocation rules. Before M08-M12, approve payroll, disbursement, detailed ledger and reconciliation specifications. No dispatch path may bypass those controls. Before analytics, approve source export schema, lineage, metrics and late-event treatment. Record exact schemas and deployment evidence in later repository documents; this baseline deliberately does not invent concrete bank schemas or credentials.

## M01 foundation update

M01 adds four independent executable application foundations, separate databases, a development identity provider and technical RabbitMQ and SFTP transports. The Hub remains one deployment and persistence boundary. These technical foundations do not implement financial processing.
