-- Customer activity and repeat-purchase rate.
WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND NOT is_returned) AS completed_orders,
        SUM(
            CASE
                WHEN payment_status = 'paid' AND NOT is_returned
                THEN quantity * unit_price * (1 - discount_pct)
                ELSE 0
            END
        ) AS recognised_revenue,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS unique_customers,
    COUNT(*) FILTER (WHERE total_orders > 1) AS repeat_customers,
    ROUND(
        COUNT(*) FILTER (WHERE total_orders > 1)::numeric / NULLIF(COUNT(*), 0),
        4
    ) AS repeat_customer_rate,
    SUM(completed_orders) AS completed_orders,
    ROUND(SUM(recognised_revenue), 2) AS recognised_revenue
FROM customer_activity;

-- Top customers by recognised revenue.
WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND NOT is_returned) AS completed_orders,
        SUM(
            CASE
                WHEN payment_status = 'paid' AND NOT is_returned
                THEN quantity * unit_price * (1 - discount_pct)
                ELSE 0
            END
        ) AS recognised_revenue,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_orders,
    completed_orders,
    ROUND(recognised_revenue, 2) AS recognised_revenue,
    first_order_date,
    last_order_date
FROM customer_activity
ORDER BY recognised_revenue DESC, completed_orders DESC
LIMIT 20;
