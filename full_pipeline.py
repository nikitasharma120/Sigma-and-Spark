import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ["python", "1. Ingestion/scraper.py"],
    ["python", "2. Transformation/cleaner.py"],
    ["python", "3. Storage/load_sqlite.py"],
    ["python", "4. Serving/execute_output.py"],
    ["python", "analytics/build_search_corpus.py"],
    ["python", "recommender/build_vector_index.py"],
    ["python", "recommender/embeddings.py"],
    ["python", "recommender/search.py"],
]

def run_step(cmd):
    print(f"\n▶ RUNNING: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=False
    )

    if result.returncode != 0:
        print(f"\n❌ FAILED: {' '.join(cmd)}")
        sys.exit(1)

def main():
    print("\n🚀 STARTING FULL DATA + ML PIPELINE\n")

    for step in STEPS:
        run_step(step)

    output_file = ROOT / "faculty_output.json"

    if not output_file.exists():
        print("\n❌ faculty_output.json NOT FOUND")
        print("Pipeline is lying. Fix execute_output.py.")
        sys.exit(1)

    print("\n✅ PIPELINE COMPLETED SUCCESSFULLY")
    print(f"📄 Output → {output_file}")

if __name__ == "__main__":
    main()
