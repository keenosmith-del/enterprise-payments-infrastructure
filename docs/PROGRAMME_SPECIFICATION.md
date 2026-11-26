# Programme master specification

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Authority and change control

Owner and approval authority: project maintainer. Source baseline: approved Documents 01-04, with Document 04 controlling the implementation catalogue, crosswalk and milestone gates. The approved name is Enterprise Payments Infrastructure. Decisions proposed in earlier discussion remain candidates until validated and recorded. Do not infer vendor architecture or production readiness from independent design. If sources conflict, retain the original statements and record a proposed change with rationale; do not silently choose a replacement.

## 2. Mandate, business outcomes and scope

The programme will deliver a locally reproducible enterprise payments and collections ecosystem for a representative South African insurer. Its principal deliverable is an independent payments hub that receives financial instructions from established business systems, facilitates authorised collections and disbursements across simulated payment channels, preserves the evidence of execution and settlement, and returns reconciled financial outcomes to the originating systems. The surrounding applications will be independently functioning systems, not views over a shared set of fabricated dashboard records.

The solution is based on the publicly documented MoneyHub functional baseline established in Document 02 and the financial and institutional analysis in Document 03. Document 01 remains the programme mandate. This document converts those assessments into a proposed implementation baseline. It is not an assertion about the architecture of Q LINK or Sanlam, a proprietary product reproduction, a certified payment integration or a production readiness declaration.

The four-system boundary, public functional coverage, integration workstream, analytical workstream and independent verification approach remain agreed programme commitments. The component architecture, concrete contracts, technical selections, quantitative targets and sequencing below are proposed decisions for detailed design. No implementation or measured result is represented as complete. A detailed accounting specification, security model, provider contract specifications and architecture decision records must be approved before the associated production-quality code is accepted.

Insurance organisations must maintain continuity between the financial obligations arising from insurance contracts and the execution of payment instructions by external organisations. A premium can be due without a valid mandate; a submitted deduction can remain unconfirmed; a successful deduction can precede settlement; and a settled amount can remain unallocated. A claim approval does not itself move money. Each transition has different evidence, ownership and timing.

A fragmented infrastructure can impose repeated transformations, manually exchanged files, inconsistent reference formats and different operational views of the same financial event. Introducing a hub is intended to reduce this coordination complexity, not to move every responsibility into one database. A central canonical instruction model and consistent controls should enable the insurer to add a provider or modify an eligible product without rewriting

unrelated systems. This hypothesis must be demonstrated through a working integration change and verified regression tests.

The outcome is a reference implementation with defensible answers to five questions. Can financial obligations be executed only under appropriate authority? Can interrupted or repeated submissions be handled without repeated financial effects? Can every monetary discrepancy be explained from independent source evidence? Can an enterprise change its processing route without losing continuity? Can financial and operational reports be reproduced from the records that generated them? The system must show negative cases as clearly as successful transactions.

Core release (C). The four systems, premium billing, claims and refunds, recurring and once-off collections, EFT debit, DebiCheck, Registered Mandate, payroll deductions, EFT credits, cash-deposit matching, beneficiary and mandate lifecycle, canonical contracts, REST, durable messaging, secure batch exchange, configurable rules, operational journal, settlement, reconciliation, allocation, exception handling, tenant controls, observability and evidence exports. The core includes traceable export of operational records and verified operational reporting; the full analytical pipeline and data lake follow in the enterprise release. These are baseline requirements, not discretionary features.

Enterprise delivery and expansion (E). Data-lake transformations and business intelligence, independent connector onboarding, rules simulation, historical replay, shadow processing and controlled legacy migration, additional simulated instant credit and request-to-pay interfaces, stress testing and operational recovery. These are planned programme capabilities and will be delivered after financial correctness gates are met. Their detailed sequencing may be adjusted without silently removing them.

Optional research (O). Predictive collection modelling, anomaly detection or assisted matching may be evaluated after the deterministic platform is verified. Optional AI work is not a prerequisite for the core or enterprise delivery release. A model that offers no measurable improvement over a baseline should not be retained.

Excluded. Real funds, live consumer data, real bank credentials, direct clearing or SAMOS access, regulated payment provision, a real TPPP onboarding, actual mandate creation, production insurance underwriting, actuarial pricing, full IFRS 17 accounting, a complete payroll or human resources platform, and proprietary Q LINK or Sanlam protocols. External schemes, payment calendars and legal constraints will be represented by independently owned and explicitly labelled simulation policies. Commercial deployment would require a distinct legal, contractual, security and certification programme. The 25 November 2026 regulatory snapshot in Document 03 is not a substitute for future regulatory verification.

## 3. Four systems and supporting workstreams

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

The enterprise integration layer provides ESB capabilities: protocol translation, validation, routing, correlation, durable delivery, partner configuration and receipt management. It does not determine whether a premium is owed or authorise a financial transaction. An integration receipt proves transport and intake status only. The hub applies business authorisation and duplicate controls even when an upstream connector has already validated a message.

The broker transports durable work and outcome events; it is not the authoritative source of financial state. SFTP supplies secure partner-specific file exchange. Object storage retains raw files and analytical datasets with a metadata catalogue. The identity service provides authentication and token issuance, while each application enforces its own tenant and business permissions. Observability infrastructure receives operational signals without storing unnecessary sensitive account or mandate data.

The analytical pipeline extracts committed events and controlled snapshots into raw, validated and business-ready datasets. It consumes outcomes from the PAS, hub, bank and payroll interfaces under explicit data contracts. It must not access other databases as an ungoverned integration mechanism. An analytical outage may delay reports but must not block a valid payment or change a transaction outcome. A reporting dashboard is not a financial system of record.

Normal flow: the PAS creates an obligation and originates an instruction; the integration layer validates and routes it to the hub; the hub validates authority and dispatches an eligible attempt; the independent provider executes and returns evidence; the hub reconciles observations with independent settlement records; a controlled allocation or disbursement result is returned to the PAS. The data platform receives committed records for reporting. Every boundary crossing carries an immutable source identifier and correlation metadata.

## 4. Acceptance and release commitments

Completion will be assessed through verifiable engineering outcomes. The project will not be considered complete solely because the applications run or the interfaces are visually polished. The following acceptance conditions establish the initial verification baseline; detailed test specifications and quantitative service-level targets will be defined during requirements and architecture work.

Functional baseline: every applicable publicly documented capability is mapped to an implemented and tested requirement, or a clearly justified exclusion. A complete synthetic insurance billing cycle demonstrates collections, disbursements, settlement, reconciliation and return of outcomes to the PAS.

Integration: equivalent valid instructions arriving through API, message queue and SFTP interfaces produce consistent canonical processing results. Invalid records, incomplete files, duplicate submissions and incompatible contracts are rejected or isolated with inspectable evidence.

Financial integrity: journal entries balance and repeated instructions do not result in duplicate financial postings or simulated deductions. Expected obligations, processor outcomes and settlement records can be reconciled at transaction and aggregate levels. Unmatched records remain visible until resolved through authorised controls.

Reliability and isolation: interrupted workers, ambiguous provider acknowledgements, delayed responses, retries and reversals are exercised in automated scenarios. Recovery does not silently lose instructions or repeat financial effects. Tenant boundaries and authorisation controls are verified through negative as well as positive tests.

Data and reporting: operational and analytical outputs are derived from generated transaction data, with traceable calculations and documented freshness. Reporting totals can be reproduced against the underlying records, including corrected or late-arriving events.

Scale and reproducibility: the initial stress-test ambition is a synthetic population of 100,000 policyholders and a workload of up to one million financial events. These are proposed targets, not achieved metrics. Tests will document hardware, workload composition, throughput, latency, recovery behaviour and any resource limitations.

Delivery evidence: another engineer can reproduce the environment, follow the documented integration contracts, execute the verification suite and inspect the results. Extension claims will be supported by comparison or testing, with remaining limitations clearly identified.

## 5. Governance and milestones

C means mandatory core, E means planned enterprise expansion, O means optional research. A deferred E requirement is outstanding, not a dropped obligation. Requirements, design decisions, and verification statuses are separate. M00 design approval is the next gate; the maintainer approves scope changes, selected technologies, deviations from quantitative targets and milestone releases. The implementer owns design proposals and evidence, not approval by default. The detailed business, functional and non-functional specifications remain deliverables in Volume 02. For each component, approve ownership, domain model, contracts, security, failure states, invariants and acceptance cases before implementing it. Record dependencies and design risks in the linked registers. The final portfolio claims only results backed by reproducible evidence.

## 6. Controlled change process

Use a unique change ID (CR-0001 onwards), affected baseline identifiers, rationale, alternatives, compatibility and migration impact, test updates, evidence and maintainer approval. Do not reassign identifiers; supersede or add child identifiers. Record date and commit with each approved change, update the impacted documents, and retain the earlier baseline. An unresolved discrepancy prevents dependent work, not unrelated design. See the implementation roadmap for stage gates.
