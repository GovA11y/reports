from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

from insight.core import database


def test_environment_variables():
    assert database.DB_USER is not None
    assert database.DB_PASSWORD is not None
    assert database.DB_HOST is not None
    assert database.DB_PORT is not None
    assert database.DB_NAME is not None


def test_database_connection():
    try:
        with database.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except OperationalError:
        assert False