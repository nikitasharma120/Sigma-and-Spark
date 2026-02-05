# LLM Usage Log

This file records all interactions with the Large Language Model (LLM) for  
**Project: DA-IICT Faculty Data Pipeline & Search System**.

Each entry documents **human analysis notes**, the **prompt**, and the **complete LLM response (code)** to ensure transparency, reproducibility, and academic compliance.

---

## Entry 1: Data Ingestion

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Scrape faculty profiles from the university website.  
- **Context:** The website has multiple listing pages (faculty, adjunct, etc.) and individual profile pages. We need to handle broken links, missing images, and unstructured text lists.

### Prompt

```text
You are a Web Scraping Expert.
Write a Python script using `requests` and `BeautifulSoup`.

1. URLs to scrape:
   - https://www.daiict.ac.in/faculty
   - https://www.daiict.ac.in/adjunct-faculty
   - ... (other categories)

2. Logic:
   - Crawl the listing page to find all faculty profile links.
   - For each profile link, visit the page and extract:
     - Name, Image URL, Education
     - Contact info (Phone, Email, Address)
     - Biography (text)
     - Sections: Specialization, Teaching, Research, Openings, Publications (Journal/Conference/Other)
   - Store everything in `faculty_profiles.json`.
   - Use `logging` to track progress.
```

### Response (Generated Code)

*(See `1. Ingestion/scraper.py` for full output)*

---

## Entry 2: Data Transformation

- **Date:** 2026-01-16  
- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Clean and transform scraped JSON.  
- **Context:** Normalizing strings, separating mixed education/biography fields, and standardizing contact objects.

### Prompt

```text
You are a Data Transformation Assistant.
Generate Python code to clean faculty profile data stored in JSON.

Input: Data/faculty_profiles.json
Output: Data/faculty_cleaned.json

Cleaning rules:
- Normalize whitespace.
- Replace null/empty with "Not Available" or [].
- Separate education from biography if mixed.
- Merge phone, email, address into a "contact" object.
- Remove HTML tags.
- Output strict JSON schema.
```

### Response (Generated Code)

*(See `2. Transformation/cleaner.py` for full output)*

---

## Entry 3: Data Storage

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Load cleaned JSON into a Relational Database.  
- **Context:** We need a SQLite database `faculty.db` with normalized tables: `faculty`, `contact`, `teaching`, `research`, `openings`, `publications`.

### Prompt

```text
Write a Python script to load `faculty_cleaned.json` into a SQLite database `3. Storage/faculty.db`.

Requirements:
1. Create Tables:
   - faculty (id, name, type, bio, etc.)
   - contact (faculty_id, phone, email...)
   - teaching, research, openings (linked by faculty_id)
   - publications (faculty_id, type, citation)
2. Iterate through the JSON and insert data using FK relationships.
3. Use `sqlite3` library.
```

### Response (Generated Code)

*(See `3. Storage/load_sqlite.py` for full output)*

---

## Entry 4: Serving API (Basic)

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Serve the raw data via REST API.  
- **Context:** A simple endpoint to get all faculty details including their joined relational data.

### Prompt

```text
Create a FastAPI app (`app.py`) to serve the data from `faculty.db`.

Endpoint: `GET /faculty`
Logic:
- Connect to SQLite.
- Fetch all faculty rows.
- For each faculty, fetch their related contact, teaching, research, etc. from other tables.
- Return a nested JSON response.
- On startup, run a script `execute_output.py`.
```

### Response (Generated Code)

*(See `4. Serving/app.py` for full output)*

---

## Entry 5: Search Corpus Preparation

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Prepare data for the Recommendation Engine.  
- **Context:** We need a flattened text field for TF-IDF vectorization.

### Prompt

```text
Write a script `execute_output.py` that:
1. Reads `faculty_cleaned.json`.
2. Creates a new field `search_text` for each user by joining:
   - Name
   - Specialization
   - Research Areas
   - Teaching Subjects
3. Saves this optimized list to `faculty_output.json` for the Recommender system.
```

### Response (Generated Code)

*(See `4. Serving/execute_output.py` for full output)*

---

## Entry 5.5: Search Corpus Construction

- **Tool Used:** ChatGPT (LLM)
- **Purpose:** Flatten structured faculty data into a single text block for search.
- **Context:** The recommender needs a single string per faculty (bio + research + pubs) to calculate TF-IDF. This script bridges the gap between the structured JSON and the search engine.

### Prompt

```text
Write a script `analytics/build_search_corpus.py` that:
1. Reads `faculty_output.json`.
2. For each faculty, combines:
   - Specialization, Education, Biography
   - All Teaching subjects
   - All Research topics
   - All Publications (Journal, Conference, Other)
   - Openings description
3. Lowercases and joins them into a single `search_text` field.
4. Saves to `search_corpus.json`.
```

### Response (Generated Code)

*(See `analytics/build_search_corpus.py` for full output)*

---

## Entry 6: Recommender System (Embeddings & Search)

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Build the Semantic Search Engine.  
- **Context:** We need to find similar faculty based on user queries using TF-IDF and Cosine Similarity.

### Prompt

```text
I need to build a search engine. Help me write 3 scripts:

1. `embeddings.py`:
   - Function `generate_tfidf_embeddings(corpus)`.
   - Use `TfidfVectorizer` from sklearn.
   - Return vectorizer and matrix.

2. `build_vector_index.py`:
   - Load `faculty_output.json`.
   - Call the embedding function.
   - Save `vectorizer.pkl` and `tfidf_matrix.pkl` using pickle.

3. `search.py`:
   - Function `search(query, top_k)`.
   - Load pickles.
   - Transform query to vector.
   - Calculate Cosine Similarity.
   - Return top k matching results.
```

### Response (Generated Code)

*(See `recommender/` folder for full output)*

---

## Entry 7: Recommender API

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Serve the search engine via API.  
- **Context:** An endpoint that accepts a query and returns ranked results.

### Prompt

```text
Create `API/recommender_app.py` using FastAPI.

- Load `faculty_output.json` into memory for fast lookup.
- Endpoint `POST /recommend`:
  - Body: { "query": "str" }
  - Logic: Call `search(query)` from the recommender module.
  - Return: List of faculty details with similarity scores.
```

### Response (Generated Code)

*(See `API/recommender_app.py` for full output)*

---

## Entry 8: User Interface

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Frontend for the search engine.  
- **Context:** A user-friendly web page to query the system.

### Prompt

```text
Build a Flask UI (`ui/ui.py`).
- Route `/`: Render `index.html`.
- On POST:
  - Take 'query' from form.
  - Send POST request to `API_URL` (env var).
  - Display results in Cards (Name, Score, Bio).
```

### Response (Generated Code)

*(See `ui/ui.py` for full output)*

---

## Entry 9: Deployment (Docker)

- **Tool Used:** ChatGPT (LLM)  
- **Purpose:** Deploy API and UI in a single container.  
- **Context:** Railway deployment requires a single entry point for simplicity.

### Prompt

```text
Write a `Dockerfile` that:
1. Installs Python 3.13.
2. Copies all code.
3. Installs requirements for BOTH API and UI.
4. Sets `API_URL` to localhost.
5. CMD: Runs both `uvicorn` (API) and `python ui.py` (Frontend) in parallel.
```

### Response (Generated Code)

*(See `docker/Dockerfile.combined` for full output)*

---

## Entry 10: Search Optimization (Trigrams)

- **Tool Used:** Google Agent (Antigravity)
- **Purpose:** Improve search result relevance for multi-word phrases (e.g., "Deep Learning in Finance").
- **Context:** Initial testing showed that phrases were splitting into independent keywords (OR logic). We updated the TF-IDF configuration to capture trigrams.

### Action Taken
Updated `recommender/embeddings.py`:
- Changed `ngram_range` from `(1, 2)` to `(1, 3)`.
- Increased `max_features` to `10000` to accommodate the larger vocabulary.
- This improvement ensures that unique 3-word combinations are treated as specific distinct features, boosting scores for exact phrase matches.

---

## Human Oversight & Refinement

While the core logic for the components listed above was generated by the LLM, every script underwent rigorous human analysis. We reviewed the generated code for correctness, security, and efficiency, making slight manual modifications where necessary to fit the specific project structure and requirements (e.g., path adjustments, error handling improvements, and schema enforcement).
