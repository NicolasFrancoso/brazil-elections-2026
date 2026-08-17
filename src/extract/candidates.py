from pathlib import Path
import requests

from config import RAW_DIR, TSE_CANDIDATES_URL
from src.utils.logger import get_logger

from zipfile import ZipFile


logger = get_logger(__name__)


def download_candidates() -> Path:

    destination = RAW_DIR / "consulta_cand_2026.zip"

    logger.info("Downloading TSE candidates dataset")

    response = requests.get(
        TSE_CANDIDATES_URL,
        timeout=120
    )

    response.raise_for_status()

    destination.write_bytes(response.content)

    logger.info(
        "Candidates dataset downloaded: %s",
        destination
    )

    return destination

def extract_candidates_zip(zip_path: Path) -> Path:

    extract_dir = RAW_DIR / "candidates_2026"

    extract_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info("Extracting candidates ZIP file")

    with ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(extract_dir)

    logger.info(
        "Candidates files extracted to: %s",
        extract_dir
    )

    return extract_dir