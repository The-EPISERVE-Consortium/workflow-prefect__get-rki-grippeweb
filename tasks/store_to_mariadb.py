"""Prefect task for writing the downloaded TSV data into MariaDB."""

import os

import pymysql
from prefect import task

from tasks._logging import get_logger


@task
def store_to_mariadb(df, table: str, database: str) -> None:
    """Write a DataFrame to a MariaDB table, replacing it if it already exists."""
    logger = get_logger(__name__)
    host = os.environ["MARIADB_HOST"]
    logger.info("Connecting to %s/%s", host, database)

    conn = pymysql.connect(
        host=host,
        user=os.environ["MARIADB_USER"],
        password=os.environ["MARIADB_PASSWORD"],
    )
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")
        cursor.execute(f"USE `{database}`")
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
