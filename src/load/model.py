from pathlib import Path

import pandas as pd

from config import PROCESSED_DIR
from src.utils.database import get_connection
from src.utils.logger import get_logger


logger = get_logger(__name__)


MODEL_DIR = PROCESSED_DIR / "model"


def save_dimension_parquet(
    df: pd.DataFrame,
    table_name: str,
) -> Path:

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        MODEL_DIR
        / f"{table_name}.parquet"
    )

    logger.info(
        "Saving %s to Parquet",
        table_name,
    )

    df.to_parquet(
        output_path,
        index=False,
    )

    logger.info(
        "%s saved: %s",
        table_name,
        output_path,
    )

    return output_path


def load_dimension_duckdb(
    parquet_path: Path,
    table_name: str,
) -> None:

    logger.info(
        "Loading %s into DuckDB",
        table_name,
    )

    connection = get_connection()

    try:
        connection.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_parquet(?)
            """,
            [str(parquet_path)],
        )

        logger.info(
            "%s loaded into DuckDB",
            table_name,
        )

    finally:
        connection.close()

def persist_dimensions(
    dimensions: dict[str, pd.DataFrame],
    ) -> dict[str, Path]:

    logger.info(
        "Persisting dimensional model"
    )

    paths = {}

    for table_name, df in dimensions.items():

        parquet_path = save_dimension_parquet(
            df,
            table_name,
        )

        load_dimension_duckdb(
            parquet_path,
            table_name,
        )

        paths[table_name] = parquet_path

    logger.info(
        "Dimensional model persisted successfully"
    )

    return paths

