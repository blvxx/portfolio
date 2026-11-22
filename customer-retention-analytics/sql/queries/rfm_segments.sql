WITH refund_totals AS (
    SELECT
        customer_id,
        SUM(refund_amount) AS refunds_gbp
    FROM refunds
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
),
customer_metrics AS (
    SELECT
        s.customer_id,
        MAX(s.invoice_date) AS last_purchase,
        COUNT(DISTINCT s.invoice_no) AS frequency,
        MAX(COALESCE(r.refunds_gbp, 0)) AS refund_amount,
        SUM(s.revenue) AS gross_monetary
    FROM sales AS s
    LEFT JOIN refund_totals AS r
        ON r.customer_id = s.customer_id
    WHERE s.customer_id IS NOT NULL
    GROUP BY s.customer_id
),
monetary_metrics AS (
    SELECT
        customer_id,
        last_purchase,
        frequency,
        MAX(gross_monetary - refund_amount, 0) AS monetary_gbp
    FROM customer_metrics
),
scored AS (
    SELECT
        customer_id,
        CAST(julianday((SELECT MAX(invoice_date) FROM sales)) - julianday(last_purchase) AS INTEGER) AS recency_days,
        frequency,
        monetary_gbp,
        5 - NTILE(4) OVER (ORDER BY last_purchase DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_gbp ASC) AS m_score
    FROM monetary_metrics
),
classified AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_gbp,
        r_score,
        f_score,
        m_score,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal customers'
            WHEN r_score >= 3 AND f_score <= 2 THEN 'Promising'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At risk'
            ELSE 'Needs attention'
        END AS segment
    FROM scored
)
SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(AVG(recency_days), 2) AS avg_recency_days,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary_gbp), 2) AS avg_monetary_gbp
FROM classified
GROUP BY segment
ORDER BY customers DESC;
