import duckdb

from config import DATABASE_PATH
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_connection():
    
    logger.info(
        "Connecting to DuckDB: %s",
        DATABASE_PATH,
    )
    
    connection = duckdb.connect(
        str(DATABASE_PATH)
    )
    
    return connection