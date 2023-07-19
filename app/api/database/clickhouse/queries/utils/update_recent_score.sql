-- app/api/database/clickhouse/queries/utils/update_recent_score.sql
-- SQL to update the Axe Recent Score Table
INSERT INTO axe_tests_recent_score (domain, url, axe_id, rule_type, impact, count_tests, updated_at)
SELECT
    domain,
    url,
    axe_id,
    rule_type,
    impact,
    COUNT() AS count_tests,
    now() AS updated_at
FROM gova11y.axe_tests_recent
WHERE created_at > (SELECT MAX(updated_at) FROM axe_tests_recent_score)
GROUP BY
    domain,
    url,
    axe_id,
    rule_type,
    impact;