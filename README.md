# Artem Kalinin — QA Engineering Portfolio

**QA Engineer · API / Web / Mobile Testing · Android TV / Smart TV · Python Automation**

A quality-engineering portfolio focused on product risk, API and integration quality, web/mobile user journeys, device compatibility, test automation and release decisions.

**[QA Portfolio — evidence and case studies](./qa-portfolio.md)** · [QA Engineering Strategy](./qa-engineering-strategy.md) · [Mobile / TV Checklist](./qa-mobile-tv-checklist.md) · [Business-value Casebook](./qa-commercial-casebook.md) · [GitHub Profile](https://github.com/blvxx)

## Positioning

This portfolio is structured around middle-level QA responsibilities: independently analysing requirements, identifying product and data risks, designing traceable coverage, choosing test levels, investigating defects, verifying fixes and communicating release risk.

It combines web, mobile and API testing experience with executable public evidence from independent automation and integration projects.

## Choose a route

| Target role | Start with | Evidence |
|---|---|---|
| **QA Engineer / Middle Manual QA** | [QA Portfolio](./qa-portfolio.md) · [QA Strategy](./qa-engineering-strategy.md) | Risk analysis, test plans, traceability, manual and exploratory testing, defect lifecycle, release gates |
| **API QA / QA Automation (Python)** | [API Automation](./api-automation/) · [Booking API](./qa-cases/api-contract-negative/) | 62 API tests, 31 contract/business-rule tests, JSON Schema, negative cases, idempotency and CI |
| **Mobile / Android TV / Smart TV QA** | [Mobile & TV Checklist](./qa-mobile-tv-checklist.md) | Lifecycle, permissions, network resilience, D-pad/focus, remote control, installation and media playback scenarios |
| **Web QA / UI Automation** | [Checkout Regression](./qa-cases/checkout-regression/) · [Playwright QA Lab](https://github.com/blvxx/playwright-qa-lab) | 24 checkout scenarios, 11 E2E tests, 20 manual cases, accessibility and responsive checks |
| **FinTech / Integration QA** | [FinTech QA Platform](./fintech-qa-platform/) | Payment/Ledger integration, PostgreSQL, transaction invariants, observability and failure/recovery checks |
| **Application Support / Support Engineer** | [Linux Support Lab](./support-engineering-lab/) · [Incident Investigation](./incident-lab/) | Log triage, SQL diagnostics, RCA, incident timelines and recovery verification |

## QA case studies

### 1. Python API Automation
A reusable requests client and pytest suite for REST CRUD contracts, JSON Schema, negative and boundary cases, pagination, timeout propagation and safe retry behavior. The reviewed CI run passed 62 tests on Python 3.10 and 3.12.

[Project overview](./api-automation/) · [Successful CI run](https://github.com/blvxx/portfolio/actions/runs/45102695248)

### 2. Booking API — Contract and Business-rule Testing
A fictional booking API with 31 pytest cases covering request/response contracts, pagination, validation, authorization, overlapping reservations, cancellation and idempotency. CI enforces 100% statement coverage for the authored app.py and store.py modules.

[Project overview](./qa-cases/api-contract-negative/) · [Test matrix](./qa-cases/api-contract-negative/test-matrix.md) · [Successful CI run](https://github.com/blvxx/portfolio/actions/runs/44993766677)

### 3. Checkout & Cart — Web Regression
A fictional storefront with 24 Playwright scenarios covering cart and stock boundaries, price calculations, promotions, fulfilment transitions, checkout validation and duplicate-submit protection. CI retains JUnit output, traces and failure screenshots.

[Project overview](./qa-cases/checkout-regression/) · [Test plan](./qa-cases/checkout-regression/test-plan.md) · [Successful CI run](https://github.com/blvxx/portfolio/actions/runs/44993763830)

### 4. Playwright UI Automation Lab
A task-tracker case study with 11 automated browser scenarios, 20 documented manual cases, an execution report and two accessibility findings fixed with regression checks.

[Live application](https://blvxx.github.io/playwright-qa-lab/) · [Source repository](https://github.com/blvxx/playwright-qa-lab) · [Successful CI run](https://github.com/blvxx/playwright-qa-lab/actions/runs/45155361776)

### 5. FinTech QA Engineering Platform
A fictional payment product with Payment and Ledger services. Includes REST API and service-integration testing, PostgreSQL, ledger invariants, idempotent retry checks, Docker Compose, Playwright, observability and a controlled dependency-outage/recovery exercise.

[Project overview](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/) · [Successful CI run](https://github.com/blvxx/portfolio/actions/runs/45100258032)

## Quality engineering framework

The portfolio now includes reusable working documents:

- [QA Engineering Strategy](./qa-engineering-strategy.md) — risk model, test levels, requirements traceability, API/integration strategy, defect lifecycle, CI gates and release readiness.
- [Mobile / Android TV / Smart TV Checklist](./qa-mobile-tv-checklist.md) — install/upgrade, lifecycle, network, remote navigation, focus, playback and device-matrix reporting.
- [QA & Commercial Problem-Solving Casebook](./qa-commercial-casebook.md) — e-commerce, financial integrity, wholesale order intake and AI-assisted support scenarios with value hypotheses and measurement plans.

## Technical toolkit

**Manual and product QA:** functional · regression · exploratory · acceptance · mobile · Android TV / Smart TV · test design · defect management  
**Web and device diagnostics:** Chrome DevTools · Network · Console · Application · responsive emulation · ADB · device/build context  
**API and data:** REST · HTTP · Postman · Swagger / OpenAPI · JSON Schema · Charles · Proxyman · SQL · PostgreSQL  
**Automation:** Python · pytest · requests · JavaScript · Playwright  
**Delivery and environments:** Git · GitHub Actions · Docker Compose · Allure · JUnit XML · traces · logs · metrics

## Evidence and current status

Selected CI runs reviewed on 23 November 2026:

- [API Automation](https://github.com/blvxx/portfolio/actions/runs/45102695248) — 62 tests on Python 3.10 and 3.12.
- [Booking API QA](https://github.com/blvxx/portfolio/actions/runs/44993766677) — 31 tests; 100% statement coverage on app.py and store.py.
- [Checkout Regression](https://github.com/blvxx/portfolio/actions/runs/44993763830) — 24 browser scenarios.
- [FinTech QA Platform](https://github.com/blvxx/portfolio/actions/runs/45100258032) — quality, Compose smoke, observability and UI E2E jobs.
- [Playwright QA Lab](https://github.com/blvxx/playwright-qa-lab/actions/runs/45155361776) — 11 browser E2E tests.

A successful workflow verifies only the checks included in that run. It does not imply public production deployment, production certification or full coverage of every supported device.

## Business-oriented thinking

I connect QA work to measurable product outcomes: checkout correctness, transaction integrity, data quality, support effort and release risk. The casebook includes commercial solution concepts such as wholesale Excel/CSV order intake validation and AI-assisted support triage, with proposed pilot metrics.

Implemented portfolio sandboxes, product concepts and verified commercial deliveries are kept clearly distinct. No customer revenue, paid implementation or business savings are claimed without evidence.

## Transparency

The automated case studies are independent portfolio projects and practice environments. Payment, booking, checkout and incident scenarios are synthetic. Public demo APIs may simulate writes. The Booking API uses an in-memory store and simplified test authentication. Checkout has no real payment or inventory backend. The mobile/TV checklist is a reusable test-design artifact; actual device coverage must be reported against the exact models, OS/firmware and builds executed. CI validation is distinguished from live production behavior.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)
