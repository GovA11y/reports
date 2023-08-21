-- app/api/database/postgres/queries/domain/edit_add.sql
-- Add new domains
INSERT INTO targets.domains ("domain", active, is_objective)
VALUES (LOWER(:domain), TRUE, TRUE)
RETURNING "domain", id;
