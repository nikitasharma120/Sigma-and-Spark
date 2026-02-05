# Faculty Data Pipeline: Project 1

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/srishti7103/Sigma-and-Spark&envs=API_URL,FACULTY_DATA_PATH)
> **[LINK TO DEPLOYED APP](https://sigma-and-spark-production-dedf.up.railway.app/)** 👈 Click here to see the live app!

## Project Summary:

This project implements an **end-to-end data engineering pipeline** to crawl, clean, store, and serve faculty information from DAIICT university website. The final objective is to prepare a **clean, structured dataset** that can later be used for **semantic search and NLP applications**.
All file paths are dynamic to project to ensure flexibility to collaborators.

---

## Folder Structure

```
Sigma-and-Spark/
│
├── 1. Ingestion/
│   └── scraper.py
│
├── 2. Transformation/
│   └── cleaner.py
│
├── 3. Storage/
│   ├── load_sqlite.py
│   └── faculty.db
│
├── 4. Serving/
│   ├── app.py
│   └── execute_output.py  <-- Generates JSON for API
│
├── analytics/
│   ├── data_exploration.py
│   └── build_search_corpus.py
│
├── API/
│   ├── recommender_app.py <-- FastAPI Backend
│   └── requirements.txt
│
├── recommender/
│   ├── build_vector_index.py
│   ├── embeddings.py
│   └── search.py
│
├── ui/
│   ├── templates/
│   ├── static/
│   ├── ui.py              <-- Flask Frontend
│   └── requirements.txt
│
├── docker/
│   ├── Dockerfile.combined
│   └── docker-compose.yml
│
├── pipeline.py
├── requirements.txt
├── RAILWAY_DEPLOY.md      <-- Deployment Guide
├── llm_usage.md
└── README.md
```

> **LLM Usage**: For a detailed breakdown of which scripts were generated using LLM (ChatGPT) including the key prompts used, please refer to [llm_usage.md](llm_usage.md).

---

## Pipeline Architecture

### 1. Ingestion: (The Scraper)
Crawls faculty listing + profile pages.
Extracts raw data: name, type, bio, education, specialization, teaching subjects, research areas, publications (journals, conferences, others, external links), contact info, profile URL.

**Error Handling:**
* Handles broken links and failed requests
* Skips duplicate faculty profiles
* Continues scraping even if individual profiles fail

---

### 2. Transformation: (The Cleaner)
Clean and normalizes JSON data.
**Rules:**
* Replace missing/invalid fields → "Not Available"
* Standardize contact info
* Ensure lists exist for teaching & publications

---

### 3. Storage: (The Structured Home)
**Database:** `faculty.db` (SQLite).
Stores normalized data in relational tables: `faculty`, `contact`, `teaching`, `research`, `openings`, `publications`.

---

### 4. Serving: (The Hand-off)
REST API endpoint: `http://localhost:8000/faculty` (Basic extraction).
**Enhanced Serving:**
*   `execute_output.py`: Extracts all data from `faculty.db` and generates a flat `faculty_output.json`.
*   **Purpose**: This JSON is the critical data source for the Recommender System and API.

---

### 5. Analytics & Search Prep
*   **Analytics**: `data_exploration.py` generates statistics (Faculty Type Distribution, Missing Values, Text Lengths).
*   **Search Corpus**: `build_search_corpus.py` processes `faculty_output.json` to create `search_corpus.json`.
    *   It flattens rich text fields (bio, research, publications) into a single "searchable" string for each faculty member.

---

### 6. Recommender System
*   **Build Index**: `build_vector_index.py` reads `search_corpus.json`, computes TF-IDF embeddings, and saves the vector index.
*   **Search Engine**: `search.py` performs cosine similarity search to find relevant faculty based on user queries.

---

### 7. API Layer: (The Brain)
*   **Framework**: FastAPI
*   **File**: `API/recommender_app.py`
*   **Function**: Loads the faculty data and vector index. Exposes the `/recommend` endpoint.
*   **Docs**: Auto-generated Swagger UI at `http://localhost:8000/docs`.

---

### 8. User Interface: (The Face)
*   **Framework**: Flask
*   **File**: `ui/ui.py`
*   **Function**: A clean web interface where users can search for faculty. It communicates with the API to fetch results.

---

### 9. Dockerization
*   **Containerization**: We use a combined Dockerfile (`docker/Dockerfile.combined`) to package both the API and UI.
*   **Orchestration**: `docker/docker-compose.yml` orchestrates the services, networking, and volume mounts.

---

## How to Run the Pipeline (Step-by-Step)

### Prerequisites
*   Python 3.9+
*   Git

### 1. Clone & Install
```bash
git clone https://github.com/<username>/Sigma-and-Spark.git
cd Sigma-and-Spark
pip install -r requirements.txt
```

### 2. Run Core Pipeline (Steps 1-4)
This script runs Ingestion, Transformation, Storage, and the basic Serving app sequentially.
```bash
python pipeline.py
```

### 3. Generate Output JSON (Critical)
Prepare the data for the API.
```bash
python "4. Serving/execute_output.py"
```

### 4. Run Analytics (Optional)
```bash
python analytics/data_exploration.py
```

### 5. Build Search Corpus
Prepare the text data for the search engine.
```bash
python analytics/build_search_corpus.py
```

### 6. Build Vector Index
Create the TF-IDF index for the recommender.
```bash
python recommender/build_vector_index.py
```

### 7. Start the API
Run the FastAPI backend.
```bash
uvicorn API.recommender_app:app --reload --port 8000
```
> **Check:** Open `http://localhost:8000/docs` to see the API docs.

### 8. Start the UI
Open a **new terminal**, set the API URL, and run the Flask app.
```bash
# Windows (PowerShell)
$env:API_URL="http://127.0.0.1:8000/recommend"
python ui/ui.py

# Mac/Linux
export API_URL="http://127.0.0.1:8000/recommend"
python ui/ui.py
```
> **Access:** Open `http://localhost:5000` to use the application.

---

## Alternative: Run with Docker (Recommended)

Skip the manual steps above and run everything with one command.

```bash
docker-compose -f docker/docker-compose.yml up --build
```
*   **UI**: `http://localhost:5000`
*   **API**: `http://localhost:8000/docs`

---

## Deployment

We deploy to **Railway** using a Dockerfile.
For detailed deployment instructions, please read **[RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)**.

---

## Credits
Built by **Sigma & Spark**: where B.Sc. Statistics meets Leveled Sparks 

**Srishti Lamba**: 202518003 
*Catching quirks which others miss*

**Nikita Sharma**: 202518038
*If disciplining data was a task*
