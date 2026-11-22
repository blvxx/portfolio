-- Current backlog and age bands. Snapshot is query execution time, not historical daily backlog.
WITH active AS (
 SELECT ticket_id, priority, status, created_at,
        NOW() - created_at AS age
 FROM tickets
 WHERE resolved_at IS NULL
)
SELECT priority, COUNT(*) AS backlog,
       COUNT(*) FILTER (WHERE age < INTERVAL '24 hours') AS under_24h,
       COUNT(*) FILTER (WHERE age >= INTERVAL '24 hours' AND age < INTERVAL '72 hours') AS age_24_72h,
       COUNT(*) FILTER (WHERE age >= INTERVAL '72 hours') AS over_72h,
       ROUND(AVG(EXTRACT(EPOCH FROM age)/3600)::numeric,2) AS avg_age_hours
FROM active
GROUP BY priority
ORDER BY priority;
