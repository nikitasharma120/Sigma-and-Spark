import subprocess

for cmd in [
    'python "1. Ingestion/scraper.py"',
    'python "2. Transformation/cleaner.py"',
    'python "3. Storage/load_sqlite.py"',
    'uvicorn --reload --app-dir "4. Serving" app:app'
]:
    subprocess.run(cmd, shell=True)
