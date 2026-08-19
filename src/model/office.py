import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_dim_office(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Building dim_office")

    dim_office = (
        df[
            [
                "CD_CARGO",
                "DS_CARGO",
            ]
        ]
        .drop_duplicates()
        .sort_values("CD_CARGO")
        .reset_index(drop=True)
    )

    logger.info(
        "dim_office built: %s rows",
        len(dim_office),
    )

    return dim_office
