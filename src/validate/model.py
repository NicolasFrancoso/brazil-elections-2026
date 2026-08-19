import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def validate_dimensions(
    dim_party: pd.DataFrame,
    dim_office: pd.DataFrame,
    dim_election: pd.DataFrame,
    dim_location: pd.DataFrame,
    dim_candidacy: pd.DataFrame,
) -> None:

    logger.info("Validating dimensional model")

    _validate_primary_key(
        dim_party,
        key_columns=["NR_PARTIDO"],
        dimension_name="dim_party",
    )

    _validate_primary_key(
        dim_office,
        key_columns=["CD_CARGO"],
        dimension_name="dim_office",
    )

    _validate_primary_key(
        dim_election,
        key_columns=["CD_ELEICAO"],
        dimension_name="dim_election",
    )

    _validate_primary_key(
        dim_location,
        key_columns=["LOCATION_KEY"],
        dimension_name="dim_location",
    )

    _validate_primary_key(
        dim_candidacy,
        key_columns=["CANDIDACY_KEY"],
        dimension_name="dim_candidacy",
    )

    _validate_referential_integrity(
        dim_candidacy,
        dim_party,
        child_column="NR_PARTIDO",
        parent_column="NR_PARTIDO",
        relationship_name="candidacy -> party",
    )

    _validate_referential_integrity(
        dim_candidacy,
        dim_office,
        child_column="CD_CARGO",
        parent_column="CD_CARGO",
        relationship_name="candidacy -> office",
    )

    _validate_referential_integrity(
        dim_candidacy,
        dim_election,
        child_column="CD_ELEICAO",
        parent_column="CD_ELEICAO",
        relationship_name="candidacy -> election",
    )

    _validate_referential_integrity(
        dim_candidacy,
        dim_location,
        child_column="LOCATION_KEY",
        parent_column="LOCATION_KEY",
        relationship_name="candidacy -> location",
    )

    logger.info(
        "Dimensional model validated successfully"
    )

def _validate_primary_key(
    df: pd.DataFrame,
    key_columns: list[str],
    dimension_name: str,
) -> None:

    if df[key_columns].isna().any().any():
        raise ValueError(
            f"{dimension_name} contains null values "
            f"in primary key: {key_columns}"
        )

    duplicated_keys = df.duplicated(
        subset=key_columns
    ).sum()

    if duplicated_keys > 0:
        raise ValueError(
            f"{dimension_name} contains "
            f"{duplicated_keys} duplicated primary keys"
        )

    logger.info(
        "%s primary key validated",
        dimension_name,
    )

def _validate_referential_integrity(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_column: str,
    parent_column: str,
    relationship_name: str,
) -> None:

    child_values = set(
        child_df[child_column]
        .dropna()
        .unique()
    )

    parent_values = set(
        parent_df[parent_column]
        .dropna()
        .unique()
    )

    missing_values = (
        child_values - parent_values
    )

    if missing_values:
        raise ValueError(
            f"Referential integrity failed for "
            f"{relationship_name}. "
            f"Missing values: {missing_values}"
        )

    logger.info(
        "Referential integrity validated: %s",
        relationship_name,
    )
