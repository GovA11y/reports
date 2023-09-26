-- Test Coverage by Domain
-- app/api/database/postgres/queries/axe/coverage.sql

SELECT
    d.domain,
    COUNT(u.id) AS total_urls,
    COUNT(CASE WHEN u.active_scan_axe THEN 1 END) AS active_axe_urls,
    COUNT(CASE WHEN u.is_objective THEN 1 END) AS is_objective_urls,
    COUNT(CASE WHEN u.errored THEN 1 END) AS errored_urls,
    COUNT(DISTINCT sd.url_id) AS axe_tested_count,
    ROUND(
        100.0 * COUNT(CASE WHEN u.active_scan_axe THEN 1 END) / NULLIF(COUNT(u.id), 0),
        2
    ) AS domain_coverage_axe
FROM targets.domains d
LEFT JOIN targets.urls u ON d.id = u.domain_id
LEFT JOIN axe.scan_data sd ON u.id = sd.url_id
WHERE d."domain" LIKE '%s'
GROUP BY d.domain
ORDER BY d.domain;



