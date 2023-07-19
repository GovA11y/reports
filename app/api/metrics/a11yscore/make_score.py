# app/api/metrics/a11yscore/make_score.py
from app.logging import logger
from .normalize import normalize
from .weight import weight_normalized_violations
from .calculate import resolve_score
from .get_data import get_from_clickhouse


def generate_a11yscore(domain):
    # Get A11yScore Values from ClickHouse
    raw_result = get_from_clickhouse(domain)
    # if got good values, then continue, else error message
    if raw_result:
        logger.info(f"Raw Metrics{raw_result}")

        # Now we normalize
        normalized_result = normalize(raw_result)

        # Apply weights..
        weighted_violations = weight_normalized_violations(normalized_result)

        # Calculate Score
        # Prepare
        # Prepare parameters for score calculation
        score_data = {**raw_result,
            **weighted_violations,
            **normalized_result,
            'domain': domain
            }
        a11yscores = resolve_score(score_data)

        # Add a11yscore
        # score_data['a11yscore'] = a11yscore
        a11yscore_data = {**score_data, **raw_result, **normalized_result, **weighted_violations, **a11yscores}
        return a11yscore_data
    else:
        logger.error("Error in getting values from ClickHouse")



