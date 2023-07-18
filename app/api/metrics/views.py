# app/api/metrics/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from app.api.database.clickhouse.connect import client as clickhouse_conn
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


@metrics_bp.route('/score/a11y', methods=['GET'])
def return_a11yscore():
    raw_domain = request.args.get('domain', 'nasa.gov')
    domain = f"{raw_domain}"
    logger.info(f'Request: A11y Score Requested for\nDomain: {raw_domain}')

    # get the score information
    score_info = calculate_score(domain)

    return jsonify(score_info)
