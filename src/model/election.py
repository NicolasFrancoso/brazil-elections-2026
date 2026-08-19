import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_dim_election(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Building dim_election")

    columns = [
        "CD_ELEICAO",
        "ANO_ELEICAO",
        "NR_TURNO",
        "DS_ELEICAO",
        "DT_ELEICAO",
    ]

    dim_election = (
        df[columns]
        .drop_duplicates()
        .sort_values("CD_ELEICAO")
        .reset_index(drop=True)
    )

    logger.info(
        "dim_election built: %s rows",
        len(dim_election),
    )

    return dim_election
