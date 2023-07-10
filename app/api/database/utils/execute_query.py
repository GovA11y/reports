# execute_query.py
# Relative Path: app/api/database/utils/execute_query.py
from sqlalchemy import text


def row2dict(row):
    return {column: str(value) for column, value in zip(row.keys(), row)}

def execute_sql_from_file(conn, filename, domain):
    with open(filename, 'r') as fd:
        sql_file = fd.read()

    formatted_sql_file = sql_file % domain

    result_proxy = conn.execute(text(formatted_sql_file))

    result = [dict(row) for row in result_proxy.fetchall()]

    return result