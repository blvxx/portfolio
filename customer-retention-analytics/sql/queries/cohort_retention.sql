WITH customer_months AS (
    SELECT DISTINCT
        customer_id,
        substr(invoice_date, 1, 7) AS active_month
    FROM sales
    WHERE customer_id IS NOT NULL
),
first_purchase AS (
    SELECT
        customer_id,
        MIN(active_month) AS cohort_month
    FROM customer_months
    GROUP BY customer_id
),
cohort_activity AS (
    SELECT
        p.cohort_month,
        m.customer_id,
        m.active_month,
        (
            (CAST(substr(m.active_month, 1, 4) AS INTEGER)
             - CAST(substr(p.cohort_month, 1, 4) AS INTEGER)) * 12
            + CAST(substr(m.active_month, 6, 2) AS INTEGER)
            - CAST(substr(p.cohort_month, 6, 2) AS INTEGER)
        ) AS month_index
    FROM customer_months AS m
    JOIN first_purchase AS p
        ON p.customer_id = m.customer_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM cohort_activity
    WHERE month_index = 0
    GROUP BY cohort_month
),
cohort_counts AS (
    SELECT
        cohort_month,
        month_index,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohort_activity
    GROUP BY cohort_month, month_index
)
SELECT
    c.cohort_month,
    c.month_index,
    s.cohort_size,
    c.active_customers,
    ROUND(1.0 * c.active_customers / NULLIF(s.cohort_size, 0), 4) AS retention_rate
FROM cohort_counts AS c
JOIN cohort_sizes AS s
    ON s.cohort_month = c.cohort_month
ORDER BY c.cohort_month, c.month_index;
