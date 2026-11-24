# QA Engineering Portfolio — Artem Kalinin

**Target roles:** Junior QA Engineer · API Tester · QA Automation Engineer (Python)

A focused index of independent QA case studies. The projects demonstrate how I translate requirements into risk-based checks, test API contracts and browser workflows, investigate negative and boundary cases, document defects, and retain reproducible CI evidence.

> **Portfolio scope:** these are self-directed practice projects and authored test targets. They are not represented as commercial client deliveries or production testing experience. Each project states what is simulated and what its tests actually verify.

## Evidence at a glance

| Area | Evidence | What it demonstrates |
|---|---|---|
| API automation | [Python API Automation](./api-automation/) — 62 tests; CI on Python 3.10 and 3.12 | REST CRUD, JSON Schema, positive/negative cases, pagination, timeouts, safe retry boundaries |
| API quality / test design | [Booking API QA Sandbox](./qa-cases/api-contract-negative/) — 31 tests; 100% statement coverage for `app.py` and `store.py` | Risk-based coverage, authorization, idempotency, booking invariants, boundary validation and traceability |
| Web checkout regression | [Checkout & Cart QA](./qa-cases/checkout-regression/) — 24 Playwright scenarios | Revenue-critical flows, calculations, promotions, stock limits, form validation and duplicate-submit protection |
| UI automation + manual QA | [Playwright QA Lab](https://github.com/blvxx/playwright-qa-lab) — 11 E2E tests and 20 documented manual cases | Browser regression, accessibility checks, persistence, responsive smoke and defect documentation |
| Integration / system QA | [FinTech QA Platform](./fintech-qa-platform/) | API and service integration, PostgreSQL, Docker Compose, ledger invariants, browser flows and observability |

## Featured case studies

### 1. Python API Automation

**Stack:** Python · pytest · requests · JSON Schema · Postman · Allure · GitHub Actions

A reusable REST client and automated suite against the public JSONPlaceholder demo API, complemented by isolated client tests and deterministic local HTTP fault injection.

- CRUD methods and response contracts for Posts and Comments.
- Positive, negative and parametrized validation scenarios.
- JSON Schema checks for request and response payloads.
- Pagination boundaries, timeout propagation and malformed response handling.
- Retry policy verifies that transient read requests can retry while write requests are not automatically replayed.
- Importable Postman collection and CI reporting.

**Evidence:** [README and test plan](./api-automation/) · [Successful CI run — 23 Nov 2026](https://github.com/blvxx/portfolio/actions/runs/45102695248)

**Boundary:** JSONPlaceholder simulates writes; successful POST/PUT/PATCH/DELETE responses do not prove persistent server-side changes. The suite does not claim production authentication, database, load or security coverage.

### 2. Booking API — Contract and Negative Testing

**Stack:** Python · FastAPI · pytest · Pydantic · coverage · GitHub Actions

A self-contained API and test suite for a fictional booking service.

- 31 automated test cases.
- 100% statement coverage for the authored `app.py` and `store.py` modules in the verified run.
- Contract checks for status codes, response fields and pagination.
- Boundary and negative scenarios for dates, capacity and invalid payloads.
- Authorization and cross-user access checks.
- Overlapping reservations, cancellation and idempotency replay.
- Requirement-to-test traceability and hypothetical defect examples, clearly labelled as such.

**Evidence:** [Project README](./qa-cases/api-contract-negative/) · [Test matrix](./qa-cases/api-contract-negative/test-matrix.md) · [Successful CI run — 22 Nov 2026](https://github.com/blvxx/portfolio/actions/runs/44993766677)

**Boundary:** the API uses an isolated in-memory store and simplified test-token authentication. It does not verify database transactions, distributed concurrency or a production identity provider. 100% statement coverage is not the same as 100% branch or requirements coverage.

### 3. Checkout & Cart — Browser Regression

**Stack:** Python · pytest · Playwright · Chromium · GitHub Actions

A fictional storefront used to test a revenue-critical checkout workflow.

- 24 automated browser scenarios.
- Cart quantity and stock boundaries.
- Subtotal, discount and delivery-cost calculations.
- Valid, expired and unknown promotions.
- Required-field and email validation.
- Delivery / pickup state transitions.
- Successful confirmation and rapid duplicate-submit protection.
- Responsive layout and accessible form labels.
- CI retains JUnit results, traces and failure screenshots.

**Evidence:** [Project README](./qa-cases/checkout-regression/) · [Test plan](./qa-cases/checkout-regression/test-plan.md) · [Test cases](./qa-cases/checkout-regression/test-cases.md) · [Successful CI run — 22 Nov 2026](https://github.com/blvxx/portfolio/actions/runs/44993763830)

**Boundary:** the storefront, product catalogue and order confirmation are simulated. No real payment gateway, inventory backend or shipping provider is connected.

### 4. Playwright UI Automation Lab

**Stack:** JavaScript · Playwright · Chromium · GitHub Actions

A browser-based task tracker used for UI test design and accessibility regression.

- 11 automated end-to-end scenarios.
- 20 documented manual test cases and one exploratory responsive check.
- Empty/whitespace validation, keyboard submission, completion, deletion and persistence.
- Accessible names and semantic label interaction.
- Malformed local-storage recovery.
- Two accessibility findings documented, fixed in the sample application and covered by regression tests.

**Evidence:** [Repository](https://github.com/blvxx/playwright-qa-lab) · [Manual test cases](https://github.com/blvxx/playwright-qa-lab/blob/main/docs/test-cases.md) · [Execution report](https://github.com/blvxx/playwright-qa-lab/blob/main/docs/test-execution-report.md) · [Successful CI run — 23 Nov 2026](https://github.com/blvxx/playwright-qa-lab/actions/runs/45155361776)

**Execution note:** the manual report records an isolated Chromium harness run. The report documents the local-file navigation restriction and storage shim; native browser persistence is separately exercised by the Playwright CI suite. It is not presented as a user-operated production test session.

### 5. FinTech QA Engineering Platform

**Stack:** Python · FastAPI · pytest · Playwright · PostgreSQL · Docker Compose · Prometheus · Grafana

A fictional payment and ledger sandbox used to exercise API and service-integration behavior.

- Payment and Ledger service flows.
- Ledger debit/credit invariants and idempotent retry checks.
- PostgreSQL-backed integration tests.
- Docker Compose smoke checks and browser-level flows.
- Observability and a guarded dependency-outage/recovery drill.

**Evidence:** [Project overview](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/) · [Successful CI run — 23 Nov 2026](https://github.com/blvxx/portfolio/actions/runs/45100258032)

**Boundary:** payment providers and business transactions are simulated. This is a QA sandbox, not a deployed financial product or production certification.

## Test design and quality practices

| Practice | Portfolio evidence |
|---|---|
| Requirement decomposition and risk prioritisation | [Booking API test matrix](./qa-cases/api-contract-negative/test-matrix.md) · [Checkout test plan](./qa-cases/checkout-regression/test-plan.md) |
| Positive, negative and boundary testing | API Automation · Booking API · Checkout Regression |
| State-transition and business-rule testing | Booking lifecycle · Cart / promo / fulfilment transitions |
| API contract validation | HTTP status, headers, JSON Schema, response shape and pagination |
| UI regression and accessibility | Playwright QA Lab · Checkout Regression |
| Defect reporting | [Booking API examples](./qa-cases/api-contract-negative/bug-reports.md) · [Checkout examples](./qa-cases/checkout-regression/bug-reports.md) · [Playwright examples](https://github.com/blvxx/playwright-qa-lab/blob/main/docs/sample-bug-reports.md) |
| CI evidence | GitHub Actions, JUnit XML, coverage reports, Playwright traces and failure screenshots |

**Defect-report transparency:** examples marked hypothetical are test-design illustrations, not claims that a real customer or production system experienced those defects.

## Tools

**Automation:** Python · pytest · requests · Playwright · JavaScript · Postman  
**API / data:** HTTP · REST · JSON · JSON Schema · SQL · PostgreSQL  
**Test engineering:** test plans · test cases · traceability · risk-based testing · equivalence / boundary scenarios · negative testing · regression · exploratory checks · bug reports  
**Delivery:** Git · GitHub Actions · Docker Compose · Allure · JUnit XML · Playwright traces

## How I approach testing

1. Clarify expected behavior, scope, dependencies and business impact.
2. Identify the highest-risk paths and failure modes.
3. Derive positive, negative, boundary and state-transition scenarios.
4. Prepare isolated test data and repeatable setup.
5. Execute checks at the appropriate API, integration or UI level.
6. Record evidence, report reproducible defects and verify fixes.
7. Summarise coverage, limitations and residual risk.

## Additional engineering background

For roles combining QA with production troubleshooting, see the [Linux Support Engineering Lab](./support-engineering-lab/) and [Incident Investigation Lab](./incident-lab/). They demonstrate log analysis, SQL reconciliation, incident timelines, RCA and recovery verification.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)
