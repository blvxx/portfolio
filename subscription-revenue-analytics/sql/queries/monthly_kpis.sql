-- Monthly recurring-revenue bridge and three-month moving average.
SELECT month_start,opening_mrr,new_mrr,expansion_mrr,contraction_mrr,churned_mrr,
       ending_mrr,ending_arr,active_customers,active_subscriptions,
       gross_revenue_retention_pct,net_revenue_retention_pct,
       ROUND(AVG(ending_mrr) OVER (
         ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ),2) AS ending_mrr_3m_avg,
       mrr_bridge_delta
FROM bi_mart_monthly_kpis
ORDER BY month_start;
