-- File Path: app/api/database/clickhouse/queries/metrics/a11yscore_by_axe_id.sql
   WITH
    -- Count of URLs analyzed
    url_count AS (
        SELECT axe_id, COUNT(DISTINCT url) as Ut
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        GROUP BY axe_id
    ),
    -- Count of total passes
    pass_count AS (
        SELECT axe_id, SUM(count_tests) as Pt
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'passes'
        GROUP BY axe_id
    ),
    -- Count of total violations
    total_violation_count AS (
        SELECT axe_id, SUM(count_tests) as Vt
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'violations'
        GROUP BY axe_id
    ),
    -- Count of critical violations
    critical_violation_count AS (
        SELECT axe_id, SUM(count_tests) as Vc
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'violations'
        AND impact = 'critical'
        GROUP BY axe_id
    ),
    -- Count of serious violations
    serious_violation_count AS (
        SELECT axe_id, SUM(count_tests) as Vs
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'violations'
        AND impact = 'serious'
        GROUP BY axe_id
    ),
    -- Count of moderate violations
    moderate_violation_count AS (
        SELECT axe_id, SUM(count_tests) as Vmo
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'violations'
        AND impact = 'moderate'
        GROUP BY axe_id
    ),
    -- Count of minor violations
    minor_violation_count AS (
        SELECT axe_id, SUM(count_tests) as Vmi
        FROM axe_tests_recent_score
        WHERE domain = '%s'
        AND rule_type = 'violations'
        AND impact = 'minor'
        GROUP BY axe_id
    )
SELECT
    pc.axe_id,
    COALESCE(uc.Ut, 0) as Ut,
    COALESCE(pc.Pt, 0) as Pt,
    COALESCE(tvc.Vt, 0) as Vt,
    COALESCE(cvc.Vc, 0) as Vc,
    COALESCE(svc.Vs, 0) as Vs,
    COALESCE(mvc.Vmo, 0) as Vmo,
    COALESCE(mic.Vmi, 0) as Vmi
FROM pass_count as pc
LEFT JOIN url_count as uc ON pc.axe_id = uc.axe_id
LEFT JOIN total_violation_count as tvc ON pc.axe_id = tvc.axe_id
LEFT JOIN critical_violation_count as cvc ON pc.axe_id = cvc.axe_id
LEFT JOIN serious_violation_count as svc ON pc.axe_id = svc.axe_id
LEFT JOIN moderate_violation_count as mvc ON pc.axe_id = mvc.axe_id
LEFT JOIN minor_violation_count as mic ON pc.axe_id = mic.axe_id;