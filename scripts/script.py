import requests

DUNE_PUBLICATIONS = "https://inspirehep.net/api/literature?sort=mostrecent&size=188&page=1&q=accelerator_experiments.record.%24ref%3A1346343"

def _getID(entry: dict) -> list:
    """
    Gets and formats the links to a particular entry.
    """    
    links = []
    if "arxiv_eprints" in entry:
        id = str(entry["arxiv_eprints"][0]["value"])
        links.append(f"<a href=https://arxiv.org/abs/{id}>arXiv:{id}</a>")
    if "dois" in entry:
        id = str(entry["dois"][0]["value"])
        if "publication_info" in entry:
            pub_info = entry["publication_info"][0]
            place = " ".join([pub_info["journal_title"], pub_info.get("journal_volume", ""),
                              pub_info.get("artid", ""), "(" + str(pub_info.get("year", "")) + ")"])
        else:
            place = f"DOI: {id}"
        links.append(f"<a href=https://doi.org/{id}>{place}</a>")
    return links

def _getCollabInfo(entry: dict) -> list:
    """
    Gets the information for a collaboration entry and enters it into a list.
    """
    # author = entry["first_author"]["full_name"]
    author = "DUNE Collaboration"
    title = f"\"{entry['titles'][0]['title']}\""
    return [author, title] + _getID(entry)

def makeQuery(page: str) -> dict:
    """
    Sorts the entries on a given page into collaborations, theses, and related publications.
    Places them into a format ready for HTML tagging.
    """
    entries = requests.get(page).json()["hits"]["hits"]
    publications = {"Journal Publications": [], "Other Publications": []}
    for i in range(len(entries)): # Iterate through and format entries
        c_entry = entries[i]["metadata"]
        if "conference paper" not in c_entry["document_type"] \
                and "collaborations" in c_entry \
                and "DUNE" in [collab['value'].upper() for collab in c_entry["collaborations"]]:
            raw = _getCollabInfo(c_entry)
            if "doi.org" in raw[-1]: key = "Journal Publications"
            else: key = "Other Publications"
            publications[key].append(", ".join(raw))
    return publications

def getRawHTML(header: str, publications: list) -> str:
    """
    Converts the result of running make_query into a string representing the raw HTML file.
    """
    formatted = f"<h2>{header}</h2>\n<ul>\n"
    for item in publications: formatted += f"\t<li>{item}</li>\n"
    formatted += "</ul>"
    return formatted

output = makeQuery(DUNE_PUBLICATIONS)
pubs = [getRawHTML(key, output[key]) for key in output]
print("\n".join(pubs))