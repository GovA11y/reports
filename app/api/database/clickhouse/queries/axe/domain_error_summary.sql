-- File Path: app/api/database/clickhouse/queries/axe/domain_error_summary.sql
-- Summary of errors by domain
SELECT "domain",
    COUNT(CASE WHEN impact = 'critical' THEN 1 END) AS count_critical,
    COUNT(CASE WHEN impact = 'serious' THEN 1 END) AS count_serious,
    COUNT(CASE WHEN impact = 'moderate' THEN 1 END) AS count_moderate,
    COUNT(CASE WHEN impact = 'minor' THEN 1 END) AS count_minor
FROM axe_tests_recent atr
WHERE rule_type = 'violations'
AND `domain` ILIKE '%s'
GROUP BY `domain`
ORDER BY count_critical DESC;