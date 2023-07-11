-- Get Curent Violations
-- Relative Path: app/api/database/clickhouse/queries/axe/current_violations.sql
SELECT *
FROM gova11y.axe_tests_recent
WHERE domain ILIKE '%s'
  AND rule_type IN (%s)
ORDER BY tested_at DESC
LIMIT %s;
