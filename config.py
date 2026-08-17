from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"
PROCESSED_DIR = DATA_DIR / "processed"

DATABASE_DIR = BASE_DIR / "database"
LOG_DIR = BASE_DIR / "logs"

DATABASE_PATH = DATABASE_DIR / "elections.duckdb"


TSE_CANDIDATES_URL = (
    "https://cdn.tse.jus.br/estatistica/sead/odsele/"
    "consulta_cand/consulta_cand_2026.zip"
)

DIRECTORIES = [
    RAW_DIR,
    STAGING_DIR,
    PROCESSED_DIR,
    DATABASE_DIR,
    LOG_DIR,
]

def create_directories():
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok = True)