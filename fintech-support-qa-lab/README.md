# Fintech Support & QA Lab

A practical sandbox for demonstrating API testing, SQL investigation, incident troubleshooting, webhook integrations and technical documentation.

> This is a learning/demo project. It does not process real payments, connect to a bank, or contain real customer data.

## Scope

- FastAPI service for a minimal payment lifecycle.
- SQLAlchemy persistence; SQLite for local tests and PostgreSQL in Docker.
- Automated API tests with pytest and FastAPI TestClient.
- HMAC-SHA256 webhook signature validation.
- Idempotent webhook processing with event-ID uniqueness and payload-hash conflict detection.
- SQL investigation playbook with practical support queries.
- Synthetic JSONL logs and a Python CLI for filtering by correlation ID or severity.
- GitHub Actions CI for automated tests, including a live PostgreSQL service integration check.

## Quick start (local)

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir src
```

For local webhook testing, set `WEBHOOK_SECRET` to a private test value before starting the API. The built-in default is for local demonstration only and must not be used in a real environment.

Open Swagger UI at http://127.0.0.1:8000/docs.

## Run tests

```bash
pytest -q
```

## Analyze the synthetic logs

From the project root:

```bash
python scripts/analyze_logs.py
python scripts/analyze_logs.py --level ERROR
python scripts/analyze_logs.py --correlation-id corr-a81
```

The sample dataset is in `samples/payment-api.log`. It contains synthetic events only.

## Run with PostgreSQL

```bash
docker compose up --build
```

The API is available at http://localhost:8000 and PostgreSQL is exposed on port 5432.

## Postman collection

Import `postman/fintech-support-qa-lab.postman_collection.json` into Postman. Set the collection variables `baseUrl` (default `http://localhost:8000`) and `webhook_secret` to the same value as the API `WEBHOOK_SECRET`. Run the requests in order: health check, create payment, retrieve payment, signed webhook, then the invalid-transition check. The webhook pre-request script calculates the HMAC-SHA256 signature and generates a fresh event ID for each run.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/payments` | Create a demo payment |
| GET | `/payments/{payment_id}` | Retrieve payment |
| PATCH | `/payments/{payment_id}/status` | Change payment status |
| POST | `/webhooks/payment-status` | Receive signed, idempotent payment events |

Webhook details are documented in [docs/webhooks.md](docs/webhooks.md). SQL support queries are in [docs/sql-investigation.md](docs/sql-investigation.md), and payment states are in [docs/payment-lifecycle.md](docs/payment-lifecycle.md).

## Project structure

```
src/app/       FastAPI application and persistence
tests/         API, webhook and log analyzer tests
docs/          Support and integration documentation
samples/       Synthetic application logs
scripts/       Log analysis CLI
```

## Roadmap

- [x] Initial API and automated tests
- [x] Webhook HMAC signature validation
- [x] Idempotent webhook processing and event conflict detection
- [x] SQL investigation playbook
- [x] Synthetic incident logs and analysis CLI
- [x] PostgreSQL persistence integration test in CI
- [ ] Local Docker Compose smoke test
- [x] Postman collection with signed webhook request

## Transparency

All records are generated locally for demonstration. No production systems, real payments or personal data are used.
