import requests
import json
from pathlib import Path
import arrow
import pandas as pd
from fpdf import FPDF

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

# #Saving raw data as JSON
# raw_path = Path("Data/Raw")
# raw_path.mkdir(parents=True, exist_ok=True)
now = arrow.now()

# raw_file = raw_path / f"uniprot_{organism}_{search_term}_{size}_raw_{now.format("YYYY_MM_DD_HHmmss")}.json"

# with raw_file.open("w", encoding="utf-8") as file:
#     json.dump(dataset, file, indent=4)

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

    return flat_records

processed_data = transform_data(dataset)

# #Saving processed data as JSON
# processed_path = Path("Data/Processed")
# processed_path.mkdir(parents=True, exist_ok=True)

# processed_file = processed_path / f"uniprot_{organism}_{search_term}_{size}_processed_{now.format("YYYY_MM_DD_HHmmss")}.json"

# with processed_file.open("w", encoding="utf-8") as file:
#     json.dump(processed_data, file, indent=4)

# #Transforming the processed data into a pandas DataFrame
# df = pd.DataFrame(processed_data)

#=====================================================================================================
#           LOAD
#=====================================================================================================

report_path = Path("Reports")
report_path.mkdir(parents=True, exist_ok=True)

# #Create a .csv Report
# df.to_csv(
#     report_path / f"Report_Uniprot_{organism}_{search_term}_{size}_{now.format("YYYY_MM_DD_HHmmss")}.csv",
#     index = False, 
#     sep= ",")

#Create a pdf report

report_title = f"UniProt PDF Rerpot - {organism}/{search_term}/{size}"

class PDF(FPDF):

    def header(self):
        
        self.set_font("helvetica", "B", 16)

        #Calculate the width of title and position
        title_w = self.get_string_width(report_title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w)/2)

        #Thickness of the frame (border)
        self.set_line_width(1)

        #Title
        self.cell(title_w, 10, report_title, align = "C")
        self.ln(10)

    def footer(self):

        #Footer formatting
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.set_text_color(169,169,169)

        #Page counter
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align = "R", ln=False)

        #File Name
        self.cell(0, 10, f"uniprot_{organism}_{search_term}_{size}_processed_{now.format("YYYY_MM_DD_HHmmss")}.json", align = "L")

pdf = PDF("P", "mm", "A4")
pdf.set_title = report_title

pdf.add_page()


pdf.output(f"{report_path}/Report_Uniprot_{organism}_{search_term}_{size}_{now.format("YYYY_MM_DD_HHmmss")}.pdf")

