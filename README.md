# Artem Kalinin | Application Support · Technical Support · QA Automation

Practical engineering portfolio covering incident investigation, REST API testing, automation, SQL analysis and frontend work.

**[Engineering showcase](https://blvxx.github.io/portfolio/engineering/)** · **[Freelance web portfolio](https://blvxx.github.io/portfolio/)** · **[All repositories](https://github.com/blvxx?tab=repositories)**

[![FinTech QA](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml)
[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)
[![Data Analytics](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml)

## Start here

| Direction | Case study | Evidence |
|---|---|---|
| **Application / Technical Support** | [Incident Investigation Lab](./incident-lab/) | Log analysis, webhook diagnostics, SQL reconciliation, RCA, recovery runbooks and a unified CLI |
| **QA Engineering** | [FinTech QA Platform](./fintech-qa-platform/) | Payment/Ledger services, API and integration tests, Playwright E2E, PostgreSQL, Docker and observability |
| **API Automation** | [Python + pytest API suite](./api-automation/) | Reusable HTTP client, CRUD contracts, JSON Schema, negative cases, mocks and Postman |
| **Data Analysis** | [E-commerce SQL + Python](./data-analytics/) | KPI calculations, PostgreSQL reporting, pandas validation and reproducible exports |
| **UI Automation** | [Todo Test](https://github.com/blvxx/todo-test) | 8 authored Playwright scenarios and 17 documented manual test cases |
| **Web Development** | [Frontend Portfolio](https://github.com/blvxx/frontend-portfolio) | Responsive website concepts and interactive business-oriented interfaces |

## Featured engineering projects

### 1. Incident Investigation Lab — Payment Webhook Failure

A simulated support incident: the payment provider reports successful payments while some storefront orders remain in `pending_payment`.

- Investigation timeline, impact assessment and generated application logs.
- Python log analysis and a unified command-line operations toolkit.
- SQL diagnostics for duplicate provider IDs and payment/order state mismatches.
- HTTP webhook troubleshooting, Root Cause Analysis, recovery and reconciliation runbooks.

**Skills demonstrated:** incident triage · log analysis · HTTP / webhooks · Python · SQL · RCA · operational documentation.

[Open the case study](./incident-lab/)

### 2. FinTech QA Engineering Platform

An end-to-end QA sandbox for a fictional payment product with separate Payment and Ledger services.

- REST API, service-integration and negative testing.
- Idempotency checks and debit/credit balance invariants.
- PostgreSQL persistence and Docker Compose environment.
- Playwright browser tests for payment submission and balance verification.
- Postman collection, test strategy, risk analysis, Allure reporting and observability setup.

**Stack:** Python · FastAPI · pytest · Playwright · SQLAlchemy · PostgreSQL · Docker · Postman · Allure · GitHub Actions.

[Open the project overview and screenshots](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/)

![FinTech demo payment UI](./fintech-qa-platform/docs/screenshots/payment-ui.png)

### 3. Python API Automation

A REST API automation suite for the public JSONPlaceholder demo service.

- GET, POST, PUT, PATCH and DELETE contract checks.
- Positive, negative and parametrized scenarios.
- Reusable requests client with explicit timeouts.
- JSON Schema validation and isolated unit tests with mocked HTTP sessions.
- Postman collection and GitHub Actions CI.

**Stack:** Python · pytest · requests · jsonschema · Allure · Postman · Ruff.

[Open project](./api-automation/)

### 4. SQL + Python Data Analytics

An end-to-end analysis of 360 synthetic e-commerce orders.

- PostgreSQL schema and SQL queries for monthly KPIs, customer groups and segments.
- pandas pipeline for revenue, order and customer metrics.
- Regional, category and channel breakdowns.
- Input validation, business-rule tests and reproducible CSV / JSON reports.

**Stack:** SQL · PostgreSQL · Python · pandas · pytest.

[Open project and findings](./data-analytics/)

### 5. Todo Test — Playwright UI Automation

A browser-based task tracker used as the target for manual and automated QA.

- 8 authored Playwright end-to-end scenarios.
- 17 documented manual test cases.
- Test report and bug-report templates.
- GitHub Actions workflow for Chromium-based tests.

[Open repository](https://github.com/blvxx/todo-test) · [Test documentation](https://github.com/blvxx/todo-test/tree/main/docs)

## How to evaluate the work

1. Start with the [Engineering Showcase](https://blvxx.github.io/portfolio/engineering/) for a concise visual overview.
2. Read the [Incident Investigation Lab](./incident-lab/) to see a complete support-style investigation.
3. Open the [FinTech QA Platform](./fintech-qa-platform/) to inspect the architecture, test strategy and screenshots.
4. Review [API Automation](./api-automation/) and [Data Analytics](./data-analytics/) for reproducible commands and test evidence.

## Technologies

**Support & troubleshooting:** HTTP · REST APIs · Webhooks · SQL · PostgreSQL · Logs · Incident Triage · RCA · Runbooks

**QA & automation:** Python · pytest · requests · Playwright · Postman · JSON Schema · Allure · Ruff

**Development & delivery:** FastAPI · JavaScript · HTML5 · CSS3 · Docker · GitHub Actions · Prometheus · Grafana

**Analytics:** SQL · Python · pandas · CSV / JSON reporting · KPI analysis

## Separate freelance direction

For website creation, redesign and small-business projects, visit the **[freelance web portfolio](https://blvxx.github.io/portfolio/)** or the [frontend source repository](https://github.com/blvxx/frontend-portfolio).

## Transparency

- Payment systems and incidents are simulated.
- Datasets, logs, orders and payment records are synthetic.
- The API automation project targets a public demo service; simulated write operations are not represented as persistent production changes.
- These repositories are independent portfolio projects, not claims of production access or commercial client delivery.
- Workflow badges and linked Actions runs show the actual CI status; a configured workflow alone is not proof of a passing run.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Telegram](https://t.me/blvlxx) · [Email](mailto:blvx8x@gmail.com) · [Profile README template](./github-profile-readme.md) · [Publishing guide](./docs/publish-github-profile-readme.md)
