# Artem Kalinin

## Python Automation & Application Engineering

Python · API Integrations · Workflow Automation · QA Engineering · Systems Reliability

I build and investigate software workflows with an emphasis on clear boundaries, predictable failure handling, automated verification and operational documentation.

**[Engineering portfolio](https://blvxx.github.io/portfolio/engineering/)** · **[GitHub repositories](https://github.com/blvxx?tab=repositories)** · **[Web development portfolio](https://blvxx.github.io/web-development-portfolio/)**

[![Telegram Business Assistant](https://github.com/blvxx/portfolio/actions/workflows/telegram-business-assistant.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/telegram-business-assistant.yml)
[![FinTech QA Platform](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml)
[![Python API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)

---

## Engineering focus

| Area | Practical evidence |
|---|---|
| **Python application development** | Async Telegram application, validation, persistence, configuration and deployment |
| **API and workflow automation** | REST clients, request validation, retry boundaries, webhook investigation and integration tests |
| **Quality engineering** | pytest, Playwright, API contracts, negative scenarios, test strategy and CI |
| **Systems and incident analysis** | Linux troubleshooting, log triage, incident timelines, SQL reconciliation and recovery runbooks |
| **Data and SQL** | PostgreSQL, CTEs, window functions, data validation, cohort and revenue analysis |
| **Engineering delivery** | Git, GitHub Actions, Docker Compose, technical documentation and architecture decision records |

## Selected engineering projects

### 1. [Telegram Business Assistant](https://github.com/blvxx/portfolio/tree/main/telegram-business-assistant)

An independently developed and deployed Python Telegram bot MVP for collecting structured business enquiries.

- aiogram 3, asynchronous handlers, finite-state workflow and input validation.
- Two runtime profiles: single-instance SQLite + polling fallback, and a shared PostgreSQL + Redis + HTTPS webhook profile for multi-replica deployment.
- Atomic PostgreSQL lead/outbox transactions, idempotent replay handling, advisory-locked migrations and SKIP LOCKED worker distribution.
- Redis FSM state with TTL and per-conversation event isolation across replicas.
- Health/readiness endpoints, Prometheus metrics and alert rules for service dependency failures, dead letters and stalled queue.
- Ruff + 53 tests, real PostgreSQL 17 / Redis 7.4 CI integration, disposable PostgreSQL backup/restore drill, Prometheus rule validation and Docker image build.
- Architecture decision records, threat model, operations runbook and evidence-based engineering roadmap.

**Live demo:** [@blvlxxbot](https://t.me/blvlxxbot)

**Project status:** the PostgreSQL/Redis/webhook multi-replica profile passes CI integration tests, but it has not yet been deployed to the Dada Cloud demo. The existing hosted bot was tested previously as a single long-polling worker. Host-level persistent storage, external backups and restore remain unverified; this is not represented as a production client system.

### 2. [AI Support Triage Agent](https://github.com/blvxx/portfolio/tree/main/ai-support-triage-agent)

A retrieval-grounded support triage workflow using the OpenAI Responses API and structured Pydantic output.

- Retrieves relevant local runbook evidence and checks model citations against the retrieved source IDs.
- Produces typed severity/category, hypotheses, read-only diagnostics and a draft customer reply.
- Treats incident reports as untrusted input; removes state-changing recommendations and escalates weakly grounded cases.
- Includes 6 offline tests and a separate live-model regression evaluator for synthetic incidents.

**Status:** source integration and offline CI are verified; the live API evaluator requires a configured API key and has not been run. No ticketing, messaging or infrastructure write tools are connected.

### 3. [FinTech QA Engineering Platform](https://github.com/blvxx/portfolio/tree/main/fintech-qa-platform)

A multi-service payment sandbox used to demonstrate API, integration and browser-level quality engineering.

- Payment and Ledger services with PostgreSQL persistence.
- pytest API/integration coverage and Playwright end-to-end flows.
- Docker Compose, Postman, Allure and GitHub Actions.
- Observability and a guarded local dependency-outage/recovery exercise.

**Stack:** Python · FastAPI · pytest · Playwright · PostgreSQL · Docker.

### 4. [Python API Automation](https://github.com/blvxx/portfolio/tree/main/api-automation)

A reusable REST API test suite with positive and negative scenarios.

- CRUD contract checks and JSON Schema validation.
- Explicit timeouts, bounded pagination and conservative retries for idempotent methods.
- Mocked unit tests, Postman collection and CI.

**Stack:** Python · requests · pytest · jsonschema · Postman.

### 5. [Linux Support Engineering Lab](https://github.com/blvxx/portfolio/tree/main/support-engineering-lab)

A reproducible troubleshooting lab with 10 incident playbooks and a Python log-triage CLI.

- systemd, Nginx, DNS, TLS, disk/inode, OOM and PostgreSQL connection scenarios.
- Severity-ranked findings with source-line evidence.
- Unit tests and CI-generated JSON reports.

### 6. [Incident Investigation Lab — Payment Webhook Failure](https://github.com/blvxx/portfolio/tree/main/incident-lab)

A simulated payment incident taken from initial symptoms through investigation and recovery.

- Python log analysis and HTTP/webhook diagnostics.
- SQL reconciliation for duplicate provider IDs and payment/order state mismatches.
- Incident timeline, RCA and recovery runbooks.

### 7. [Playwright UI Automation Lab](https://github.com/blvxx/playwright-qa-lab)

A small browser application with 8 authored Playwright scenarios and 17 documented manual test cases.

- Form validation, keyboard interaction, state changes and persistence across reload.
- Test execution report and bug report templates.
- GitHub Actions execution.

## Data and BI case studies

- [Customer Retention & Sales Analytics](https://blvxx.github.io/portfolio/customer-retention-analytics/) — public UCI Online Retail dataset, transaction cleaning, RFM segmentation, cohort retention and aggregate dashboard.
- [Subscription Revenue & Retention](https://blvxx.github.io/portfolio/subscription-revenue-analytics/) — PostgreSQL subscription lifecycle model, MRR/ARR, GRR/NRR and data-quality assertions.
- [Support Operations Analytics](https://github.com/blvxx/portfolio/tree/main/support-operations-analytics) — SQL analysis of SLA, backlog, priority mix and workload.

## How I approach engineering work

1. Clarify the requirement, constraints and expected behaviour.
2. Identify system boundaries, dependencies and failure modes.
3. Choose the simplest design that meets the requirements.
4. Verify behaviour with automated tests and reproducible checks.
5. Document operational constraints, trade-offs and recovery steps.

## Current engineering direction

The Telegram Business Assistant now has two runtime profiles, a shared PostgreSQL persistence adapter, Redis-backed FSM and event isolation, HTTPS webhook mode, a transactional outbox with SKIP LOCKED worker coordination, replay-safe submission, health/readiness endpoints, Prometheus metrics and alert rules. CI validates 53 tests against PostgreSQL and Redis services, a PostgreSQL backup/restore drill in a disposable database, Prometheus configuration/rules and a Docker build.

A separate AI Support Triage Agent integrates the OpenAI Responses API with a runbook retrieval layer, structured output validation, evidence allow-listing and read-only safety guardrails. Six offline tests pass; live model evaluation remains opt-in and requires an API key.

The remaining operational work is to deploy the shared-runtime profile to a suitable host, verify persistent managed storage, set up scheduled off-host backups and alert notification delivery, and complete a real host-level restore drill.

The current project status and planned work are documented separately:
- [Architecture and current-state analysis](https://github.com/blvxx/portfolio/blob/main/telegram-business-assistant/docs/engineering/architecture.md)
- [Security threat model](https://github.com/blvxx/portfolio/blob/main/telegram-business-assistant/docs/engineering/security/threat-model.md)
- [Engineering roadmap](https://github.com/blvxx/portfolio/blob/main/telegram-business-assistant/docs/engineering/roadmap.md)

## Delivery process and business constraints

A [delivery simulation pack](https://github.com/blvxx/portfolio/tree/main/docs/delivery-simulation) demonstrates requirements decomposition, a prioritised backlog, acceptance criteria, a scope-change decision, simulated review feedback, UAT, handover and a retrospective. The company and stakeholders in this pack are fictional. This is practice evidence, not a claim of real client delivery, team employment or commercial budget ownership.

## Project transparency

The projects above are independent portfolio work. FinTech payment flows and incident records are simulated; the subscription analytics fixture is fictional; the customer-retention case uses the attributed public UCI Online Retail dataset. These projects are not presented as commercial client deliveries or employment history. Each repository documents its own scope and limitations.

## Contact

- **Email:** [blvx8x@gmail.com](mailto:blvx8x@gmail.com)
- **Telegram:** [@blvlxx](https://t.me/blvlxx)
