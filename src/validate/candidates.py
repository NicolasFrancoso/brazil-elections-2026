import pandas as pd

from src.utils.logger import get_logger


logger = get_logger(__name__)


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