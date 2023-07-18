


def get_from_clickhouse(domain):
    # Set the SQL File
    sql_file = "app/api/database/clickhouse/queries/metrics/a11yscore.sql"
    # Read sql file
    with open(sql_file) as file:
        sql_content = file.read()
    formatted_sql_content = sql_content % (domain)
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

        # If everything is good, we expect one row of result with the statistics.
        if len(results) == 1:
            return results[0]
        else:
            logger.error("Expected one row of results, got different.")
            return None

    except Exception as e:
        logger.error(str(e))
        return None