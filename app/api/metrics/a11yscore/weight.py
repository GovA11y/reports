# app/api/metrics/a11yscore/weight.py
from app.logging import logger
from .get_data import get_violation_weights

"""
To generate and calculate the weights
"""

# Weight Normalized Violations
def weight_normalized_violations(normalized_violations):
    logger.info('Weighting Normalized Violations')
    # Define Variables
    NVt = normalized_violations['NVt']
    NVc = normalized_violations['NVc']
    NVs = normalized_violations['NVs']
    NVmo = normalized_violations['NVmo']
    NVmi = normalized_violations['NVmi']
    # Get Violations Weights
    severity_weights = get_violation_weights()
    if 'error' in severity_weights:
        logger.error(f"Error while getting weights: {severity_weights['error']}")
        return {"error": severity_weights['error']}, 500
    # Weighted Violations by Severity
    # Critical, Serious, Moderate, Minor
    # Generate Weights
    weighted_violations = {
        "WVc": NVc * severity_weights.get('Sc', 1.0),
        "WVs": NVs * severity_weights.get('Ss', 1.0),
        "WVmo": NVmo * severity_weights.get('Smo', 1.0),
        "WVmi": NVmi * severity_weights.get('Smi', 1.0)
    }
    logger.debug(f'Weighted Violations:\n{weighted_violations}')
    weighted_violations_response = {**weighted_violations, **severity_weights}
    return weighted_violations_response


