from pathlib import Path

import pandas as pd

from src.utils.database import get_connection
from src.utils.logger import get_logger


logger = get_logger(__name__)


def validate_dimension_persistence(
    df: pd.DataFrame,
    parquet_path: Path,
    table_name: str,
) -> None:

    dataframe_count = len(df)

    parquet_count = len(
        pd.read_parquet(
            parquet_path,
        )
    )

    connection = get_connection()

    try:
        duckdb_count = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            """
        ).fetchone()[0]

    finally:
        connection.close()

    logger.info(
        "%s row counts | DataFrame: %s | Parquet: %s | DuckDB: %s",
        table_name,
        dataframe_count,
        parquet_count,
        duckdb_count,
    )

    if not (
        dataframe_count
        == parquet_count
        == duckdb_count
    ):
        raise ValueError(
            f"Persistence validation failed "
            f"for {table_name}"
        )

    logger.info(
        "%s persistence validated successfully",
        table_name,
    )
