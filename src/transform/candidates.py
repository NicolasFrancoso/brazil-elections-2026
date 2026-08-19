import pandas as pd
import numpy as np

from config import RAW_DIR
from src.utils.logger import get_logger


logger = get_logger(__name__)

DATE_COLUMNS = [
    "DT_GERACAO",
    "DT_ELEICAO",
    "DT_NASCIMENTO",
]


TEXT_NULL_VALUES = [
    "#NULO",
    "#NE",
    "NÃO DIVULGÁVEL",
]

DROP_COLUMNS = [
    "NR_CPF_CANDIDATO",
    "DS_EMAIL",
    "NR_TITULO_ELEITORAL_CANDIDATO",
    "CD_SITUACAO_CANDIDATURA",
    "DS_SITUACAO_CANDIDATURA",
]



def load_candidates_raw(
        snapshot_dir,
    ) -> pd.DataFrame:
    file_path = (
        snapshot_dir
        / "extracted"
        / "consulta_cand_2026_BRASIL.csv"
    )

    logger.info(
        "Loading raw candidates dataset: %s",
        file_path,
    )

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



def _create_business_flags(
    df: pd.DataFrame
) -> pd.DataFrame:

    df["TEM_NOME_SOCIAL"] = (
        df["NM_SOCIAL_CANDIDATO"] != "#NULO"
    )

    df["TEM_FEDERACAO"] = (
        df["NM_FEDERACAO"] != "#NULO"
    )

    return df

def _replace_special_text_values(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.replace(
        TEXT_NULL_VALUES,
        pd.NA,
    )

    return df

def _convert_dates(
    df: pd.DataFrame
) -> pd.DataFrame:

    for column in DATE_COLUMNS:

        df[column] = pd.to_datetime(
            df[column],
            format="%d/%m/%Y",
            errors="coerce",
        )

    return df

def _create_candidate_name(
    df: pd.DataFrame
) -> pd.DataFrame:

    df["NOME_CANDIDATO"] = (
        df["NM_SOCIAL_CANDIDATO"]
        .fillna(df["NM_CANDIDATO"])
    )

    return df

def _create_snapshot_datetime(
    df: pd.DataFrame
) -> pd.DataFrame:

    df["SNAPSHOT_DATETIME"] = pd.to_datetime(
        (
            df["DT_GERACAO"].dt.strftime("%Y-%m-%d")
            + " "
            + df["HH_GERACAO"]
        ),
        errors="coerce",
    )

    return df

def _create_age_at_election(
    df: pd.DataFrame
) -> pd.DataFrame:

    election_date = df["DT_ELEICAO"]
    birth_date = df["DT_NASCIMENTO"]

    age = (
        election_date.dt.year
        - birth_date.dt.year
    )

    has_not_had_birthday = (
        (election_date.dt.month < birth_date.dt.month)
        |
        (
            (election_date.dt.month == birth_date.dt.month)
            &
            (election_date.dt.day < birth_date.dt.day)
        )
    )

    df["IDADE_NA_ELEICAO"] = (
        age - has_not_had_birthday.astype("Int64")
    )

    return df

def _create_derived_columns(
    df:pd.DataFrame
) -> pd.DataFrame:

    df = _create_candidate_name(df)
    df = _create_snapshot_datetime(df)
    df = _create_age_at_election(df)

    return df

def _drop_non_analytical_columns(
    df: pd.DataFrame
) -> pd.DataFrame:

    columns_to_drop = [
        column
        for column in DROP_COLUMNS
        if column in df.columns
    ]

    df = df.drop(
        columns=columns_to_drop
    )

    return df

def _create_age_group(
    df: pd.DataFrame
    ) -> pd.DataFrame:

    bins = [
        18,
        29,
        39,
        49,
        59,
        69,
        120,
    ]

    labels = [
        "18-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70+",
    ]

    df["FAIXA_ETARIA"] = pd.cut(
        df["IDADE_NA_ELEICAO"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    return df

def _create_key_age_group(
    df: pd.DataFrame
    ) -> pd.DataFrame:

    labels = [
        "18-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70+",
    ]

    age_group = df["FAIXA_ETARIA"]

    condlist = [
    age_group == labels[0],   # Condition 1
    age_group == labels[1],
    age_group == labels[2],
    age_group == labels[3],
    age_group == labels[4],
    age_group == labels[5]
]

    # Define corresponding outcomes
    choicelist = [
        1,
        2,
        3,
        4,
        5,
        6
    ]

    df["FAIXA_ETARIA_KEY"] = np.select(condlist, choicelist, default=6)

    return df

def transform_candidates(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Transforming candidates dataset")

    df = df.copy()

    df = _create_business_flags(df)
    df = _replace_special_text_values(df)
    df = _convert_dates(df)
    df = _create_derived_columns(df)
    df = _drop_non_analytical_columns(df)
    df = _create_age_group(df)
    df = _create_key_age_group(df)

    logger.info(
        "Candidates dataset transformed: %s rows, %s columns",
        df.shape[0],
        df.shape[1],
    )

    return df


