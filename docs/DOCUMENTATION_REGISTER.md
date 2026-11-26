# Documentation and delivery register

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Scope and numbering

The original five-volume programme remains the long-term framework. The four approved discovery documents consolidated six originally proposed topics. Preserve their actual Document 01-04 filenames and titles. The original list numbers below are planning references only (`V01-T01` etc.); they are not new document numbers. No competing Document 05 is created by this bundle. Subsequent formal PDF numbering will be approved before publication; repository specifications can be updated independently.

## 2. Volume 01: Research and discovery (approved)

- Original topics 01 and 02: actual Documents 01 and 02, respectively.
- Original topics 03 and 04: actual Document 03, including South African payments and insurance billing/domain analysis.
- Original topics 05 and 06: actual Document 04, including functional baseline, traceability and proposed solution.

All four source snapshots are included. Existing tables in historical PDFs remain untouched; future formal narrative documents and new register entries contain no tables or em dashes.

## 3. Volume 02: Requirements and architecture (planned)

The following original topics remain required, elaborated as living specifications before the dependent milestone. The current foundation extracts do not constitute final detailed specifications.

### Original topic 07: Business Requirements Specification

Status: planned. Design prerequisite: M00; detailed stakeholder responsibilities, business outcomes and scope.

### Original topic 08: Functional Requirements Specification

Status: planned. Design prerequisite: M00 initial slice, then before affected milestones.

### Original topic 09: Non-Functional Requirements Specification

Status: planned. Design prerequisite: M00; calibrate targets and verify release controls.

### Original topic 10: System Architecture and Design

Status: planned. Design prerequisite: M00; application ownership, topology, interfaces and security.

### Original topic 11: Financial Domain Model and Data Architecture

Status: planned. Design prerequisite: M02; data entities, ownership and migration design.

### Original topic 12: Financial Ledger and Accounting Design

Status: planned. Design prerequisite: M02 primitive and M10 full specification.

### Original topic 13: Payment Orchestration and State Machine Specification

Status: planned. Design prerequisite: M05-M07; before any dispatch.

### Original topic 14: Reconciliation Engine Specification

Status: planned. Design prerequisite: M07 minimal independent matching, M11-M12 complete design.

### Original topic 15: Enterprise Integration and API Contracts

Status: planned. Design prerequisite: M04, and before each provider/partner adapter.

### Original topic 16: Security, Governance and Regulatory Considerations

Status: planned. Design prerequisite: M00/M01 baseline, before each sensitive capability, M16 assessment.

### Original topic 17: Technology Selection and Architecture Decision Record

Status: planned. Design prerequisite: M00; version pins and feasibility evidence.

Additional approved workstreams: ESB integration, messaging, SFTP/file exchange, data lake and analytical architecture, semantic model and BI, TPPP/regulatory boundary assessment. Integrate these into the relevant volume topic and milestone specifications, without silently omitting them.

## 4. Volume 03: Implementation and verification (progressive)

### Original topic 18: Engineering Implementation Plan

Status: planned. Timing: M00/M01, maintain milestone-specific instructions.

### Original topic 19: Testing and Verification Strategy

Status: planned. Timing: M00, maintain with each release.

### Original topic 20: Synthetic Data and Simulation Design

Status: planned. Timing: M02/M03 and before provider fixtures.

### Original topic 21: Performance and Scalability Assessment

Status: planned. Timing: M20, using measured workloads.

### Original topic 22: Financial Integrity and Reliability Assessment

Status: planned. Timing: continuous; consolidate M20/M22.

### Original topic 23: Security and Threat Modelling Assessment

Status: planned. Timing: baseline M00, M16 formal review.

### Original topic 24: Legacy Migration and Enterprise Implementation Strategy

Status: planned. Timing: M18 design and verified cutover/rollback.

### Original topic 25: Deployment, Monitoring and Operational Runbook

Status: planned. Timing: incrementally from M01, final M23.

## 5. Volume 04: Improvements and future development (planned)

### Original topic 26: Functional Expansion and Improvement Assessment

Status: planned. Timing: M18-M19; compare to public baseline without claiming missing vendor features.

### Original topic 27: Financial Intelligence and AI Feasibility Assessment

Status: planned. Timing: M21; optional implementation, documented evaluation or deferral.

### Original topic 28: Proposed Product Development Roadmap

Status: planned. Timing: after measured baseline and expansion results.

### Original topic 29: Independent Technical Review

Status: planned. Timing: M22; independent evidence and remediation.

### Original topic 30: Final Engineering Assessment and Lessons Learned

Status: planned. Timing: M23; measured results and unresolved limitations.

## 6. Volume 05: Presentation and portfolio bundle (M23)

Executive brief; business case; engineering case study; executive presentation; technical presentation; live demonstration; technical walkthrough video; functional demonstration video; evidence appendix; reproducible GitHub repository; portfolio entry; interview preparation dossier. Each is planned. Ensure consistent scope, real evidence, independent project identity and explicit limitations. Hosted deployment status may be verified, deferred or blocked; local reproducibility remains required.

## 7. Document maintenance

Every new specification identifies its source baseline, predecessor, owner, revision, affected requirements and decision IDs, approval status, linked implementation and test evidence. Update this register with path, commit and date after approval. Do not replace source snapshots or invent achieved results. Use original Lato and Liberation Sans visual styling for formal PDF deliverables, original project-specific headings, no tables or em dashes. The new Markdown foundation is version 0.1.0, issued 26 November 2026. It is a bridge between discovery and the remaining volumes, not a replacement.

## 8. M00 engineering designs prepared for review

- V02-T07 to V02-T10 and V02-T16: [architecture assessment](milestones/m00/M00_ARCHITECTURE_ASSESSMENT.md) documents initial stakeholder and application ownership, integration, security and deployment requirements.
- V02-T11 to V02-T14: [financial contract baseline](milestones/m00/M00_FINANCIAL_CONTRACT_BASELINE.md) defines preliminary controls and independent worked examples. M02 through M12 retain the detailed specification gates.
- V02-T15: [architecture assessment](milestones/m00/M00_ARCHITECTURE_ASSESSMENT.md) defines integration contract boundaries pending reviewed schemas.
- V02-T17: [technology selection](milestones/m00/M00_TECHNOLOGY_SELECTION.md) and [host findings](milestones/m00/M00_DEVELOPMENT_ENVIRONMENT.md) record candidate choices and execution evidence.
- V03-T18 and V03-T19: [M01 preparation](milestones/m00/M00_M01_IMPLEMENTATION_PREPARATION.md) and [architecture verification](milestones/m00/M00_ARCHITECTURE_VERIFICATION.md) describe release sequencing and probe coverage.
- The [completion report](milestones/m00/M00_COMPLETION_REPORT.md) records gate status. These are repository specifications for review and preserve the formal volume and document numbering plan.

## M01 foundation update

The M01 implementation, infrastructure, database, identity, developer, verification and completion records are maintained under `docs/milestones/m01/`. They support the original Volume 02 and Volume 03 topics without changing the five-volume programme.
