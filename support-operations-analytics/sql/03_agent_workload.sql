-- Workload context: assigned ticket count, active queue and median resolution time.
SELECT a.agent_name, a.team,
       COUNT(t.ticket_id) AS assigned_total,
       COUNT(*) FILTER (WHERE t.resolved_at IS NULL) AS active_queue,
       COUNT(*) FILTER (WHERE t.reopened_count > 0) AS tickets_reopened,
       ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at-t.created_at))/3600)::numeric,2) AS avg_resolution_hours,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (t.resolved_at-t.created_at))/3600))::numeric,2) AS median_resolution_hours
FROM agents a LEFT JOIN tickets t ON t.agent_id=a.agent_id
GROUP BY a.agent_id,a.agent_name,a.team
ORDER BY active_queue DESC, assigned_total DESC;
