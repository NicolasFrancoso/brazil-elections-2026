import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_dim_party(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Building dim_party")

    dim_party = (
        df[
            [
                "NR_PARTIDO",
                "SG_PARTIDO",
                "NM_PARTIDO",
            ]
        ]
        .drop_duplicates()
        .sort_values("NR_PARTIDO")
        .reset_index(drop=True)
    )

    logger.info(
        "dim_party built: %s rows",
        len(dim_party),
    )

    return dim_party
