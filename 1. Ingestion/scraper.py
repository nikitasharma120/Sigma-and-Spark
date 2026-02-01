import requests
import json
import logging
import os
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Set, Optional

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_URL = "https://www.daiict.ac.in"
TIMEOUT = 20

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "faculty_profiles.json")

LISTING_PAGES = [
    ("https://www.daiict.ac.in/faculty", "faculty"),
    ("https://www.daiict.ac.in/adjunct-faculty", "adjunct"),
    ("https://www.daiict.ac.in/adjunct-faculty-international", "international"),
    ("https://www.daiict.ac.in/distinguished-professor", "distinguished"),
    ("https://www.daiict.ac.in/professor-practice", "practice"),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------------------------------------
# UTILITIES
# --------------------------------------------------

def fetch_html(url: str) -> Optional[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
    except Exception:
        logging.exception(f"Failed to fetch URL: {url}")
        return None

def clean(el) -> str:
    return " ".join(el.stripped_strings) if el else ""

def normalize_url(href: str) -> Optional[str]:
    if not href:
        return None
    href = href.strip()
    return href if href.startswith("http") else BASE_URL + href

# --------------------------------------------------
# LISTING PARSER
# --------------------------------------------------

def parse_listing_page(html: str, listing_url: str, faculty_type: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for a in soup.select("div.facultyInformation h3 a"):
        href = normalize_url(a.get("href"))
        if not href:
            continue

        records.append({
            "name": a.get_text(strip=True),
            "profile_url": href,
            "faculty_type": faculty_type,
            "source_listing_url": listing_url
        })

    return records

# --------------------------------------------------
# PROFILE PARSER
# --------------------------------------------------

def parse_profile_page(
    html: str,
    profile_url: str,
    faculty_type: str,
    source_listing_url: str
) -> Optional[Dict]:

    soup = BeautifulSoup(html, "html.parser")
    cover = soup.select_one("div.col-md-8 .rit-cover")
    if not cover:
        return None

    data = {
        "name": clean(soup.select_one(".field--name-field-faculty-names")),
        "faculty_type": faculty_type,
        "education": clean(soup.select_one(".field--name-field-faculty-name")),
        "phone": clean(soup.select_one(".field--name-field-contact-no")),
        "email": clean(soup.select_one(".field--name-field-email .field__item")),
        "address": clean(soup.select_one(".field--name-field-address")),
        "biography": None,
        "specialization": "",
        "teaching": [],
        "research": [],
        "openings": None,
        "publications": {
            "journal": [],
            "conference": [],
            "other": [],
            "external_links": []
        },
        "profile_url": profile_url,
        "source_listing_url": source_listing_url,
        "scraped_at": datetime.utcnow().isoformat()
    }

    # BIOGRAPHY (Drupal field)
    bio_el = soup.select_one(".field--name-field-biography")
    if bio_el:
        data["biography"] = clean(bio_el)

    # --------------------------------------------------
    # SECTION WALKER (THE CORE)
    # --------------------------------------------------

    for h2 in cover.find_all("h2", class_="rit-titl"):
        title = h2.get_text(strip=True).lower()

        wrapper = h2.find_parent("div")
        content = wrapper.find_next_sibling("div") if wrapper else None
        if not content:
            continue

        # ---------------- SPECIALIZATION ----------------
        if title == "specialization":
            data["specialization"] = clean(content)

        # ---------------- TEACHING ----------------
        elif title == "teaching":
            for li in content.select("li"):
                txt = clean(li)
                if txt:
                    data["teaching"].append(txt)

        # ---------------- OPENINGS ----------------
        elif title == "openings":
            txt = clean(content)
            data["openings"] = txt if txt else None

        # ---------------- RESEARCH ----------------
        elif title == "research":
            bullets = [clean(li) for li in content.select("li") if clean(li)]
            if bullets:
                data["research"] = bullets
            else:
                raw = clean(content)
                if raw:
                    data["research"] = [raw]

        # ---------------- PUBLICATIONS (ALL CASES) ----------------
        elif title == "publications":

            # 1️⃣ Capture ALL links (not just Google Scholar)
            for a in content.select("a[href]"):
                href = a.get("href")
                if href:
                    data["publications"]["external_links"].append(href.strip())

            # 2️⃣ Sectioned lists
            if content.find("h4"):
                current = None
                for el in content.children:
                    if getattr(el, "name", None) == "h4":
                        t = el.get_text(strip=True).lower()
                        if "journal" in t:
                            current = "journal"
                        elif "conference" in t:
                            current = "conference"
                        else:
                            current = "other"

                    elif getattr(el, "name", None) == "ul" and current:
                        for li in el.find_all("li"):
                            txt = clean(li)
                            if txt:
                                data["publications"][current].append(txt)

            # 3️⃣ Flat list
            else:
                for li in content.select("ul li"):
                    txt = clean(li)
                    if txt:
                        data["publications"]["other"].append(txt)

    return data

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    visited: Set[str] = set()
    records: List[Dict] = []

    for listing_url, faculty_type in LISTING_PAGES:
        logging.info(f"Scraping listing: {listing_url}")
        html = fetch_html(listing_url)
        if not html:
            continue

        people = parse_listing_page(html, listing_url, faculty_type)

        for p in people:
            url = p["profile_url"]
            if url in visited:
                continue
            visited.add(url)

            logging.info(f"Scraping profile: {url}")
            profile_html = fetch_html(url)
            if not profile_html:
                continue

            record = parse_profile_page(
                profile_html,
                url,
                p["faculty_type"],
                p["source_listing_url"]
            )

            if record:
                records.append(record)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    logging.info(f"FINISHED — {len(records)} profiles written")

# --------------------------------------------------

if __name__ == "__main__":
    main()
