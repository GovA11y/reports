## app/api/metrics/a11yscore/normalize.py
from app.logging import logger


def normalize(data):
    logger.debug(f'Normalizing Data...')
    total_urls = data['Ut']
    normalized_data = {
        'NVc': data['Vc'] / total_urls if total_urls != 0 else 0,
        'NVs': data['Vs'] / total_urls if total_urls != 0 else 0,
        'NVmo': data['Vmo'] / total_urls if total_urls != 0 else 0,
        'NVmi': data['Vmi'] / total_urls if total_urls != 0 else 0,
        'NUt': 1,  # because we are normalizing per URL
        'NPt': data['Pt'] / total_urls if total_urls != 0 else 0,
        'NVt': data['Vt'] / total_urls if total_urls != 0 else 0,
    }
    logger.debug(f'Normalized...')
    return normalized_data


