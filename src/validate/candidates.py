import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "CD_ELEICAO",
    "SQ_CANDIDATO",
    "NOME_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "DS_CARGO",
    "SG_PARTIDO",
    "DS_GENERO",
    "IDADE_NA_ELEICAO",
]

def profile_candidates(df: pd.DataFrame) -> None:
    logger.info("Profiling candidates dataset")

    print("\n=== DATASET SHAPE ===")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    print("\n=== FIRST ROWS ===")
    print(df.head())

    print("\n=== COLUMNS ===")
    for column in df.columns:
        print(column)

    print("\n=== DATA TYPES ===")
    print(df.dtypes)

    print("\n=== DUPLICATED ROWS ===")
    print(df.duplicated().sum())

    print("\n=== SPECIAL TSE VALUES ===")

    special_values = [
        "#NULO",
        "#NE",
        "NÃO DIVULGÁVEL",
    ]

    for value in special_values:
        count = (
            df.astype(str)
            .eq(value)
            .sum()
            .sum()
        )

        print(f"{value}: {count:,}")

    print("\n=== CANDIDATE KEY CHECK ===")

    if {"CD_ELEICAO", "SQ_CANDIDATO"}.issubset(df.columns):
        duplicated_keys = df.duplicated(
            subset=["CD_ELEICAO", "SQ_CANDIDATO"]
        ).sum()

        print(
            "Duplicated CD_ELEICAO + SQ_CANDIDATO:",
            duplicated_keys,
        )

    print("\n=== CANDIDATE STATUS ===")

    for column in [
        "DS_SITUACAO_CANDIDATURA",
        "DS_SIT_TOT_TURNO",
    ]:
        if column in df.columns:
            print(f"\n{column}")
            print(
                df[column]
                .value_counts(dropna=False)
                .head(20)
            )
            
    print("\n=== SPECIAL VALUES BY COLUMN ===")

    special_values = [
        "#NULO",
        "#NE",
        "NÃO DIVULGÁVEL",
    ]

    for column in df.columns:

        counts = {}

        for value in special_values:
            count = (
                df[column]
                .astype(str)
                .eq(value)
                .sum()
            )

            if count > 0:
                counts[value] = count

        if counts:
            print(f"\n{column}")

            for value, count in counts.items():
                print(f"  {value}: {count:,}")
                
def validate_transformed_candidates(
    df: pd.DataFrame
) -> None:
    logger.info("Validating transformed candidates dataset")
    
    _validate_required_columns(df)
    _validate_candidate_key(df)
    _validade_candidate_name(df)
    _validate_age(df)
    _validate_social_name(df)
    _validation_federation(df)
    
    logger.info(
        "Transformed candidates dataset validated successfully"
    )
    
def _validate_required_columns(
    df: pd.DataFrame
) -> None:
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]
    
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )
    
def _validate_candidate_key(
    df: pd.DataFrame
) -> None:
    
    key_columns = [
        "CD_ELEICAO",
        "SQ_CANDIDATO"
    ]
    
    if df[key_columns].isna().any().any():
        raise ValueError(
            "Candidate key contains null values"
        )
        
    duplicated_keys = df.duplicated(
        subset=key_columns
    ).sum()
    
    if duplicated_keys > 0:
        raise ValueError(
            f"Caniddate key contains {duplicated_keys} duplicated records"
        )
        
def _validade_candidate_name(
    df: pd.DataFrame
) -> None:
    
    if df["NOME_CANDIDATO"].isna().any():
        raise ValueError(
            "NOME_CANDIDATO contains null values" 
        )
    
    
    
def _validate_age(
    df: pd.DataFrame
) -> None:
    invalid_age = (df["IDADE_NA_ELEICAO"].notna()
    &
    ~df["IDADE_NA_ELEICAO"].between(
        18,
        120,
        )
    )
    
    if invalid_age.any():
        raise ValueError(
            f"Found {invalid_age.sum()} records with invalid age"
        )
    
    
def _validate_social_name(
    df: pd.DataFrame
) -> None:
    
    inconsistent = (
        df["TEM_NOME_SOCIAL"]
        != df["NM_SOCIAL_CANDIDATO"].notna()
    )
    
    if inconsistent.any():
        raise ValueError(
            f"Found {inconsistent.sum()} inconsistent social name records"
        )
    
    
def _validation_federation(
    df: pd.DataFrame
) -> None:
     
    inconsistent = (
    df["TEM_FEDERACAO"]
    != df["NM_FEDERACAO"].notna()
)
    
    if inconsistent.any():
        raise ValueError(
            f"Found {inconsistent.sum()} inconsistent federation records"
        )