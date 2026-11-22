SELECT priority, COUNT(*) FILTER (WHERE resolved_at IS NOT NULL) AS resolved_count,
       ROUND(AVG(EXTRACT(EPOCH FROM (resolved_at-created_at))/3600)::numeric,2) AS avg_hours,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (resolved_at-created_at))/3600))::numeric,2) AS median_hours,
       ROUND((PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (resolved_at-created_at))/3600))::numeric,2) AS p90_hours
FROM tickets
GROUP BY priority
ORDER BY priority;
