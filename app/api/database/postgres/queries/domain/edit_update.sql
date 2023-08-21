-- app/api/database/postgres/queries/domain/edit_update.sql
-- Updates existing domains
UPDATE targets.domains
SET active = :active,
    is_objective = :is_objective
WHERE "domain" = :domain
RETURNING "domain", id, active, is_objective;
