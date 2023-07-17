# app/api/metrics/a11yscore/get_data.py
from app.logging import logger
from app.api.database.clickhouse.connect import client as clickhouse_conn
from sqlalchemy import text
from app.api.database.postgres.connect import postgres_conn


def get_violation_weights():
    # Set the SQL File
    sql_file = "app/api/database/postgres/queries/metrics/violations_weights.sql"
    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content

    weights = {}
    try:
        # Established database connection from connect.py
        with postgres_conn.begin() as connection:
            result_proxy = connection.execute(text(formatted_sql_content))
            keys = result_proxy.keys()  # Get the column names
            for row in result_proxy:
                row_as_dict = dict(zip(keys, row))  # Convert row to dictionary
                weights[row_as_dict['variable']] = row_as_dict['weight']
        logger.debug(f'Weights: {weights}')
        return weights
    except Exception as e:
        logger.error(f"Error while getting violation weights: {str(e)}")
        return {"error": str(e)}



