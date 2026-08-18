from config import create_directories
from src.extract.candidates import (
    download_candidates,
    extract_candidates_zip,
)
from src.transform.candidates import (
    load_candidates_raw,
    transform_candidates,
)

from src.validate.candidates import (
    validate_transformed_candidates,
)

from src.load.candidates import (
    save_candidates_staging,
    load_candidates_duckdb
)

def main():

    create_directories()

    zip_path = download_candidates()

    extract_candidates_zip(zip_path)
    
    df_candidates_raw = load_candidates_raw()

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
    
    
    


if __name__ == "__main__":
    main()