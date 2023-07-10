# app/api/axe/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from app.api.database.clickhouse.connect import client as clickhouse_conn
from app.logging import logger

# Blueprint Configuration
axe_bp = Blueprint(
    'axe_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/axe'
)


@axe_bp.route('/summary', methods=['GET'])
def axe_summary():
    raw_domain = request.args.get('domain', 'gsa.gov')
    domain = f"%{raw_domain}"
    sql_file = "app/api/database/clickhouse/queries/axe/domain_summary.sql"
    logger.info(f'Request: Axe Domain Summary\nDomain: {raw_domain}')

    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content % domain

    results = []
    try:
        # Run the query using ClickHouse's execute method
        rows = clickhouse_conn.execute(formatted_sql_content, with_column_types=True)
        keys = [col[0] for col in rows[1]]
        for row in rows[0]:
            results.append({key: value for key,value in zip(keys, row)})
        return jsonify(results), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@axe_bp.route('/results_raw', methods=['GET'])
def axe_results_raw():
    raw_domain = request.args.get('domain', 'gsa.gov')
    domain = f"%{raw_domain}"
    limit = request.args.get('limit')
    if limit is not None:
        limit = int(limit)
    else:
        limit = 5000
    sql_file = "app/api/database/clickhouse/queries/axe/current_violations.sql"
    rule_type = request.args.get('rule_type', 'violations')
    logger.info(f'Request: Axe Raw Results\nDomain: {raw_domain}\nRule Type: {rule_type}\nLimit: {limit}')

    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content % (domain, rule_type, limit)

    results = []
    try:
        # Run the query using ClickHouse's execute method
        rows = clickhouse_conn.execute(formatted_sql_content, with_column_types=True)
        keys = [col[0] for col in rows[1]]
        for row in rows[0]:
            row_dict = {}
            for key, value in zip(keys, row):
                if isinstance(value, bytes):
                    try:
                        value = value.decode('latin1')
                    except Exception as e:
                        logger.error(f"Error decoding column '{key}': {str(e)}")
                row_dict[key] = value
            results.append(row_dict)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


