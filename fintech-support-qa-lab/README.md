# Fintech Support & QA Lab

A practical sandbox for demonstrating API testing, SQL investigation, incident troubleshooting and technical documentation.

> This is a learning/demo project. It does not process real payments, connect to a bank, or contain real customer data.

## Scope

- FastAPI service for a minimal payment lifecycle.
- SQLAlchemy persistence; SQLite for local tests and PostgreSQL in Docker.
- Automated API tests with pytest and FastAPI TestClient.
- Reproducible incident scenarios and support runbooks (being added).
- Postman collection and CI workflow (being added).

## Quick start (local)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir src
```

Open Swagger UI at http://127.0.0.1:8000/docs.

## Run tests

```bash
pytest -q
```

## Run with PostgreSQL

```bash
docker compose up --build
```

The API is available at http://localhost:8000 and PostgreSQL is exposed on port 5432.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/payments` | Create a demo payment |
| GET | `/payments/{payment_id}` | Retrieve payment |
| PATCH | `/payments/{payment_id}/status` | Change payment status |

Allowed status transitions are documented in `docs/payment-lifecycle.md`.

## Project structure

```
src/app/       FastAPI application and persistence
 tests/        API tests
 docs/         Support and incident documentation
```

## Roadmap

- [x] Initial API and automated tests
- [ ] PostgreSQL integration verification
- [ ] Webhook signature validation and idempotency
- [ ] Synthetic incident logs and analysis CLI
- [ ] SQL investigation playbook
- [ ] Postman collection and CI test report

## Transparency

All records are generated locally for demonstration. No production systems, real payments or personal data are used.
