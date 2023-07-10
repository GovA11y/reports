# connect.py
# Relative Path: app/database/postgres/connect.py
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
import os
from .. import logger

# load .env variables
load_dotenv()

# Retrieving environment variables
DB_USER = os.getenv("DB_POSTGRES_USER")
DB_PASSWORD = os.getenv("DB_POSTGRES_PASSWORD")
DB_NAME = os.getenv("DB_POSTGRES_NAME")
DB_HOST = os.getenv("DB_POSTGRES_HOST")
DB_PORT = os.getenv("DB_POSTGRES_PORT")

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/database"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instead of using declarative_base()
# Base = declarative_base()

# We use registry
mapper_registry = registry()
Base = mapper_registry.generate_base()

postgres_conn = SessionLocal


def test_connection():
    connection = None
    try:
        connection = engine.connect()
        logger.debug("Connected to 🐘")
    except Exception as e:
        logger.error(f"Unable to connect to PostgreSQL: {str(e)}")
    finally:
        # Ensure the connection object is not None before trying to close it
        if connection:
            connection.close()
            logger.debug("🐘 Connection closed")



test_connection()