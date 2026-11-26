# Research, assumptions and evidence register

Baseline: EPI 0.1.0 | 26 November 2026 | Discovery documents approved; engineering design pending validation.

## 1. Evidence policy

The included discovery PDFs are the approved source snapshots. Product and industry assertions remain dated to the research in those documents. No fresh external-source or regulatory audit has been performed for this bundle. Distinguish direct public documentation, wider ecosystem evidence, inference, proposed design, approved decision and independently verified implementation. Never convert a proposed design into a vendor fact. Do not use non-public materials or real data. Before production-facing claims, revalidate current official legal and scheme sources and obtain appropriate permissions and independent review; real payment activity is excluded.

Document 02 classification: D (documented public capability or relationship), E (wider ecosystem evidence, not proven native), I (engineering interpretation, not recovered specification), U (unresolved), P (proposed independent design). Use the separate state VERIFIED only for actual implementation evidence.

## 2. Immutable source manifest

### D01

File: `docs/discovery/01_Independent_Engineering_Exploration_Brief_Revised.pdf`. Pages: 5. SHA-256: `12e09d9eacd7dc2eea02fb5c2d93954e1e73d5852cb5acc93b0bc1f055379d00`. Status: approved discovery snapshot.

### D02

File: `docs/discovery/02_Comprehensive_MoneyHub_Current_State_Assessment.pdf`. Pages: 14. SHA-256: `01373df0d4e63f647122a60dc1408668e5a73b224751c7eb8b6336994c91a3d5`. Status: approved discovery snapshot.

### D03

File: `docs/discovery/03_South_African_Payments_Collections_and_Insurance_Infrastructure_Assessment.pdf`. Pages: 16. SHA-256: `c7fee0383c6967c9afc13c0c27b2eb762d1a3d8660ae78ae36df831d1d1b3398`. Status: approved discovery snapshot.

### D04

File: `docs/discovery/04_Proposed_Solution_and_Engineering_Requirements.pdf`. Pages: 28. SHA-256: `9eaa585dc593161fae870be990644d71bb4c348a9286cb309b0bba374773d3ec`. Status: approved discovery snapshot.

## 3. MoneyHub unresolved questions (Document 02 section 22)

### U-01

Sanlam implementation scope. Which business unit, systems and payment streams are included? Is the engagement a new implementation, integration extension or legacy migration?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-02

Financial ownership. Does the client or MoneyHub own particular billing, mandate, settlement and ledger records? Which system is authoritative for each financial state?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-03

Interfaces and topology. Which file schemas, transport methods, brokers, APIs, service boundaries and deployment models apply to the specific implementation?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-04

Technology stack. What parts of the solution run on IRIS, Python or other platforms? Which databases and analytics tools are actually deployed?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-05

Financial matching. What are the exact three reconciliation sources, matching rules, settlement calendars, treatment of fees and correction procedures?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-06

Operational and compliance controls. What are the actual access boundaries, control procedures, throughput, recovery objectives, audit obligations and regulatory roles?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

### U-07

Intelligence. Which AI-related initiatives are operational and which remain exploratory? What evaluations support their use?

Status: OPEN; independent project design may proceed without resolving the vendor-specific question. Owner: research/design lead. No private evidence is required.

## 4. Programme assumptions and risks

### ASM-001: representative insurer

The PAS owns obligations and claims; the hub processes instructions. This is our independent boundary, not a verified Sanlam implementation. Validate through PAS contract and full lifecycle. Links: ADR-P01/P05, FR-001-004.

### ASM-002: independent simulated provider evidence

Synthetic banks and payroll providers implement explicit authority, operation and settlement semantics. Not scheme-certified or actual provider formats. Validate with independently generated statements, incompatible contracts and fault scenarios. Links: ADR-P06/P08, FR-014-025.

### ASM-003: local infrastructure feasibility

Python/SQL direction and proposed broker, object store and identity services need compatibility, licensing, footprint and fault checks on intended hardware. Links: ADR-P03/P04/P07/P08, NFR-005/009. Status: unverified.

### ASM-004: reporting environment

Power BI verification depends on compatible tooling and licensing. Preserve BI-ready extracts and browser reporting; do not claim Microsoft integration without a successful run. Links: FR-033, NFR-008.

### ASM-005: regulatory snapshot

Industry assessment is dated 25 November 2026; bank contracts, scheme formats, actual legal policies and final authorisation reforms are not verified for a live implementation. No real processing, compliance, custody or TPPP certification claim. Links: NFR-011.

### ASM-006: scale targets

100,000 synthetic policyholders, up to one million events, proposed 100 accepted instructions/s for ten minutes and p95 durable intake <=500 ms. Targets only; hardware, event mix and limits to be frozen before test. Links: NFR-005.

Document 04 section 22 risks follow:

Financial modelling risk. A superficially plausible journal may misrepresent custody, allocation or period treatment. Mitigate with the dedicated ledger specification, independent source reconciliation, exact-value tests and a review of accounting assumptions. Full insurance accounting is excluded.

External contract risk. Simulated bank or payroll behaviour may differ substantially from private scheme and provider contracts. Mitigate by explicitly labelling each fixture, defining adapter capabilities and testing multiple independent schemas. Actual bank certification is outside scope.

Distributed execution risk. Duplicate delivery, uncertain provider response or restored local state may create a second external effect. Mitigate with durable identities, unknown-state holds, independent enquiry and recovery reconciliation. A provider with neither idempotency nor enquiry requires a conservative manual boundary.

Infrastructure complexity risk. Four applications, integration services, analytics and observability may exceed local resource capacity. Start with a minimal vertical slice, share infrastructure only where access is isolated, benchmark resource use and add components when justified. Avoid unnecessary brokers and orchestration systems.

Reporting and licensing risk. Power BI development or deployment may require an environment or licence not available locally. Maintain a working SQL/data extract and browser reporting path, record the actual blocker and do not label the Microsoft integration complete without evidence.

Scope and traceability risk. A large programme can drift from the original product baseline or prematurely treat an assumption as a fact. Preserve the crosswalk in Section 17, enforce requirement-level change control, and review the source evidence before making external product or regulatory claims. Documents 02 and 03 remain their existing revisions; this crosswalk resolves the identifier collision but does not constitute an exhaustive revalidation of all their external references.

## 5. Public evidence register: Document 02

### D02.S01

Q LINK | MoneyHub Primary product description; direct functional baseline, not implementation detail.

### D02.S02

Q LINK | About Q LINK and solutions portfolio Company context and wider service portfolio.

### D02.S03

Competition Tribunal | SPE Mid-Market Fund I / Q Link, LM107OCT21 10 December 2021. Official merger reasons; paragraphs 6-8 establish historic service relationship and information-sharing considerations. Public redactions retained.

### D02.S04

EBnet | Sanlam Private Equity acquisition announcement 12 July 2022. Reported acquisition and MoneyHub expansion rationale.

### D02.S05

Apis Partners | Sale of interest in Q Link 31 May 2022. Investor announcement corroborating ownership transaction.

### D02.S06

InterSystems | Enabling Responsible Money Movement Across South Africa Indexed October 2026. Technology partner case study; IRIS, integration and strategic development direction. Vendor-reported evidence.

### D02.S07

Q LINK | Bank Collections Recurring processing, pre-validation, mandate management and optimisation.

### D02.S08

Q LINK | Collections Solutions Current wider collection offerings; not a client-specific feature list.


### D02.S09

Q LINK | Payroll Collections Employer rules, validation, affordability and electronic reconciliation.

### D02.S10

Q LINK | Payments Solutions Online Payment System and Automated Payment System; wider disbursement services.

### D02.S11

MyJobMag | Sanlam Debit Order Team Leader and Analyst 18 May 2021. Historical recruitment advertisement naming Q LINK in SDM operations.

### D02.S12

MyJobMag | Jobs at Sanlam 22 June 2021. Historical operational reference to Q LINK and bank billing/collections.

### D02.S13

LinkedIn | Sanlam Collections Analyst 2026 indexed search result. Listing redirects; SQL Server and BI evidence treated as secondary and limited.

### D02.S14

LinkedIn | Stefan Cronje, professional profile Indexed description of Old Mutual CMoS. Direct retrieval restricted; supports only the limited comparable implementation description.

### D02.S15

Q LINK | Is your Business geared for the changes within the Payments Landscape? Industry insights publication by Leana Hanscomb; Q LINK API, online and SFTP integration options.

### D02.S16

South African Reserve Bank | Payments and Settlements Authoritative payment-system participant and regulatory context.

### D02.S17

South African Reserve Bank | Payments Ecosystem Modernisation Programme Industry development direction and payment interoperability context.

### Embedded PDF source links

- Page 13: Q LINK | MoneyHub | <https://www.qlink.co.za/moneyhub.php>

- Page 13: Q LINK | About Q LINK and solutions portfolio | <https://www.qlink.co.za/about-us.php>

- Page 13: Competition Tribunal | SPE Mid-Market Fund I / Q Link, LM107OCT21 | <https://comptrib.co.za/uploads/topics/CompTrib_Case_Files/PUBLIC%20Reasons%20-%20SPE%20And%20QLink%20LM107OCT21%20%2810122021%29%20corrected.pdf>

- Page 13: EBnet | Sanlam Private Equity acquisition announcement | <https://www.ebnet.co.za/sanlam-private-equity-announces-acquisition-of-controlling-interest-in-q-link/>

- Page 13: Apis Partners | Sale of interest in Q Link | <https://www.apis.pe/news/apis-growth-fund-i-announces-sale-of-interest-in-q-link-to-sanlam-private-equity/>

- Page 13: InterSystems | Enabling Responsible Money Movement Across South Africa | <https://www.intersystems.com/it/success-stories/q-link-money-movement-south-africa-success-story/>

- Page 13: Q LINK | Bank Collections | <https://www.qlink.co.za/services_Bank_Collections.php>

- Page 13: Q LINK | Collections Solutions | <https://www.qlink.co.za/collections.php>

- Page 14: Q LINK | Payroll Collections | <https://www.qlink.co.za/services_Payroll_Collections.php>

- Page 14: Q LINK | Payments Solutions | <https://www.qlink.co.za/payments.php>

- Page 14: MyJobMag | Sanlam Debit Order Team Leader and Analyst | <https://www.myjobmag.co.za/job/debit-order-team-leader-and>

- Page 14: MyJobMag | Jobs at Sanlam | <https://www.myjobmag.co.za/jobs/jobs-at-sanlam-29>

- Page 14: LinkedIn | Sanlam Collections Analyst | <https://za.linkedin.com/jobs/view/collections-analyst-at-sanlam-4438337527>

- Page 14: LinkedIn | Stefan Cronje, professional profile | <https://za.linkedin.com/in/stefan-cronje-062a6438>

- Page 14: Q LINK | Is your Business geared for the changes within the Payments Landscape? | <https://www.qlink.co.za/assets/documents/Is%20Your%20Business%20Geared%20For%20The%20Changes%20Within%20The%20Payments%20Landscape.pdf>

- Page 14: South African Reserve Bank | Payments and Settlements | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements>

- Page 14: South African Reserve Bank | Payments Ecosystem Modernisation Programme | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements/pem>

## 6. Public evidence register: Document 03

### D03.S01

South African Government | National Payment System Act 78 of 1998 Statutory payment, clearing and settlement framework.

### D03.S02

SARB | Payments and Settlements NPS responsibility and participant categories.

### D03.S03

SARB | Regulation Oversight, directives and consultation status; NPS cyber and payment initiation context.

### D03.S04

SARB | Domestic Settlement Services SAMOS and settlement services.

### D03.S05

SARB | PSMB Transition 2026 PASA transition, transfer dates and interim registration arrangements.

### D03.S06

SARB | 2007 non-bank stakeholder directives announcement Historical directive context for payments involving third persons.

### D03.S07

Prudential Authority | Communication 10 of 2026 Consultation on proposed exemption and authorisation framework; not final legislation.

### D03.S08

SARB | Rewiring Payments: Open. Connected. Inclusive. October 2026 speech; intended reform timeline, not evidence of promulgation.

### D03.S09

PASA | Debit Orders Historical industry explanation of three debit-order types.

### D03.S10

PASA | Debit Payments Historical overview of debit authority and mandate concepts.

### D03.S11

SARB | Payments Ecosystem Modernisation Programme Modernisation direction, PayShap and interoperability.

### D03.S12

Q LINK | Payments Solutions Vendor description of disbursement services; not a private implementation specification.

### D03.S13

South African Government | Insurance Act 18 of 2017 Insurance regulatory context.

### D03.S14

South African Government | Financial Sector Regulation Act 9 of 2017 Prudential Authority and FSCA framework.

### D03.S15

Acts Online | PPR Rule 15A: Payment of Premiums Secondary reproduction; premium non-payment and notification provisions; current applicability needs validation.

### D03.S16

LawLibrary | Policyholder Protection Rules (Long-term Insurance), 2017 Historical consolidation as at October 2018; Rule 2A and policy protection context.

### D03.S17

South African Government | Basic Conditions of Employment Act 75 of 1997 Employment law foundation; section 34 deductions.

### D03.S18

Department of Employment and Labour | Basic Guide to Deductions General guidance; not a complete payroll scheme contract.

### D03.S19

Q LINK | Payroll Collections Vendor description of validation and affordability capabilities.

### D03.S20

IFRS Foundation | IFRS 17 Insurance Contracts Insurance accounting context; not an implementation of IFRS 17.

### D03.S21

Q LINK | MoneyHub Product reference for integration and reconciliation capabilities, as assessed in Document 02.

### D03.S22

South African Government | Protection of Personal Information Act 4 of 2013 Personal information protection framework.

### D03.S23

Information Regulator | Handling of security compromises Security compromise escalation and notification guidance.

### D03.S24

Financial Intelligence Centre | Compliance and supervision Accountable institutions, risk management, due diligence and reporting context.

### D03.S25

SARB | Joint Communication 5 of 2026 Joint IT governance and cyber-resilience incident notification context.

### Embedded PDF source links

- Page 15: South African Government | National Payment System Act 78 of 1998 | <https://www.gov.za/ss/documents/national-payment-system-act>

- Page 15: SARB | Payments and Settlements | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements>

- Page 15: SARB | Regulation | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements/regulation>

- Page 15: SARB | Domestic Settlement Services | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements/settlement-services>

- Page 15: SARB | PSMB Transition | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements/psmb>

- Page 15: SARB | 2007 non-bank stakeholder directives announcement | <https://www.resbank.co.za/en/home/publications/publication-detail-pages/media-releases/2007/4256>

- Page 15: Prudential Authority | Communication 10 of 2026 | <https://www.resbank.co.za/en/home/publications/publication-detail-pages/prudential-authority/pa-public-awareness/Communication/2026/prudential-communication-10-of-2026>

- Page 15: SARB | Rewiring Payments: Open. Connected. Inclusive. | <https://www.resbank.co.za/en/home/publications/publication-detail-pages/speeches/speeches-by-governors/2026/kganyago-payments-conference>

- Page 15: PASA | Debit Orders | <https://pasa.org.za/pasa-resources/pasa-debit-orders/>

- Page 16: PASA | Debit Payments | <https://pasa.org.za/about-payments/introduction-to-payments/debit-payments/>

- Page 16: SARB | Payments Ecosystem Modernisation Programme | <https://www.resbank.co.za/en/home/what-we-do/payments-and-settlements/pem>

- Page 16: Q LINK | Payments Solutions | <https://www.qlink.co.za/payments.php>

- Page 16: South African Government | Insurance Act 18 of 2017 | <https://www.gov.za/documents/acts/insurance-act-18-2017-english-afrikaans-18-jan-2018>

- Page 16: South African Government | Financial Sector Regulation Act 9 of 2017 | <https://www.gov.za/documents/financial-sector-regulation-act-9-2017-english-sepedi-22-aug-2017-0000>

- Page 16: Acts Online | PPR Rule 15A: Payment of Premiums | <https://www.acts.co.za/long-term-insurance-act-1998/n1407_rule_15a__payment_of_pre>

- Page 16: LawLibrary | Policyholder Protection Rules (Long-term Insurance), 2017 | <https://lawlibrary.org.za/akn/za/act/gn/2017/1407/eng%402018-10-01>

- Page 16: South African Government | Basic Conditions of Employment Act 75 of 1997 | <https://www.gov.za/documents/basic-conditions-employment-act>

- Page 16: Department of Employment and Labour | Basic Guide to Deductions | <https://www.labour.gov.za/DocumentCenter/Pages/Basic-Guide-to-Deductions.aspx>

- Page 16: Q LINK | Payroll Collections | <https://www.qlink.co.za/services_Payroll_Collections.php>

- Page 16: IFRS Foundation | IFRS 17 Insurance Contracts | <https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/>

- Page 16: Q LINK | MoneyHub | <https://www.qlink.co.za/services_MoneyHub.php>

- Page 16: South African Government | Protection of Personal Information Act 4 of 2013 | <https://www.gov.za/documents/protection-personal-information-act>

- Page 16: Information Regulator | Handling of security compromises | <https://inforegulator.org.za/2025/08/19/fact-sheet-handling-of-security-compromises/>

- Page 16: Financial Intelligence Centre | Compliance and supervision | <https://www.fic.gov.za/compliance/>

- Page 16: SARB | Joint Communication 5 of 2026 | <https://www.resbank.co.za/en/home/publications/publication-detail-pages/prudential-authority/pa-public-awareness/Communication/2026/joint-communication-5-of-2026-determination-of-notification-template-for-material-it-and-cyber-incidents>

## 7. Implementation evidence record format

Create EVD-0001 onwards only when work is executed. Required fields: ID, requirement and scenario IDs, milestone, commit, run ID, UTC timestamps, environment and versions, dataset seed/hash, inputs, independent expected result, actual result, status (pass/fail/skipped/blocked), artefact path and SHA-256, reviewer, limitations and corrective action. Keep secrets and private data out of artefacts. No implementation evidence exists at baseline initialisation.
