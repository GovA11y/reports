# app/api/domain/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from ..utils import format_output


# Blueprint Configuration
domain_bp = Blueprint(
    'domain_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/domain'
)


@domain_bp.route('/summary', methods=['GET'])
def domain_summary():
    raw_domain = request.args.get('domain', 'nasa.gov')
    domain = f"%{raw_domain}"
    sql_file = "app/api/database/postgres/queries/domain/summary.sql"

    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content % domain

    results = []
    try:
        # Established database connection from connect.py
        with postgres_conn.begin() as connection:
            result_proxy = connection.execute(text(formatted_sql_content))
            keys = result_proxy.keys()
            for row in result_proxy:
                results.append({key: value for key,value in zip(keys,row)})
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
