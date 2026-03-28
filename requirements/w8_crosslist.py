"""
W8 crosslist loader.

Parses requirements/w8_crosslist.csv into normalized mappings used by engines.
"""

from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

CSV_PATH = Path(__file__).with_name("w8_crosslist.csv")

_COURSE_RE = re.compile(r"([A-Z]{3,4})\s*[- ]?\s*(\d{3,4})")


def _normalize_course_tokens(raw_text: str) -> list[str]:
    """Normalize a free-form course list into DEPT_#### course codes."""
    if not raw_text:
        return []
    text = raw_text.upper().replace("/", " / ")
    tokens = [t.strip() for t in re.split(r"[,;]", text) if t.strip()]
    out: list[str] = []
    last_dept = ""
    for token in tokens:
        m = _COURSE_RE.search(token)
        if m:
            dept, num = m.groups()
            last_dept = dept
            code = f"{dept}_{num}"
            if code not in out:
                out.append(code)
            continue

        # Handle abbreviated entries like ", 3450, 4100" where dept is omitted.
        m_num = re.search(r"\b(\d{3,4})\b", token)
        if m_num and last_dept:
            code = f"{last_dept}_{m_num.group(1)}"
            if code not in out:
                out.append(code)
    return out


def _parse_rows() -> dict[str, list[str]]:
    """
    Return mapping keyed by line id from the crosslist sheet.

    Example key: "165" -> ["BSNS_1050", "BSNS_4110", ...]
    """
    line_to_courses: dict[str, list[str]] = {}
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 2:
        return line_to_courses

    header = rows[1]
    try:
        line_idx = header.index("Line")
        courses_idx = header.index("Courses that Satisfy W8 Experiential")
    except ValueError:
        return line_to_courses

    for row in rows[2:]:
        if len(row) <= max(line_idx, courses_idx):
            continue
        line = (row[line_idx] or "").strip()
        if not line:
            continue
        courses = _normalize_course_tokens((row[courses_idx] or "").strip())
        line_to_courses[line] = courses
    return line_to_courses


@lru_cache(maxsize=1)
def get_w8_crosslist_lines() -> dict[str, list[str]]:
    """Get crosslist rows keyed by line number."""
    return _parse_rows()


@lru_cache(maxsize=1)
def get_w8_fsb_by_major() -> dict[str, list[str]]:
    """Get FSB major-key -> W8 course list from crosslist rows."""
    lines = get_w8_crosslist_lines()
    # FSB majors mapped by crosslist line number.
    mapping = {
        "sport_marketing": lines.get("165", []),
        "marketing": lines.get("140", []),
        "accounting": lines.get("80", []),
        "business_analytics": lines.get("90", []),
        "finance": lines.get("110", []),
        "global_business": lines.get("120", []),
        "management": lines.get("130", []),
        "engineering_management": lines.get("135", []),
        "music_entertainment_business": lines.get("160", []),
        "business_integrative_leadership": lines.get("75", []),
    }
    return mapping


@lru_cache(maxsize=1)
def get_w8_non_fsb_by_major() -> dict[str, list[str]]:
    """Get non-FSB program-key -> W8 course list from crosslist rows."""
    lines = get_w8_crosslist_lines()
    mapping = {
        "psychology": lines.get("10", []),
        "youth_leadership_development_complementary": lines.get("10", []),
        "cinema_media_arts": lines.get("20", []),
        "public_relations_complementary": lines.get("22", []),
        "journalism_complementary": lines.get("23", []),
        "multimedia_journalism_complementary": lines.get("23", []),
        "visual_communication": lines.get("25", []),
        "literary_studies": lines.get("30", []),
        "writing": lines.get("30", []),
        "english_studies_minor": lines.get("30", []),
        "elementary_education": lines.get("40", []),
        "social_studies_teaching": lines.get("40", []),
        "language_arts_teaching": lines.get("40", []),
        "math_teaching_ba": lines.get("40", []),
        "spanish_education": lines.get("40", []),
        "christian_ministries": lines.get("60", []),
        "christian_ministries_complementary": lines.get("60", []),
        "youth_ministries": lines.get("60", []),
        "christian_spiritual_formation_complementary": lines.get("65", []),
        "math_ba": lines.get("170", []),
        "math_bs": lines.get("170", []),
        "exercise_science": lines.get("190", []),
        "sport_recreational_leadership": lines.get("200", []),
        "nursing_bsn": lines.get("210", []),
        "nursing_accelerated": lines.get("210", []),
        "nursing_rn_bsn": lines.get("210", []),
        "history": lines.get("220", []),
        "public_history": lines.get("330", []),
        "political_science": lines.get("222", []),
        "polsci_philosophy_economics": lines.get("222", []),
        "international_relations": lines.get("224", []),
        "national_security": lines.get("226", []),
        "criminal_justice_major": lines.get("230", []),
        "criminal_justice_major_online": lines.get("230", []),
        "social_work": lines.get("240", []),
        "family_science_major": lines.get("240", []),
        "spanish": lines.get("250", []),
        "voice_performance_bmus": lines.get("261", []),
        "instrumental_performance_bmus": lines.get("262", []),
        "musical_theatre_bmus": lines.get("263", []),
        "worship_arts_ba": lines.get("264", []),
        "musical_theatre_ba": lines.get("265", []),
        "music_education_bmus": lines.get("266", []),
        "songwriting": lines.get("267", []),
        "dance_major": lines.get("270", []),
        "dance_complementary": lines.get("270", []),
        "theatre_ba": lines.get("271", []),
        "cs_ba": lines.get("275", []),
        "cs_bs": lines.get("275", []),
        "cs_complementary": lines.get("275", []),
        "business_info_systems_complementary": lines.get("275", []),
        "data_science_ba": lines.get("277", []),
        "data_science_bs": lines.get("277", []),
        "data_science_complementary": lines.get("277", []),
        "biochemistry_ba": lines.get("290", []),
        "biochemistry_bs": lines.get("290", []),
        "chemistry_ba": lines.get("290", []),
        "chemistry_bs": lines.get("290", []),
        "electrical_engineering_bs": lines.get("315", []),
        "mechanical_engineering_bs": lines.get("315", []),
        "mechatronics_engineering_bs": lines.get("315", []),
        "civil_engineering_bs": lines.get("315", []),
        "engineering_physics_bs": lines.get("315", []),
        "computer_engineering_bs": lines.get("325", []),
        "public_health_ba": lines.get("340", []),
        "public_health_bs": lines.get("340", []),
        "public_health_minor": lines.get("340", []),
        "cybersecurity_major": lines.get("350", []),
        "ministry_studies": lines.get("355", []),
        # No W8 course required for these programs.
        "biology_ba": [],
        "biology_bs": [],
        "sociology_minor": [],
    }
    return mapping


@lru_cache(maxsize=1)
def get_fsb_w8_courses_by_major() -> dict[str, list[str]]:
    """Backward-compatible alias for FSB W8 mapping."""
    return get_w8_fsb_by_major()


@lru_cache(maxsize=1)
def get_non_fsb_w8_courses_by_major() -> dict[str, list[str]]:
    """Backward-compatible alias for non-FSB W8 mapping."""
    return get_w8_non_fsb_by_major()


def get_fsb_w8_courses(major_key: str, default: list[str] | None = None) -> list[str]:
    """Get W8 courses for one FSB major key."""
    default_courses = default if default is not None else []
    return get_fsb_w8_courses_by_major().get(major_key, default_courses)


def get_non_fsb_w8_courses(major_key: str, default: list[str] | None = None) -> list[str]:
    """Get W8 courses for one non-FSB major key."""
    default_courses = default if default is not None else []
    return get_non_fsb_w8_courses_by_major().get(major_key, default_courses)


def get_non_fsb_w8_no_course_required(major_key: str) -> bool:
    """Whether this non-FSB major is explicitly exempt from a W8 course."""
    return major_key in {"biology_ba", "biology_bs", "sociology_minor"}
