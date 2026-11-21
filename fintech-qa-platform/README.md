# FinTech QA Engineering Platform

[![FinTech QA Platform](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/fintech-qa-platform.yml)

An end-to-end QA engineering portfolio project for a fictional payment product. It demonstrates manual test design, REST API testing, service integration, database validation, Python automation and CI.

Demo environment only. No real money, banks, customer records or production systems are involved.

## Architecture

- Payment Service accepts payment requests, validates business rules and coordinates ledger posting.
- Ledger Service records balanced debit/credit entries and exposes account balances.
- PostgreSQL persists payments, transfers and ledger entries. The services own separate tables in the demo database.
- pytest covers isolated API behavior and cross-service contracts.
- Postman provides an executable manual API collection.
- GitHub Actions runs linting, automated tests and a Docker Compose smoke flow.

See Test Strategy, Test Plan, Test Cases, and Risk Analysis in the docs directory.

## Quick start

~~~
cd fintech-qa-platform
docker compose up --build
~~~

Services:
- Payment API: http://localhost:8000/docs
- Ledger API: http://localhost:8001/docs

Create a payment:

~~~
curl -X POST http://localhost:8000/payments \
  -H "Content-Type: application/json" \
  -d '{
    "idempotency_key": "demo-payment-0001",
    "customer_account": "customer-001",
    "merchant_account": "merchant-001",
    "amount_minor": 2500,
    "currency": "RUB"
  }'
~~~

Verify balances:

~~~
curl http://localhost:8001/accounts/customer-001/balance
curl http://localhost:8001/accounts/merchant-001/balance
~~~

The customer balance should be debited by 2500 minor units and the merchant balance credited by the same amount.

## Run tests locally

~~~
python -m venv .venv
pip install -r requirements.txt
pytest
ruff check services tests
~~~

The automated test suite uses isolated in-memory SQLite databases and controlled dependency fakes. It does not require Docker or external network access.

## Test coverage

- Payment creation and status retrieval.
- Ledger debit/credit conservation.
- Idempotent retries and conflicting key reuse.
- Invalid amounts and identical account validation.
- Payment-to-ledger dependency failure.
- API response and HTTP status assertions.
- Docker Compose smoke test against PostgreSQL.

See the Postman collection in postman/fintech-qa-platform.postman_collection.json.

## Known limitations

- Both services use one PostgreSQL instance in this demonstration, but own separate tables.
- The payment-to-ledger call is synchronous. This is not a distributed transaction and does not implement an outbox/saga pattern.
- Authentication, authorization, rate limiting, load testing and production security controls are out of scope.
- The bug report file contains templates and illustrative examples, not claims of observed defects.

## Maintainer

Artem Kalinin — https://github.com/blvxx
