from sqlalchemy import create_engine

def get_pg_engine(conn_str: str):
    return create_engine(conn_str)