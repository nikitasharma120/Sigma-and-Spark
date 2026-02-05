import json
from pathlib import Path

INPUT_FILE = Path("faculty_output.json")
OUTPUT_FILE = Path("search_corpus.json")

def build_search_text(f):
    # Flatten teaching subjects
    teaching = " ".join(f.get("teaching", []))

    # Flatten publications (journal, conference, other)
    pubs = []
    publications = f.get("publications", {})
    for key in ["journal", "conference", "other"]:
        pubs.extend(publications.get(key, []))
    publications_text = " ".join(pubs)

    # Flatten research topics
    research = " ".join(f.get("research", []))

    fields = [
        f.get("specialization", ""),
        f.get("education", ""),
        f.get("biography", ""),
        teaching,
        research,
        publications_text,
        str(f.get("openings", ""))  # handle null safely
    ]
    return " ".join(fields).lower()

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    corpus = []
    for f in data:
        corpus.append({
            "faculty_id": f.get("id"),
            "name": f.get("name", ""),
            "search_text": build_search_text(f),
            "raw": f
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
