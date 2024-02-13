from datetime import datetime
from re import match
import dune_pubs

DUNE_THESES = "https://inspirehep.net/api/literature?sort=mostrecent&size=200&page=1&q=accelerator_experiments.record.%24ref%3A1346343"

def process(item: dict) -> str:
    if "report_numbers" in item:
        found_match = False
        for num in item["report_numbers"]:
            if num["value"].startswith("FERMILAB-THESIS"):
                found_match = True
                break
        if found_match:
            return format_entry(item)
    else:
        return False

def format_entry(entry: dict) -> str:
    """
    Helper for process(). Formats an entry.
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
    Helper for format_entry(). Formats a publication date.
    """
    if match("\d{4}-\d{2}", input_date): # YYYY-MM
        date = datetime.strptime(input_date, '%Y-%m').strftime('%B %Y')
    else:
        date = input_date
    return date

def write_theses(filename: str, mode: str):
    q = dune_pubs.make_query(DUNE_THESES, process=process, assign_key=lambda x: "DUNE Theses")
    with open(filename, mode=mode) as output:
        print(dune_pubs.get_raw_html("DUNE Theses", q["DUNE Theses"]), file=output)

if __name__ == "__main__":
    write_theses("./theses.html", "w")
    print("theses.html created successfully.")