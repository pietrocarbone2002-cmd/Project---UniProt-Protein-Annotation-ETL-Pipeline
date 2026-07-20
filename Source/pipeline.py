import requests
import json
import sys
import pprint
from pathlib import Path
import arrow
import pandas as pd

#=====================================================================================================
#           EXTRACT
#=====================================================================================================

BASE_URL = "https://rest.uniprot.org/uniprotkb/search"

def get_uniprot_data(organism_id: int, search_term: str, size: int):

    #Check if the given parameters are valid

    if not isinstance(organism_id, int) or organism_id <= 0:
        raise ValueError("organism_id must be a positive integer!")
    
    if not isinstance(search_term, str) or not search_term.strip():
        raise ValueError("search_term must be a non-empty string!")
    
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer!")
    
    #QUery and final url formation
    query = f'organism_id:{organism_id} AND {search_term} AND reviewed%3Atrue&size={size}'
    get_url = f'{BASE_URL}?query={query}'

    #Check for possible issues. If something goes wrong, nothing gets returned
    try:
        response = requests.get(get_url, timeout=30)
        response.raise_for_status()
    
    except requests.exceptions.Timeout as ex:
        raise RuntimeError("The UniProt request timed out") from ex
    
    except requests.exceptions.ConnectionError as ex:
        raise RuntimeError("Could not connect to the UniProt API.") from ex

    except requests.exceptions.HTTPError as ex:
        raise RuntimeError(f' UniProt returned HTTP {response.status_code}:{response.text[:300]}') from ex

    except requests.exceptions.RequestException as ex:
        raise RuntimeError(f'The UniProt request failed: {ex}') from ex

    return response.json()

#Parameters for the Query
organism = 9606 #=human
search_term = "cancer"
size = 10

#Data fetching
dataset = get_uniprot_data(organism, search_term, size)

#Saving raw data as JSON
raw_path = Path("Data/Raw")
raw_path.mkdir(parents=True, exist_ok=True)
now = arrow.now()

raw_file = raw_path / f"uniprot_cancer_raw_{now.format("YYYY_MM_DD_HHmmss")}.json"

with raw_file.open("w", encoding="utf-8") as file:
    json.dump(dataset, file, indent=4)

#=====================================================================================================
#           TRANSFORM
#=====================================================================================================

def transform_data(data:dict):

    #Validate the input
    if not isinstance(data, dict):
        raise TypeError("The Data is not in a supported format!")

    #Extract values
    flat_records = []
    for i in dataset["results"]:

        #Check if there is a protein name. If not -> None. This prevents error when data is missing
        protein_name = None
        try:
            protein_name = (i["proteinDescription"]["alternativeNames"][0]["shortNames"][0]["value"])
        except (KeyError, IndexError, TypeError):
            protein_name = None

        #Check if there is a gene name. If not -> None. This prevents error when data is missing
        gene_name = None
        try:
            gene_name = i["genes"][0]["geneName"]["value"]
        except (KeyError, IndexError, TypeError):
            gene_name = None

        flat_record = {
            "Accession": i.get("primaryAccession"),
            "Protein Name": protein_name,
            "Gene Name": gene_name,
            "Organism Name": i.get("organism", {}).get("scientificName"),
            "Sequence Length": i.get("sequence", {}).get("length"),
        }

        flat_records.append(flat_record)

    #Create the DataFrame
    df = pd.DataFrame(flat_records)

    #Return the transformed record
    return df[["Accession","Protein Name", "Gene Name", "Organism Name", "Sequence Length"]]

transform_data(dataset)

#=====================================================================================================
#           Load
#=====================================================================================================


