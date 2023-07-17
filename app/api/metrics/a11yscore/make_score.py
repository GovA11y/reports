# app/api/metrics/a11yscore/make_score.py
from app.logging import logger
from .normalize import normalize
from app.api.database.clickhouse.connect import client as clickhouse_conn
from .weight import weight_normalized_violations
from .calculate import resolve_score


# app/api/metrics/a11yscore/make_score.py
def generate_a11yscore(domain):
    # Get A11yScore Values from ClickHouse
    result = get_from_clickhouse(domain)
    # if got good values, then continue, else error message
    if result:
        logger.info("Values to Normalize:")
        for key, value in result.items():
            logger.info(f"{key}: {value}")

        # Now we normalize
        normalized_result = normalize(result)

        # Now we log both original and normalized result variables here
        logger.info("Original Values and Normalized Values:")
        for key in result.keys():
            normalized_key = 'N' + key  # because in normalize, you prefix all keys with 'N'
            if normalized_key in normalized_result:
                logger.info(f"{key}: {result[key]} -> {normalized_result[normalized_key]}")
            else:
                logger.info(f"{key}: {result[key]} -> Key {normalized_key} not found in normalized results")

        # Apply weights..
        weighted_violations = weight_normalized_violations(normalized_result)

        # Calculate Score


        # Below is just so I can test things... not real...
        a11yscore = 42
        logger.warning(f'BS Placeholder for A11yScore: {a11yscore}')
        return a11yscore
    else:
        logger.error("Error in getting values from ClickHouse")



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

