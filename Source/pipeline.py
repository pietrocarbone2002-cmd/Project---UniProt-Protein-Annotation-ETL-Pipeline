import requests
import json
import sys
import pprint

base_url = "https://rest.uniprot.org/uniprotkb/search"

def get_raw_request(organism_id: int, search_term: str, size: int):

    if not isinstance(organism_id, int) or organism_id <= 0:
        raise ValueError("organism_id must be a positive integer!")
    
    if not isinstance(search_term, str) or not search_term.strip():
        raise ValueError("search_term must be a non-empty string!")
    
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer!")
    
    query = f'{organism_id} AND {search_term} AND reviewed%3Atrue&size={size}'
    get_url = f'{base_url}?query={query}'

    
    try:
        response = requests.get(get_url, timeout=30)
        response.raise_for_status()
    
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("The UniProt request timed out") from exc
    
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Could not connect to the UniProt API.") from exc

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f' UniProt returned HTTP {response.status_code}:{response.text[:300]}') from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f'The UniProt request failed: {exc}') from exc

    return response.json()

#Parameters and Query
organism = 9606 #=human
search_term = "cancer"
size = 10

dataset = get_raw_request(organism, search_term, size)

record = dataset["results"][0]

#Keys of interest
print(f'''
Primary Accession:          {record['primaryAccession']}
Protein Name:               {record['proteinDescription']['alternativeNames'][0]['shortNames'][0]['value']}
Gene Name:                  {record['genes'][0]['geneName']['value']}
Organism Scientific Name:   {record['organism']['scientificName']}
Sequence Length:            {record['sequence']['length']}
''')