# app/api/metrics/a11yscore/calculate.py
from app.logging import logger

"""
Final calculation
"""

def resolve_score(score_data):
    logger.debug('Calculating Scores...')

    ASV = calc_a11yscore(score_data)
    logger.debug(f'A11yScore: {ASV["a11yscore"]}')

    impacts = ['ASVc', 'ASVs', 'ASVmo', 'ASVmi']
    a11yscores = {
        'ASV': ASV['a11yscore']
    }

    # Calculate A11yScores for each Impact
    for impact in impacts:
        score = impact_a11yscores(impact, score_data)
        logger.debug(f'{impact}: {score}')
        a11yscores[impact] = score

    return a11yscores


def calc_a11yscore(score_data):
    # Total weighted violations
    WVtotal = score_data['WVc'] + score_data['WVs'] + score_data['WVmo'] + score_data['WVmi']
    a11yscore = (WVtotal) / (score_data['NVt'] + score_data['NPt'])
    response = {'WVtotal':WVtotal,'a11yscore':a11yscore}
    return response


def impact_a11yscores(impact,score_data):
    # Replace the 'AS' prefix with 'WV' to get the corresponding score_data key
    score_key = impact.replace('ASV', 'WV')

    if score_key in score_data:
        score = score_data[score_key] / (score_data['NVt'] + score_data['NPt'])
        return score

    return None
