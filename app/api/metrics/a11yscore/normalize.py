## app/api/metrics/a11yscore/normalize.py
from app.logging import logger


def normalize(data):
    total_urls = data['Ut']
    total_violations = data['Vt']
    normalized_data = {
        'NVc': data['Vc'] / total_urls if total_urls != 0 else 0,
        'NVs': data['Vs'] / total_urls if total_urls != 0 else 0,
        'NVmo': data['Vmo'] / total_urls if total_urls != 0 else 0,
        'NVmi': data['Vmi'] / total_urls if total_urls != 0 else 0,
        'NUt': data['Ut'] / total_urls if total_urls != 0 else 0,
        'NPt': data['Pt'] / total_urls if total_urls != 0 else 0,
        'NVt': data['Vt'] / total_urls if total_urls != 0 else 0,
    }
    logger.debug(f'Normalized...\n{normalized_data}')
    return normalized_data


