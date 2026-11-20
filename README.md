# QA, Data Analytics & Development Portfolio

Selected practical projects in REST API testing, data analysis, UI automation and frontend development.

## Featured QA projects

### [API Automation — Python / pytest](./api-automation/)

[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)

REST API test suite for the JSONPlaceholder Posts resource.

- Reusable HTTP client built with `requests`.
- CRUD coverage: GET, POST, PUT, PATCH and DELETE.
- Positive, negative and parametrized scenarios.
- Request/response validation with JSON Schema.
- Isolated unit tests with mocked HTTP sessions.
- Allure labels and GitHub Actions CI for Python 3.10 and 3.12.
- Importable Postman collection with response assertions.

**Stack:** Python · pytest · requests · jsonschema · Allure · Postman · Ruff · GitHub Actions

> JSONPlaceholder simulates write operations; this project tests HTTP contracts and does not claim persistent data changes.

## Featured Data Analytics project

### [SQL + Python Data Analytics — E-commerce Sales](./data-analytics/)

End-to-end analytics case study using a transparent synthetic dataset of 360 orders.

- PostgreSQL schema and three SQL analysis scripts.
- pandas pipeline for revenue, order and customer KPIs.
- Monthly, regional, category and channel breakdowns.
- Input validation and unit tests for business rules.
- Reproducible CSV and JSON report exports.
- GitHub Actions workflow for Python 3.10 and 3.12.

**Stack:** PostgreSQL · SQL · Python · pandas · pytest · GitHub Actions

> Dataset is synthetic and created for demonstration; it does not represent real client or company data.

## UI automation

### [Todo Test — Playwright UI Automation](https://github.com/blvxx/todo-test)

Browser-based task tracker with manual test documentation and Playwright scenarios.

- Functional UI coverage for task creation, completion, deletion and clearing.
- Input validation and localStorage persistence scenarios.
- 17 documented manual test cases.
- GitHub Actions workflow for Chromium-based tests.

**Stack:** Playwright · JavaScript · HTML · CSS · GitHub Actions

> Test automation is authored; consult the repository's Actions tab for the latest confirmed run status.

## Frontend projects

### [Frontend Portfolio](https://github.com/blvxx/frontend-portfolio)

Responsive website concepts demonstrating HTML, CSS and JavaScript:

- NOIR COFFEE — café landing page.
- FRAME STUDIO — creative studio portfolio.
- IRON DISTRICT — fitness club landing page.
- VÉRA SKIN — e-commerce interface concept.

> These are independent concept projects, not commercial client deliveries.

## Additional experiments

- [Treker](https://github.com/blvxx/Treker) — standalone responsive recovery milestone tracker (single-page HTML app).
- [HabitForge](https://github.com/blvxx/HabitForge) — habit tracker concept; implementation is not yet complete.

## Incident investigation

### [Incident Investigation Lab — Payment Webhook Failure](./incident-lab/)

Simulated production incident: successful payments are not reflected in order status due to webhook signature validation failure.

- Incident ticket, scope and timeline.
- Application logs and Python log-analysis script.
- SQL checks for order/payment mismatches and duplicate records.
- HTTP webhook troubleshooting matrix.
- Root Cause Analysis (5 Whys), corrective actions and recovery runbook.

**Stack:** HTTP · Webhooks · Python · PostgreSQL / SQL · Incident Management · RCA

> Fictional scenario and generated evidence for practice; not a real production incident.

## About

Artem Kalinin — [GitHub profile](https://github.com/blvxx) · [Web portfolio](https://blvxx.github.io/portfolio/)
