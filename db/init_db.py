from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

def ensure_movies_database_exists():
    load_dotenv()
    default_conn_str = os.getenv("DB_CONNECTION")
    movies_db_name = "movies"

    try:
        engine = create_engine(default_conn_str, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname" : movies_db_name}
            )
            if not result.scalar():
                print(f"Database '{movies_db_name}' does not exist. Creating...")
                conn.execute(text(f"CREATE DATABASE {movies_db_name}"))
                print(f"Database {movies_db_name} created sucessfully.")
            else:
                print(f"Database '{movies_db_name}' already exists.")
    except OperationalError as e:
        print(f"[ERROR] Failed to connect or create database: {e}")