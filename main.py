from config import create_directories
from src.extract.candidates import (
    extract_candidates,
)
from src.transform.candidates import (
    load_candidates_raw,
    transform_candidates,
)

from src.validate.candidates import (
    validate_transformed_candidates,
    validate_candidates_analytics,
)

from src.load.candidates import (
    save_candidates_staging,
    load_candidates_duckdb
)

from src.validate.pipeline import (
    validate_candidates_pipeline,
)

from src.analytics.candidates import (
    build_candidates_analytics,
)

from src.load.candidates import (
    save_candidates_analytics,
    load_candidates_analytics_duckdb,
)

from src.model.party import build_dim_party
from src.model.office import build_dim_office
from src.model.election import build_dim_election
from src.model.location import build_dim_location
from src.model.candidacy import build_dim_candidacy

from src.validate.model import (
    validate_dimensions,
)

from src.load.model import (
    persist_dimensions,
)
from src.validate.persistence import (
    validate_dimension_persistence,
)


def main():

    create_directories()

    snapshot_dir = (
        extract_candidates()
        )

    df_candidates_raw = (
        load_candidates_raw(
            snapshot_dir
        )
    )

    df_candidates = transform_candidates(
        df_candidates_raw
    )

    validate_transformed_candidates(
        df_candidates
    )

    parquet_path = (
        save_candidates_staging(
            df_candidates
        )
    )

    load_candidates_duckdb(
        parquet_path
    )

    validate_candidates_pipeline(
        df_candidates,
        parquet_path,
        )

    df_candidates_analytics = (
    build_candidates_analytics(
        df_candidates
    )
    )

    analytics_path = (
        save_candidates_analytics(
            df_candidates_analytics
        )
    )

    load_candidates_analytics_duckdb(
        analytics_path
    )

    validate_candidates_analytics(
        df_candidates_analytics
    )

    df_candidates_analytics = build_candidates_analytics(
    df_candidates
)

    validate_candidates_analytics(
        df_candidates_analytics
    )

    dim_party = build_dim_party(
        df_candidates_analytics
    )


    dim_office = build_dim_office(
        df_candidates_analytics
    )

    dim_election = build_dim_election(
        df_candidates_analytics
    )

    dim_location = build_dim_location(
        df_candidates_analytics
    )

    dim_candidacy = build_dim_candidacy(
        df_candidates_analytics
    )
    print("\n=== DIMENSIONS ===")
    print(f"dim_party: {len(dim_party)}")
    print(f"dim_office: {len(dim_office)}")
    print(f"dim_election: {len(dim_election)}")
    print(f"dim_location: {len(dim_location)}")
    print(f"dim_candidacy: {len(dim_candidacy)}")

    print(
    dim_location.to_string(
        index=False
        )
    )

    print("\n=== DATASET VERSION ===")

    print(
        df_candidates_analytics[
            "SNAPSHOT_DATETIME"
        ].unique()
    )

    print(
        "\nCandidates:",
        len(df_candidates_analytics)
    )

    print("\n=== DIM ELECTION ===")

    print(
        dim_election.to_string(
            index=False
        )
    )

    print("\n=== CANDIDATES BY ELECTION ===")

    print(
        df_candidates_analytics[
            [
                "CD_ELEICAO",
                "DS_ELEICAO",
                "NR_TURNO",
                "DT_ELEICAO",
            ]
        ]
        .value_counts()
    )

    validate_dimensions(
        dim_party,
        dim_office,
        dim_election,
        dim_location,
        dim_candidacy,
        )

    dimensions = {
        "dim_party": dim_party,
        "dim_office": dim_office,
        "dim_election": dim_election,
        "dim_location": dim_location,
        "dim_candidacy": dim_candidacy,
        }

    dimension_paths = persist_dimensions(
        dimensions
        )

    for table_name, df in dimensions.items():
        validate_dimension_persistence(
            df=df,
            parquet_path=dimension_paths[
                table_name
            ],
            table_name=table_name,
        )




if __name__ == "__main__":
    main()
