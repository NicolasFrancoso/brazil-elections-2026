import pandas as pd

from src.utils.database import get_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

def validate_candidates_pipeline(
    df: pd.DataFrame,
    parquet_path,
) -> None:
    logger.info(
        "Validating candidates pipeline consistency"
    )
    
    df_count = len(df)
    
    parquet_count = len(
        pd.read_parquet(parquet_path)
    )
    
    connection = get_connection()
    
    try:
        duckdb_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM stg_candidates
            """ 
        ).fetchone()[0]
        
    finally:
        connection.close()
        
    logger.info(
        "Row counts | DataFrame: %s | Parquet: %s | DuckDB: %s",
        df_count,
        parquet_count,
        duckdb_count,
    )

    if not (
        df_count
        == parquet_count
        == duckdb_count
    ):
        raise ValueError(
            "Row count mismatch between "
            "DataFrame, Parquet and DuckDB. "
            f"DataFrame={df_count}, "
            f"Parquet={parquet_count}, "
            f"DuckDB={duckdb_count}"
        )

    logger.info(
        "Candidates pipeline consistency validated successfully"
    )