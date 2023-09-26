# app/api/domain/views.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn
from ..utils import format_output
from app.logging import logger

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
    domain = f"{raw_domain}"
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


# List active domains
@domain_bp.route('/list', methods=['GET'])
def domain_list():
    sql_file = "app/api/database/postgres/queries/domain/list_domains.sql"

    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content

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



@domain_bp.route('/list-update', methods=['GET'])
def domain_update_list():
    domain = request.args.get('domain', '%')
    sql_file = "app/api/database/postgres/queries/domain/list_edit_domains.sql"

    # Read sql file
    with open(sql_file) as file:
        sql_content = text(file.read())

    results = []
    try:
        with postgres_conn.begin() as connection:
            result_proxy = connection.execute(sql_content.params(domain=domain)) # use params method
            keys = result_proxy.keys()
            for row in result_proxy:
                results.append({key: value for key,value in zip(keys,row)})
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@domain_bp.route('/update', methods=['POST'])
def domain_update():
    data = request.get_json()
    sql_file = "app/api/database/postgres/queries/domain/edit_update.sql"

    domain = data.get('domain')
    active = data.get('active')
    is_objective = data.get('is_objective')

    if not domain or active is None or is_objective is None:
        return jsonify({"error": "Invalid input data"}), 400

    # Read sql file
    with open(sql_file) as file:
        sql_content = text(file.read())

    results = []
    try:
        with postgres_conn.begin() as connection:
            result_proxy = connection.execute(sql_content.params(domain=domain, active=active, is_objective=is_objective)) # use params method
            keys = result_proxy.keys()
            for row in result_proxy:
                results.append({key: value for key,value in zip(keys,row)})
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@domain_bp.route('/add', methods=['POST'])
def domain_add():
    data = request.get_json()
    sql_file = "app/api/database/postgres/queries/domain/edit_add.sql"

    domain = data.get('domain')
    if not domain:
        return jsonify({"error": "Invalid input data"}), 400

    # Read sql file
    with open(sql_file) as file:
        sql_content = text(file.read())

    results = []
    try:
        with postgres_conn.begin() as connection:
            result_proxy = connection.execute(sql_content.params(domain=domain)) # use params method
            keys = result_proxy.keys()
            for row in result_proxy:
                results.append({key: value for key,value in zip(keys,row)})
        output_format = request.args.get('format', 'json')
        return format_output(results, output_format, 'domain_summary')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
