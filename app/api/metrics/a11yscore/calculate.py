# app/api/metrics/a11yscore/calculate.py
from app.logging import logger

"""

"""

def resolve_score(score_data):
    logger.debug('Calculating Score...')

    # Total weighted violations
    total_weighted_violations = score_data['WVc'] + score_data['WVs'] + score_data['WVmo'] + score_data['WVmi']

    # Total passes
    Pt = score_data['NPt']

    # Total URLs, which is 1 because you are normalizing per URL
    Ut = score_data['NUt']

    logger.info(f"\nA11yScore Calculation Variables:\n\
                  Weighted Violations Critical (WVc): {score_data['WVc']}\n\
                  Weighted Violations Serious (WVs): {score_data['WVs']}\n\
                  Weighted Violations Moderate (WVmo): {score_data['WVmo']}\n\
                  Weighted Violations Minor (WVmi): {score_data['WVmi']}\n\
                  Total Weighted Violations: {total_weighted_violations}\n\
                  Total Passes (Pt): {Pt}\n\
                  Total URLs (Ut): {Ut}" )

    # Calculate A11yScore
    a11yscore = (total_weighted_violations - Pt) / Ut

    logger.info(f"A11yScore: {a11yscore}")  # Log the generated score

    return a11yscore