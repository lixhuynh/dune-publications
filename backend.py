# =======
# IMPORTS

import requests

# ============
# PAGE REQUEST

ENTRIES = requests.get("https://inspirehep.net/api/literature?sort=mostrecent&size=1000&page=1&q=accelerator_experiments.record.%24ref%3A1346343").json()["hits"]["hits"]
f_entries = []

for i in range(len(1)): # Iterate through and format entries
    c_entry = ENTRIES[i]
    c_author = c_entry["metadata"]["authors"][0]["first_name"] + " " + c_entry["metadata"]["authors"][0]["last_name"] + " et al., "
    c_title = "\"" + c_entry["metadata"]["titles"][0]["title"] + "\", "
    c_arxiv = "arXiv:" + c_entry["metadata"]["arxiv_eprints"][0]["value"]
    f_entries.append(c_author + c_title + c_arxiv)

print(f_entries)