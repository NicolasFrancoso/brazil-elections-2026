import pandas as pd

from src.utils.database import get_connection
from src.utils.logger import get_logger


logger = get_logger(__name__)


KEY_COLUMNS = [
    "CD_ELEICAO",
    "SQ_CANDIDATO",
]


def _get_candidate_keys(
    df: pd.DataFrame
) -> set:

    return set(
        zip(
            df["CD_ELEICAO"],
            df["SQ_CANDIDATO"],
        )
    )


def validate_candidates_pipeline(
    df: pd.DataFrame,
    parquet_path,
) -> None:

    logger.info(
        "Validating candidates pipeline consistency"
    )

    # -------------------------
    # DataFrame
    # -------------------------

    df_count = len(df)

    df_keys = _get_candidate_keys(
        df
    )

    # -------------------------
    # Parquet
    # -------------------------

    parquet_df = pd.read_parquet(
        parquet_path
    )

    parquet_count = len(
        parquet_df
    )

    parquet_keys = _get_candidate_keys(
        parquet_df
    )

    # -------------------------
    # DuckDB
    # -------------------------

    connection = get_connection()

    try:

        duckdb_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM stg_candidates
            """
        ).fetchone()[0]

        duckdb_keys_df = connection.execute(
            """
            SELECT
                CD_ELEICAO,
                SQ_CANDIDATO
            FROM stg_candidates
            """
        ).fetchdf()

    finally:

        connection.close()

    duckdb_keys = _get_candidate_keys(
        duckdb_keys_df
    )

    # -------------------------
    # Row count validation
    # -------------------------

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
            "DataFrame, Parquet and DuckDB"
        )

    # -------------------------
    # Key validation
    # -------------------------

    if df_keys != parquet_keys:
        raise ValueError(
            "Candidate keys differ between "
            "DataFrame and Parquet"
        )

    if df_keys != duckdb_keys:
        raise ValueError(
            "Candidate keys differ between "
            "DataFrame and DuckDB"
        )

    logger.info(
        "Candidates pipeline consistency validated successfully"
    )