import dune_pubs

DUNE_PUBLICATIONS = "https://inspirehep.net/api/literature?sort=mostrecent&size=188&page=1&q=accelerator_experiments.record.%24ref%3A1346343"

def process(item: dict) -> str:
    """
    Returns the publication, formatted.
    """
    if "conference paper" not in item["document_type"] and "collaborations" in item and "DUNE" in [c["value"].upper() for c in item["collaborations"]]:
        author = "DUNE Collaboration"
        title = f"\"{item['titles'][0]['title']}\""
        links = get_links(item)
        return ", ".join([author, title] + links)
    else:
        return False

def assign_key(item: dict) -> str:
    """
    Decides whether the item is a journal publication or miscellaneous.
    """
    links = get_links(item)
    if links and "doi.org" in links[-1]: return "Journal Publications"
    return "Other Publications"

def get_links(entry: dict) -> list:
    """
    Helper for process(). Gets and formats the links to a particular entry.
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

def write_publications(filename: str, mode: str):
    q = dune_pubs.make_query(DUNE_PUBLICATIONS, process=process, assign_key=assign_key)
    with open(filename, mode=mode) as output:
        print(dune_pubs.get_raw_html("Journal Publications", q["Journal Publications"]), file=output)
        print(dune_pubs.get_raw_html("Other Publications", q["Other Publications"]), file=output)

if __name__ == "__main__":
    write_publications("./publications.html", "w")
    print("publications.html created successfully.")