"""Prefect task for saving a downloaded TSV to local storage."""

import pandas as pd
from prefect import task


@task
def save_locally(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to the local filesystem as a TSV file."""
    df.to_csv(path, sep="\t", index=False)
