-- File Path: app/api/database/clickhouse/queries/axe/activity_import_axe_rules.sql
-- Captures How Many Axe Tests were recently imported
SELECT
    `domain`,
    count(*) AS imported_total,
    countIf(created_at BETWEEN '%s' AND '%s') AS imported_range,
    countIf(created_at >= now() - INTERVAL 15 MINUTE) AS imported_minute_15,
    countIf(created_at >= now() - INTERVAL 1 HOUR) AS imported_hour_1,
    countIf(created_at >= now() - INTERVAL 12 HOUR) AS imported_hour_12,
    countIf(created_at >= now() - INTERVAL 1 WEEK) AS imported_week,
    countIf(created_at >= now() - INTERVAL 1 MONTH) AS imported_month
FROM
    axe_tests
WHERE
    `domain` ILIKE '%s'
GROUP BY
    `domain`
ORDER BY
    imported_total DESC;