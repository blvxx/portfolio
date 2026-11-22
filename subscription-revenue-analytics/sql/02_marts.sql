-- Analytical marts: month-end state, event movements, MRR bridge and cohorts.
CREATE OR REPLACE VIEW bi_mart_subscription_month_end AS
WITH bounds AS (
 SELECT date_trunc('month',MIN(event_at))::date AS first_month,
        date_trunc('month',MAX(event_at))::date AS last_month
 FROM bi_subscription_events
),
months AS (
 SELECT generate_series(first_month,last_month,INTERVAL '1 month')::date AS month_start
 FROM bounds
),
ranked_events AS (
 SELECT m.month_start,e.subscription_id,e.customer_id,e.event_type,e.event_at,
        e.plan_id,e.mrr_after,
        ROW_NUMBER() OVER (
          PARTITION BY m.month_start,e.subscription_id
          ORDER BY e.event_at DESC,e.event_id DESC
        ) AS event_rank
 FROM months m
 JOIN bi_subscription_events e
   ON e.event_at < (m.month_start + INTERVAL '1 month')
)
SELECT month_start,subscription_id,customer_id,plan_id,
       mrr_after AS ending_mrr
FROM ranked_events
WHERE event_rank=1 AND event_type <> 'cancelled';

CREATE OR REPLACE VIEW bi_mart_event_movements AS
WITH ordered_events AS (
 SELECT e.*,
        LAG(mrr_after) OVER (
          PARTITION BY subscription_id
          ORDER BY event_at,event_id
        ) AS previous_mrr
 FROM bi_subscription_events e
)
SELECT event_id,subscription_id,customer_id,event_type,event_at,
       date_trunc('month',event_at)::date AS month_start,
       plan_id,
       COALESCE(previous_mrr,0)::numeric(12,2) AS previous_mrr,
       mrr_after,
       CASE WHEN event_type='activated' THEN mrr_after ELSE 0 END::numeric(12,2) AS new_mrr,
       CASE WHEN event_type='upgraded' THEN mrr_after-previous_mrr ELSE 0 END::numeric(12,2) AS expansion_mrr,
       CASE WHEN event_type='downgraded' THEN previous_mrr-mrr_after ELSE 0 END::numeric(12,2) AS contraction_mrr,
       CASE WHEN event_type='cancelled' THEN previous_mrr ELSE 0 END::numeric(12,2) AS churned_mrr
FROM ordered_events;

CREATE OR REPLACE VIEW bi_mart_monthly_kpis AS
WITH bounds AS (
 SELECT date_trunc('month',MIN(event_at))::date AS first_month,
        date_trunc('month',MAX(event_at))::date AS last_month
 FROM bi_subscription_events
),
months AS (
 SELECT generate_series(first_month,last_month,INTERVAL '1 month')::date AS month_start
 FROM bounds
),
balances AS (
 SELECT m.month_start,
        COALESCE(SUM(s.ending_mrr),0)::numeric(14,2) AS ending_mrr,
        COUNT(DISTINCT s.subscription_id)::integer AS active_subscriptions,
        COUNT(DISTINCT s.customer_id)::integer AS active_customers
 FROM months m
 LEFT JOIN bi_mart_subscription_month_end s USING(month_start)
 GROUP BY m.month_start
),
movements AS (
 SELECT month_start,
        SUM(new_mrr)::numeric(14,2) AS new_mrr,
        SUM(expansion_mrr)::numeric(14,2) AS expansion_mrr,
        SUM(contraction_mrr)::numeric(14,2) AS contraction_mrr,
        SUM(churned_mrr)::numeric(14,2) AS churned_mrr,
        COUNT(*) FILTER (WHERE event_type='activated')::integer AS new_subscriptions,
        COUNT(*) FILTER (WHERE event_type='cancelled')::integer AS churned_subscriptions
 FROM bi_mart_event_movements
 GROUP BY month_start
),
with_opening_balance AS (
 SELECT b.*,
        COALESCE(LAG(b.ending_mrr) OVER (ORDER BY b.month_start),0)::numeric(14,2) AS opening_mrr,
        COALESCE(m.new_mrr,0)::numeric(14,2) AS new_mrr,
        COALESCE(m.expansion_mrr,0)::numeric(14,2) AS expansion_mrr,
        COALESCE(m.contraction_mrr,0)::numeric(14,2) AS contraction_mrr,
        COALESCE(m.churned_mrr,0)::numeric(14,2) AS churned_mrr,
        COALESCE(m.new_subscriptions,0)::integer AS new_subscriptions,
        COALESCE(m.churned_subscriptions,0)::integer AS churned_subscriptions
 FROM balances b
 LEFT JOIN movements m USING(month_start)
)
SELECT month_start,opening_mrr,new_mrr,expansion_mrr,contraction_mrr,churned_mrr,
       ending_mrr,(ending_mrr*12)::numeric(14,2) AS ending_arr,
       active_subscriptions,active_customers,new_subscriptions,churned_subscriptions,
       CASE WHEN opening_mrr=0 THEN NULL
            ELSE ROUND(100*(opening_mrr-contraction_mrr-churned_mrr)/opening_mrr,2)
       END AS gross_revenue_retention_pct,
       CASE WHEN opening_mrr=0 THEN NULL
            ELSE ROUND(100*(opening_mrr+expansion_mrr-contraction_mrr-churned_mrr)/opening_mrr,2)
       END AS net_revenue_retention_pct,
       ROUND(ending_mrr-(opening_mrr+new_mrr+expansion_mrr-contraction_mrr-churned_mrr),2)
           AS mrr_bridge_delta
FROM with_opening_balance;

CREATE OR REPLACE VIEW bi_mart_cohort_retention AS
WITH first_activation AS (
 SELECT customer_id,date_trunc('month',MIN(event_at))::date AS cohort_month
 FROM bi_subscription_events
 WHERE event_type='activated'
 GROUP BY customer_id
),
cohort_sizes AS (
 SELECT cohort_month,COUNT(*)::integer AS cohort_size
 FROM first_activation
 GROUP BY cohort_month
),
month_spine AS (
 SELECT DISTINCT month_start FROM bi_mart_monthly_kpis
),
cohort_grid AS (
 SELECT c.cohort_month,m.month_start,
        ((EXTRACT(YEAR FROM m.month_start)::integer-EXTRACT(YEAR FROM c.cohort_month)::integer)*12
         + EXTRACT(MONTH FROM m.month_start)::integer-EXTRACT(MONTH FROM c.cohort_month)::integer)
           ::integer AS month_number,
        c.cohort_size
 FROM cohort_sizes c
 JOIN month_spine m ON m.month_start>=c.cohort_month
),
active_by_cohort AS (
 SELECT g.cohort_month,g.month_start,g.month_number,g.cohort_size,
        COUNT(DISTINCT s.customer_id)::integer AS active_customers
 FROM cohort_grid g
 JOIN first_activation f USING(cohort_month)
 LEFT JOIN bi_mart_subscription_month_end s
   ON s.month_start=g.month_start AND s.customer_id=f.customer_id
 GROUP BY g.cohort_month,g.month_start,g.month_number,g.cohort_size
)
SELECT cohort_month,month_start,month_number,cohort_size,active_customers,
       ROUND(100.0*active_customers/NULLIF(cohort_size,0),2) AS retention_pct
FROM active_by_cohort;

CREATE OR REPLACE VIEW bi_mart_channel_performance AS
SELECT s.month_start,c.acquisition_channel,c.region,
       COUNT(DISTINCT s.customer_id)::integer AS active_customers,
       COUNT(DISTINCT s.subscription_id)::integer AS active_subscriptions,
       SUM(s.ending_mrr)::numeric(14,2) AS ending_mrr
FROM bi_mart_subscription_month_end s
JOIN bi_customers c USING(customer_id)
GROUP BY s.month_start,c.acquisition_channel,c.region;
