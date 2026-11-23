# Artem Kalinin — Engineering Portfolio

**Application Support · Technical Support · QA Automation · Python**

Evidence-led engineering projects focused on troubleshooting, incident investigation, API quality and automation. Start with a role below, inspect the implementation, then open the linked CI evidence.

[**Engineering showcase**](https://blvxx.github.io/portfolio/engineering/) · [GitHub profile](https://github.com/blvxx) · [Frontend portfolio](https://blvxx.github.io/web-development-portfolio/) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)

## Choose a route

| Role | Start with | Evidence |
|---|---|---|
| **Application Support L2** | [Linux Support Lab](./support-engineering-lab/) · [Incident Investigation](./incident-lab/) | 10 troubleshooting playbooks, log triage, SQL diagnostics, RCA and recovery verification |
| **Technical Support / Support Engineer** | [Support Operations Analytics](./support-operations-analytics/) · [Support playbooks](./support-engineering-lab/docs/incident-playbooks.md) | SLA, backlog, issue categorisation, incident communication and escalation practices |
| **Games Support** | [Games Support Casebook](./games-support-casebook/) | Fictional player-support cases, prioritisation, response templates and escalation decisions |
| **Junior QA / API Testing** | [FinTech QA Platform](./fintech-qa-platform/) · [API Automation](./api-automation/) | pytest, API contracts, negative cases, integration tests, PostgreSQL and Playwright |
| **Python application development** | [Telegram Business Assistant](./telegram-business-assistant/) · [AI Support Triage Agent](./ai-support-triage-agent/) | Async Python, aiogram, PostgreSQL, Redis, idempotency and guarded AI workflows |
| **Frontend / Web Development** | [Frontend portfolio](https://blvxx.github.io/web-development-portfolio/) | Responsive interfaces and interactive HTML/CSS/JavaScript concepts |

## Featured case studies

### 1. Linux Support Engineering Lab
A reproducible troubleshooting lab for common Linux and web-service failures.

- 10 playbooks: systemd, disk/inodes, Nginx 502/504, DNS, TLS, OOM, PostgreSQL pools, permissions and port conflicts.
- Python log-triage CLI with severity ranking, source-line evidence and JSON output.
- Unit tests and a GitHub Actions report artifact.

[Project and playbooks](./support-engineering-lab/) · [Visual walkthrough](./support-engineering-lab/overview.html)

### 2. Incident Investigation — Payment Webhook Failure
A simulated incident in which a payment provider reports successful payments while selected store orders remain pending.

- Investigation timeline, impact assessment and generated application logs.
- Python log analysis and operational CLI.
- SQL checks for duplicate provider IDs and payment/order mismatches.
- Root-cause analysis, recovery and reconciliation runbooks.

[Open the case](./incident-lab/)

### 3. FinTech QA Engineering Platform
An end-to-end QA sandbox for a fictional payment product with separate Payment and Ledger services.

- REST API, service-integration and negative testing.
- Ledger debit/credit invariants and idempotent retry checks.
- PostgreSQL, Docker Compose, Playwright, Postman, Allure and Prometheus/Grafana.
- Guarded local Ledger-outage and recovery drill.

[Project overview](./fintech-qa-platform/overview.html) · [Source and setup](./fintech-qa-platform/) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/45100258032)

### 4. Python API Automation
A reusable HTTP client and pytest suite for REST CRUD contracts, response schemas, negative scenarios, pagination and transport resilience.

- Safe retry boundaries: transient read requests can retry; write requests are not automatically replayed.
- Mocked unit tests and deterministic local HTTP fault injection.
- Postman collection and Allure/JUnit reporting.
- Reviewed CI run: **62 tests passed on Python 3.10 and 3.12**.

[Open project](./api-automation/) · [Latest successful CI run](https://github.com/blvxx/portfolio/actions/runs/45102695248)

### 5. Playwright UI Automation
A browser-based task tracker and QA case study.

- Eight automated Playwright end-to-end scenarios.
- 17 designed manual scenarios with a separate execution report.
- Functional checks for task creation, validation, completion, deletion and persistence.

[Open the application](https://blvxx.github.io/playwright-qa-lab/) · [Source repository](https://github.com/blvxx/playwright-qa-lab)

## Additional engineering projects

| Project | Scope |
|---|---|
| [Games Support Casebook](./games-support-casebook/) | Synthetic player-support scenarios, response quality, severity, escalation and handover |
| [Telegram Business Assistant](./telegram-business-assistant/) | Async Telegram enquiry workflow, PostgreSQL, Redis FSM, transactional outbox, idempotency, health checks and Docker |
| [AI Support Triage Agent](./ai-support-triage-agent/) | Runbook retrieval, structured L2 triage, citation validation and human-approval safeguards |
| [Booking API QA](./qa-cases/api-contract-negative/) | 31 pytest cases for API contracts, pagination, validation, conflicts, idempotency and access control |
| [Checkout Regression QA](./qa-cases/checkout-regression/) | 24 Playwright browser scenarios for cart, checkout, validation and duplicate submissions |
| [Support Operations Analytics](./support-operations-analytics/) | SQL analysis of ticket volume, SLA performance, backlog age and agent workload |
| [SQL + Python Data Analytics](./data-analytics/) | PostgreSQL and pandas pipeline with validation and CSV/JSON reports |
| [Customer Retention Analytics](./customer-retention-analytics/) | Public UCI dataset, RFM segmentation, cohorts and dashboard |
| [Subscription Revenue & Retention](./subscription-revenue-analytics/) | PostgreSQL BI model for MRR/ARR, GRR/NRR and recurring-revenue movement |
| [Playwright UI Automation Lab](https://github.com/blvxx/playwright-qa-lab) | Eight automated scenarios and manual QA artefacts |

## Technical toolkit

**Support & operations:** Linux · systemd · journalctl · Nginx · DNS · TLS · TCP/IP · incident triage · log analysis · RCA · runbooks

**QA & automation:** Python · pytest · requests · Playwright · Postman · JSON Schema · API contracts · negative testing · Allure

**Application engineering:** HTTP · REST · webhooks · FastAPI · aiogram · PostgreSQL · Redis · Docker · GitHub Actions

**Observability & data:** Prometheus · Grafana · SQL · pandas · CTEs · window functions · SLA/KPI analysis

## Evidence and current status

Selected workflows were reviewed on **23 November 2026**:

- [FinTech QA Platform](https://github.com/blvxx/portfolio/actions/runs/45100258032) — quality, Compose smoke and UI E2E jobs passed.
- [API Automation](https://github.com/blvxx/portfolio/actions/runs/45102695248) — Python 3.10 and 3.12 matrix jobs passed.
- [Telegram Business Assistant](https://github.com/blvxx/portfolio/actions/runs/45102741553) — unit/service integration tests, PostgreSQL backup/restore drill, Prometheus validation and Docker image build passed.
- [Frontend Portfolio](https://github.com/blvxx/web-development-portfolio/actions/runs/45103113568) — content/link checks and Chromium browser regression passed.
- [Playwright QA Lab](https://github.com/blvxx/playwright-qa-lab/actions/runs/45100286227) — eight E2E tests passed.

CI evidence verifies the recorded workflow run; it does not imply a public production deployment. For example, the current Telegram Business Assistant PostgreSQL/Redis/Webhook profile is validated in CI but has not yet been deployed to a public host.

## Working method

1. **Understand impact** — identify the affected workflow, users, time window and expected behavior.
2. **Reproduce** — use a safe, repeatable test and preserve the evidence.
3. **Investigate** — inspect logs, API responses, data and dependencies.
4. **Verify** — check the correction with positive, negative and regression scenarios.
5. **Communicate** — record the result, limitations, remaining risk and next owner.

## Transparency

These are independent portfolio projects and practice labs. Payment and incident scenarios plus selected datasets are synthetic; the Customer Retention case uses the attributed public UCI Online Retail dataset. Public demo APIs may simulate writes rather than persist them. Projects are not represented as commercial client deliveries or production employment. A configured workflow is not evidence of a pass unless a successful run is linked. Live API calls and public deployments are identified separately from offline tests and CI validation.

---

**Artem Kalinin** · [GitHub](https://github.com/blvxx) · [Email](mailto:blvx8x@gmail.com) · [Telegram](https://t.me/blvlxx)
