-- app/api/database/postgres/queries/domain/list_edit_domains.sql
-- Select domains from search before editing
SELECT d."domain",
       COUNT(u.url) AS url_count,
       d.active,
       d.is_objective,
       d.is_valid,
       date_trunc('day', age(now(), d.created_at)) AS created_ago,
       date_trunc('day', age(now(), d.updated_at)) AS updated_ago
FROM targets.domains d
LEFT JOIN targets.urls u ON d.id = u.domain_id
WHERE d."domain" ILIKE '%s'
AND is_valid = TRUE
GROUP BY d."domain", d.active, d.is_objective, d.is_valid, d.created_at, d.updated_at;