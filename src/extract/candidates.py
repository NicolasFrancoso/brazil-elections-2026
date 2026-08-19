from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
import pandas as pd
import shutil

import requests

from config import (
    CANDIDATES_RAW_DIR,
    TSE_CANDIDATES_URL,
)
from src.utils.logger import get_logger


logger = get_logger(__name__)


def download_candidates() -> Path:

    temp_dir = (
        CANDIDATES_RAW_DIR
        / "_temp"
    )

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        temp_dir
        / "consulta_cand_2026.zip"
    )

    logger.info(
        "Downloading TSE candidates dataset"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }

    try:
        response = requests.get(
            TSE_CANDIDATES_URL,
            headers=headers,
            timeout=120,
        )

        response.raise_for_status()

    except requests.RequestException as exc:

        logger.error(
            "Failed to download candidates dataset. "
            "Status: %s | URL: %s",
            getattr(response, "status_code", "unknown"),
            TSE_CANDIDATES_URL,
        )
        raise

    destination.write_bytes(
        response.content
    )

    logger.info(
        "Candidates dataset downloaded temporarily: %s",
        destination,
    )

    return destination

def extract_candidates_zip(
    zip_path: Path,
) -> Path:

    extract_dir = (
        zip_path.parent
        / "extracted"
    )

    if extract_dir.exists():
        import shutil
        shutil.rmtree(extract_dir)

    extract_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "Extracting candidates ZIP file"
    )

    with ZipFile(
        zip_path,
        "r",
    ) as zip_file:

        zip_file.extractall(
            extract_dir
        )

    logger.info(
        "Candidates files extracted to: %s",
        extract_dir,
    )

    return extract_dir

def get_candidates_snapshot_timestamp(
    extract_dir: Path,
    ) -> str:

    file_path = (
        extract_dir
        / "consulta_cand_2026_BRASIL.csv"
    )

    metadata = pd.read_csv(
        file_path,
        sep=";",
        encoding="latin1",
        quotechar='"',
        usecols=[
            "DT_GERACAO",
            "HH_GERACAO",
        ],
        nrows=1,
        keep_default_na=False,
    )

    generation_datetime = pd.to_datetime(
        (
            metadata.loc[0, "DT_GERACAO"]
            + " "
            + metadata.loc[0, "HH_GERACAO"]
        ),
        format="%d/%m/%Y %H:%M:%S",
    )

    snapshot_timestamp = (
        generation_datetime.strftime(
            "%Y-%m-%d_%H%M%S"
        )
    )

    return snapshot_timestamp

def persist_candidates_snapshot(
    zip_path: Path,
    extract_dir: Path,
    ) -> Path:

    snapshot_timestamp = (
        get_candidates_snapshot_timestamp(
            extract_dir
        )
    )

    snapshot_dir = (
        CANDIDATES_RAW_DIR
        / snapshot_timestamp
    )

    if snapshot_dir.exists():

        logger.info(
            "Candidates snapshot already exists: %s",
            snapshot_dir,
        )

        shutil.rmtree(
            zip_path.parent
        )

        return snapshot_dir

    snapshot_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    shutil.move(
        str(zip_path),
        str(
            snapshot_dir
            / "consulta_cand_2026.zip"
        ),
    )

    shutil.move(
        str(extract_dir),
        str(
            snapshot_dir
            / "extracted"
        ),
    )

    temp_dir = zip_path.parent

    if temp_dir.exists():
        shutil.rmtree(
            temp_dir
        )

    logger.info(
        "Candidates snapshot persisted: %s",
        snapshot_dir,
    )

    return snapshot_dir

def extract_candidates() -> Path:

    zip_path = (
        download_candidates()
    )

    extract_dir = (
        extract_candidates_zip(
            zip_path
        )
    )

    snapshot_dir = (
        persist_candidates_snapshot(
            zip_path,
            extract_dir,
        )
    )

    return snapshot_dir
