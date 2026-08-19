import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_dim_candidacy(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Building dim_candidacy")

    dim_candidacy = df.copy()

    dim_candidacy["CANDIDACY_KEY"] = (
        dim_candidacy["CD_ELEICAO"].astype(str)
        + "|"
        + dim_candidacy["SQ_CANDIDATO"].astype(str)
    )

    dim_candidacy["LOCATION_KEY"] = (
        dim_candidacy["TP_ABRANGENCIA"].astype(str)
        + "|"
        + dim_candidacy["SG_UE"].astype(str)
    )

    columns = [
        "CANDIDACY_KEY",

        "CD_ELEICAO",
        "SQ_CANDIDATO",

        "NR_PARTIDO",
        "CD_CARGO",
        "LOCATION_KEY",

        "NR_CANDIDATO",

        "NM_CANDIDATO",
        "NM_URNA_CANDIDATO",
        "NM_SOCIAL_CANDIDATO",
        "NOME_CANDIDATO",
        "TEM_NOME_SOCIAL",

        "TP_AGREMIACAO",

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
    ]

    dim_candidacy = (
        dim_candidacy[columns]
        .drop_duplicates(
            subset=["CANDIDACY_KEY"]
        )
        .reset_index(drop=True)
    )

    logger.info(
        "dim_candidacy built: %s rows",
        len(dim_candidacy),
    )

    return dim_candidacy
