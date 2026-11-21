-- Incident Lab: PostgreSQL diagnostic queries
-- Fictional schema/data. Adapt and review before running on any real system.

-- 1. Paid payments where the order is not marked paid (primary incident).
SELECT o.id AS order_id, o.status AS order_status, p.status AS payment_status,
       p.provider_payment_id, p.paid_at, o.total_amount
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE p.status = 'succeeded' AND o.status <> 'paid'
ORDER BY p.paid_at;

-- 2. Orders with multiple successful payment rows.
SELECT order_id, COUNT(*) AS successful_payment_rows,
       COUNT(DISTINCT provider_payment_id) AS distinct_provider_payments
FROM payments
WHERE status = 'succeeded'
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 3. Repeated provider payment identifiers.
SELECT provider_payment_id, COUNT(*) AS rows_count,
       COUNT(DISTINCT order_id) AS orders_count
FROM payments
GROUP BY provider_payment_id
HAVING COUNT(*) > 1;

-- 4. Pending orders without successful payment records.
SELECT o.id, o.status, o.total_amount, COUNT(p.id) AS payment_rows
FROM orders o
LEFT JOIN payments p ON p.order_id = o.id AND p.status = 'succeeded'
WHERE o.status = 'pending_payment'
GROUP BY o.id, o.status, o.total_amount
HAVING COUNT(p.id) = 0
ORDER BY o.created_at;

-- 5. Summary reconciliation counts.
SELECT
  COUNT(*) FILTER (WHERE o.status = 'pending_payment' AND p.status = 'succeeded')
      AS paid_but_pending_orders,
  COUNT(*) FILTER (WHERE p.status = 'failed')
      AS failed_payment_rows,
  COUNT(*) FILTER (WHERE p.status = 'succeeded')
      AS successful_payment_rows
FROM orders o
JOIN payments p ON p.order_id = o.id;
