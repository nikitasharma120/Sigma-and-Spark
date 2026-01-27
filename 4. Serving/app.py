from fastapi import FastAPI, HTTPException #for error handling 
import sqlite3 #db connectt
from typing import List, Dict #structure mention
import json

app = FastAPI(title="Faculty API", description="Serve faculty data")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "3. Storage", "faculty.db")

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row #row for dicts
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Db connection failed: {e}")


def get_contact(cursor, faculty_id: int) -> Dict:
    cursor.execute("SELECT phone, email, address FROM contact WHERE faculty_id=?", (faculty_id,))
    row = cursor.fetchone()
    return dict(row) if row else {}


def get_teaching(cursor, faculty_id: int) -> List[str]:
    cursor.execute("SELECT subject FROM teaching WHERE faculty_id=?", (faculty_id,))
    return [r["subject"] for r in cursor.fetchall()]


def get_publications(cursor, faculty_id: int) -> List[str]:
    cursor.execute("SELECT publication FROM publications WHERE faculty_id=?", (faculty_id,))
    return [r["publication"] for r in cursor.fetchall()]


def fetch_all_faculty() -> List[Dict]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty")
        faculty_rows = cursor.fetchall()

        results = []
        for row in faculty_rows:
            faculty_id = row["id"]
            results.append({"id": faculty_id,
                "name": row["name"],
                "faculty_type":row["faculty_type"],
                "education": row["education"],
                "biography": row["biography"],
                "specialization": row["specialization"],
                "profile_url": row["profile_url"],
                "contact": get_contact(cursor, faculty_id),
                "teaching": get_teaching(cursor, faculty_id),
                "publications": get_publications(cursor, faculty_id)})

        return results
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


@app.get("/faculty", response_model=List[Dict])
def get_faculty():
    data = fetch_all_faculty()
    if not data:
        raise HTTPException(status_code=404, detail="No faculty data found, handle your code better!")

    output_path = os.path.join(BASE_DIR, "faculty_output.json") 
    with open(output_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False) 
    return data