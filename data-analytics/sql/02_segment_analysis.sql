-- Compare commercial performance by region and product category.
WITH order_values AS (
    SELECT
        region,
        category,
        payment_status,
        is_returned,
        CASE
            WHEN payment_status = 'paid' AND NOT is_returned
            THEN quantity * unit_price * (1 - discount_pct)
            ELSE 0
        END AS recognised_revenue
    FROM orders
)
SELECT
    'region' AS segment_type,
    region AS segment,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE payment_status = 'paid' AND NOT is_returned) AS completed_orders,
    ROUND(SUM(recognised_revenue), 2) AS recognised_revenue,
    ROUND(
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND is_returned)::numeric
        / NULLIF(COUNT(*) FILTER (WHERE payment_status = 'paid'), 0),
        4
    ) AS return_rate
FROM order_values
GROUP BY region

UNION ALL

SELECT
    'category' AS segment_type,
    category AS segment,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE payment_status = 'paid' AND NOT is_returned) AS completed_orders,
    ROUND(SUM(recognised_revenue), 2) AS recognised_revenue,
    ROUND(
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND is_returned)::numeric
        / NULLIF(COUNT(*) FILTER (WHERE payment_status = 'paid'), 0),
        4
    ) AS return_rate
FROM order_values
GROUP BY category
ORDER BY segment_type, recognised_revenue DESC;
