import os
import json
import sqlite3

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATABASE = os.path.join(
    PROJECT_ROOT,
    "3. Storage",
    "faculty.db"
)

OUTPUT_JSON = os.path.join(
    PROJECT_ROOT,
    "faculty_output.json"
)

# --------------------------------------------------
# DB CONNECTION
# --------------------------------------------------

def get_connection():
    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_contact(cur, fid):
    cur.execute(
        "SELECT phone, email, address FROM contact WHERE faculty_id=?",
        (fid,)
    )
    row = cur.fetchone()
    return dict(row) if row else {}

def get_teaching(cur, fid):
    cur.execute(
        "SELECT subject FROM teaching WHERE faculty_id=?",
        (fid,)
    )
    return [r["subject"] for r in cur.fetchall()]

def get_research(cur, fid):
    cur.execute(
        "SELECT topic FROM research WHERE faculty_id=?",
        (fid,)
    )
    return [r["topic"] for r in cur.fetchall()]

def get_openings(cur, fid):
    cur.execute(
        "SELECT description FROM openings WHERE faculty_id=?",
        (fid,)
    )
    row = cur.fetchone()
    return row["description"] if row else None

def get_publications(cur, fid):
    cur.execute(
        "SELECT type, citation FROM publications WHERE faculty_id=?",
        (fid,)
    )

    pubs = {
        "journal": [],
        "conference": [],
        "other": [],
        "external_links": []
    }

    for r in cur.fetchall():
        pubs.setdefault(r["type"], []).append(r["citation"])

    return pubs

# --------------------------------------------------
# CORE LOGIC (JSON GENERATOR)
# --------------------------------------------------

def generate_faculty_output():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM faculty")
    rows = cur.fetchall()

    if not rows:
        raise RuntimeError("No faculty data found")

    result = []

    for row in rows:
        fid = row["id"]
        result.append({
            "id": fid,
            "name": row["name"],
            "faculty_type": row["faculty_type"],
            "image_url": row["image_url"],

            "education": row["education"],
            "biography": row["biography"],
            "specialization": row["specialization"],
            "profile_url": row["profile_url"],
            "source_listing_url": row["source_listing_url"],
            "contact": get_contact(cur, fid),
            "teaching": get_teaching(cur, fid),
            "research": get_research(cur, fid),
            "openings": get_openings(cur, fid),
            "publications": get_publications(cur, fid)
        })

    conn.close()

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f" faculty_output.json generated at: {OUTPUT_JSON}")


if __name__ == "__main__":
    generate_faculty_output()
