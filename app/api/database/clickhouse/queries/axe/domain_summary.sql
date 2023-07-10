# Relative Path: app/api/database/clickhouse/queries/axe/domain_summary.sql
-- Domain Filter with URL Count
SELECT
    at.domain AS "domain_name",
    COUNT(DISTINCT at.url_id) AS "urls_testes",
    COUNTIf(at.rule_type = 'passes') AS "count_passes",
    COUNTIf(at.rule_type = 'violations') AS "count_violations",
    COUNTIf(at.rule_type = 'incompatible') AS "count_incompatibles",
    COUNT(*) AS "count_recent_tests"
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
GROUP BY at.domain;