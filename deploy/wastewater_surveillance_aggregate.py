"""Prefect deployment definition for the RKI aggregated wastewater surveillance dataset."""

from deploy.common import deploy_dataset
from flow.dataset_flow import run_dataset

DEPLOYMENT_NAME = "wastewater_surveillance_aggregate"
PARAMETERS = {
    "source_url": (
        "https://raw.githubusercontent.com/robert-koch-institut/"
        "Abwassersurveillance_AMELAG/refs/heads/main/"
        "amelag_aggregierte_kurve.tsv"
    ),
    "source_delimiter": "\t",
    "local_path": "/tmp/wastewater_surveillance_aggregate.tsv",
    "lakefs_repo": "sandbox",
    "lakefs_branch": "main",
    "lakefs_object_path": "RAW/RKI/wastewater_surveillance_aggregate.tsv",
    "lakefs_commit_message": "new version from RKI",
    "mariadb_table": "wastewater_surveillance_aggregate",
    "mariadb_database": "test",
}


if __name__ == "__main__":
    deploy_dataset(run_dataset, DEPLOYMENT_NAME, PARAMETERS)
