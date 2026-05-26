"""Shared default configuration for the GrippeWeb workflow and deployment."""

RKI_URL = (
    "https://raw.githubusercontent.com/robert-koch-institut/"
    "GrippeWeb_Daten_des_Wochenberichts/refs/heads/main/"
    "GrippeWeb_Daten_des_Wochenberichts.tsv"
)
DEFAULT_PATH = "/tmp/grippeweb.tsv"
DEFAULT_LAKEFS_REPO = "sandbox"
DEFAULT_LAKEFS_BRANCH = "main"
DEFAULT_LAKEFS_OBJECT_PATH = "RAW/RKI/grippeweb.tsv"
DEFAULT_MARIADB_DATABASE = "test"
