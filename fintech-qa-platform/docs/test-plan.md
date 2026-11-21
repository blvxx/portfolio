# Test Plan

## Scope

Payment creation, ledger posting, idempotency, account balances, input validation, service readiness and cross-service failure handling.

## Out of scope

Real payment rails, bank integrations, authentication/authorization, production security certification, load testing and distributed transaction guarantees.

## Environments

| Environment | Components | Purpose |
|---|---|---|
| Local tests | FastAPI TestClient + SQLite | Deterministic unit/API checks |
| CI | Python 3.12 + SQLite | Lint and automated test suite |
| Compose | Payment + Ledger + PostgreSQL | Cross-service smoke test |

## Scenarios

1. Valid payment creates a ledger debit and credit.
2. Ledger balance remains conserved across both accounts.
3. Repeated payment request with the same idempotency key does not call Ledger twice.
4. Same key with a changed amount returns HTTP 409.
5. Zero or negative amount is rejected with HTTP 422.
6. Same source and destination account is rejected.
7. Ledger failure is surfaced as HTTP 502 and payment is marked failed.
8. Unknown payment returns HTTP 404.
9. Readiness endpoint executes a database query.

## Risks and mitigations

See risk-analysis.md. Test data is isolated per test and no external APIs are called by the automated suite.
