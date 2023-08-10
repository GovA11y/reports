-- app/api/database/postgres/queries/domain/list_domains.sql
-- Lists is_objective domains
SELECT "domain"
FROM targets.domains d
WHERE is_objective = TRUE
ORDER BY "domain" ASC;