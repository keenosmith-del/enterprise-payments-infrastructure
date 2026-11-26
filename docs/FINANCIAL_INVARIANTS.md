# Financial invariants and control baseline

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Purpose and authority

Derived from Document 04 sections 6-8, 12, FR-010/011/019-025 and NFR-001/002/003/007. These invariants are mandatory constraints; they are not an accounting certification or a completed detailed posting specification. The insurer owns receivables and payables; the hub is non-custodial. Each invariant receives explicit unit, real database integration and adversarial verification as applicable. Proposed IDs FI-01 onwards supplement the FR/NFR catalogue and do not replace it.

## 2. Invariants and proof obligations

### FI-01: exact monetary values

No binary floats in financial calculation or transport. ZAR integer minor units, explicit currency and direction; Decimal for rates with documented rounding at calculation boundaries. Reject invalid scale, overflow and mismatched totals. Test conversion, limits, partial allocations and conservation. FR-020, NFR-001.

### FI-02: authority precedes dispatch

An obligation is not a mandate; account verification is not consent; claim approval is not execution. Evaluate current channel-specific authority, amount, dates, eligibility and independent approvals at dispatch; fail closed. Test revocation after scheduling, stale versions, excessive amount, unauthorised claims and payroll constraints. FR-003/011-018, SC-04/06.

### FI-03: unique business effect

Namespaced source identity and canonical material payload hash yield one acceptance record. Identical replay returns original receipt; changed payload under same key conflicts. Use unique attempt/provider operation and source-purpose posting keys; transport IDs alone do not define a financial operation. Test concurrent API, broker and SFTP duplicates. FR-010/020, SC-02.

### FI-04: ambiguous outcome hold

Timeout is not failure. Preserve operation identity, resolve via independent enquiry or evidence, never issue another debit or credit when prior outcome remains unknown. If provider offers neither safe idempotency nor enquiry, hold for approved investigation. FR-019/025, SC-03.

### FI-05: no excess execution or allocation

Reserve eligible amount during unresolved attempts; use transaction locks or guarded version updates. Aggregate allocated, refunded and reversed amounts may not exceed eligible balances; currency and legal entity must agree. Test race conditions and partial or aggregated amounts. FR-013/018/022-024, SC-05/07.

### FI-06: balanced immutable journals

Each posted journal balances within currency and legal entity. Enforce database and application posting guards and unique source-purpose entries; state and outbox commit together. Correct through linked compensating entries; closed periods use authorised adjustment periods with original value date. FR-020, SC-07.

### FI-07: independent evidence and lifecycle separation

Intake, acceptance, attempt, provider execution, settlement and allocation are distinct. Provider and payroll records must be generated independently, not derived from hub expectations. Never infer settlement from a successful response or PAS update from an outgoing event. FR-015/019/021/023/024, SC-01/03/05.

### FI-08: explain all discrepancies

Track expected, attempted, unpaid, unknown, gross settled, net settled, fees, reversals and unapplied values independently. No invented balancing entries; missing fee or source evidence remains an exception. Explicit source revision and matching rule version. FR-021-025, SC-07.

### FI-09: isolation and approvals

Tenant and legal entity are server-derived, with separate data ownership. Sensitive actions require distinct maker/checker principals; no bypass through message, file, BI or privileged UI. Test negative role and tenant cases across all interfaces. FR-025/028/029, SC-09.

### FI-10: safe replay and recovery

Committed state and outbox/inbox are durable; pre-commit crash leaves no effect; post-commit redelivery cannot duplicate. Restore internal data then reconcile independent providers before resuming dispatch. Shadow processing never executes; cutover requires exclusive owner and rollback resolves already submitted work. FR-007/036/037, SC-08/11/12.

### FI-11: analytical non-authority

Reports derive from versioned committed data and never authorise or mutate financial state. Late events and duplicate imports must not distort measures. Optional AI cannot approve, execute or post. FR-031-033/038, SC-10.

## 3. Authoritative processing model (Document 04 section 7)

### 7.1 Instruction and attempt lifecycles

An instruction is received, validated or rejected, held for authority or approval if required, scheduled, and eligible for dispatch. Its financial intent may be fulfilled, partially fulfilled, cancelled before execution, exhausted or under investigation. An execution attempt progresses through created, ready, submitted, pending or unknown, then a definitive result when evidence permits. Provider acceptance, execution outcome, settlement and allocation are recorded as independent dimensions, not forced into a single linear status. A late return after settlement produces a new event rather than erasing the original success.

Transitions are guarded by an explicit versioned state machine. A transaction locks the relevant instruction or enforces optimistic version checks before changing processing state and recording its outbox event. A durable worker leases work with bounded expiry; another worker may resume abandoned work only under the same operation identity. A cancellation before dispatch blocks new execution; a cancellation after dispatch requires status resolution and, if necessary, a separately authorised reversal. An apparent failure is not sufficient reason to dispatch an alternative route.

### 7.2 Mandate and channel authority

A recurring arrangement links the obligation source, debtor, account reference, amount constraints, frequency, authorised channel, validity period and external mandate reference. Distinct states represent request, pending authentication, active, rejected, suspended, amendment pending, revoked and expired. Versions retain prior terms. A change in amount, account, date or channel must be evaluated against the applicable authority and may require new approval or authentication. Account verification confirms a limited account property and does not establish consent.

Each channel exposes its supported operations and authorisation model. DebiCheck requires the simulator's affirmative authentication evidence before activation; Registered Mandate and ordinary EFT debit use distinct simulated authority records and validation paths. Payroll authority is subject to employer and employee constraints. A direct credit or cash deposit is payer-initiated and must not be treated as a debit instruction. A fallback route is eligible only after the existing attempt is resolved, the alternative authority is independently valid and configured collection limits permit another attempt.

### 7.3 Collections, disbursements and operational limits

For bank collections, schedule attempts from outstanding authorised obligations, with rules for maximum amount, permissible dates, number of attempts, hold periods and provider capabilities. A successful partial collection decreases only the appropriate available outstanding amount after the required allocation evidence. Reserve the amount eligible for execution while attempts are unresolved so concurrent processes cannot exceed the obligation. An adjustment to a bill during processing is handled through an explicit change or review, not a rewrite of a submitted amount.

For a disbursement, an insurer-approved payable or refund becomes an instruction with a stable approval reference, beneficiary version, payment amount, currency and reason. The hub checks approval limits, beneficiary status, duplicate operation identity and payment authority. A refund is constrained by the eligible original amount net of previous refunds and reversals. Beneficiary changes and sensitive releases require maker-checker approval by distinct

principals. A returned disbursement is tracked and accounted for before any replacement attempt is authorised. Same-day and next-day processing are simulator policy choices, not promised settlement guarantees.

### 7.4 Financial journal and accounting boundary

The insurer retains ownership of premium receivables, claims payables and policy-level accounting. The hub maintains a non-custodial operational financial-control journal representing amounts facilitated, pending settlement, matched or allocated, including fees and reversals. The journal must not imply that the hub holds customer money. The final chart of accounts and posting rules require the separate ledger design specification. The bank and payroll simulators maintain independent records of their own economic movements.

For each posted journal, total debits equal total credits for each currency and legal entity. Entries are immutable once posted; corrections are new balanced entries with references to the original transaction and approval evidence. Application checks and database-enforced posting controls must prevent incomplete or unbalanced journals from becoming visible as posted. Journals and the corresponding financial state and outbox message commit atomically within the owning service. Uniqueness of posting purpose and source event prevents duplicate posting on replay. Period closing blocks new ordinary postings to closed periods; late corrections are recorded in an authorised open adjustment period with the original value date retained.

Illustrative hub control treatment: an independently confirmed R750 collection may increase a collection-in-transit control balance with an equal opposite facilitated-collection control entry. When the R750 settlement is independently matched, the in-transit balance is cleared against a settlement-confirmed control account. The allocation back to the PAS closes the remaining control responsibility according to the final posting model. These are not actual cash custody or insurer revenue entries. The insurer applies its own receivable and cash accounting when the requisite evidence is received. The example is a proposed control treatment, not an IFRS 17 specification.

## 4. Three-way reconciliation and worked example (Document 04 section 8)

The proposed three-way model compares (1) expected obligations and payment instructions, (2) independent execution outcomes, and (3) independent settlement or statement evidence. It is our chosen implementation of the publicly documented three-way capability; the actual MoneyHub sources and matching algorithm are not established. For payroll, deduction results and employer remittances form a subordinate chain that is tied to actual simulated bank receipt evidence. For payer-initiated deposits, an execution-side receipt or deposit record may originate outside a debit instruction; the matcher must establish the appropriate obligation or leave it unmatched.

Ingestion preserves original records, control totals, provider identifiers, currency, dates and received file revisions. Duplicate detection must be based on source identity and content, not amount alone. A replacement settlement file is registered as a revision and reviewed rather than automatically counted as additional funds. The engine first resolves stable references and explicit links, then considers deterministic combinations of amount, currency, business date and approved tolerance policies. Ambiguous candidates are ranked for review, not automatically posted based solely on matching amounts. Fees are explicit reconciling items and never hidden by a tolerance.

Support one-to-one, one-to-many, many-to-one and partial allocation. Each matching operation reserves or locks the available balance in the database, records applied amounts and prevents the sum allocated against an item from exceeding its eligible balance. Matching across tenants, incompatible currencies or unrelated legal entities is forbidden. Reconciliation runs record the source snapshot, rule version, processing period and decisions so that rerunning the

same snapshot can reproduce the same result. Incremental reconciliation consumes late or changed evidence without double counting previous results. Closed cases may reopen with a linked new case when a late reversal or correction occurs.

Worked synthetic example: the PAS submits R100,000 of eligible obligations. The provider reports R92,000 successful, R6,000 unpaid and R2,000 unknown. Independent statement evidence contains R90,500 net receipts. A settlement schedule proves R1,000 of fees and R500 of successful items not yet settled. Gross settled value is R91,500, leaving R500 of known execution awaiting settlement; the additional R8,000 is not collected or remains unknown. The control report must distinguish unpaid, unknown, outstanding settlement and fees. If the R1,000 fee record is absent, the engine must show an unexplained difference rather than manufacture an expense.

A separate allocation process applies eligible matched receipts to PAS obligations and communicates an immutable result with a unique allocation ID. If the PAS rejects the result or is unavailable, the hub holds the result for controlled replay. It does not mark the PAS account updated until an independent receipt confirms consumption. Allocation reversals generate corresponding insurer-side adjustment messages, while historical allocation evidence remains intact.

## 5. Required pre-dispatch design reviews

M02 must establish the journal primitive and exact values before financial processing. M05-M07 must review the authority matrix, state transition guards, provider contract and independent settlement/matching primitive. M10 and M12 elaborate rather than retroactively introduce mandatory controls. Freeze worked examples and expected results in fixtures before implementation; do not derive expected results from the same algorithm under test. Financial correctness failures are release blockers regardless of benchmark or UI success.
