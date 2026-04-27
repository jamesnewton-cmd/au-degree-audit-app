"""
Anderson University — CSV Transcript Parser

Parses the SIS CSV export into a normalized course map.

CSV columns:
  Course Code | Course Name | Equivalent Course | Registration Date |
  Section | Credits | Status | Campus | Instructor | Numeric Grade | Letter Grade

Status values in CSV:
  "Grade Posted"  → completed
  "Current"       → in progress this semester
  "Scheduled"     → registered for future semester
  "Dropped"       → dropped (skip)
  ""              → not started (skip)

Letter Grade "T" = transfer credit (treat as Satisfied)
"""

import csv
import re
from dataclasses import dataclass


# ─────────────────────────────────────────────────────────────────────────────
# NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def norm(code: str) -> str:
    """Normalize course code: uppercase, underscore separator, strip trailing _23 etc."""
    c = code.strip().upper().replace("-", "_").replace(" ", "_")
    # Strip catalog year suffix like _23, _22, _24 at end
    c = re.sub(r"_\d{2}$", "", c)
    return c


def _resolve_transfer_code(raw_code: str, equiv: str) -> str:
    """
    If the course code is a transfer/ELCT/LAWK wrapper, extract the real course code.
    Transfer codes look like: ELCT-2000-1629045-ENGL-1110 or LAWK-12SC-1629045-BIOL-111
    """
    raw = raw_code.strip()
    # ELCT or LAWK prefix = transfer/equivalency wrapper
    if raw.upper().startswith(("ELCT-", "ELCT_", "LAWK-", "LAWK_", "POSC-1600", "POSC_1600")):
        # Try to extract the real course from the end of the code
        # Format: PREFIX-LEVEL-STUDENTID-DEPT-NUMBER
        parts = raw.replace("_", "-").split("-")
        if len(parts) >= 5:
            dept = parts[-2].upper()
            num = parts[-1].upper()
            if dept.isalpha() and num.isdigit():
                return f"{dept}-{num}"
        # Fall back to equiv if available
        if equiv and equiv.strip():
            return equiv.strip()
    # Strip catalog year suffix from code (e.g. BSNS-2450_23 → BSNS-2450)
    raw = re.sub(r"[_-]\d{2}$", "", raw)
    return raw


def _canonical_status(status_raw: str, reg_date: str) -> str:
    """Normalize the status field to lowercase canonical values."""
    s = status_raw.strip().lower()
    if s == "grade posted":
        return "grade posted"
    if s == "current":
        return "current"
    if s == "scheduled":
        return "scheduled"
    if s in ("dropped", "drop"):
        return "dropped"
    if s == "":
        return "not started"
    return s


def _priority(course: dict) -> int:
    """
    Priority for deduplication when the same course appears multiple times.
    Lower number = higher priority (kept over higher numbers).
    """
    g = course.get("grade", "").upper()
    s = course.get("status", "")
    if s == "grade posted" and g == "T":
        return 0   # Transfer credit — highest priority
    if s == "grade posted" and g not in ("", "W", "WF", "DRP", "NC", "F"):
        return 1   # Completed with passing grade
    if s == "current":
        return 2   # In progress
    if s == "scheduled":
        return 3   # Scheduled
    if s == "grade posted" and g in ("F", "WF"):
        return 4   # Failed
    if s == "grade posted" and g == "NC":
        return 5   # No credit
    if s == "dropped" or g in ("DRP", "W", "WF"):
        return 6   # Dropped
    return 7


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_csv(path: str) -> dict:
    """
    Parse a student transcript CSV and return a normalized course map.

    Returns:
        dict: {normalized_code: course_record}
        where course_record = {
            "code": normalized code (DEPT_NNNN),
            "raw": original resolved code (DEPT-NNNN),
            "name": course name string,
            "cr": credit hours (int),
            "status": "grade posted" | "current" | "scheduled" | "dropped",
            "grade": letter grade string,
        }

    Deduplication: when the same course appears multiple times (retaken,
    transfer + native, etc.), the highest-priority record is kept.
    """
    rows = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            raw_code = r.get("Course Code", "").strip()
            equiv = r.get("Equivalent Course", "").strip()
            if not raw_code:
                continue

            resolved = _resolve_transfer_code(raw_code, equiv)
            status = _canonical_status(r.get("Status", ""), r.get("Registration Date", ""))
            grade = r.get("Letter Grade", "").strip()

            # Skip rows with no useful information
            if status == "not started" and not grade:
                continue
            if status == "dropped":
                continue  # Dropped courses never count

            try:
                credits = int(float(r.get("Credits", "0") or "0"))
            except (ValueError, TypeError):
                credits = 0

            rows.append({
                "code": norm(resolved),
                "raw": resolved.upper().replace("_", "-"),
                "name": r.get("Course Name", "").strip(),
                "cr": credits,
                "status": status,
                "grade": grade,
            })

    # Deduplicate: keep highest-priority record per course code
    best: dict[str, dict] = {}
    for c in rows:
        k = c["code"]
        if k not in best or _priority(c) < _priority(best[k]):
            best[k] = c

    # Apply institutional blanket exceptions automatically
    if "ENGR_3140" in best and "ENGR_3150" in best and "ENGR_3100" not in best:
        best["ENGR_3100"] = {
            "code": "ENGR_3100", "raw": "ENGR-3100", "name": "Mechanics Lab (Subbed by 3140+3150)",
            "cr": 2, "status": "grade posted", "grade": "CR"
        }
    if "ENGR_4140" in best and "ENGR_4320" in best and "ENGR_4100" not in best:
        best["ENGR_4100"] = {
            "code": "ENGR_4100", "raw": "ENGR-4100", "name": "Thermal-Fluids Lab (Subbed by 4140+4320)",
            "cr": 2, "status": "grade posted", "grade": "CR"
        }
    if "ENGR_2200" in best and "CPSC_2320" not in best:
        best["CPSC_2320"] = {
            "code": "CPSC_2320", "raw": "CPSC-2320", "name": "C++ Programming (Subbed by ENGR-2200)",
            "cr": 1, "status": best["ENGR_2200"]["status"], "grade": best["ENGR_2200"]["grade"]
        }

    return best


def get_student_info(path: str) -> dict:
    """
    Extract student metadata from the CSV filename or first row.
    Returns dict with 'name', 'major', 'catalog_year' (best-effort).
    """
    import os
    filename = os.path.basename(path)
    # Try to parse "FirstnameLastname-Major22-23.csv" pattern
    name_part = filename.replace(".csv", "").replace(".CSV", "")
    info = {"name": name_part, "major": "", "catalog_year": "2022-23"}

    # Extract catalog year pattern like 22-23, 23-24, 24-25
    year_match = re.search(r"(\d{2})-(\d{2})", name_part)
    if year_match:
        info["catalog_year"] = f"20{year_match.group(1)}-{year_match.group(2)}"
        name_part = name_part[:year_match.start()].strip("-")

    # Split name from major: "JenniferEisinger-PoliticalScience"
    if "-" in name_part:
        parts = name_part.split("-", 1)
        info["name"] = _split_camel(parts[0])
        info["major"] = _camel_to_key(parts[1]) if len(parts) > 1 else ""
    else:
        info["name"] = _split_camel(name_part)

    return info


def _split_camel(s: str) -> str:
    """Convert CamelCase to 'First Last' format."""
    return re.sub(r"([A-Z])", r" \1", s).strip()


def _camel_to_key(s: str) -> str:
    """Convert 'PoliticalScience' to 'political_science'."""
    return re.sub(r"([A-Z])", r"_\1", s).strip("_").lower()
