
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Load database credentials from .env
load_dotenv()


def get_engine():

    # Read database configuration
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    # Check whether credentials are available
    if not all([host, port, database, username, password]):
        raise ValueError("Missing PostgreSQL configuration in .env")

    # Build a safe database connection URL
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database
    )

    # Create SQLAlchemy engine
    engine = create_engine(
        database_url,
        pool_pre_ping=True
    )

    return engine
