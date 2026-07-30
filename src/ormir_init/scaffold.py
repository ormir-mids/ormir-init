"""
scaffold.py

Creates the folder structure for a MIDS dataset based on Figure 3
of Bonaretti et al. 2026 and the MIDS standard Santini et al. 2026

Usage:
    ormir-init <root_directory> <dataset_name> --license <license> 

    --license: The license for the dataset (APACHE, MIT, ISC, GPL, CC) default CC

Created by: S.D. McGarry 07/08/2026
Last modified: 07/23/2026
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

def validate_git_available() -> None:
    if shutil.which("git") is None:
        raise RuntimeError(
            "Git is not installed or is not available on PATH."
        )

def validate_inputs(root_directory: str, dataset_name: str) -> Path:
    root = Path(root_directory)

    if not root.exists():
        sys.exit(f"ERROR: Root directory does not exist:\n{root}")

    if not root.is_dir():
        sys.exit(f"ERROR: Root path is not a directory:\n{root}")

    if not re.fullmatch(r"[A-Za-z0-9_-]+", dataset_name):
        sys.exit(
            "ERROR: Dataset name may only contain letters, numbers, "
            "underscores (_), and hyphens (-)."
        )

    dataset_root = root / dataset_name

    if dataset_root.exists():
        sys.exit(
            f"ERROR: Dataset directory already exists:\n"
            f"{dataset_root}\n\n"
            "Refusing to overwrite an existing dataset."
        )

    return dataset_root


def create_file_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")

def create_mids_scaffold(dataset_root: Path, license_name: str) -> None:
    folders = [
        "data/raw",
        "data/mids",
        "data/derivatives",
        "data/results",
        "data/data_docs",
        "publication",
        "code/src",
        "code/notebooks",
        "code/batch_scripts",
        "code/code_docs",
    ]

    dataset_root.mkdir(exist_ok=False)
    
    for folder in folders:
        folder_path = dataset_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    participants_tsv = dataset_root / "data" / "mids" / "participants.tsv"
    create_file_if_missing(
        participants_tsv,
        "participant_id\tage\tsex\n"
    )

    license_info = SUPPORTED_LICENSES[license_name]

    dataset_description = {
        "Name": dataset_root.name,
        "License": license_info["spdx"],
        "MIDSVersion": "",
        "DatasetType": "",
        "Authors": [],
        "Acknowledgements": "",
        "Funding": [],
        "ReferencesAndLinks": [],
        "DatasetDOI": ""
    }

    write_license_file(dataset_root, license_name)

    dataset_description_path = dataset_root / "dataset_description.json"
    if not dataset_description_path.exists():
        dataset_description_path.write_text(
            json.dumps(dataset_description, indent=4) + "\n"
                                            , encoding="utf-8")

def setup_git(dataset_root: Path) -> None:
    try:
        subprocess.run(
            ["git", "init"],
            cwd=dataset_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        sys.exit(
            "ERROR: Git is not installed or not available on PATH.\n"
            "Dataset scaffold was created, but Git was not initialized."
        )
    except subprocess.CalledProcessError as error:
        sys.exit(
            "ERROR: Failed to initialize Git repository.\n"
            f"An incomplete project remains at:\n{dataset_root}\n\n"
            f"Git reported:\n{error.stderr.strip()}"
        )

    write_gitignore(dataset_root)

def read_package_text(relative_path: str) -> str:
    return (
        files("ormir_init")
        .joinpath(relative_path)
        .read_text(encoding="utf-8")
    )


def write_license_file(dataset_root: Path, license_name: str) -> None:
    license_info = SUPPORTED_LICENSES[license_name]
    license_text = read_package_text(f"licenses/{license_info['file']}")
    create_file_if_missing(dataset_root / "LICENSE", license_text)

def write_gitignore(dataset_root: Path) -> None:
    gitignore_text = read_package_text("gitignore.txt")
    create_file_if_missing(dataset_root / ".gitignore", gitignore_text)

SUPPORTED_LICENSES = {
    "cc": {
        "spdx": "CC-BY-SA",
        "file": "cc.txt",
    },
    "mit": {
        "spdx": "MIT",
        "file": "mit.txt",
    },
    "isc": {
        "spdx": "ISC",
        "file": "isc.txt",
    },
    "apache": {
        "spdx": "Apache-2.0",
        "file": "apache.txt",
    },
    "gpl": {
        "spdx": "GPL-3.0-only",
        "file": "gpl.txt",
    },
}

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a MIDS dataset folder structure."
    )
    parser.add_argument(
        "root_directory",
        type=str,
        help="Root directory where the dataset will be created."
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="Name of the dataset."
    )
    parser.add_argument(
        "--license",
        type=str,
        default="cc",
        choices=SUPPORTED_LICENSES,
        help="Data license for the dataset. Default: cc (CC-BY-SA)"
    )

    args = parser.parse_args()

    dataset_root = validate_inputs(args.root_directory, args.dataset_name)
    validate_git_available()

    create_mids_scaffold(dataset_root, args.license)
    setup_git(dataset_root)

    print(f"MIDS scaffold created at: {dataset_root}")

if __name__ == "__main__":
    main()
    
