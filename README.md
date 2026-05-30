# Cancer-Related Protein Annotation ETL Pipeline

## Overview

This repository contains a Python-based ETL pipeline for extracting, transforming, and analyzing cancer-related protein annotation data from the UniProt REST API.

The project focuses on human proteins associated with cancer biology and converts nested JSON API responses into structured, analysis-ready datasets. The processed data is then used for exploratory data analysis of protein properties such as sequence length, annotation quality, biological keywords, functional descriptions, and subcellular localization.

## Project Motivation

Cancer is driven by complex molecular processes involving genes, proteins, signaling pathways, mutations, and changes in cellular regulation. Public biological databases such as UniProt provide rich protein-level information that can support exploratory research into cancer-associated proteins.

However, API responses from biological databases are often deeply nested and require careful parsing before they can be analyzed. This project demonstrates how cancer-related protein data can be extracted from a public life-science API, transformed into clean tabular data, and explored using Python-based data science methods.

## Data Source

The data is collected from the UniProt REST API.

UniProt provides information about proteins, including:

- Protein accession IDs
- Protein names
- Gene names
- Organism information
- Protein sequence length
- Functional annotations
- Biological keywords
- Subcellular locations
- Annotation scores
- Reviewed status

This project focuses on human cancer-related protein records.

## Research Focus

The central research focus of this project is:

**What are the common structural and annotation patterns among human cancer-related proteins available in UniProt?**

The analysis investigates questions such as:

- Which cancer-related proteins are retrieved from UniProt?
- What is the distribution of protein sequence lengths?
- Which biological keywords occur most frequently?
- Which subcellular locations are most common?
- How complete are the annotations for these proteins?
- Are there visible patterns between protein length and annotation score?

## Pipeline Architecture

The project follows a simple ETL structure:

### Extract

The extraction step sends API requests to the UniProt REST API and stores the raw JSON responses locally.

The API query is designed to retrieve human proteins associated with cancer-related terms.

Raw API responses are saved in:

data/raw/

### Transform

The transformation step parses the nested JSON response and extracts selected protein attributes into a clean pandas DataFrame.

The processed dataset includes fields such as:

- UniProt accession
- Protein name
- Gene name
- Organism
- Sequence length
- Reviewed status
- Annotation score
- Biological keywords
- Subcellular location
- Functional comments

Processed data is saved in:

data/processed/

### Load

The cleaned dataset is exported as a CSV file for downstream analysis.

Optional output formats may include:

- Parquet files
- SQLite tables

## Exploratory Data Analysis

The exploratory analysis focuses on describing and visualizing the cancer-related protein dataset.

Planned analyses include:

- Summary statistics of protein sequence lengths
- Distribution of annotation scores
- Frequency analysis of biological keywords
- Frequency analysis of subcellular locations
- Comparison of reviewed and unreviewed UniProt entries
- Exploration of the relationship between protein length and annotation score

## Visualizations

The project includes visual summaries created with Matplotlib and/or Seaborn.

Example visualizations include:

- Histogram of cancer-related protein sequence lengths
- Bar chart of the most frequent UniProt keywords
- Bar chart of common subcellular locations
- Scatter plot of protein length versus annotation score
- Count plot of reviewed versus unreviewed records

Figures are saved in:

reports/figures/

## Key Features

- API-based extraction of cancer-related protein records from UniProt
- Local storage of raw JSON responses
- Parsing of nested JSON structures
- Transformation into a clean tabular dataset
- Export of processed data as CSV
- Exploratory data analysis of cancer-related protein annotations
- Scientific visualizations for portfolio presentation
- Reproducible GitHub project structure

## Current Scope

The current version focuses on human cancer-related proteins retrieved from UniProt. The project emphasizes API usage, JSON parsing, ETL design, clean data transformation, and exploratory analysis.

This project does not aim to make clinical claims or diagnostic predictions. The analysis is exploratory and intended for learning data engineering and data science workflows in a life-science context.

## Future Improvements

Potential extensions include:

- Refining the UniProt query strategy for more specific cancer-related protein groups
- Comparing oncogenes and tumor suppressor proteins
- Adding pathway-level information from external APIs
- Integrating gene-level metadata from Ensembl
- Storing processed data in SQLite
- Adding unit tests for transformation functions
- Building an interactive Streamlit dashboard
- Adding logging and validation to the ETL pipeline
- Comparing reviewed and unreviewed UniProt records

## Skills Demonstrated

This project demonstrates practical skills in:

- REST API usage
- JSON data extraction
- ETL pipeline design
- Bioinformatics data handling
- Nested JSON parsing
- Data cleaning with pandas
- Exploratory data analysis
- Scientific visualization
- Reproducible GitHub repository organization

## Status

In development