"""Prefect deployment definition for the RKI GrippeWeb dataset."""

from deploy.common import deploy_dataset
from flow.dataset_flow import run_dataset

DEPLOYMENT_NAME = "grippeweb-downloader"
PARAMETERS = {
    "source_url": (
        "https://raw.githubusercontent.com/robert-koch-institut/"
        "GrippeWeb_Daten_des_Wochenberichts/refs/heads/main/"
        "GrippeWeb_Daten_des_Wochenberichts.tsv"
    ),
    "local_path": "/tmp/grippeweb.tsv",
    "lakefs_repo": "sandbox",
    "lakefs_branch": "main",
    "lakefs_object_path": "RAW/RKI/grippeweb.tsv",
    "lakefs_commit_message": "new version from RKI",
    "mariadb_table": "grippeweb",
    "mariadb_database": "test",
}


if __name__ == "__main__":
    deploy_dataset(run_dataset, DEPLOYMENT_NAME, PARAMETERS)
