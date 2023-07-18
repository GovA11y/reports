# app/api/metrics/a11yscore/make_score.py
from app.logging import logger
from .normalize import normalize
from .weight import weight_normalized_violations
from .calculate import resolve_score
from .get_data import get_from_clickhouse


# app/api/metrics/a11yscore/make_score.py
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
        score_data = {
            'WVc': weighted_violations['WVc'],
            'WVs': weighted_violations['WVs'],
            'WVmo': weighted_violations['WVmo'],
            'WVmi': weighted_violations['WVmi'],
            'NUt': normalized_result['NUt'],
            'NPt': normalized_result['NPt'],
            'Ut': raw_result['Ut']
        }
        a11yscore = resolve_score(score_data)

        # Below is just so I can test things... not real...
        return a11yscore
    else:
        logger.error("Error in getting values from ClickHouse")



