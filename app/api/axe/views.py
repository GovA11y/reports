# app/api/axe/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from app.api.database.clickhouse.connect import client as clickhouse_conn
from app.logging import logger
from ..utils import format_output

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
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@axe_bp.route('/results_raw', methods=['GET'])
def axe_results_raw():
    raw_domain = request.args.get('domain', 'gsa.gov')
    domain = f"{raw_domain}"
    limit = request.args.get('limit')
    if limit is not None:
        limit = int(limit)
    else:
        limit = 5000

    # Time Filter
    tested_from = request.args.get('tested_from')
    tested_to = request.args.get('tested_to')

    # Decide which SQL file to use
    if tested_from and tested_to:
        sql_file = "app/api/database/clickhouse/queries/axe/current_violations_time.sql"
    else:
        sql_file = "app/api/database/clickhouse/queries/axe/current_violations.sql"

    rule_types = request.args.get('rule_type', 'inapplicable,passes,violations,incomplete')
    rule_types = ', '.join([f"'{rt}'" for rt in rule_types.split(',')])
    logger.info(f'Request: Axe Raw Results\nDomain: {raw_domain}\nRule Types: {rule_types}\nLimit: {limit}')

    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()

    # Format sql content based on parameters
    if tested_from and tested_to:
        formatted_sql_content = sql_content % (domain, rule_types, tested_from, tested_to, limit)
    else:
        formatted_sql_content = sql_content % (domain, rule_types, limit)

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
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


