# UniProt Protein Annotation ETL Pipeline

## Overview

This repository contains a Python-based ETL pipeline for extracting, transforming, and analyzing protein annotation data from the UniProt REST API.

The project focuses on human proteins related to a selected biological topic and converts nested JSON API responses into structured, analysis-ready datasets. The resulting data is used for exploratory analysis of protein properties such as sequence length, annotation quality, biological keywords, and subcellular localization.

## Project Motivation

Public biological databases contain large amounts of structured and semi-structured information. However, this data often needs to be extracted from APIs, cleaned, normalized, and transformed before it can be used for downstream analysis.

This project demonstrates how REST API data from a major life-science database can be turned into a reproducible data science workflow using Python.

## Data Source

The data is collected from the UniProt REST API.

UniProt provides curated and computationally annotated information about proteins, including:

- Protein names
- Gene names
- Organism information
- Protein sequences
- Functional annotations
- Keywords
- Subcellular locations
- Annotation scores
- Reviewed status

## Pipeline Architecture

The project follows a simple ETL structure:

### Extract

The extraction step sends API requests to UniProt and stores the raw JSON responses locally.

Raw data is saved in:

data/raw/

### Transform

The transformation step parses the nested JSON structure and converts selected protein attributes into a clean tabular format.

The processed dataset includes fields such as:

- UniProt accession
- Protein name
- Gene name
- Organism
- Sequence length
- Reviewed status
- Annotation score
- Keywords
- Subcellular location
- Functional comments

Processed data is saved in:

data/processed/

### Load

The cleaned dataset is exported as a CSV file and used for exploratory data analysis.

Optional output formats may include:

- Parquet files
- SQLite tables

## Exploratory Data Analysis

The analysis investigates patterns in the protein dataset, including:

- Distribution of protein sequence lengths
- Most frequent biological keywords
- Most common subcellular locations
- Relationship between protein length and annotation score
- Differences between reviewed and unreviewed entries

## Visualizations

The project includes visual summaries created with Matplotlib and/or Seaborn, such as:

- Histogram of protein sequence lengths
- Bar chart of frequent UniProt keywords
- Bar chart of common subcellular locations
- Scatter plot of protein length versus annotation score

Figures are saved in:

reports/figures/

## Technologies Used

- Python
- requests
- pandas
- json
- pathlib
- matplotlib
- seaborn
- Jupyter Notebook
- UniProt REST API

## Key Features

- API-based data extraction from UniProt
- Local storage of raw JSON responses
- Parsing of nested JSON structures
- Transformation into a clean pandas DataFrame
- Export of processed data as CSV
- Exploratory analysis of protein annotations
- Reproducible project structure for data science workflows

## Example Research Focus

The pipeline can be configured for different biological topics, such as:

- Human kinases
- Mitochondrial proteins
- Cancer-related proteins
- Antibiotic resistance proteins
- Proteins involved in glucose metabolism
- Neurodegeneration-related proteins

## Current Scope

The initial version focuses on a selected set of human proteins retrieved from UniProt. The project emphasizes clean data engineering, readable code, and exploratory analysis rather than advanced machine learning.

## Future Improvements

Potential extensions include:

- Adding command-line arguments for different search topics
- Comparing proteins across organisms
- Storing processed data in SQLite
- Adding unit tests for transformation functions
- Building an interactive Streamlit dashboard
- Enriching the dataset with data from other biological APIs
- Adding automated logging and pipeline validation

## Skills Demonstrated

This project demonstrates practical skills in:

- REST API usage
- JSON parsing
- ETL pipeline design
- Bioinformatics data handling
- Data cleaning with pandas
- Exploratory data analysis
- Scientific visualization
- Reproducible GitHub project organization

## Status

In development.