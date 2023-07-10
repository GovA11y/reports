-- Get Curent Violations
-- Relative Path: app/api/database/clickhouse/queries/axe/current_violations.sql
SELECT *
FROM
    axe_tests at
INNER JOIN
    (
    SELECT url_id, axe_id, target, max(tested_at) as max_tested_at
    FROM axe_tests
    GROUP BY url_id, axe_id, target
    ) sub
ON at.url_id=sub.url_id AND at.axe_id=sub.axe_id AND at.target=sub.target AND at.tested_at=sub.max_tested_at
WHERE at.domain LIKE '%s'
AND rule_type = '%s';