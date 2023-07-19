# app/api/utils/cleanup/axe_score.py
from app.logging import logger
from app.api.database.clickhouse.connect import client as clickhouse_conn


def update_axe_score_table():
    # Set the SQL File
    sql_file = "app/api/database/clickhouse/queries/utils/update_recent_score.sql"
    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content

    try:
        # Run the query using ClickHouse's execute method
        result = clickhouse_conn.execute(formatted_sql_content)
        num_updated_rows = len(result)  # Get the number of updated rows
        # logger.debug(f'Axe Score Table updated...')

    except Exception as e:
        logger.error(str(e))
        return None

