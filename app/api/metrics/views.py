# app/api/metrics/views.py
from flask import Blueprint, jsonify, request
from app.logging import logger
from ..utils import format_output
from .a11yscore import calculate_score


# Blueprint Configuration
metrics_bp = Blueprint(
    'metrics_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/metrics'
)


@metrics_bp.route('/a11yscore', methods=['GET'])
def return_a11yscore():
    raw_domain = request.args.get('domain', 'nasa.gov')
    domain = f"{raw_domain}"
    logger.info(f'Request: A11y Score Requested for\nDomain: {raw_domain}')

    # Get the score information
    score_info = calculate_score(domain)

    # Check if the user specified the output format
    output_format = request.args.get('format', 'json')

    if output_format == 'json':
        return jsonify(score_info)
    else:
        # Convert the score_info JSON to an index-based format
        formatted_score_info = {}
        for key, value in score_info.items():
            formatted_score_info[key] = [value]

        return format_output(formatted_score_info, output_format, 'a11yscore_data')



