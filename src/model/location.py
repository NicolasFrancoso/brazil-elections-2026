import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_dim_location(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Building dim_location")

    dim_location = (
        df[
            [
                "TP_ABRANGENCIA",
                "SG_UF",
                "SG_UE",
                "NM_UE",
            ]
        ]
        .drop_duplicates()
        .copy()
    )

    dim_location["LOCATION_KEY"] = (
        dim_location["TP_ABRANGENCIA"].astype(str)
        + "|"
        + dim_location["SG_UE"].astype(str)
    )

    dim_location = (
        dim_location[
            [
                "LOCATION_KEY",
                "TP_ABRANGENCIA",
                "SG_UF",
                "SG_UE",
                "NM_UE",
            ]
        ]
        .sort_values("LOCATION_KEY")
        .reset_index(drop=True)
    )

    logger.info(
        "dim_location built: %s rows",
        len(dim_location),
    )

    return dim_location
