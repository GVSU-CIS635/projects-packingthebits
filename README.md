# Code Setup

This project consists of a series of Python scripts (found in the `code` directory) that can either be run individually
or through the `main.py` entrypoint. The following dependencies are needed to run this project:

| Dependency | Version |
|:-----------|:-------:|
| Python     | 3.14    |
| Pandas     | 2.3.3   |
| Numpy      | 2.3.3   |

To simplify the process of retrieving the dependencies, an `environment.yml` file has been provided for use with `conda`
or similar package management systems (`mamba`, `pixi`, etc.). An example of setting up with `conda` is:

1. Install `conda` if not already installed. Directions can be found
[online](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
2. Download dependencies and create new environment: `conda env create -f environment.yml`
3. Activate environment: `conda activate packing_the_bits`

Once the environment has been activated, you are ready to run the project.

# Project Directory Overview

- `code`: Contains code for running the project
- `documents`: Proposal, progress report, and final report as submitted on Blackboard.
- `data`: Contains example data for running the project. The data submitted within the report are protected data, and
cannot be shared at this time.

# Example Data

Example data can be downloaded from GitHub (INCLUDE LINK HERE ONCE GENERATED). It can also be created by the user via:

```
# Start from the top level project directory
cd data

# Download required file
wget https://github.com/huishenlab/biscuit/releases/download/v1.7.1.20250908/hg38_biscuit_qc_assets.zip
unzip hg38_biscuit_qc_assets.zip

# Run script to create example data
python create_data.py hg38/cpg.bed.gz
```

# Project Code Overview

## Running the Whole Pipeline

```
# Start from the top level project directory
cd code

# Run default pipeline
python main.py

# If you have your own data that conforms to the example data
python main.py --config your_config.toml
```

## Running Individual Components

Coming soon!

--------------------------------------------------------------------
# Original README

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/z6Xh1xsp)
# Term Project

Hello everyone,

Welcome to your term project for CIS 635! This project is a significant part of our course and an excellent opportunity for you to apply the concepts and techniques we've learned.

You will find all the detailed instructions and requirements for the term project in the link provided below. Please make sure to read through these instructions carefully to understand the scope and expectations of the project.

## [📎 CIS 635 Term Project Overview](https://gvsu-cis635.github.io/project/project-overview.html)

## Key Points to Remember

1. **Team Collaboration**: Each team is required to create a single Git repository for the project. All team members are expected to collaborate and contribute to this shared repository. Please ensure that you push all your code and data to this repository. If the data is too large, include a download link for the data file instead.
2. **Submission Requirements**: Each team is required to submit one project proposal, one progress report, and one final report to the Git repository. For details about the term project and submission deadlines, please visit the [project overview](https://gvsu-cis635.github.io/project/project-overview.html) page.

Best wishes on your term project!
