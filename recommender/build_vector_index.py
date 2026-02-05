import json
import pickle
from pathlib import Path
from embeddings import build_tfidf

CORPUS_FILE = Path("search_corpus.json")
OUT_DIR = Path("embeddings_index")

def main():
    if not CORPUS_FILE.exists():
        raise FileNotFoundError(f"Corpus file not found: {CORPUS_FILE}")

    # Load corpus safely with UTF-8
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    if not corpus:
        raise ValueError("Corpus is empty. Check your search_corpus.json file.")

    # Extract search texts
    corpus_texts = [entry["search_text"] for entry in corpus]

    # Build TF-IDF vectorizer + matrix
    tfidf_vectorizer, tfidf_matrix = build_tfidf(corpus_texts)

    # Ensure output directory exists
    OUT_DIR.mkdir(exist_ok=True)

    # Save vectorizer
    with open(OUT_DIR / "vectorizer.pkl", "wb") as f:
        pickle.dump(tfidf_vectorizer, f)

    # Save matrix
    with open(OUT_DIR / "tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)

    # Save metadata (trimmed for search use)
    metadata = [
        {
            "faculty_id": entry.get("faculty_id"),
            "name": entry.get("name", ""),
            "search_text": entry.get("search_text", "")
        }
        for entry in corpus
    ]

    with open(OUT_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Embedding index built successfully in {OUT_DIR}")

if __name__ == "__main__":
    main()
