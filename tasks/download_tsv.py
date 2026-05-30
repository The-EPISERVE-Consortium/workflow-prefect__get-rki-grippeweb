"""Prefect task for downloading a delimited text dataset into a DataFrame."""

import pandas as pd
from prefect import task

from tasks._logging import get_logger


@task
def download_tsv(url: str, source_delimiter: str, skiprows: int = 0) -> pd.DataFrame:
    """Download a delimited file from the given URL and return it as a DataFrame."""
    logger = get_logger(__name__)
    logger.info("Start download %s", url)
    df = pd.read_csv(url, sep=source_delimiter, skiprows=skiprows)
    size_kb = len(df.to_csv(sep="\t", index=False).encode()) / 1024
    logger.info("Download done. Downloaded %.1f KB", size_kb)
    return df
