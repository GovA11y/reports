-- Relative Path: app/api/database/postgres/queries/domain/summary.sql
-- Selects the domain and subdomain of the search term along with how many urls each domain has
SELECT
    targets.domains.id AS "domain_id",
    targets.domains.domain,
    COUNT(targets.urls.url) AS "url_count"
FROM
    targets.domains
JOIN
    targets.urls
ON
    targets.domains.id = targets.urls.domain_id
WHERE
    targets.domains.domain ILIKE '%s'
    AND targets.domains.is_valid = TRUE
GROUP BY
    targets.domains.id,
    targets.domains.domain
ORDER BY
    COUNT(targets.urls.url) DESC;