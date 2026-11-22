SELECT
    substr(invoice_date, 1, 7) AS month,
    ROUND(SUM(revenue), 2) AS revenue_gbp,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(quantity), 0) AS units,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT invoice_no), 0), 2) AS average_order_value_gbp
FROM sales
GROUP BY substr(invoice_date, 1, 7)
ORDER BY month;
