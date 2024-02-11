import re
import requests
from datetime import datetime

DUNE_THESES = "https://inspirehep.net/api/literature?sort=mostrecent&size=200&page=1&q=accelerator_experiments.record.%24ref%3A1346343"

def make_query(page: str) -> list:
    """
    Makes a request to INSPIRE for the entries.
    """
    entries = requests.get(page).json()["hits"]["hits"]
    theses = []
    for i in range(len(entries)):
        c_entry = entries[i]["metadata"]
        if "report_numbers" in c_entry:
            found_match = False
            for num in c_entry["report_numbers"]:
                if num["value"].startswith("FERMILAB-THESIS"):
                    found_match = True
                    break
            if found_match:
                theses.append(format_entry(c_entry))
    return theses

def format_entry(entry: dict) -> str:
    """
    Formats an entry.
    """
    name = f'{entry["first_author"]["first_name"]} {entry["first_author"]["last_name"]}'
    title = entry["titles"][0]["title"]
    url = entry["urls"][0]["value"]
    degree = entry["thesis_info"]["degree_type"]
    university = entry["thesis_info"]["institutions"][0]["name"]
    date = format_date(entry["thesis_info"]["date"])

    return f'{name}, <a href="{url}">{title}</a>, {university}, {degree}, {date}'

def format_date(input_date: str) -> str:
    """
    Formates a publication date.
    """
    if re.match("\d{4}-\d{2}", input_date): # YYYY-MM
        date = datetime.strptime(input_date, '%Y-%m').strftime('%B %Y')
    else:
        date = input_date
    return date

def get_raw_html(header: str, items: list) -> str:
    """
    Converts the result of running make_query into a string representing the raw HTML file.
    """
    formatted = f"<h2>{header}</h2>\n<ul>\n"
    for item in items: formatted += f"\t<li>{item}</li>\n"
    formatted += "</ul>"
    return formatted

with open("./theses.html", mode="w") as output:
    print(get_raw_html("DUNE Theses", make_query(DUNE_THESES)), file=output)