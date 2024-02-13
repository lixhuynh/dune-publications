import requests

def make_query(page: str, process, assign_key) -> list:
    """
    Makes a request to INSPIRE for the entries.
    """
    entries = requests.get(page).json()["hits"]["hits"]
    items = {}
    for entry in entries:
        processed = process(entry["metadata"])
        if processed:
            key = assign_key(entry["metadata"])
            items[key] = items.get(key, []) + [processed]
    return items

def get_raw_html(header: str, items: list) -> str:
    """
    Converts a page query into a raw HTML file.
    """
    formatted = f"<h2>{header}</h2>\n<ul>\n"
    for item in items:
        formatted += f"\t<li>{item}</li>\n"
    formatted += "</ul>"
    return formatted