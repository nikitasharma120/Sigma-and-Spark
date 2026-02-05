import json
import os
import re
from typing import Any, Dict, List

# --------------------------------------------------
# PATH CONFIG (PROJECT SAFE)
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

INPUT_PATH = os.path.join(PROJECT_ROOT, "faculty_profiles.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "faculty_cleaned.json")

NA = "Not Available"

# --------------------------------------------------
# BASIC CLEANERS
# --------------------------------------------------

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)

def clean_string(value: Any) -> str:
    if not value or not isinstance(value, str):
        return NA

    value = strip_html(value)
    value = normalize_whitespace(value)

    if value.lower() in {"", "none", "null", "-", "--"}:
        return NA

    return value

def clean_address(value: Any) -> str:
    if not value or not isinstance(value, str):
        return NA

    value = value.replace("#", "")
    value = strip_html(value)
    value = normalize_whitespace(value)

    return value if value else NA

def clean_list(values: Any) -> List[str]:
    if not isinstance(values, list):
        return []

    cleaned = []
    for v in values:
        if isinstance(v, str):
            v = normalize_whitespace(strip_html(v))
            if v:
                cleaned.append(v)
    return cleaned

# --------------------------------------------------
# PUBLICATIONS CLEANER
# --------------------------------------------------

def clean_publications(pub: Any) -> Dict[str, List[str]]:
    """
    Keeps structure:
    journal / conference / other / external_links
    """
    result = {
        "journal": [],
        "conference": [],
        "other": [],
        "external_links": []
    }

    if not isinstance(pub, dict):
        return result

    for key in result.keys():
        if key in pub:
            if isinstance(pub[key], list):
                result[key] = clean_list(pub[key])

    return result

# --------------------------------------------------
# MAIN TRANSFORM
# --------------------------------------------------

def transform_record(r: Dict[str, Any]) -> Dict[str, Any]:

    return {
        "name": clean_string(r.get("name")),
        "faculty_type": clean_string(r.get("faculty_type")),
        "image_url": clean_string(r.get("image_url")),

        # -------- PROFILE INFO --------
        "education": clean_string(r.get("education")),
        "biography": clean_string(r.get("biography")),
        "specialization": clean_string(r.get("specialization")),

        # -------- ACADEMICS --------
        "teaching": clean_list(r.get("teaching")),
        "research": clean_list(r.get("research")),
        "openings": clean_string(r.get("openings")),

        # -------- PUBLICATIONS --------
        "publications": clean_publications(r.get("publications")),

        # -------- CONTACT (GROUPED) --------
        "contact": {
            "phone": clean_string(r.get("phone")),
            "email": clean_string(r.get("email")),
            "address": clean_address(r.get("address")),
        },

        # -------- META --------
        "profile_url": clean_string(r.get("profile_url")),
        "source_listing_url": clean_string(r.get("source_listing_url")),
    }

# --------------------------------------------------
# DRIVER
# --------------------------------------------------

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Missing input file: {INPUT_PATH}")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cleaned = []
    for record in raw:
        try:
            cleaned.append(transform_record(record))
        except Exception:
            # pipeline must NEVER crash
            continue

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f" Cleaned {len(cleaned)} records → {OUTPUT_PATH}")

# --------------------------------------------------

if __name__ == "__main__":
    main()
