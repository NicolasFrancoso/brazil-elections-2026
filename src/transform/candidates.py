import pandas as pd

from config import RAW_DIR
from src.utils.logger import get_logger


logger = get_logger(__name__)


def load_candidates_raw() -> pd.DataFrame:
    file_path = (
        RAW_DIR
        / "candidates_2026"
        / "consulta_cand_2026_BRASIL.csv"
    )

    logger.info("Loading raw candidates dataset")

    df = pd.read_csv(
        file_path,
        sep=";",
        encoding="latin1",
        quotechar='"',
        low_memory=False,
        keep_default_na=False,
    )

    logger.info(
        "Candidates dataset loaded: %s rows, %s columns",
        df.shape[0],
        df.shape[1],
    )

    return df

DATE_COLUMNS = [
    "DT_GERACAO",
    "DT_ELEICAO",
    "DT_NASCIMENTO",
]

def transform_dates(
    df: pd.DataFrame
) -> pd.DataFrame:

    for column in DATE_COLUMNS:

        df[column] = pd.to_datetime(
            df[column],
            format="%d/%m/%Y",
            errors="coerce",
        )

    return df

def transform_candidates(df: pd.DataFrame) -> pd.DataFrame:
    
    logger.info("Transforming candidates dataset")
    
    df = df.copy()
    
    df = transform_dates(df)
    
    return df 


