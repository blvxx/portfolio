-- Long-form customer cohort output, ready for a BI pivot or heatmap.
SELECT cohort_month,month_number,cohort_size,active_customers,retention_pct
FROM bi_mart_cohort_retention
ORDER BY cohort_month,month_number;
