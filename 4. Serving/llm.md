# LLM Usage Log

This document records the use of Large Language Models (LLMs) during the development of this project to ensure transparency and academic integrity.

---

## Project Overview

- **Description:** FastAPI application serving faculty data from a SQLite database  
- **Database:** SQLite (`faculty.db`)  
- **Technologies:** FastAPI, SQLite3, HTTPS  

---

## LLM Information

- **Tool Used:** ChatGPT (GPT-5.2)  
- **Provider:** OpenAI  
- **Usage Type:** Code generation  
- **Human Oversight:** Yes (all outputs reviewed and modified where necessary)

---

## LLM Usage Summary

### 1. Application Structure
- **Date:** 2026-01-20  
- **Purpose:** Generate FastAPI app structure and endpoint flow  
- **LLM Contribution:** App setup and routing logic  
- **Human Role:** Verified paths, added comments, improved error handling  

### 2. Database Connectivity
- **Purpose:** SQLite connection helper  
- **LLM Contribution:** `get_connection()` with row factory and exceptions  
- **Human Role:** Validated database path and runtime behavior  

### 3. Data Fetching Logic
- **Purpose:** Retrieve data  
- **LLM Contribution:** Helper functions
- **Human Role:** Schema verification and testing  

### 4. API 
- **LLM Contribution:** `fetch_all_faculty()` logic  
- **Human Role:** Validation and endpoint testing  

---

## Data Integrity

- No data was generated or altered by the LLM.
- LLM usage was limited to **code structure and logic assistance**.
- All data originates from verified project sources.

---

## Declaration

LLM assistance was used responsibly and all outputs were reviewed, tested, and validated by group members.
