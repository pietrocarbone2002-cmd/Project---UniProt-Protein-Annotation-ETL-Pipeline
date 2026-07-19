import requests
import json
import sys
import pprint

base_url = "https://rest.uniprot.org/uniprotkb/search"

#Parameters and Query
organism = "organism_id:9606" #=human
search_term = "cancer"
size = 10

query = f'{organism} AND {search_term} AND reviewed%3Atrue&size={size}'

#URL
get_url = f'{base_url}?query={query}'
response = requests.get(get_url)

if response.status_code == 200:
    dataset = response.json()
else:
    print(f'Error at request: {response}')

#API Test
print(f'''
response.status_code:           {response.status_code}
dataset.keys():                 {dataset.keys()}
len(dataset["results"]):        {len(dataset["results"])}
dataset["results"][0].keys():   {dataset["results"][0].keys()}
''')

record = dataset["results"][0]

#Keys of interest
print(f'''
Primary Accession:          {record['primaryAccession']}
Protein Name:               {record['proteinDescription']['alternativeNames'][0]['shortNames'][0]['value']}
Gene Name:                  {record['genes'][0]['geneName']['value']}
Organism Scientific Name:   {record['organism']['scientificName']}
Sequence Length:            {record['sequence']['length']}
''')