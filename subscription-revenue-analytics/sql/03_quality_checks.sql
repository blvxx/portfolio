-- Assertions intentionally raise exceptions so CI fails on a broken data model.
DO $$
BEGIN
 IF (SELECT COUNT(*) FROM bi_customers) <> 30 THEN
   RAISE EXCEPTION 'Expected 30 synthetic customers';
 END IF;
 IF (SELECT COUNT(*) FROM bi_subscription_events) <> 43 THEN
   RAISE EXCEPTION 'Expected 43 subscription events';
 END IF;
 IF (SELECT COUNT(*) FROM bi_mart_monthly_kpis) <> 18 THEN
   RAISE EXCEPTION 'Expected 18 monthly reporting periods';
 END IF;

 IF EXISTS (
   SELECT 1 FROM (
     SELECT e.*,
       LAG(e.mrr_after) OVER (PARTITION BY e.subscription_id ORDER BY e.event_at,e.event_id) AS previous_mrr,
       LAG(e.event_type) OVER (PARTITION BY e.subscription_id ORDER BY e.event_at,e.event_id) AS previous_event_type,
       ROW_NUMBER() OVER (PARTITION BY e.subscription_id ORDER BY e.event_at,e.event_id) AS event_number
     FROM bi_subscription_events e
   ) ordered
   WHERE (event_number=1 AND event_type<>'activated')
      OR (event_number>1 AND event_type='activated')
      OR (previous_event_type='cancelled')
      OR (event_type='upgraded' AND (previous_mrr IS NULL OR mrr_after<=previous_mrr))
      OR (event_type='downgraded' AND (previous_mrr IS NULL OR mrr_after>=previous_mrr OR mrr_after=0))
      OR (event_type='cancelled' AND (previous_mrr IS NULL OR previous_mrr<=0 OR mrr_after<>0))
 ) THEN
   RAISE EXCEPTION 'Invalid subscription lifecycle transition';
 END IF;

 IF EXISTS (
   SELECT 1 FROM bi_subscription_events e
   JOIN bi_plans p USING(plan_id)
   WHERE e.event_type<>'cancelled' AND e.mrr_after<>p.monthly_price
 ) THEN
   RAISE EXCEPTION 'Event MRR does not match referenced plan price';
 END IF;

 IF EXISTS (
   SELECT 1 FROM bi_subscription_events
   GROUP BY subscription_id
   HAVING COUNT(DISTINCT customer_id)<>1
 ) THEN
   RAISE EXCEPTION 'A subscription is associated with multiple customers';
 END IF;

 IF EXISTS (
   SELECT 1 FROM bi_mart_monthly_kpis
   WHERE ABS(mrr_bridge_delta)>0.01
 ) THEN
   RAISE EXCEPTION 'Monthly MRR bridge does not reconcile';
 END IF;

 IF EXISTS (
   SELECT 1 FROM bi_mart_cohort_retention
   WHERE retention_pct<0 OR retention_pct>100
 ) THEN
   RAISE EXCEPTION 'Cohort retention percentage is outside 0-100';
 END IF;

 RAISE NOTICE 'All subscription analytics quality checks passed.';
END;
$$;
