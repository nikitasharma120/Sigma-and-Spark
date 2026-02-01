from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List, Dict
import os
import json

# --------------------------------------------------
# APP INIT
# --------------------------------------------------

app = FastAPI(
    title="Faculty API",
    description="Serve structured DA-IICT faculty data",
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "3. Storage", "faculty.db")

# --------------------------------------------------
# DB CONNECTION
# --------------------------------------------------

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {e}"
        )

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_contact(cursor, faculty_id: int) -> Dict:
    cursor.execute(
        "SELECT phone, email, address FROM contact WHERE faculty_id=?",
        (faculty_id,)
    )
    row = cursor.fetchone()
    return dict(row) if row else {}


def get_teaching(cursor, faculty_id: int) -> List[str]:
    cursor.execute(
        "SELECT subject FROM teaching WHERE faculty_id=?",
        (faculty_id,)
    )
    return [r["subject"] for r in cursor.fetchall()]


def get_research(cursor, faculty_id: int) -> List[str]:
    cursor.execute(
        "SELECT topic FROM research WHERE faculty_id=?",
        (faculty_id,)
    )
    return [r["topic"] for r in cursor.fetchall()]


def get_openings(cursor, faculty_id: int) -> str:
    cursor.execute(
        "SELECT description FROM openings WHERE faculty_id=?",
        (faculty_id,)
    )
    row = cursor.fetchone()
    return row["description"] if row else ""


def get_publications(cursor, faculty_id: int) -> Dict[str, List[str]]:
    cursor.execute("""
        SELECT type, citation
        FROM publications
        WHERE faculty_id=?
    """, (faculty_id,))

    pubs = {
        "journal": [],
        "conference": [],
        "other": [],
        "external_links": []
    }

    for r in cursor.fetchall():
        key = r["type"]
        if key not in pubs:
            pubs[key] = []
        pubs[key].append(r["citation"])

    return pubs

# --------------------------------------------------
# CORE FETCH
# --------------------------------------------------

def fetch_all_faculty() -> List[Dict]:
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM faculty")
        faculty_rows = cursor.fetchall()

        results = []

        for row in faculty_rows:
            fid = row["id"]

            record = {
                "id": fid,
                "name": row["name"],
                "faculty_type": row["faculty_type"],
                "education": row["education"],
                "biography": row["biography"],
                "specialization": row["specialization"],
                "profile_url": row["profile_url"],
                "source_listing_url": row["source_listing_url"],
                "contact": get_contact(cursor, fid),
                "teaching": get_teaching(cursor, fid),
                "research": get_research(cursor, fid),
                "openings": get_openings(cursor, fid),
                "publications": get_publications(cursor, fid),
            }

            results.append(record)

        return results

    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {e}"
        )
    finally:
        if conn:
            conn.close()

# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.get("/faculty", response_model=List[Dict])
def get_faculty():
    data = fetch_all_faculty()

    if not data:
        raise HTTPException(
            status_code=404,
            detail="No faculty data found"
        )

    # Optional debug dump
    output_path = os.path.join(BASE_DIR, "faculty_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data
