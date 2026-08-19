import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


ANALYTICS_COLUMNS = [
    "CD_ELEICAO",
    "SQ_CANDIDATO",
    "DS_ELEICAO",
    "ANO_ELEICAO",
    "NR_TURNO",
    "DT_ELEICAO",

    "SG_UF",
    "SG_UE",
    "NM_UE",

    "CD_CARGO",
    "DS_CARGO",

    "TP_ABRANGENCIA",

    "NR_CANDIDATO",
    "NM_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "NM_SOCIAL_CANDIDATO",
    "NOME_CANDIDATO",
    "TEM_NOME_SOCIAL",

    "TP_AGREMIACAO",

    "NR_PARTIDO",
    "SG_PARTIDO",
    "NM_PARTIDO",

    "NR_FEDERACAO",
    "NM_FEDERACAO",
    "SG_FEDERACAO",
    "DS_COMPOSICAO_FEDERACAO",
    "TEM_FEDERACAO",

    "SQ_COLIGACAO",
    "NM_COLIGACAO",
    "DS_COMPOSICAO_COLIGACAO",

    "SG_UF_NASCIMENTO",
    "IDADE_NA_ELEICAO",

    "CD_GENERO",
    "DS_GENERO",

    "CD_GRAU_INSTRUCAO",
    "DS_GRAU_INSTRUCAO",

    "CD_ESTADO_CIVIL",
    "DS_ESTADO_CIVIL",

    "CD_COR_RACA",
    "DS_COR_RACA",

    "CD_OCUPACAO",
    "DS_OCUPACAO",

    "CD_SIT_TOT_TURNO",
    "DS_SIT_TOT_TURNO",

    "SNAPSHOT_DATETIME",
]

def build_candidates_analytics(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info(
        "Building candidates analytics dataset"
    )

    analytics_df = (
        df[ANALYTICS_COLUMNS]
        .copy()
    )

    logger.info(
        "Candidates analytics dataset built: %s rows, %s columns",
        analytics_df.shape[0],
        analytics_df.shape[1],
    )

    return analytics_df
