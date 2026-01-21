# Faculty Data Pipeline: Project 1

## Project Summary:

This project implements an **end-to-end data engineering pipeline** to crawl, clean, store, and serve faculty information from DAIICT university website. The final objective is to prepare a **clean, structured dataset** that can later be used for **semantic search and NLP applications**.
All file paths are dynamic to project to ensure flexibility to collaborators.
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
│   ├── logs/
│   │   └── llm_usage.md
├── pipeline.py
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

**Error Handling:**

* Handles broken links and failed requests
* Skips duplicate faculty profiles
* Continues scraping even if individual profiles fail

---

### 2. Transformation: (The Cleaner)

**Responsibility:**

* Clean messy scraped JSON data
* Normalize missing and null fields
* Remove HTML noise

**Rules:**

* Replaces empty or invalid fields with `"Not Available"`
* Standardizes contact information
* Ensures lists exist for teaching and publications

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
* JSON for downstream NLP and embedding tasks
* Returns all faculty records with contact, teaching, and publication data

---

## How to Run the Pipeline

### 1. Clone the repository:

```
```bash
git clone https://github.com/<username>/Sigma-and-Spark.git
cd Sigma-and-Spark
```

### 2. Run the pipeline:

```
python pipeline.py
```

### 3. Access application on:

```
http://127.0.0.1:8000/faculty
```

### NOTE: [Install Dependencies if not]

```
pip install -r requirements.txt
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
