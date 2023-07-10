# File: api/domain/views.py

from flask import Blueprint, request, jsonify
from ..database.utils.execute_query import execute_sql_from_file
from ..database.postgres.connect import postgres_conn  # your PostgreSQL connection function

domain_bp = Blueprint('domain', __name__, url_prefix='/domain')

@domain_bp.route('/summary', methods=['GET'])
def domain_summary():
    # Get "domain" from URL query parameters
    domain = request.args.get('domain', 'gsa.gov')