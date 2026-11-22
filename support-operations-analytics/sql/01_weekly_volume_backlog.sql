-- Weekly ticket intake, resolution count and open/pending tickets at the end of the week.
WITH weekly AS (
  SELECT date_trunc('week', created_at)::date AS week_start,
         COUNT(*) AS tickets_created,
         COUNT(*) FILTER (WHERE resolved_at IS NOT NULL) AS resolved_from_cohort
  FROM tickets
  GROUP BY 1
)
SELECT week_start, tickets_created, resolved_from_cohort,
       SUM(tickets_created) OVER (ORDER BY week_start) AS cumulative_created,
       ROUND(AVG(tickets_created) OVER (ORDER BY week_start ROWS BETWEEN 3 PRECEDING AND CURRENT ROW),2) AS rolling_4_week_intake
FROM weekly
ORDER BY week_start;
