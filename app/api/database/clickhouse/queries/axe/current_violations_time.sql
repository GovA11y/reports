-- Get Curent Violations with timefilter
-- Relative Path: app/api/database/clickhouse/queries/axe/current_violations_time.sql
SELECT *
FROM gova11y.axe_tests_recent
WHERE domain ILIKE '%s'
  AND rule_type IN (%s)
  AND tested_at BETWEEN '%s' AND '%s'
ORDER BY tested_at DESC
LIMIT %s;
