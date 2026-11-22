-- First response and resolution SLA by priority. Unresolved tickets are not included in resolved SLA.
WITH sla_targets AS (
  SELECT * FROM (VALUES
    ('P1',60,8),('P2',60,24),('P3',240,72),('P4',240,120)
  ) AS t(priority, first_response_minutes, resolution_hours)
),
metrics AS (
 SELECT t.*, s.first_response_minutes, s.resolution_hours,
        EXTRACT(EPOCH FROM (first_response_at-created_at))/60 AS first_response_min,
        EXTRACT(EPOCH FROM (resolved_at-created_at))/3600 AS resolution_hours_actual
 FROM tickets t JOIN sla_targets s USING(priority)
)
SELECT priority, COUNT(*) AS total_tickets,
       COUNT(*) FILTER (WHERE first_response_at IS NOT NULL) AS responded,
       ROUND(100.0*COUNT(*) FILTER (WHERE first_response_at IS NOT NULL AND first_response_min <= first_response_minutes)/NULLIF(COUNT(*) FILTER (WHERE first_response_at IS NOT NULL),0),2) AS first_response_sla_pct,
       COUNT(*) FILTER (WHERE resolved_at IS NOT NULL) AS resolved,
       ROUND(100.0*COUNT(*) FILTER (WHERE resolved_at IS NOT NULL AND resolution_hours_actual <= resolution_hours)/NULLIF(COUNT(*) FILTER (WHERE resolved_at IS NOT NULL),0),2) AS resolution_sla_pct
FROM metrics
GROUP BY priority
ORDER BY priority;
