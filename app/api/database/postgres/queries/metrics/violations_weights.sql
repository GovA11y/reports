-- app/api/database/postgres/queries/metrics/violations_weights.sql
--  Postgresql Queries
SELECT variable, weight
FROM refs.weights
WHERE variable IN (
    'Sc',
    'Ss',
    'Smo',
    'Smi'
    );
