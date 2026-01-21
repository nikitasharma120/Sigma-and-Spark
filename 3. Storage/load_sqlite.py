import sqlite3
import json
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_FILE = os.path.join(PROJECT_ROOT, "faculty_cleaned.json")
DB_PATH = os.path.join(PROJECT_ROOT, "3. Storage", "faculty.db")


def load_faculty_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON root must be a list of faculty entries")
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"format error: {e}")
        return []
    except ValueError as e:
        print(f"Data validation error: {e}")
        return []

def create_schema(conn):
    cursor = conn.cursor()
    try:
        cursor.executescript("""
        DROP TABLE IF EXISTS faculty;
        DROP TABLE IF EXISTS contact;
        DROP TABLE IF EXISTS teaching;
        DROP TABLE IF EXISTS publications;

        CREATE TABLE faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            education TEXT,
            biography TEXT,
            specialization TEXT,
            profile_url TEXT
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

        CREATE TABLE publications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id INTEGER,
            publication TEXT,
            FOREIGN KEY (faculty_id) REFERENCES faculty(id)
        );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Schema creation error: {e}")
        conn.rollback()

def insert_faculty_data(conn, cleaned_data):
    cursor = conn.cursor()
    try:
        for entry in cleaned_data:
            cursor.execute("""
            INSERT INTO faculty (name, education, biography, specialization, profile_url)
            VALUES (?, ?, ?, ?, ?)
            """, (
                entry.get("name"),
                entry.get("education"),
                entry.get("biography"),
                entry.get("specialization"),
                entry.get("profile_url")
            ))
            faculty_id = cursor.lastrowid

            contact = entry.get("contact", {})
            cursor.execute("""
            INSERT INTO contact (faculty_id, phone, email, address)
            VALUES (?, ?, ?, ?)
            """, (
                faculty_id,
                contact.get("phone"),
                contact.get("email"),
                contact.get("address")
            ))

            for subject in entry.get("teaching", []):
                cursor.execute("INSERT INTO teaching (faculty_id, subject) VALUES (?, ?)", (faculty_id, subject))

            for pub in entry.get("publications", []):
                cursor.execute("INSERT INTO publications (faculty_id, publication) VALUES (?, ?)", (faculty_id, pub))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Insert failed: {e}")
        conn.rollback()

def main():
    cleaned_data = load_faculty_data(DATA_FILE)
    if not cleaned_data:
        print("No data.")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            create_schema(conn)
            insert_faculty_data(conn, cleaned_data)
            print("Faculty data stored in db")
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    main()
