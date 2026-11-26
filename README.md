# Enterprise Payments Infrastructure | Engineering Foundation Bundle

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

This is the repository-ready engineering baseline for an independent reference implementation in the South African insurance and payments domain. Enterprise Payments Infrastructure (EPI) is the approved project identity; suggested repository slug: `enterprise-payments-infrastructure`. The four original discovery PDFs are included unchanged. The original discovery bundle did not itself create a repository or establish engineering verification; subsequent milestone work is recorded below.

## Start here

1. Read [Programme specification](docs/PROGRAMME_SPECIFICATION.md) and the approved discovery PDFs in `docs/discovery/`.
2. Review [Requirements register](docs/REQUIREMENTS_REGISTER.md), [Architecture decisions](docs/ARCHITECTURE_DECISIONS.md), [System architecture](docs/SYSTEM_ARCHITECTURE.md) and [Financial invariants](docs/FINANCIAL_INVARIANTS.md).
3. Read [Research, assumptions and evidence](docs/RESEARCH_ASSUMPTIONS_EVIDENCE.md), [Implementation roadmap](docs/IMPLEMENTATION_ROADMAP.md), [Verification strategy](docs/VERIFICATION_STRATEGY.md) and [Documentation register](docs/DOCUMENTATION_REGISTER.md).
4. Review root [AGENTS.md](AGENTS.md) before giving Codex any instruction. Run `python3 scripts/validate_baseline.py` from the extracted folder. The validator checks source fingerprints, canonical identifier coverage and baseline catalogue text; it does not test software or establish completeness of external research.
5. Review the accepted M00 foundation baseline and current M01 records. No payment dispatch is permitted before the relevant financial and authority controls pass.

## Why Markdown now

These files implement the persistent controls required by Document 04 sections 21 and 23. They are not a new volume, a replacement for the remaining volumes or an alternative set of requirements. The detailed business and architecture specifications still belong to Volume 02. Draft them in the repository, before implementing the dependent component; publish formal PDFs as appropriate. Preserve original volume topic references, without renumbering Documents 01-04.

## Repository use

Extract the ZIP into an empty local project folder. Keep this structure when initialising Git. The original PDFs are immutable discovery snapshots. `baseline.json` is a generated initial machine-readable catalogue and source fingerprint manifest; Markdown is the human-readable working baseline. Subsequent approved changes require an explicit revision of both representations, with history retained. Do not silently regenerate a changed baseline to make the checker pass. The `docs/discovery` PDFs retain their original approved formatting, including historical tables; all new Markdown uses headings and paragraphs rather than tables. No private material is included.

Current status: M00 was accepted for foundation implementation and M01 is in progress. The repository includes synthetic application foundations and a local development stack. See the [M01 implementation report](docs/milestones/m01/M01_IMPLEMENTATION_REPORT.md) and [completion report](docs/milestones/m01/M01_COMPLETION_REPORT.md) for verified status.

## M00 engineering specifications

See the [M00 completion report](docs/milestones/m00/M00_COMPLETION_REPORT.md) for the provisional design, executed probes and open acceptance gates.
# enterprise-payments-infrastructure

## M01 local development

Install Python 3.14, Node.js 24, Git, Docker with Compose and OpenSSH client tools. From a fresh checkout run `make bootstrap` and `make up`. The [developer environment](docs/milestones/m01/M01_DEVELOPER_ENVIRONMENT.md) lists the four application URLs, synthetic login, profiles and shutdown procedure. The local configuration is for synthetic development only.
