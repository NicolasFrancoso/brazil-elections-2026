from config import create_directories
from src.extract.candidates import (
    download_candidates,
    extract_candidates_zip,
)
from src.transform.candidates import load_candidates_raw
from src.validate.candidates import profile_candidates

def main():

    create_directories()

    zip_path = download_candidates()

    extract_candidates_zip(zip_path)
    
    df_candidates = load_candidates_raw()

    profile_candidates(df_candidates)


if __name__ == "__main__":
    main()