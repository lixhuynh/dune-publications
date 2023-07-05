# =======
# IMPORTS

import requests

# ============
# PAGE REQUEST

def get_id(entry: dict) -> list:
    """
    Gets and formats the links to a particular entry.
    """    
    links = []
    if "arxiv_eprints" in entry:
        id = str(entry["arxiv_eprints"][0]["value"])
        links.append("<a href=https://arxiv.org/abs/" + id + ">arXiv:" + id + "</a>")
    if "dois" in entry:
        id = str(entry["dois"][0]["value"])
        if "publication_info" in entry:
            pub_info = entry["publication_info"][0]
            place = " ".join([pub_info["journal_title"], pub_info.get("journal_volume", ""),
                            pub_info.get("artid", ""), "(" + str(pub_info.get("year", "")) + ")"])
        else:
            place = "DOI: " + id
        links.append("<a href=https://doi.org/" + id + ">" + place + "</a>")
    return links

def get_collab_info(entry: dict) -> list:
    """
    Gets the information for a collaboration entry and enters it into a list.
    """
    author = "DUNE collaboration"
    title = "\"" + entry["titles"][0]["title"] + "\""
    return [author, title] + get_id(entry)

def retrieve_metadata(page: str) -> dict:
    """
    Returns the metadata for a single entry.
    """
    entry = requests.get(page).json()["metadata"]
    return entry

def make_query(page: str) -> list:
    """
    Sorts the entries on a given page into collaborations, theses, and related publications.
    Places them into a format ready for HTML tagging.
    """
    entries = requests.get(page).json()["hits"]["hits"]
    publications = []
    for i in range(len(entries)): # Iterate through and format entries
        c_entry = entries[i]["metadata"]
        if "conference paper" not in c_entry["document_type"] \
            and "collaborations" in c_entry \
                and "DUNE" in [collab['value'].upper() for collab in c_entry["collaborations"]]:
            raw = get_collab_info(c_entry)
            publications.append(", ".join(raw))
    return publications

def get_raw_html(publications: dict) -> str:
    """
    Converts the result of running make_query into a string representing the raw HTML file.
    """
    formatted = "<h2>Publications/Documents by the DUNE Collaboration</h2><ul>"
    for item in publications:
        formatted += "<li>" + item + "</li>"
    formatted += "</ul>"
    return formatted

def format_html(page_content: str, page_title: str, template_name: str) -> str:
    """
    Takes the raw HTML and puts it into the given template.
    """
    with open(template_name, "r") as file:
        template = file.read()
    title_start = template.find("entry-title") + 13
    title_end = template.find("</h1>", title_start)
    content_start = template.find("entry-content", title_end) + 15
    content_end = template.find("</div>", content_start)
    formatted = template[:title_start] + page_title + template[title_end:content_start] + page_content + template[content_end:]
    return formatted

output = make_query("https://inspirehep.net/api/literature?sort=mostrecent&size=188&page=1&q=accelerator_experiments.record.%24ref%3A1346343")
raw = get_raw_html(output)
formatted = format_html(raw, "Documents and Publications", "template.html")
print(formatted)