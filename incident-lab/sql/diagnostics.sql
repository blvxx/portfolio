-- Incident Investigation Lab: PostgreSQL diagnostic queries
-- Illustrative schema only. Do not run against a real database without adapting and reviewing.

-- 1. Orders stuck awaiting payment while payment record says succeeded
SELECT
    o.id AS order_id,
    o.created_at,
    o.status AS order_status,
    p.status AS payment_status,
    p.provider_payment_id,
    p.paid_at
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE o.status = 'pending_payment'
  AND p.status = 'succeeded'
ORDER BY p.paid_at;

-- 2. Count potentially affected orders by status mismatch
SELECT
    o.status AS order_status,
    p.status AS payment_status,
    COUNT(*) AS records_count
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE o.created_at >= TIMESTAMP '2026-11-20 09:12:00'
  AND o.created_at <  TIMESTAMP '2026-11-20 10:04:00'
GROUP BY o.status, p.status
ORDER BY records_count DESC;

-- 3. Failed webhook events during the incident window
SELECT
    id,
    provider_event_id,
    event_type,
    received_at,
    processing_status,
    error_message
FROM webhook_events
WHERE received_at >= TIMESTAMP '2026-11-20 09:12:00'
  AND received_at <  TIMESTAMP '2026-11-20 10:04:00'
  AND processing_status = 'failed'
ORDER BY received_at;

-- 4. Check duplicate provider payment IDs (should return no rows)
SELECT provider_payment_id, COUNT(*) AS duplicate_count
FROM payments
WHERE provider_payment_id IS NOT NULL
GROUP BY provider_payment_id
HAVING COUNT(*) > 1;

-- 5. Reconciliation summary: paid provider records vs order state
SELECT
    COUNT(*) FILTER (WHERE p.status = 'succeeded') AS successful_payments,
    COUNT(*) FILTER (WHERE p.status = 'succeeded' AND o.status <> 'paid') AS paid_payment_order_mismatches
FROM payments p
JOIN orders o ON o.id = p.order_id;
