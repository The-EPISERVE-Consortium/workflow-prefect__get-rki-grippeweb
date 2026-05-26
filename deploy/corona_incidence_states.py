"""Prefect deployment definition for the RKI state-level COVID incidence dataset."""

from deploy.common import deploy_dataset
from flow.dataset_flow import run_dataset

DEPLOYMENT_NAME = "corona_incidence_states"
PARAMETERS = {
    "source_url": (
        "https://raw.githubusercontent.com/robert-koch-institut/"
        "COVID-19_7-Tage-Inzidenz_in_Deutschland/refs/heads/main/"
        "COVID-19-Faelle_7-Tage-Inzidenz_Bundeslaender.csv"
    ),
    "source_delimiter": ",",
    "local_path": "/tmp/covid_states.tsv",
    "lakefs_repo": "sandbox",
    "lakefs_branch": "main",
    "lakefs_object_path": "RAW/RKI/covid_states.tsv",
    "lakefs_commit_message": "new version from RKI",
    "mariadb_table": "corona_incidence_states",
    "mariadb_database": "test",
}


if __name__ == "__main__":
    deploy_dataset(run_dataset, DEPLOYMENT_NAME, PARAMETERS)
