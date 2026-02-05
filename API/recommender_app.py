from fastapi import FastAPI
from pydantic import BaseModel
from recommender.search import search
import json
import os
import subprocess


app = FastAPI(title="Faculty Finder API")

# --------- LOAD SHARED FACULTY DATA ---------
FACULTY_DATA_PATH = os.environ.get("FACULTY_DATA_PATH", "/app/data/faculty_output.json")

with open(FACULTY_DATA_PATH, "r", encoding="utf-8") as f:
    FACULTY_DATA = json.load(f)

FACULTY_BY_ID = {f["id"]: f for f in FACULTY_DATA}

# --------- REQUEST MODEL ---------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    alpha: float = 0.7

# --------- API ENDPOINT ---------
@app.post("/recommend")
def recommend_faculty(req: QueryRequest):
    ranked = search(req.query, top_k=req.top_k, alpha=req.alpha)

    results = []
    for r in ranked:
        faculty = FACULTY_BY_ID.get(r["faculty_id"])
        if faculty:
            results.append({
                **faculty,
                "score": r.get("score", None)
            })

    return {
        "query": req.query,
        "count": len(results),
        "results": results
    }
