# =======
# IMPORTS

from datetime import datetime
import requests

# ============
# PAGE REQUEST

def get_id(entry: dict):
    pass

def get_collab_info(entry: dict):
    author = "DUNE collaboration"
    title = "\"" + entry["titles"][0]["title"] + "\""
    return [author, title]

def get_thesis_info(entry: dict):
    author = " ".join(entry["authors"][0]["full_name"].split(", ")[::-1])
    title = entry["titles"][0]["title"]
    institution = entry["thesis_info"]["institutions"][0]["name"]
    if institution[-2:] == "U.":
        institution = institution[:-2] + "University"
    date = datetime.strptime(entry["thesis_info"]["date"], "%Y-%m").strftime("%B %Y")
    return [author, title, institution, "Ph.D.", date]

def get_related_info(entry: dict):
    author = " ".join(entry["authors"][0]["full_name"].split(", ")[::-1]) + " et al."
    title = "\"" + entry["titles"][0]["title"] + "\""
    return [author, title]

def make_query(page: str) -> dict:
    entries = requests.get(page).json()["hits"]["hits"]
    publications = {"collab": [], "thesis": [], "related": []}
    for i in range(10): # Iterate through and format entries
        c_entry = entries[i]["metadata"]
        if "collaborations" in c_entry and "DUNE" in c_entry["collaborations"][0]["value"]: # Publication by DUNE Collaboration
            raw = get_collab_info(c_entry)
            publications["collab"].append(", ".join(raw))
        elif "thesis" in c_entry["document_type"]: # DUNE Thesis
            raw = get_thesis_info(c_entry)
            publications["thesis"].append(", ".join(raw))
        else: # Related publications by DUNE Collaborators
            raw = get_related_info(c_entry)
            publications["related"].append(", ".join(raw))
    return publications