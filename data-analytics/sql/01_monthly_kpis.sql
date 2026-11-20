-- Monthly order funnel and sales KPIs.
WITH order_metrics AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS order_month,
        COUNT(*) AS total_orders,
        COUNT(*) FILTER (WHERE payment_status = 'paid') AS paid_orders,
        COUNT(*) FILTER (WHERE payment_status = 'cancelled') AS cancelled_orders,
        COUNT(*) FILTER (WHERE payment_status = 'pending') AS pending_orders,
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND NOT is_returned) AS completed_orders,
        COUNT(*) FILTER (WHERE payment_status = 'paid' AND is_returned) AS returned_orders,
        SUM(
            CASE
                WHEN payment_status = 'paid' AND NOT is_returned
                THEN quantity * unit_price * (1 - discount_pct)
                ELSE 0
            END
        ) AS recognised_revenue
    FROM orders
    GROUP BY 1
)
SELECT
    order_month,
    total_orders,
    paid_orders,
    cancelled_orders,
    pending_orders,
    completed_orders,
    returned_orders,
    ROUND(recognised_revenue, 2) AS recognised_revenue,
    ROUND(recognised_revenue / NULLIF(completed_orders, 0), 2) AS average_order_value,
    ROUND(returned_orders::numeric / NULLIF(paid_orders, 0), 4) AS return_rate
FROM order_metrics
ORDER BY order_month;
