WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice_no) AS invoice_count
    FROM sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS identified_customers,
    SUM(CASE WHEN invoice_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        100.0 * SUM(CASE WHEN invoice_count > 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_rate_pct
FROM customer_orders;
