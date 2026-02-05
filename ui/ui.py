from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Docker service name (as you already use)
# Docker service name (as you already use)
import os
API_URL = os.environ.get("API_URL", "http://faculty_api:8000/recommend")


@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        # ---- USER INPUTS ----
        query = request.form.get("query", "").strip()
        faculty_type = request.form.get("faculty_type", "").strip()
        limit = request.form.get("limit", "10")

        try:
            limit = int(limit)
        except ValueError:
            limit = 10

        # ---- API CALL ----
        if query:
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=10
                )

                if response.status_code == 200:
                    results = response.json().get("results", [])

                    # ---- FILTER: FACULTY TYPE ----
                    if faculty_type:
                        results = [
                            r for r in results
                            if r.get("details", {}).get("faculty_type") == faculty_type
                        ]

                    # ---- LIMIT RESULTS ----
                    results = results[:limit]

            except requests.exceptions.RequestException as e:
                results = []

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
