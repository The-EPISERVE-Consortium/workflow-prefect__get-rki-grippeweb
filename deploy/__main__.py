"""CLI entrypoint for deploying one or more dataset configurations to Prefect."""

import argparse

from deploy.common import deploy_from_registry, get_dataset_keys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deploy dataset-specific Prefect deployments from YAML.")
    parser.add_argument(
        "dataset",
        nargs="?",
        help="Dataset key from deploy/datasets.yaml, for example 'grippeweb'.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="deploy_all",
        help="Deploy all enabled datasets from deploy/datasets.yaml.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.deploy_all:
        deploy_from_registry()
        return

    if args.dataset:
        deploy_from_registry(args.dataset)
        return

    available = ", ".join(get_dataset_keys())
    parser.error(f"Provide a dataset key or use --all. Available datasets: {available}")


if __name__ == "__main__":
    main()
