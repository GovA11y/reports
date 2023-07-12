# app/api/axe/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from app.api.database.clickhouse.connect import client as clickhouse_conn
from app.logging import logger
from ..utils import format_output
# from .view_makers import import_axe

# Blueprint Configuration
activity_bp = Blueprint(
    'activity_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/activity'
)


@activity_bp.route('/imports/axe_tests', methods=['GET'])
def make_import_axe_rules():
    raw_domain = request.args.get('domain', 'nasa.gov')
    domain = f"%{raw_domain}"
    imported_from = request.args.get('imported_from', '2022-01-01')
    imported_to = request.args.get('imported_to', '2024-12-31')

    sql_file = "app/api/database/clickhouse/queries/axe/activity_import_axe_rules.sql"

    # Log Request
    logger.info(f'Request: Activity Import Axe Rules\nDomain: {raw_domain}\nImported Range:{imported_from} - {imported_to}')

    # Read & format sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content % (imported_from, imported_to, domain)

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
        return format_output(results, output_format, 'axe_rule_import_activity')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
