-- Basic data-quality checks: each result should be zero unless explained.
SELECT 'resolved_before_created' AS check_name, COUNT(*) AS failures
FROM tickets WHERE resolved_at < created_at
UNION ALL
SELECT 'first_response_before_created', COUNT(*)
FROM tickets WHERE first_response_at < created_at
UNION ALL
SELECT 'resolved_without_first_response', COUNT(*)
FROM tickets WHERE resolved_at IS NOT NULL AND first_response_at IS NULL
UNION ALL
SELECT 'resolved_status_without_timestamp', COUNT(*)
FROM tickets WHERE status='resolved' AND resolved_at IS NULL
UNION ALL
SELECT 'active_status_with_timestamp', COUNT(*)
FROM tickets WHERE status IN ('open','pending') AND resolved_at IS NOT NULL;
