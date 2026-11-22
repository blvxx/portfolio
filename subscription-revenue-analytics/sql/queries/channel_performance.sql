-- Monthly active-customer and MRR contribution by acquisition channel and region.
SELECT month_start,acquisition_channel,region,active_customers,active_subscriptions,
       ending_mrr,
       ROUND(100.0*ending_mrr/NULLIF(SUM(ending_mrr) OVER (PARTITION BY month_start),0),2)
         AS monthly_mrr_share_pct
FROM bi_mart_channel_performance
ORDER BY month_start,ending_mrr DESC,acquisition_channel,region;
