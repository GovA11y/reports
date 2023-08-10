-- Relative Path: app/api/database/postgres/queries/domain/summary.sql
-- Selects the domain and subdomain of the search term along with how many urls each domain has
-- Get Domain Active Status
SELECT
    targets.domains.id AS "domain_id",
    targets.domains.domain,
    COUNT(targets.urls.url) AS "url_count",
    SUM(targets.urls.is_objective::int) AS "objective_urls",
    SUM(targets.urls.active_scan_axe::int) AS "active_scan_urls_axe",
    SUM(targets.urls.active_main::int) AS "active_urls",
    SUM(targets.urls.errored::int) AS "errored_urls",
    targets.domains.active as "is_domain_active",
    targets.domains.is_objective as "is_domain_objective"
FROM
    targets.domains
JOIN
    targets.urls
ON
    targets.domains.id = targets.urls.domain_id
WHERE
    targets.domains.domain LIKE '%s'
    AND targets.domains.is_valid = TRUE
GROUP BY
    targets.domains.id,
    targets.domains.domain
ORDER BY
    COUNT(targets.urls.url) DESC;