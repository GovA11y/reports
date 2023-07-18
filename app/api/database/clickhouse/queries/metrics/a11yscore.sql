-- app/api/database/clickhouse/queries/metrics/a11yscore.sql
-- A11yScore General
SELECT
    COUNT(DISTINCT url) AS Ut,
    SUM(if(rule_type = 'passes', count_tests, 0)) AS Pt,
    SUM(if(rule_type = 'violations', count_tests, 0)) AS Vt,
    SUM(if(rule_type = 'violations' AND impact = 'critical', count_tests, 0)) AS Vc,
    SUM(if(rule_type = 'violations' AND impact = 'serious', count_tests, 0)) AS Vs,
    SUM(if(rule_type = 'violations' AND impact = 'moderate', count_tests, 0)) AS Vmo,
    SUM(if(rule_type = 'violations' AND impact = 'minor', count_tests, 0)) AS Vmi
FROM axe_tests_recent_score
WHERE domain LIKE '%s';