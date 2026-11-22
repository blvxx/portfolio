-- Observed MRR-months is descriptive; it is not a contractual or predictive LTV.
WITH customer_months AS (
 SELECT customer_id,COUNT(*)::integer AS active_months,
        SUM(ending_mrr)::numeric(14,2) AS observed_mrr_months,
        MAX(month_start) AS last_active_month
 FROM bi_mart_subscription_month_end
 GROUP BY customer_id
)
SELECT c.customer_id,c.acquisition_channel,c.region,cm.active_months,
       cm.observed_mrr_months,cm.last_active_month,
       DENSE_RANK() OVER (ORDER BY cm.observed_mrr_months DESC) AS value_rank
FROM customer_months cm
JOIN bi_customers c USING(customer_id)
ORDER BY value_rank,c.customer_id;
