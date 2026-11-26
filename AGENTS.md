# EPI | engineering instructions for Codex and contributors

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Read before working

Read `README.md`, `docs/PROGRAMME_SPECIFICATION.md`, `docs/REQUIREMENTS_REGISTER.md`, `docs/ARCHITECTURE_DECISIONS.md`, `docs/SYSTEM_ARCHITECTURE.md`, `docs/FINANCIAL_INVARIANTS.md`, `docs/IMPLEMENTATION_ROADMAP.md`, `docs/VERIFICATION_STRATEGY.md`, `docs/RESEARCH_ASSUMPTIONS_EVIDENCE.md` and `docs/DOCUMENTATION_REGISTER.md`. Consult the immutable approved PDFs in `docs/discovery/` where source wording or a conflict matters. Run `python3 scripts/validate_baseline.py` before changing baseline documents. Current stage is M00 preparation; do not assume later implementation is authorised.

## 2. Work discipline

- Inspect canonical checkout, branch, status, existing code and uncommitted work before edits. Preserve unrelated work. Do not overwrite user modifications, reset, clean, force push, deploy or provision external resources without explicit authorisation.
- Work on the named milestone only. Resolve discrepancies with the maintainer. Plan files, contracts, migrations, tests, dependency decisions and evidence before coding. Do not introduce unapproved stack changes, rename identifiers or silently change scope.
- Keep four independent applications and separately owned persistence. Use explicit contracts; no cross-application domain writes or fabricated provider evidence. Shared infrastructure does not merge business authority.
- Preserve exact monetary types, balanced immutable postings, idempotency, independent provider enquiry, durable acceptance, tenant boundaries, maker/checker approval and separate execution/settlement/allocation states. No simulated dispatch until approved controls and tests are in place. Never treat timeout as failed execution, or an acknowledgement as settlement.
- All data, providers, mandates and funds are synthetic. Never use live bank/payment interfaces, real consumer data, non-public Q LINK/Sanlam materials or secrets. No regulatory certification, production parity or AI capability claims without evidence. AI remains optional, non-authoritative and downstream of deterministic verification.
- Maintain documentation, migration and configuration examples alongside code. Formal documents use no tables, no em dashes and original project-specific content. No fake metrics or UI-only placeholders represented as functioning backend features.

## 3. Verification and release

Execute relevant unit, real DB integration, contract, broker/SFTP, E2E, security and failure tests. Report exact commands, exit codes, pass/fail/skip/blocked counts, commit and environment. Do not claim a skipped test passed. Add requirement-linked evidence; separate independent expected values from actual outputs. Do not weaken tests to obtain a green run. Resolve financial and critical security defects before acceptance. If environment constraints prevent verification, state what was and was not verified, preserve evidence, and request a scoped approval for any alternative path rather than silently lowering standards.

## 4. Milestone completion report

State: milestone ID, baseline revision, implemented requirements, architecture/contract changes, files, migration status, test commands and results, evidence paths, unresolved blockers, next gate and approval request. Update appropriate registers and changelog. Only commit/push if the specific user instruction authorises it. Never claim an external deployment or review occurred if not verified. M00 requires maintainer approval before M01; future milestone prompts must explicitly authorise the scope.

## 5. Permanent milestone delivery rules

- Use `/Users/keenosmith/Programming/Projects/qlink-moneyhub/enterprise-payments-infrastructure` as the canonical local checkout and GitHub as the authoritative remote engineering source. Preserve the original engineering baseline, immutable discovery sources and canonical IDs.
- Apply these delivery rules to M00 through M23. Each milestone prompt explicitly authorises its own work. Completion requires staging, reviewing, committing and pushing all intended changes on the milestone branch, then proving that the local commit equals the remote branch tip and that the working tree is clean.
- Run all applicable tests, builds, migrations, static analysis and verification checks. Investigate failures and rerun after remediation. Never weaken, disable or remove checks to get a pass, silently skip applicable verification or report a command as run if it was not executed.
- Check applicable GitHub Actions runs for the final pushed commit. Inspect failures, push reviewed corrective commits and verify the replacement runs. Investigate safe alternatives when a command or environment initially fails. If an external blocker persists, preserve evidence, push completed work when possible, identify the unverified condition and report the milestone as blocked or incomplete.
- Update technical documentation, registers and verification evidence with the work. Keep new project documentation free of tables, em dashes, private motivations, private conversations and confidential third-party information.
- Keep work inside the named milestone and repository. Do not merge to main without explicit maintainer approval or automatically start the next milestone.
