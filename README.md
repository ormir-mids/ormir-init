# ormir-init

`ormir-init` is a Python package that provides a command-line tool for creating standardized ORMIR-MIDS project structures for musculoskeletal imaging studies.

## Installation

```bash
pip install ormir-init
```

## Requirements

- Python 3.9 or later

----

## Command Line Tools
### ormir-init
**Purpose**
Create a standardized ORMIR-MIDS project structure for organizing imaging data, analysis code, documentation, and research outputs. The tool generates the required metadata files and configures the project for version control.

**Features**
* Creates the recommended MIDS directory structure
* Generates dataset_description.json
* Generates participants.tsv
* Adds a user-selected dataset license
* Initializes a Git repository
* Creates a .gitignore configured for common medical imaging file formats
* Validates user input before creating the project

**Usage**
```bash
ormir-init <root_directory> <dataset_name> [--license {cc, mit, isc, apache, gpl}]
```
**Example**
``` bash
ormir-init /Volumes/Data MyStudy --license mit
```
**Generated project structure**
```
MyStudy/
├── code/
│   ├── batch_scripts/
│   ├── code_docs/
│   ├── notebooks/
│   └── src/
├── data/
│   ├── data_docs/
│   ├── derivatives/
│   ├── mids/
│   │   └── participants.tsv
│   ├── raw/
│   └── results/
├── publication/
├── .git/
├── .gitignore
├── dataset_description.json
└── LICENSE
```
---
