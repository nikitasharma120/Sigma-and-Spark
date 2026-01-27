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
│
├── 5. Analytics/
│   ├── data_exploration.py
│   
├── pipeline.py
├── requirements.txt
└── README.md
```

> **LLM Logs**: All LLM prompts and responses are logged inside a `logs/llm_usage.md` file within the respective folders.

---

## Pipeline Architecture

### 1. Ingestion: (The Scraper)

Crawls faculty listing + profile pages

Extracts raw data: name, type, bio, education, specialization, teaching subjects, publications, contact info, profile URL


**Error Handling:**

* Handles broken links and failed requests
* Skips duplicate faculty profiles
* Continues scraping even if individual profiles fail

---

### 2. Transformation: (The Cleaner)

Clean and normalizes JSON data

Rules:

Replace missing/invalid fields → "Not Available"

Standardize contact info

Ensure lists exist for teaching & publications

---

### 3. Storage: (The Structured Home)

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

REST API endpoint: http://127.0.0.1:8000/faculty

Returns JSON with faculty + contact + teaching + publications

Ready for NLP embeddings and semantic search

---

### 5. Analytics: (Statistics)

Total profiles + Faculty Type Distribution + Missing Value Summary + Avg. text length for biography + Specialization Distribution

Output:

Data exploration json file.

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
## From Recipe to Ingredients:
* If you have the ability to add your own touch and want to add some spices, edit code and run individual files.

 1. Ingestion
```
python "1. Ingestion/scraper.py"
```

2. Transformation
```
python "2. Transformation/cleaner.py"
```

3. Storage
```
python "3. Storage/load_sqlite.py"
```

4. Serving
```
python "4. Serving/app.py"
```

5. Analytics
```
python "5. Analytics/data_exploration.py"
```

---
## Outcomes:

* Clean, structured faculty dataset
* Relational SQLite database
* Modular codebase
* FastAPI ready for NLP
* Clear documentation and schema
* Data exploration stats
---


Built by **Sigma & Spark**: where B.Sc. Statistics meets Leveled Sparks 

Srishti Lamba: 202518003 
*Catching quirks which others miss*

Nikita Sharma: 202518038
*If disciplining data was a task*
