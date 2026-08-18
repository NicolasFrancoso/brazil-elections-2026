from pathlib import Path
import pandas as pd

from config import STAGING_DIR
from config import PROCESSED_DIR
from src.utils.logger import get_logger
from src.utils.database import get_connection

logger = get_logger(__name__)

def save_candidates_staging(
    df: pd.DataFrame
) -> Path:
    
    output_path = (
        STAGING_DIR
        / "stg_candidates.parquet"
    )
    
    logger.info(
        "Saving candidates staging dataset"
    )
    
    df.to_parquet(
        output_path,
        index=False,
    )
    
    logger.info(
        "Candidates staging dataset saved: %s",
        output_path,
    )
    
    return output_path

def load_candidates_duckdb(
    parquet_path: Path
) -> None:
    
    logger.info(
        "Loading candidates dataset into DuckDB"
    )
    
    connection = get_connection()
    
    try:
        connection.execute(
            """
            CREATE OR REPLACE TABLE stg_candidates AS
            SELECT * FROM read_parquet(?)
            """,
            [str(parquet_path)],
            )
        
        logger.info(
            "Candidates table loaded into DuckDB"
        )
        
    finally:
        connection.close()
        
    
def save_candidates_analytics(
    df: pd.DataFrame
    ):

    output_path = (
        PROCESSED_DIR
        / "analytics_candidates.parquet"
    )

    logger.info(
        "Saving candidates analytics dataset"
    )

    df.to_parquet(
        output_path,
        index=False,
    )

    logger.info(
        "Candidates analytics dataset saved: %s",
        output_path,
    )

    return output_path

def load_candidates_analytics_duckdb(
    parquet_path
    ) -> None:

    logger.info(
        "Loading candidates analytics dataset into DuckDB"
    )

    connection = get_connection()

    try:

        connection.execute(
            """
            CREATE OR REPLACE TABLE analytics_candidates AS
            SELECT *
            FROM read_parquet(?)
            """,
            [str(parquet_path)],
        )

        logger.info(
            "Candidates analytics table loaded into DuckDB"
        )

    finally:

        connection.close()

