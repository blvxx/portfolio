# Artem Kalinin | Application Support · Technical Support · QA Automation · Data Analytics

Practical engineering portfolio covering incident investigation, REST API testing, automation, SQL / PostgreSQL analytics and frontend work.

**[Engineering showcase](https://blvxx.github.io/portfolio/engineering/)** · **[Freelance web portfolio](https://blvxx.github.io/portfolio/)** · **[All repositories](https://github.com/blvxx?tab=repositories)**

[![FinTech QA](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml)
[![Checkout Playwright QA](https://github.com/blvxx/portfolio/actions/workflows/qa-checkout-regression.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/qa-checkout-regression.yml)
[![Booking API QA](https://github.com/blvxx/portfolio/actions/workflows/qa-booking-api.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/qa-booking-api.yml)
[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)
[![Data Analytics](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml)
[![Customer Retention Analytics](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml)
[![Subscription Revenue Analytics](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml)
[![Retail Dataset Refresh](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-data-refresh.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-data-refresh.yml)

## Start here

| Direction | Case study | Evidence |
|---|---|---|
| **Application / Technical Support** | [Linux Support Engineering Lab](./support-engineering-lab/) · [Incident Investigation Lab](./incident-lab/) | Linux triage, systemd, Nginx, DNS, TLS, log analysis, webhook diagnostics, SQL reconciliation, RCA and recovery runbooks |
| **QA Engineering** | [FinTech QA Platform](./fintech-qa-platform/) · [Checkout Regression QA](./qa-cases/checkout-regression/) · [Booking API QA](./qa-cases/api-contract-negative/) | Payment/Ledger integration and E2E tests; 24 Playwright checkout scenarios; 31 pytest API cases, auth, conflicts, idempotency and ownership checks |
| **API Automation** | [Python + pytest API suite](./api-automation/) | Reusable HTTP client, CRUD contracts, JSON Schema, negative cases, mocks and Postman |
| **Data Analysis** | [E-commerce SQL + Python](./data-analytics/) | KPI calculations, PostgreSQL reporting, pandas validation and reproducible exports |
| **Customer Analytics** | [Customer Retention & Sales Analytics](./customer-retention-analytics/) | UCI Online Retail, refunds, RFM segmentation, cohort retention and an interactive dashboard |
| **BI / PostgreSQL Analytics** | [Subscription Revenue & Retention](./subscription-revenue-analytics/) | MRR / ARR, revenue bridge, GRR / NRR, lifecycle events, cohort retention and SQL data-quality checks |
| **Support Analytics** | [Support Operations Analytics — SQL case](./support-operations-analytics/) | SLA, ticket backlog, priority mix, agent workload, percentiles and SQL data-quality checks |
| **UI Automation** | [Todo Test](https://github.com/blvxx/playwright-qa-lab) | 8 authored Playwright scenarios and 17 documented manual test cases |
| **Web Development** | [Frontend Portfolio](https://github.com/blvxx/web-development-portfolio) | Responsive website concepts and interactive business-oriented interfaces |

## Featured engineering projects

### 1. Linux Support Engineering Lab
A reproducible troubleshooting lab for Linux and web-service incidents, aimed at Application Support L2 and Technical Support workflows.
- 10 incident playbooks covering systemd, disk/inodes, Nginx 502/504, DNS, TLS, OOM, PostgreSQL pools, permissions and port conflicts.
- Python CLI classifies synthetic logs by severity, preserves source line evidence and suggests next diagnostic checks.
- Unit tests and GitHub Actions workflow generate a JSON triage report artifact.

**Skills:** Linux · systemd · journalctl · Nginx · DNS · TLS · Python · log analysis · incident response.

[Open the lab](./support-engineering-lab/)

### 2. Incident Investigation Lab — Payment Webhook Failure
A simulated support incident: the payment provider reports successful payments while some storefront orders remain in `pending_payment`.
- Investigation timeline, impact assessment and generated application logs.
- Python log analysis and a unified command-line operations toolkit.
- SQL diagnostics for duplicate provider IDs and payment/order state mismatches.
- HTTP webhook troubleshooting, RCA, recovery and reconciliation runbooks.

**Skills:** incident triage · log analysis · HTTP / webhooks · Python · SQL · RCA · operational documentation.

[Open the case study](./incident-lab/)

### 3. FinTech QA Engineering Platform
An end-to-end QA sandbox for a fictional payment product with separate Payment and Ledger services.
- REST API, service-integration and negative testing.
- Idempotency checks and debit/credit balance invariants.
- PostgreSQL persistence and Docker Compose environment.
- Playwright browser tests for payment submission and balance verification.
- Postman collection, test strategy, risk analysis, Allure reporting, Prometheus/Grafana and a guarded local Ledger outage/recovery drill.

**Stack:** Python · FastAPI · pytest · Playwright · SQLAlchemy · PostgreSQL · Docker · Postman · Allure · GitHub Actions.

[Overview/screenshots](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/) · [Incident drills](./fintech-qa-platform/observability/incident-drills.md)

### 4. Python API Automation
A REST API automation suite for the public JSONPlaceholder demo service.
- GET, POST, PUT, PATCH and DELETE contract checks.
- Positive, negative and parametrized scenarios.
- Reusable requests client with explicit timeouts, optional bearer-token configuration and bounded pagination.
- Safe retries for transient failures on GET / HEAD / OPTIONS only; write requests are not automatically replayed.
- JSON Schema validation, isolated unit tests with mocked HTTP sessions, Postman collection and CI.

**Stack:** Python · pytest · requests · jsonschema · Allure · Postman · Ruff.

[Open project](./api-automation/)

### 5. SQL + Python Data Analytics
An end-to-end analysis of 360 synthetic e-commerce orders.
- PostgreSQL schema and SQL queries for monthly KPIs, customer groups and segments.
- pandas pipeline for revenue, order and customer metrics.
- Regional, category and channel breakdowns.
- Input validation, business-rule tests and reproducible CSV / JSON reports.

**Stack:** SQL · PostgreSQL · Python · pandas · pytest.

[Project and findings](./data-analytics/) · [Dashboard](./data-analytics/dashboard/README.md)

### 6. Customer Retention & Sales Analytics
An end-to-end business analytics case study using the public UCI Online Retail dataset.
- Processed all 541,909 source transaction rows covering December 2010–December 2011.
- Calculated £10.67M gross sales, £896.8K refunds/cancellations and £9.77M net sales.
- Identified 4,338 customers in positive sale lines; 2,845 placed multiple invoices (65.58%).
- Built RFM segments, a 13-cohort retention matrix and a Streamlit + Plotly dashboard.
- SQLite CTEs and window functions for repeat-purchase, RFM and cohort queries, reconciled against pandas outputs.
- Aggregate-only public results and reproducible CI refresh; raw workbook and customer-level identifiers are not committed.

**Stack:** Python · pandas · Streamlit · Plotly · pytest · GitHub Actions.

[Live case study](https://blvxx.github.io/portfolio/customer-retention-analytics/) · [Findings](./customer-retention-analytics/docs/generated/findings.md) · [Source](./customer-retention-analytics/) · [Dataset attribution](./customer-retention-analytics/data/README.md)

### 7. Subscription Revenue & Retention Analytics
A PostgreSQL-first BI case study for a fictional subscription business.
- PostgreSQL schema with primary/foreign keys, constraints, indexes and deterministic fixture.
- Monthly MRR / ARR, new MRR, expansion, contraction and churn bridge.
- GRR / NRR, month-end subscription snapshots, customer cohorts and channel / region reporting.
- CTEs, ROW_NUMBER(), LAG(), generate_series(), window aggregates and reusable analytical views.
- SQL data-quality assertions, reconciliation controls and aggregate CSV exports in GitHub Actions.

**Stack:** PostgreSQL · SQL · Docker Compose · GitHub Actions · BI data modelling.

[Visual case study](https://blvxx.github.io/portfolio/subscription-revenue-analytics/) · [SQL source](./subscription-revenue-analytics/) · [CI workflow](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml)

### 8. Support Operations Analytics
SQL case study using a fictional support-ticket dataset to analyze ticket volume, priority-based SLAs, backlog aging and agent workload.
- CTE-based SLA definitions and conditional aggregation.
- Median and P90 resolution-time analysis.
- Backlog aging bands and workload context.
- Data-quality checks for timestamp and status inconsistencies.

**Stack:** PostgreSQL · SQL · Window Functions · Support KPI design.

[SQL case study and setup](./support-operations-analytics/)

### 9. Todo Test — Playwright UI Automation
A browser-based task tracker used as a target for manual and automated QA.
- 8 authored Playwright end-to-end scenarios.
- 17 documented manual test cases.
- Test report and bug-report templates.
- GitHub Actions workflow for Chromium-based tests.

[Repository](https://github.com/blvxx/playwright-qa-lab) · [Test documentation](https://github.com/blvxx/playwright-qa-lab/tree/main/docs)

## How to evaluate the work
1. Start with the [Engineering Showcase](https://blvxx.github.io/portfolio/engineering/) for a concise visual overview.
2. Read the [Incident Investigation Lab](./incident-lab/) for a complete support-style investigation.
3. Open the [FinTech QA Platform](./fintech-qa-platform/) to inspect architecture, test strategy and screenshots.
4. Review [API Automation](./api-automation/) and [Data Analytics](./data-analytics/) for reproducible commands and test evidence.
5. Open the [Subscription Analytics case](https://blvxx.github.io/portfolio/subscription-revenue-analytics/) to review BI modelling, metrics and reconciliation.

## Technologies
**Support & troubleshooting:** HTTP · REST APIs · Webhooks · SQL · PostgreSQL · Logs · Incident Triage · RCA · Runbooks  
**QA & automation:** Python · pytest · requests · Playwright · Postman · JSON Schema · Allure · Ruff  
**Development & delivery:** FastAPI · JavaScript · HTML5 · CSS3 · Docker · GitHub Actions · Prometheus · Grafana  
**Analytics:** SQL · PostgreSQL · Python · pandas · CTEs · Window Functions · KPI Modelling · Cohort Analysis · CSV / JSON reporting

## QA automation case studies

### Checkout & Cart — Web Regression
A standalone responsive storefront plus **23 Playwright browser tests**. The suite covers cart and stock boundaries, promotion calculations, shipping transitions, checkout validation, duplicate submission and mobile layout. Each test runs in a fresh Chromium context; CI retains JUnit output, Playwright traces and screenshots for failures.

[Open the application and test suite](./qa-cases/checkout-regression/) · [Test catalogue](./qa-cases/checkout-regression/test-cases.md)

### Booking API — Contract & Negative Testing
A self-contained FastAPI target and **31 pytest cases** covering response contracts, pagination boundaries, email and payload validation, booking conflicts, date intervals, user-level access control, idempotency replay and cancellation. The in-memory repository is isolated per test; the local test run achieved 100% statement coverage for `app.py` and `store.py`.

[Open the API QA case](./qa-cases/api-contract-negative/) · [Requirements-to-tests traceability](./qa-cases/api-contract-negative/test-matrix.md)

## Separate freelance direction
For website creation, redesign and small-business projects, visit the **[freelance web portfolio](https://blvxx.github.io/portfolio/)** or the [frontend source repository](https://github.com/blvxx/web-development-portfolio).

## Transparency
- Payment systems and incidents are simulated.
- Customer retention uses the attributed public UCI Online Retail dataset; other fixture datasets, logs, incident records and subscription analytics data are synthetic.
- The API automation project targets a public demo service; simulated write operations are not represented as persistent production changes.
- These repositories are independent portfolio projects, not claims of production access or commercial client delivery.
- Workflow badges and linked Actions runs show actual CI status; a configured workflow alone is not proof of a passing run.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Telegram](https://t.me/blvlxx) · [Email](mailto:blvx8x@gmail.com) · [Profile README template](./github-profile-readme.md) · [Publishing guide](./docs/publish-github-profile-readme.md)
