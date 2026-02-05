import json
import os
from collections import Counter, defaultdict
import re

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

INPUT_PATH = os.path.join(PROJECT_ROOT, "faculty_cleaned.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data_exploration_stats.json")

NA = "Not Available"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

total_profiles = len(data)

# --------------------------------------------------
# 1. FACULTY TYPE DISTRIBUTION
# --------------------------------------------------

faculty_type_distribution = Counter(
    r.get("faculty_type", NA) or NA
    for r in data
)

# --------------------------------------------------
# 2. MISSING VALUES ANALYSIS
# --------------------------------------------------

missing = defaultdict(int)

top_fields = [
    "name",
    "faculty_type",
    "education",
    "biography",
    "specialization",
    "profile_url",
]

for r in data:
    for f in top_fields:
        if r.get(f) in (None, "", NA):
            missing[f] += 1

    contact = r.get("contact", {})
    for cf in ["phone", "email", "address"]:
        if contact.get(cf) in (None, "", NA):
            missing[f"contact.{cf}"] += 1

# --------------------------------------------------
# 3. TEXT LENGTH STATISTICS
# --------------------------------------------------

def avg_length(key: str):
    vals = [
        len(r[key])
        for r in data
        if isinstance(r.get(key), str) and r[key] not in ("", NA)
    ]
    return round(sum(vals) / len(vals), 2) if vals else 0

average_lengths = {
    "biography": avg_length("biography")
}

# --------------------------------------------------
# 4. TEACHING / RESEARCH COVERAGE
# --------------------------------------------------

teaching_counts = [len(r.get("teaching", [])) for r in data]
research_counts = [len(r.get("research", [])) for r in data]

# --------------------------------------------------
# 5. PUBLICATION ANALYSIS
# --------------------------------------------------

publication_type_distribution = Counter()
faculty_with_publications = 0

for r in data:
    pubs = r.get("publications", {})
    if not isinstance(pubs, dict):
        continue

    has_any = False
    for ptype, plist in pubs.items():
        count = len(plist)
        publication_type_distribution[ptype] += count
        if count > 0:
            has_any = True

    if has_any:
        faculty_with_publications += 1

# --------------------------------------------------
# 6. SPECIALIZATION DISTRIBUTION (CLEAN)
# --------------------------------------------------

def valid_spec(token: str) -> bool:
    if not token:
        return False
    if len(token) > 120:
        return False
    if re.search(r"\b(current|worked|experience|serving)\b", token.lower()):
        return False
    return True

specialization_dist = Counter()

for r in data:
    spec = r.get("specialization", NA)

    if spec in (None, "", NA):
        specialization_dist[NA] += 1
        continue

    for part in spec.split(","):
        part = part.strip()
        if valid_spec(part):
            specialization_dist[part] += 1

# --------------------------------------------------
# FINAL STATS OBJECT
# --------------------------------------------------

stats = {
    "meta": {
        "total_profiles": total_profiles
    },

    "faculty_type_distribution": dict(faculty_type_distribution),

    "missing_values_summary": dict(missing),

    "average_text_lengths": average_lengths,

    "teaching_statistics": {
        "avg_courses_per_faculty": round(
            sum(teaching_counts) / len(teaching_counts), 2
        ) if teaching_counts else 0
    },

    "research_statistics": {
        "avg_topics_per_faculty": round(
            sum(research_counts) / len(research_counts), 2
        ) if research_counts else 0
    },

    "publication_type_distribution": dict(publication_type_distribution),

    "specialization_distribution": dict(
        specialization_dist.most_common()
    ),
}

# --------------------------------------------------
# WRITE OUTPUT
# --------------------------------------------------


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)

print(f" Data exploration stats written → {OUTPUT_PATH}")

