-- Relative Path: app/api/database/clickhouse/queries/axe/domain_summary.sql
-- Domain Filter with URL Count
SELECT
    "domain" AS "domain_name",
    COUNT(DISTINCT url) AS "urls_tested",
    COUNTIf(rule_type = 'passes') AS "count_passes",
    COUNTIf(rule_type = 'violations') AS "count_violations",
    COUNTIf(rule_type = 'inapplicable') AS "count_inapplicable",
    COUNT(*) AS "count_recent_tests"
FROM
    axe_tests_recent atr
WHERE "domain" LIKE '%s'
GROUP BY "domain"
ORDER BY "count_recent_tests" desc;