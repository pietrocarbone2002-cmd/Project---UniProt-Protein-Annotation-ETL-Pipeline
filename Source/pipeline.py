import requests
import json
import sys
import pprint

BASE_URL = "https://rest.uniprot.org/uniprotkb/search"

#=====================================================================================================
#           EXTRACT
#=====================================================================================================

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

#Expection of the first row

first_record = dataset["results"][0]

print(f'''
Primary Accession:          {first_record['primaryAccession']}
Protein Name:               {first_record['proteinDescription']['alternativeNames'][0]['shortNames'][0]['value']}
Gene Name:                  {first_record['genes'][0]['geneName']['value']}
Organism Scientific Name:   {first_record['organism']['scientificName']}
Sequence Length:            {first_record['sequence']['length']}
''')

flat_record = {
    "accession":first_record['primaryAccession'],
    "protein_name":first_record['proteinDescription']['alternativeNames'][0]['shortNames'][0]['value'],
    "gene_name" : first_record['genes'][0]['geneName']['value'],
    "organism_scientific_name":first_record['organism']['scientificName'],
    "sequence_length": first_record['sequence']['length']
}

print(flat_record)

#=====================================================================================================
#           TRANSFORM
#=====================================================================================================

def tranform_data():
    
    #Validate the input

    #Extract values

    #Clean or normalize values

    #Build the output structure

    #Return the transformed record

    pass
