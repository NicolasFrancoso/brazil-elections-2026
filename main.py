from config import create_directories
from src.extract.candidates import (
    download_candidates,
    extract_candidates_zip,
)


def main():

    create_directories()

    zip_path = download_candidates()

    extract_candidates_zip(zip_path)


if __name__ == "__main__":
    main()