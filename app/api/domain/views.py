# app/api/domain/views.py

from flask import Blueprint, jsonify, request
from app.api.database.postgres.connect import postgres_conn  # your PostgreSQL connection function
from app.api.database.utils.execute_query import execute_sql_from_file

# Blueprint Configuration
domain_bp = Blueprint(
    'domain_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/domain'
)

@domain_bp.route('/summary', methods=['GET'])
def domain_summary():
    domain = request.args.get('domain', 'gsa.gov')
    sql_file = "api/database/postgres/queries/domain/summary.sql"

    # Get data from database
    result = execute_sql_from_file(postgres_conn, sql_file, domain)

    return jsonify(result), 200