-- Weekly intake and resolution counts; rolling intake is a smoothed volume indicator.
WITH created AS (
 SELECT date_trunc('week', created_at)::date AS week_start, COUNT(*) AS tickets_created
 FROM tickets GROUP BY 1
),
resolved AS (
 SELECT date_trunc('week', resolved_at)::date AS week_start, COUNT(*) AS tickets_resolved
 FROM tickets WHERE resolved_at IS NOT NULL GROUP BY 1
),
weekly AS (
 SELECT COALESCE(c.week_start,r.week_start) AS week_start,
        COALESCE(c.tickets_created,0) AS tickets_created,
        COALESCE(r.tickets_resolved,0) AS tickets_resolved
 FROM created c FULL OUTER JOIN resolved r USING(week_start)
)
SELECT week_start, tickets_created, tickets_resolved,
       SUM(tickets_created) OVER (ORDER BY week_start) AS cumulative_created,
       ROUND(AVG(tickets_created) OVER (ORDER BY week_start ROWS BETWEEN 3 PRECEDING AND CURRENT ROW),2) AS rolling_4_week_intake
FROM weekly ORDER BY week_start;
