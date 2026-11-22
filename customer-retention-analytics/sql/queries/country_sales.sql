SELECT
    country,
    ROUND(SUM(revenue), 2) AS revenue_gbp,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM sales
GROUP BY country
ORDER BY revenue_gbp DESC
LIMIT 10;
