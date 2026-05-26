"""Prefect task for writing the downloaded TSV data into MariaDB."""

import logging
import os

import pymysql
from prefect import get_run_logger, task
from prefect.exceptions import MissingContextError


def _get_logger() -> logging.Logger:
    """Return a Prefect run logger when available, otherwise a standard logger."""
    try:
        return get_run_logger()
    except MissingContextError:
        return logging.getLogger(__name__)


@task
def store_to_mariadb(df, table: str) -> None:
    """Write a DataFrame to a MariaDB table, replacing it if it already exists."""
    logger = _get_logger()
    db = os.environ.get("MARIADB_DATABASE", "test")
    host = os.environ["MARIADB_HOST"]
    logger.info("Connecting to %s/%s", host, db)

    conn = pymysql.connect(
        host=host,
        user=os.environ["MARIADB_USER"],
        password=os.environ["MARIADB_PASSWORD"],
        database=db,
    )
    try:
        with conn.cursor() as cursor:
            cols = ", ".join(f"`{col}` TEXT" for col in df.columns)
            cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
            cursor.execute(f"CREATE TABLE `{table}` ({cols})")
            logger.info("Inserting %d rows into `%s`", len(df), table)
            placeholders = ", ".join(["%s"] * len(df.columns))
            rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
            cursor.executemany(f"INSERT INTO `{table}` VALUES ({placeholders})", rows)
        conn.commit()
        logger.info("Done. Table `%s` now has %d rows and %d columns.", table, len(df), len(df.columns))
    finally:
        conn.close()
