# Artem Kalinin — QA & Engineering Portfolio

**QA Automation · API Testing · Application Support · Python**

Independent engineering projects focused on software quality, API contracts, browser regression, service integration and evidence-led troubleshooting.

**[QA Portfolio — test projects and evidence](./qa-portfolio.md)** · [Engineering showcase](https://blvxx.github.io/portfolio/engineering/) · [GitHub profile](https://github.com/blvxx) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)

## Choose a route

| Target role | Start with | Evidence |
|---|---|---|
| **Junior QA / API Tester / QA Automation** | [QA Portfolio](./qa-portfolio.md) · [Booking API](./qa-cases/api-contract-negative/) · [Checkout Regression](./qa-cases/checkout-regression/) | API contracts, negative/boundary testing, 31 pytest cases, 24 Playwright scenarios, test plans, traceability, CI artifacts |
| **Application Support L2** | [Linux Support Lab](./support-engineering-lab/) · [Incident Investigation](./incident-lab/) | 10 troubleshooting playbooks, log triage, SQL diagnostics, RCA and recovery verification |
| **Technical Support / Support Engineer** | [Support Operations Analytics](./support-operations-analytics/) · [Support playbooks](./support-engineering-lab/docs/incident-playbooks.md) | SLA, backlog, issue categorisation, incident communication and escalation practices |
| **Games Support** | [Games Support Casebook](./games-support-casebook/) | Fictional player-support cases, prioritisation, response templates and escalation decisions |
| **Python application development** | [Telegram Business Assistant](./telegram-business-assistant/) · [AI Support Triage Agent](./ai-support-triage-agent/) | Async Python, aiogram, PostgreSQL, Redis, idempotency and guarded AI workflows |
| **Frontend / Web Development** | [Workboard React SPA](./taskboard-spa-src/) · [Frontend portfolio](https://blvxx.github.io/web-development-portfolio/) | React, TypeScript, task CRUD, filtering, responsive UI, browser storage and HTML/CSS/JavaScript concepts |

## QA case studies

### 1. Booking API — Risk-Based Contract Testing
A fictional booking API with 31 pytest cases covering request/response contracts, pagination, validation, authorization, overlapping reservations, idempotency and cancellation. CI enforces 100% statement coverage for the authored `app.py` and `store.py` modules.

[Project overview](./qa-cases/api-contract-negative/) · [Test matrix](./qa-cases/api-contract-negative/test-matrix.md) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/44993766677)

### 2. Checkout & Cart — Browser Regression
A fictional storefront with 24 Playwright scenarios covering cart and stock boundaries, price calculations, promotions, fulfilment transitions, checkout validation and duplicate-submit protection. CI retains JUnit output, traces and failure screenshots.

[Project overview](./qa-cases/checkout-regression/) · [Test plan](./qa-cases/checkout-regression/test-plan.md) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/44993763830)

### 3. Python API Automation
A reusable requests client and pytest suite for REST CRUD contracts, JSON Schema, negative scenarios, pagination and transport resilience. The reviewed CI run passed 62 tests on Python 3.10 and 3.12.

[Project overview](./api-automation/) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/45102695248)

### 4. Playwright UI Automation Lab
A task-tracker QA case study with 11 automated browser scenarios, 20 documented manual cases, an execution report and two accessibility findings fixed with regression checks.

[Open the application](https://blvxx.github.io/playwright-qa-lab/) · [Source repository](https://github.com/blvxx/playwright-qa-lab) · [Latest successful CI run](https://github.com/blvxx/playwright-qa-lab/actions/runs/45155361776)

### 5. FinTech QA Engineering Platform
An end-to-end QA sandbox for a fictional payment product with Payment and Ledger services. Includes REST API and service-integration testing, PostgreSQL, ledger invariants, idempotent retry checks, Docker Compose, Playwright and a controlled dependency-outage/recovery exercise.

[Project overview](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/45100258032)

For project boundaries, run instructions, test-design artifacts and the full QA evidence index, see the [dedicated QA Portfolio](./qa-portfolio.md).

## Additional engineering projects

| Project | Scope |
|---|---|
| [Linux Support Engineering Lab](./support-engineering-lab/) | 10 troubleshooting playbooks, log triage, severity ranking and source-line evidence |
| [Incident Investigation](./incident-lab/) | Simulated payment-webhook incident, timeline, SQL reconciliation, RCA and recovery runbooks |
| [Games Support Casebook](./games-support-casebook/) | Synthetic player-support scenarios, response quality, severity, escalation and handover |
| [Workboard — React + TypeScript SPA](./taskboard-spa-src/) | Internal task workspace with CRUD, filters, local persistence, 12 Vitest tests and 6 Playwright scenarios |
| [Telegram Business Assistant](./telegram-business-assistant/) | Async Telegram enquiry workflow, PostgreSQL, Redis FSM, transactional outbox and idempotency |
| [AI Support Triage Agent](./ai-support-triage-agent/) | Runbook retrieval, structured L2 triage, citation validation and human-approval safeguards |
| [Support Operations Analytics](./support-operations-analytics/) | SQL analysis of ticket volume, SLA, backlog age and agent workload |
| [SQL + Python Data Analytics](./data-analytics/) | PostgreSQL and pandas pipeline with validation and CSV/JSON reports |
| [Customer Retention Analytics](./customer-retention-analytics/) | Public UCI dataset, RFM segmentation, cohorts and dashboard |
| [Subscription Revenue & Retention](./subscription-revenue-analytics/) | PostgreSQL BI model for MRR/ARR, GRR/NRR and recurring-revenue movement |

## Technical toolkit

**QA:** Python · pytest · requests · Playwright · Postman · JSON Schema · API contracts · negative/boundary testing · Allure  
**Application Support:** Linux · systemd · journalctl · Nginx · DNS · TLS · TCP/IP · incident triage · RCA · runbooks  
**Application engineering:** HTTP · REST · webhooks · FastAPI · aiogram · PostgreSQL · Redis · Docker · GitHub Actions  
**Observability & data:** Prometheus · Grafana · SQL · pandas · CTEs · window functions · SLA/KPI analysis

## Evidence and current status

Selected CI runs reviewed on 23 November 2026:

- [Booking API QA](https://github.com/blvxx/portfolio/actions/runs/44993766677) — 31 tests, 100% statement coverage on `app.py` and `store.py`.
- [Checkout Regression](https://github.com/blvxx/portfolio/actions/runs/44993763830) — 24 browser scenarios passed; traces and JUnit evidence retained.
- [API Automation](https://github.com/blvxx/portfolio/actions/runs/45102695248) — 62 tests passed on Python 3.10 and 3.12.
- [FinTech QA Platform](https://github.com/blvxx/portfolio/actions/runs/45100258032) — quality, Compose smoke and UI E2E jobs passed.
- [Playwright QA Lab](https://github.com/blvxx/playwright-qa-lab/actions/runs/45155361776) — 11 browser E2E tests passed.
- [Telegram Business Assistant](https://github.com/blvxx/portfolio/actions/runs/45102741553) — integration tests, PostgreSQL backup/restore drill, Prometheus validation and Docker image build passed.

A successful workflow verifies only the checks included in that run. It does not imply a public production deployment or production certification.

## Working method

1. **Clarify expected behavior** — identify user impact, scope, constraints and acceptance criteria.
2. **Prioritise risk** — focus on critical workflows, data integrity, access control and failure modes.
3. **Design tests** — cover positive, negative, boundary and state-transition scenarios.
4. **Reproduce and investigate** — preserve requests, responses, logs and relevant state.
5. **Verify fixes** — rerun focused checks and regression coverage.
6. **Communicate** — document results, limitations, remaining risk and next owner.

## Transparency

These are independent portfolio projects and practice labs. Payment, booking, checkout and incident scenarios plus selected datasets are synthetic unless a public dataset is explicitly attributed. Public demo APIs may simulate writes rather than persist them. Projects are not represented as commercial client deliveries or production employment. A configured workflow is not evidence of a pass unless a successful run is linked. CI validation is distinguished from live API use and public production deployment.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)
