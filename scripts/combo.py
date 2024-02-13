from publications import write_publications
from theses import write_theses

if __name__ == "__main__":
    write_publications("./combo.html", "w")
    write_theses("./combo.html", "a")
    print("combo.html created successfully.")