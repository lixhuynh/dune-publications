import requests

DUNE_THESES = "https://inspirehep.net/api/literature?sort=mostrecent&size=188&page=1&collaboration=DUNE"

def make_query(page: str) -> list:
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
                theses.append(c_entry["titles"][0]["title"])
    return theses

print(make_query(DUNE_THESES))