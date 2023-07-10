# app/api/domain/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from app.api.database.clickhouse.connect import client as clickhouse_conn

# Blueprint Configuration
domain_bp = Blueprint(
    'domain_bp', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/axe'
)


@domain_bp.route('/summary', methods=['GET'])
def domain_summary():
    raw_domain = request.args.get('domain', 'gsa.gov')
    domain = f"%{raw_domain}"
    sql_file = "app/api/database/clickhouse/queries/axe/domain_summary.sql"

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
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
