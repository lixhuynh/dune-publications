# =======
# IMPORTS

from datetime import datetime
import requests

# ============
# PAGE REQUEST

def get_id(entry: dict):
    identifier = entry["control_number"]
    return "https://inspirehep.net/literature/" + str(identifier)

def get_collab_info(entry: dict):
    author = "DUNE collaboration"
    title = "\"" + entry["titles"][0]["title"] + "\""
    id = get_id(entry)
    return [author, title, id]

def get_thesis_info(entry: dict):
    author = " ".join(entry["authors"][0]["full_name"].split(", ")[::-1])
    title = entry["titles"][0]["title"]
    institution = entry["thesis_info"]["institutions"][0]["name"]
    # Formatting institution as appropriate
    if institution[:2] == "U.":
        institution = "University of" + institution[2:]
    elif "U." in institution:
        institution = institution.replace("U.", "University")
    elif institution[:5] == "Coll.":
        institution = "College of" + institution[5:]
    elif "Coll." in institution:
        institution = institution.replace("Coll.", "College")
    # Formatting date as appropriate
    raw_date = entry["earliest_date"]
    if len(raw_date) == 4:
        date = datetime.strptime(raw_date, "%Y").strftime("%Y")
    elif len(raw_date) == 7:
        date = datetime.strptime(raw_date, "%Y-%m").strftime("%B %Y")
    elif len(raw_date) == 10:
        date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%B %Y")
    else:
        date = "Unknown"
    id = get_id(entry)
    return [author, title, institution, "Ph.D.", date, id]

def get_related_info(entry: dict):
    author = " ".join(entry["authors"][0]["full_name"].split(", ")[::-1]) + " et al."
    title = "\"" + entry["titles"][0]["title"] + "\""
    id = get_id(entry)
    return [author, title, id]

def make_query(page: str) -> dict:
    entries = requests.get(page).json()["hits"]["hits"]
    publications = {"collab": [], "thesis": [], "related": []}
    for i in range(len(entries)): # Iterate through and format entries
        c_entry = entries[i]["metadata"]
        if "collaborations" in c_entry and "DUNE" in [collab['value'].upper() for collab in c_entry["collaborations"]]:
            # Publication by DUNE Collaboration
            raw = get_collab_info(c_entry)
            publications["collab"].append(", ".join(raw))
        elif "thesis" in c_entry["document_type"]: # DUNE Thesis
            raw = get_thesis_info(c_entry)
            publications["thesis"].append(", ".join(raw))
        else: # Related publications by DUNE Collaborators
            raw = get_related_info(c_entry)
            publications["related"].append(", ".join(raw))
    return publications

def format_query(publications: dict) -> str:
    formatted = "<h1>Documents and Publications</h1><h2>Publications/Documents by the DUNE Collaboration</h2><ul>"
    for item in publications["collab"]:
        formatted += "<li>" + item + "</li>"
    formatted += "</ul><h2>DUNE Theses</h2><ul>"
    for item in publications["thesis"]:
        formatted += "<li>" + item + "</li>"
    formatted += "</ul><h2>Related Publications by DUNE Collaborators</h2><ul>"
    for item in publications["related"]:
        formatted += "<li>" + item + "</li>"
    formatted += "</ul>"
    return formatted

output = make_query("https://inspirehep.net/api/literature?sort=mostrecent&size=188&page=1&q=accelerator_experiments.record.%24ref%3A1346343")
formatted = format_query(output)
print(formatted)