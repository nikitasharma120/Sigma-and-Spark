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

INPUT_PATH = os.path.join(PROJECT_ROOT, "faculty_output.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data_exploration_stats.json")

NA = "Not Available"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

total_profiles = len(data)

# --------------------------------------------------
# 1. FACULTY TYPE DISTRIBUTION (FIXED SCHEMA)
# --------------------------------------------------
faculty_type_distribution = Counter()

for record in data:
    ftype = record.get("faculty_type", NA)
    faculty_type_distribution[ftype if ftype else NA] += 1

# --------------------------------------------------
# 2. MISSING VALUES ANALYSIS
# --------------------------------------------------
missing_values = defaultdict(int)

for record in data:
    for field in [
        "name",
        "faculty_type",
        "education",
        "biography",
        "specialization",
        "profile_url"
    ]:
        if record.get(field, NA) in (None, "", NA):
            missing_values[field] += 1

    contact = record.get("contact", {})
    for cfield in ["phone", "email", "address"]:
        if contact.get(cfield, NA) in (None, "", NA):
            missing_values[f"contact.{cfield}"] += 1

# --------------------------------------------------
# 3. BIOGRAPHY LENGTH (VALID ONLY)
# --------------------------------------------------
bio_lengths = [
    len(record["biography"])
    for record in data
    if record.get("biography") not in (None, "", NA)
]

avg_bio_length = (
    round(sum(bio_lengths) / len(bio_lengths), 2)
    if bio_lengths else 0
)

# --------------------------------------------------
# 4. SPECIALIZATION DISTRIBUTION (NO GUESSING)
# --------------------------------------------------
def is_valid_specialization(token: str) -> bool:
    token = token.strip()

    if not token:
        return False
    if len(token) > 120:
        return False

    lower = token.lower()
    if lower.startswith(("meet ", "please click", "know more")):
        return False
    if re.search(r"\b(received|currently|serving|experience|worked)\b", lower):
        return False

    return True


specialization_distribution = Counter()

for record in data:
    spec = record.get("specialization", NA)

    if spec in (None, "", NA):
        specialization_distribution[NA] += 1
        continue

    parts = [s.strip() for s in spec.split(",")]
    valid_found = False

    for part in parts:
        cleaned = re.sub(r"[.\s]+$", "", part)
        if is_valid_specialization(cleaned):
            specialization_distribution[cleaned] += 1
            valid_found = True

    if not valid_found:
        specialization_distribution[NA] += 1

# --------------------------------------------------
# FINAL OUTPUT
# --------------------------------------------------
stats = {
    "meta": {
        "total_profiles": total_profiles
    },
    "faculty_type_distribution": dict(faculty_type_distribution),
    "missing_values_summary": dict(missing_values),
    "average_text_lengths": {
        "biography": avg_bio_length
    },
    "specialization_distribution": dict(
        specialization_distribution.most_common()
    )
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)

print(f" Data exploration stats written to → {OUTPUT_PATH}")
