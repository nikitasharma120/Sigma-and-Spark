import pickle, json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load vectorizer and matrix
with open("embeddings_index/vectorizer.pkl", "rb") as f:
    VEC = pickle.load(f)

with open("embeddings_index/tfidf_matrix.pkl", "rb") as f:
    MAT = pickle.load(f)

# Load metadata safely with UTF-8
with open("embeddings_index/metadata.json", "r", encoding="utf-8") as f:
    META = json.load(f)

def search(query, top_k=5, alpha=0.7):
    q = query.strip().lower()

    # 1. Exact faculty name match
    for entry in META:
        if entry["name"].lower() == q:
            return [{
                "faculty_id": entry["faculty_id"],
                "name": entry["name"],
                "score": 1.0,
                "search_text": entry["search_text"]
            }]

    # 2. Partial faculty name match (substring)
    name_matches = [entry for entry in META if q in entry["name"].lower()]
    if name_matches:
        return [{
            "faculty_id": entry["faculty_id"],
            "name": entry["name"],
            "score": 0.95,  # high confidence for name match
            "search_text": entry["search_text"]
        } for entry in name_matches]

    # 3. Fall back to TF-IDF similarity
    q_vec = VEC.transform([q])
    cosine_scores = cosine_similarity(q_vec, MAT)[0]
    keyword_scores = (MAT @ q_vec.T).toarray().flatten()
    final_scores = alpha * cosine_scores + (1 - alpha) * keyword_scores

    top_idx = np.argsort(final_scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        results.append({
            "faculty_id": META[i]["faculty_id"],
            "name": META[i]["name"],
            "score": round(float(final_scores[i]), 3),
            "search_text": META[i]["search_text"]
        })
    return results
