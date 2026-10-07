import duckdb
from config import DB_PATH

def get_db_connection():
    """DuckDB columnar veri tabani baglantisi dondurur."""
    return duckdb.connect(DB_PATH)

def execute_query(query: str, params: list = None):
    """Guvenli sorgu calistirici."""
    con = get_db_connection()
    try:
        if params:
            return con.execute(query, params).fetchall()
        return con.execute(query).fetchall()
    finally:
        con.close()
