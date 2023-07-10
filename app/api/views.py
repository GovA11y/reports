# in app/api/views.py

from flask import Blueprint, request, jsonify
from .database.utils.execute_query import execute_sql_from_file
from .database.postgres.connect import postgres_conn  # Assuming this is your PostgreSQL connection function

api = Blueprint('api', __name__)

@api.route('/domain/summary', methods=['GET'])
def domain_summary():
    # Read "domain" from URL query parameters, give a default value if it's missing
    domain = request.args.get('domain', 'gsa.gov')

    # Set up your SQL file path
    sql_file = "api/database/postgres/queries/domain/summary.sql"

    # Assuming you have set up execute_sql_from_file to return a result set
    # and changed the SQL command to use variable via string formatting
    result = execute_sql_from_file(postgres_conn, sql_file, domain)

    # Convert the result into JSON and return as HTTP response
    return jsonify(result)