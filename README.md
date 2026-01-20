# Faculty Data Pipeline: Project 1

## Project Summary:

This project implements an **end-to-end data engineering pipeline** to crawl, clean, store, and serve faculty information from DAIICT university website. The final objective is to prepare a **clean, structured dataset** that can later be used for **semantic search and NLP applications**.
All file paths are dynamic relative to project to ensure flexibility to collaborators.
---


## Folder Structure

```
Sigma-and-Spark/
│
├── 1. Ingestion/
│   ├── scraper.py
│   ├── logs/
│   │   └── llm_usage.md
│
├── 2. Transformation/
│   ├── cleaner.py
│   ├── logs/
│   │   └── llm_usage.md
│
├── 3. Storage/
│   ├── load_sqlite.py
│   ├── faculty.db
│
├── 4. Serving/
│   ├── app.py
│   ├── llm.md
│
├── Data/
│   ├── faculty_profiles.json
│   ├── faculty_cleaned.json
│
├── requirements.txt
└── README.md
```

> **LLM Logs**: All LLM prompts and responses are logged inside a `logs/llm_usage.md` file within the respective folders.

---

## Pipeline Architecture

### 1. Ingestion: (The Scraper)

**Responsibility:**

* Crawl multiple faculty listing pages
* Visit individual faculty profile pages
* Extract raw, unstructured data

**Data Extracted:**

* Name
* Faculty type
* Biography
* Education
* Specialization
* Teaching subjects
* Publications
* Contact details (email, phone, address)
* Profile URL

**Output:**

* `faculty_profiles.json`

**Error Handling:**

* Handles broken links and failed requests
* Skips duplicate faculty profiles
* Continues scraping even if individual profiles fail

---

### 2. Transformation: (The Cleaner)

**Responsibility:**

* Clean messy scraped JSON data
* Normalize missing, null, or malformed fields
* Remove HTML noise and placeholder text

**Rules:**

* Replaces empty or invalid fields with `"Not Available"`
* Standardizes contact information
* Ensures lists exist for teaching and publications

**Input:**

* `faculty_profiles.json`

**Output:**

* `faculty_cleaned.json`

---

### 3. Storage: (The Structured Home)

**Responsibility:**

* Design and create a relational SQLite schema
* Persist cleaned data into structured tables

**Database:** `faculty.db`

### Database Schema

**faculty**

* id (PK)
* name
* education
* biography
* specialization
* profile_url

**contact**

* id (PK)
* faculty_id (FK)
* phone
* email
* address

**teaching**

* id (PK)
* faculty_id (FK)
* subject

**publications**

* id (PK)
* faculty_id (FK)
* publication

---

### 4. Serving: (The Hand-off)

**Responsibility:**

* Show faculty data via REST API
* Serve structured JSON for downstream NLP and embedding tasks

**Visible at:**

```
GET /faculty
```

* Returns all faculty records with contact, teaching, and publication data

---

## How to Run the Pipeline

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Run Scraper

```
python "1. Ingestion/scraper.py"
```

### 3. Run Cleaner

```
python "2. Transformation/cleaner.py"
```

### 4. Load Data into SQLite

```
python "3. Storage/load_sqlite.py"
```

### 5. Start API Server

```
uvicorn --reload --app-dir "4.Serving" app:app
```

Visit:

```
http://127.0.0.1:8000/faculty
```

---

## Outcomes:

* Clean, structured faculty dataset
* Relational SQLite database
* Modular codebase
* FastAPI ready for NLP
* Clear documentation and schema
---


Built by **Sigma & Spark**: where B.Sc. Statistics meets Leveled Sparks 

Srishti Lamba: 202518003 
*Catching quirks which others miss*

Nikita Sharma: 202518038
*If disciplining data was a task*
