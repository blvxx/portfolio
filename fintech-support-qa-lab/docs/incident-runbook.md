# Incident troubleshooting runbook

This runbook uses synthetic demo data. Never run the example SQL against production without following the organization's access and change-control procedures.

## 1. API is up, but database readiness fails

**Symptoms**
- `GET /health` returns `200`.
- `GET /health/ready` returns `503 Database unavailable`.
- Payment requests may fail because persistence is unavailable.

**Checks**
```bash
docker compose ps
docker compose logs --tail=100 api
docker compose logs --tail=100 db
docker compose exec db pg_isready -U lab -d fintech_lab
```

**Response**
1. Check whether the database container is healthy.
2. Inspect database logs for authentication, disk, startup, or connection errors.
3. Confirm the API's `DATABASE_URL` points to host `db` on port `5432` from inside Compose.
4. Restore database availability before retrying failed writes.
5. Verify `GET /health/ready` returns `200` and then perform a controlled payment read/write check.

Do not delete the database volume as a first-line troubleshooting step.

## 2. Webhook returns 401

**Likely cause:** missing or invalid HMAC signature.

**Checks**
- Confirm sender and API use the same `WEBHOOK_SECRET`.
- Sign the exact raw request body bytes, not a re-serialized JSON object.
- Use SHA-256 HMAC and send `X-Signature: sha256=<hex_digest>`.
- Check that a proxy or client has not modified the request body.

**Expected result:** a valid signature is accepted; an invalid signature is rejected without changing payment status.

## 3. Webhook returns 409

**Possible causes**
- The event ID was reused with a different payload.
- The requested payment status transition is not allowed.
- A payment is already in a terminal state (`paid` or `failed`).

**Checks**
```sql
SELECT id, customer_reference, status, created_at
FROM payments
WHERE id = :payment_id;

SELECT event_id, payload_hash, received_at
FROM webhook_events
WHERE event_id = :event_id;
```

Compare the event ID and payload hash with the sender's delivery record. Do not manually change payment state to bypass transition validation.

## 4. Payment is not found (404)

**Checks**
```sql
SELECT id, customer_reference, amount_minor, currency, status, created_at
FROM payments
WHERE id = :payment_id;

SELECT id, customer_reference, status, created_at
FROM payments
WHERE customer_reference = :customer_reference;
```

Confirm the environment, payment ID, and customer reference. A payment created in a local SQLite environment will not automatically exist in the PostgreSQL Compose environment.

## 5. Safe recovery checklist

- Capture timestamp, endpoint, HTTP status, correlation/event ID, and sanitized error details.
- Establish scope: one payment, one customer, or all requests.
- Check API process health and database readiness separately.
- Preserve logs and database evidence before attempting recovery.
- Retry only after confirming whether the original operation committed; use the webhook event ID to avoid duplicate processing.
- Record root cause, mitigation, verification, and follow-up actions.

## Operational note

`/health` is a process-level check. `/health/ready` executes `SELECT 1` against the configured database and is the readiness signal for database-dependent operations.
