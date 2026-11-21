# SQL investigation playbook

The examples below target PostgreSQL and the demo schema. Use read-only queries first; do not manually change payment state during an investigation.

## 1. Find a payment by customer reference

```sql
SELECT id, customer_reference, amount_minor, currency, status, created_at
FROM payments
WHERE customer_reference = 'ORDER-1001';
```

## 2. Review recent payments in a non-terminal state

```sql
SELECT id, customer_reference, amount_minor, currency, status, created_at
FROM payments
WHERE status = 'pending'
  AND created_at >= NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;
```

## 3. Check whether a webhook event was already received

```sql
SELECT event_id, payload_hash, received_at
FROM webhook_events
WHERE event_id = 'evt-1001';
```

An existing event with the same ID should be treated as a retry only when the payload hash matches. A reused event ID with a different hash is a conflict requiring investigation.

## 4. Find payments with repeated customer references

```sql
SELECT customer_reference, COUNT(*) AS payment_count,
       MIN(created_at) AS first_seen, MAX(created_at) AS last_seen
FROM payments
GROUP BY customer_reference
HAVING COUNT(*) > 1
ORDER BY payment_count DESC;
```

This is an investigation signal, not proof of duplicate charging. Compare amount, currency, timestamps and upstream order IDs before escalating.

## 5. Build a status distribution

```sql
SELECT status, COUNT(*) AS payment_count,
       SUM(amount_minor) AS total_amount_minor
FROM payments
GROUP BY status
ORDER BY payment_count DESC;
```

## Suggested incident notes

Record the customer reference, payment ID, event ID, timestamps with timezone, observed status, query used, relevant log correlation ID, and the next owner/action. Redact secrets and personal/payment-card data.
