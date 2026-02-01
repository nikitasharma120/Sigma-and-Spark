import sqlite3
import json
import os

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_FILE = os.path.join(PROJECT_ROOT, "faculty_cleaned.json")
DB_PATH = os.path.join(PROJECT_ROOT, "3. Storage", "faculty.db")

# --------------------------------------------------
# LOAD JSON
# --------------------------------------------------

def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("faculty_cleaned.json must contain a list")
        return data

# --------------------------------------------------
# SCHEMA
# --------------------------------------------------

def create_schema(conn):
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS faculty;
    DROP TABLE IF EXISTS contact;
    DROP TABLE IF EXISTS teaching;
    DROP TABLE IF EXISTS research;
    DROP TABLE IF EXISTS openings;
    DROP TABLE IF EXISTS publications;

    CREATE TABLE faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        faculty_type TEXT,
        education TEXT,
        biography TEXT,
        specialization TEXT,
        profile_url TEXT,
        source_listing_url TEXT
    );

    CREATE TABLE contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        phone TEXT,
        email TEXT,
        address TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );

    CREATE TABLE teaching (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        subject TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );

    CREATE TABLE research (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        topic TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );

    CREATE TABLE openings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        description TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );

    CREATE TABLE publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        type TEXT,
        citation TEXT,
        FOREIGN KEY (faculty_id) REFERENCES faculty(id)
    );
    """)

    conn.commit()

# --------------------------------------------------
# INSERT LOGIC
# --------------------------------------------------

def insert_data(conn, records):
    cur = conn.cursor()

    for r in records:
        # ---- faculty ----
        cur.execute("""
        INSERT INTO faculty (
            name,
            faculty_type,
            education,
            biography,
            specialization,
            profile_url,
            source_listing_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("name"),
            r.get("faculty_type"),
            r.get("education"),
            r.get("biography"),
            r.get("specialization"),
            r.get("profile_url"),
            r.get("source_listing_url")
        ))

        faculty_id = cur.lastrowid

        # ---- contact ----
        contact = r.get("contact", {})
        cur.execute("""
        INSERT INTO contact (faculty_id, phone, email, address)
        VALUES (?, ?, ?, ?)
        """, (
            faculty_id,
            contact.get("phone"),
            contact.get("email"),
            contact.get("address")
        ))

        # ---- teaching ----
        for t in r.get("teaching", []):
            cur.execute(
                "INSERT INTO teaching (faculty_id, subject) VALUES (?, ?)",
                (faculty_id, t)
            )

        # ---- research ----
        for topic in r.get("research", []):
            cur.execute(
                "INSERT INTO research (faculty_id, topic) VALUES (?, ?)",
                (faculty_id, topic)
            )

        # ---- openings ----
        if r.get("openings") and r["openings"] != "Not Available":
            cur.execute(
                "INSERT INTO openings (faculty_id, description) VALUES (?, ?)",
                (faculty_id, r["openings"])
            )

        # ---- publications ----
        pubs = r.get("publications", {})
        for pub_type, entries in pubs.items():
            for citation in entries:
                cur.execute("""
                INSERT INTO publications (faculty_id, type, citation)
                VALUES (?, ?, ?)
                """, (
                    faculty_id,
                    pub_type,
                    citation
                ))

    conn.commit()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError("faculty_cleaned.json not found")

    records = load_data(DATA_FILE)

    with sqlite3.connect(DB_PATH) as conn:
        create_schema(conn)
        insert_data(conn, records)

    print(f"Loaded {len(records)} faculty records into SQLite")

# --------------------------------------------------

if __name__ == "__main__":
    main()
