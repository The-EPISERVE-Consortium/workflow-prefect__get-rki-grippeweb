"""Prefect task for downloading the RKI GrippeWeb TSV."""

import pandas as pd
from prefect import task

from tasks._logging import get_logger


@task
def download_tsv(url: str) -> pd.DataFrame:
    """Download a TSV file from the given URL and return it as a DataFrame."""
    logger = get_logger(__name__)
    logger.info("Start download %s", url)
    df = pd.read_csv(url, sep="\t")
    size_kb = len(df.to_csv(sep="\t", index=False).encode()) / 1024
    logger.info("Download done. Downloaded %.1f KB", size_kb)
    return df
