# Artem Kalinin

### Application Support · Technical Support · QA Automation

I investigate technical issues, validate API and user workflows, work with SQL data, and document findings so that problems can be understood and reproduced.

**[Engineering portfolio & case studies](https://blvxx.github.io/portfolio/engineering/)** · **[Web development portfolio](https://blvxx.github.io/portfolio/)** · **[GitHub repositories](https://github.com/blvxx?tab=repositories)**

[![Support Engineering Lab](https://github.com/blvxx/portfolio/actions/workflows/support-engineering-lab.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/support-engineering-lab.yml)
[![FinTech QA](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml)
[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)
[![Data Analytics](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/data-analytics.yml)

---

## What I work with

| Area | Practical focus |
|---|---|
| **Application / Technical Support** | Incident triage, log analysis, HTTP and webhook troubleshooting, SQL investigation, RCA, runbooks |
| **QA & API Automation** | Python, pytest, requests, REST API contracts, JSON Schema, Postman, Playwright |
| **Data Analysis** | SQL, PostgreSQL, pandas, KPI calculations, data validation, repeatable reporting |
| **Engineering workflow** | Git, GitHub Actions, Docker Compose, test reports, technical documentation |
| **Web development** | HTML, CSS, JavaScript, responsive layouts and small-business websites |

## Selected projects

### 1. [Linux Support Engineering Lab](https://github.com/blvxx/portfolio/tree/main/support-engineering-lab)
A reproducible operations lab with 10 Linux incident playbooks, a Python log triage CLI, severity-ranked evidence and CI-generated JSON reports.

**Demonstrates:** Linux troubleshooting, systemd, Nginx, DNS, TLS, resource diagnosis and incident documentation.

### 2. [Incident Investigation Lab — Payment Webhook Failure](https://github.com/blvxx/portfolio/tree/main/incident-lab)
A simulated payment incident investigated from first symptoms to recovery.

- Python log analyzer and unified operations CLI.
- SQL reconciliation for duplicate payment IDs and payment/order state mismatches.
- HTTP webhook diagnostics, incident timeline, RCA and recovery runbooks.

**Demonstrates:** incident investigation, troubleshooting, evidence-based analysis and operational documentation.

### 3. [FinTech QA Engineering Platform](https://github.com/blvxx/portfolio/tree/main/fintech-qa-platform)
A multi-service payment sandbox designed for API, integration and browser-level testing.

- Payment and Ledger services with PostgreSQL persistence.
- pytest API/integration coverage and Playwright E2E flows.
- Docker Compose, Postman, Allure and GitHub Actions.

**Demonstrates:** end-to-end QA thinking, test design, service integration and CI.

### 4. [Python API Automation](https://github.com/blvxx/portfolio/tree/main/api-automation)
A reusable requests client and pytest suite for a public demo REST API.

- CRUD contract tests and positive/negative scenarios.
- Safe retry policy for idempotent methods, optional bearer-token configuration and bounded pagination.
- JSON Schema validation, parametrization, mocked unit tests and Postman.

**Demonstrates:** API testing, Python automation and maintainable test structure.

### 5. [SQL + Python Data Analytics](https://github.com/blvxx/portfolio/tree/main/data-analytics)
A reproducible analytics case study based on 360 synthetic e-commerce orders.

- PostgreSQL schema and SQL reporting.
- pandas pipeline for revenue, orders and customer KPIs.
- Validation, unit tests and CSV/JSON exports.

**Demonstrates:** structured data analysis, SQL and Python reporting.

[Interactive dashboard](https://github.com/blvxx/portfolio/tree/main/data-analytics/dashboard)


### 6. Customer Retention & Sales Analytics

An end-to-end business analytics case study using the public UCI Online Retail dataset.

- Transaction cleaning with cancellation and refund handling.
- Gross / net sales, monthly trends, country contribution and top products.
- RFM segmentation and cohort retention analysis.
- Streamlit + Plotly dashboard, reproducible pipeline and unit tests.

**Stack:** Python · pandas · Streamlit · Plotly · pytest.

[Open the analytics case](./customer-retention-analytics/) · [Dataset provenance](./customer-retention-analytics/data/README.md)

### 7. [Todo Test — Playwright UI Automation](https://github.com/blvxx/playwright-qa-lab)
A browser app with 8 authored Playwright scenarios and 17 documented manual test cases.

**Demonstrates:** UI test design, browser automation and QA documentation.

## Selected technology

Python · pytest · requests · Playwright · Postman · SQL · PostgreSQL · pandas · FastAPI · Docker · GitHub Actions · HTML · CSS · JavaScript

## How I approach a problem

1. Reproduce the issue and define expected behavior.
2. Collect evidence from logs, requests, responses and data.
3. Isolate the failure and test likely causes.
4. Verify the result with focused and regression checks.
5. Document impact, findings and next steps.

## Contact

- **Email:** [blvx8x@gmail.com](mailto:blvx8x@gmail.com)
- **Telegram:** [@blvlxx](https://t.me/blvlxx)
- **Website projects:** [Web development portfolio](https://blvxx.github.io/portfolio/)

> **Project transparency:** payment systems and incident records are simulated; the original customer analytics case uses the attributed public UCI Online Retail dataset, while the separate E-commerce Sales Analysis uses synthetic data. These projects are not presented as production incidents or commercial client deliveries.
