# connect.py
# Relative Path: app/database/clickhouse/connect.py
"""
Creates connection to ClickHouse
"""
from clickhouse_driver import Client
from dotenv import load_dotenv
import os
from .. import logger

# Load .env variables
load_dotenv()

# Retrieve environment variables
DB_HOST = os.getenv("DB_CLICKHOUSE_HOST")
DB_PORT = os.getenv("DB_CLICKHOUSE_PORT")
DB_USER = os.getenv("DB_CLICKHOUSE_USER")
DB_PASSWORD = os.getenv("DB_CLICKHOUSE_PASSWORD")
DB_NAME = os.getenv("DB_CLICKHOUSE_NAME")

# Create ClickHouse client
client = Client(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)


def test_connection():
    try:
        result = client.execute('SELECT 1')
        if result[0][0] == 1:
            logger.debug("Connected to ClickHouse")
        else:
            logger.error("Unable to connect to ClickHouse, test query did not return expected result.")
    except Exception as e:
        logger.critical(f"Unable to connect to ClickHouse: {str(e)}")


test_connection()