"""
Anderson University — Core Audit Evaluator

This module takes a parsed course map and evaluates it against:
  1. Liberal Arts requirements (via la_rules.py)
  2. Major requirements (via major_rules.py)

Returns a structured AuditResult object ready for PDF generation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from requirements.la_rules import evaluate_la, LAResult, norm, course_status as _la_status
from requirements.major_rules import get_major_requirements


# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class RequirementRow:
    label: str
    status: str          # "Satisfied" | "In Progress" | "Scheduled" | "Not Satisfied"
    course_display: str  # e.g. "POSC-2020"
    course_name: str     # e.g. "Introduction to World Politics"
    credits_required: float
    credits_earned: float
    note: str = ""


@dataclass
class AuditResult:
    # Student info
    student_name: str
    student_id: str
    major: str
    catalog_year: str

    # Liberal Arts rows
    la_rows: list[LAResult] = field(default_factory=list)

    # Major requirement rows
    major_rows: list[RequirementRow] = field(default_factory=list)

    # Summary stats
    total_credits_earned: float = 0.0
    total_credits_in_progress: float = 0.0
    total_credits_projected: float = 0.0
    overall_gpa: float = 0.0
    major_gpa: float = 0.0
    major_credits_earned: float = 0.0
    major_credits_in_progress: float = 0.0
    major_credits_required: float = 0.0

    # Eligibility flags
    la_complete: bool = False
    major_complete: bool = False
    gpa_ok: bool = False
    major_gpa_ok: bool = False
    credits_ok: bool = False
    eligible_to_walk: bool = False

    # Outstanding items for Action Plan
    la_outstanding: list[str] = field(default_factory=list)
    major_outstanding: list[str] = field(default_factory=list)

    # All courses for Course History page
    all_courses: list[dict] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# GPA CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

GRADE_POINTS = {
    "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0,
}

def compute_gpa(course_map: dict, major_dept_prefixes: list) -> dict:
    """
    Compute overall GPA, major GPA, earned credits, and in-progress credits.
    Transfer credits (grade T) count toward earned hours but not GPA.
    """
    overall_points = 0.0
    overall_hours = 0.0
    major_points = 0.0
    major_hours = 0.0
    earned = 0.0
    in_progress = 0.0

    for code, c in course_map.items():
        s = c.get("status", "")
        g = c.get("grade", "").upper()
        cr = float(c.get("cr", 0))

        if s == "dropped" or g in ("W", "DRP"):
            continue
        if s == "current":
            in_progress += cr
            continue
        if s == "scheduled":
            in_progress += cr
            continue
        if s != "grade posted":
            continue

        earned += cr

        # Transfer credit — counts toward hours but not GPA
        if g == "T":
            continue
        # No-credit or audit
        if g in ("NC", "AU", ""):
            continue

        gp = GRADE_POINTS.get(g)
        if gp is None:
            continue

        overall_points += gp * cr
        overall_hours += cr

        # Major GPA: courses whose prefix matches major departments
        dept = code.split("_")[0] if "_" in code else code[:4]
        if dept in major_dept_prefixes:
            major_points += gp * cr
            major_hours += cr

    return {
        "overall_gpa": round(overall_points / overall_hours, 2) if overall_hours else 0.0,
        "major_gpa": round(major_points / major_hours, 2) if major_hours else 0.0,
        "earned": earned,
        "in_progress": in_progress,
        "projected": earned + in_progress,
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAJOR DEPT PREFIX MAP
# ─────────────────────────────────────────────────────────────────────────────

MAJOR_DEPT_PREFIXES = {
    "political_science": ["POSC"],
    "polsci_philosophy_economics": ["POSC", "PHIL", "ECON"],
    "international_relations": ["POSC"],
    "history": ["HIST"],
    "accounting": ["ACCT", "BSNS"],
    "visual_communication": ["ARTS", "ARTH"],
    "communication": ["COMM"],
    "psychology": ["PSYC"],
    "biology": ["BIOL"],
    "chemistry": ["CHEM"],
    "nursing": ["NURS"],
    "education": ["EDUC"],
    "elementary_education": ["EDUC"],
    "math": ["MATH"],
    "computer_science": ["CPSC"],
    "criminal_justice": ["CRIM"],
    "social_work": ["SOWK"],
    "exercise_science": ["EXSC"],
    "music": ["MUSC", "MUPF"],
    "theatre": ["THEA"],
    "dance": ["DANC"],
    "spanish": ["SPAN"],
    "engineering": ["ENGR"],
    "management": ["BSNS"],
    "marketing": ["BSNS"],
    "finance": ["BSNS"],
    "sport_marketing": ["BSNS", "SPRL"],
}

def get_major_prefixes(major_key: str) -> list:
    key = major_key.lower()
    for k, v in MAJOR_DEPT_PREFIXES.items():
        if k == key or k in key:
            return v
    return [key.split("_")[0].upper()]


# ─────────────────────────────────────────────────────────────────────────────
# MAJOR REQUIREMENT EVALUATOR
# ─────────────────────────────────────────────────────────────────────────────

def _course_status_from_map(code: str, course_map: dict) -> str:
    """Look up a course in the map and return its display status."""
    c = course_map.get(norm(code))
    if c is None:
        return "Not Satisfied"
    s = c.get("status", "")
    g = c.get("grade", "").upper()
    if s == "grade posted":
        if g in ("W", "DRP", "F", "NC"):
            return "Not Satisfied"
        return "Satisfied"
    if s == "current":
        return "In Progress"
    if s == "scheduled":
        return "Scheduled"
    return "Not Satisfied"


def evaluate_major(course_map: dict, major_key: str, catalog_year: str) -> list:
    """
    Evaluate major requirements against the course map.
    Returns list of RequirementRow objects.
    """
    req = get_major_requirements(major_key, catalog_year)
    if not req:
        return [RequirementRow(
            label=f"Major requirements not found for {major_key} ({catalog_year})",
            status="Not Satisfied",
            course_display="",
            course_name="",
            credits_required=0,
            credits_earned=0,
        )]

    rows: list[RequirementRow] = []

    # ── Required individual courses ──────────────────────────────────────────
    for code in req.get("required", []):
        n = norm(code)
        c = course_map.get(n)
        status = _course_status_from_map(code, course_map)
        cr_earned = float(c.get("cr", 0)) if c and status in ("Satisfied", "In Progress", "Scheduled") else 0.0
        rows.append(RequirementRow(
            label=code.replace("_", "-"),
            status=status,
            course_display=code.replace("_", "-"),
            course_name=c.get("name", "") if c else "",
            credits_required=float(c.get("cr", 3)) if c else 3.0,
            credits_earned=cr_earned,
        ))

    # ── Distribution groups ──────────────────────────────────────────────────
    for group in req.get("dist_groups", []):
        group_name = group.get("name", "Distribution Group")
        credits_required = float(group.get("credits_required", 6))
        min_courses = group.get("min_courses", 2)
        options = group.get("choose_from", [])

        # Find all courses from this group that the student has taken
        taken = []
        for code in options:
            c = course_map.get(norm(code))
            if c:
                s = _course_status_from_map(code, course_map)
                if s in ("Satisfied", "In Progress", "Scheduled"):
                    taken.append((code, c, s))

        credits_earned = sum(float(c.get("cr", 3)) for _, c, s in taken if s == "Satisfied")
        credits_ip = sum(float(c.get("cr", 3)) for _, c, s in taken if s in ("In Progress", "Scheduled"))

        if credits_earned >= credits_required:
            status = "Satisfied"
        elif credits_earned + credits_ip >= credits_required:
            status = "In Progress"
        elif taken:
            status = "In Progress"
        else:
            status = "Not Satisfied"

        courses_display = ", ".join(code.replace("_", "-") for code, _, _ in taken) if taken else ""
        rows.append(RequirementRow(
            label=f"{group_name} ({int(credits_required)} cr from: {', '.join(o.replace('_','-') for o in options)})",
            status=status,
            course_display=courses_display,
            course_name=f"Need {min_courses} courses / {int(credits_required)} credits",
            credits_required=credits_required,
            credits_earned=credits_earned + credits_ip,
            note=f"{len(taken)}/{min_courses} courses taken",
        ))

    # ── Elective block ───────────────────────────────────────────────────────
    elective_credits = req.get("elective_credits", 0)
    if elective_credits:
        elective_depts = req.get("elective_dept", [])
        elective_note = req.get("elective_note", "")
        elective_earned = 0.0
        elective_courses = []
        for code, c in course_map.items():
            dept = code.split("_")[0]
            if dept in elective_depts:
                s = _course_status_from_map(code, course_map)
                if s in ("Satisfied", "In Progress", "Scheduled"):
                    # Only count if not already counted in required or dist_groups
                    required_codes = {norm(r) for r in req.get("required", [])}
                    dist_codes = {norm(o) for g in req.get("dist_groups", []) for o in g.get("choose_from", [])}
                    if code not in required_codes and code not in dist_codes:
                        elective_earned += float(c.get("cr", 0))
                        elective_courses.append(code.replace("_", "-"))

        if elective_earned >= elective_credits:
            elective_status = "Satisfied"
        elif elective_earned > 0:
            elective_status = "In Progress"
        else:
            elective_status = "Not Satisfied"

        rows.append(RequirementRow(
            label=f"Major Electives ({int(elective_credits)} cr)",
            status=elective_status,
            course_display=", ".join(elective_courses[:4]),
            course_name=elective_note,
            credits_required=float(elective_credits),
            credits_earned=elective_earned,
        ))

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# MAIN AUDIT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def run_audit(
    course_map: dict,
    student_name: str,
    student_id: str,
    major_key: str,
    catalog_year: str,
) -> AuditResult:
    """
    Run a complete graduation audit for a student.

    Args:
        course_map: Output of csv_parser.parse_csv()
        student_name: Full name string
        student_id: Student ID string
        major_key: Lowercase underscore major key (e.g. "political_science")
        catalog_year: "2022-23", "2023-24", or "2024-25"

    Returns:
        AuditResult with all rows and summary statistics populated.
    """
    # ── Evaluate Liberal Arts ────────────────────────────────────────────────
    la_rows = evaluate_la(course_map, catalog_year, major_key)

    # ── Evaluate Major ───────────────────────────────────────────────────────
    major_rows = evaluate_major(course_map, major_key, catalog_year)

    # ── Get major display name ───────────────────────────────────────────────
    req = get_major_requirements(major_key, catalog_year)
    major_name = req.get("name", major_key.replace("_", " ").title()) if req else major_key.replace("_", " ").title()
    major_credits_required = float(req.get("total_credits", 0)) if req else 0.0

    # ── Compute GPA and credit totals ────────────────────────────────────────
    prefixes = get_major_prefixes(major_key)
    gpa_data = compute_gpa(course_map, prefixes)

    # ── Compute major credits earned/in-progress ─────────────────────────────
    major_credits_earned = sum(
        r.credits_earned for r in major_rows if r.status == "Satisfied"
    )
    major_credits_ip = sum(
        r.credits_earned for r in major_rows if r.status in ("In Progress", "Scheduled")
    )

    # ── Determine outstanding items ──────────────────────────────────────────
    la_outstanding = [r.label for r in la_rows if r.status == "Not Satisfied"]
    major_outstanding = [r.label for r in major_rows if r.status == "Not Satisfied"]

    # ── Eligibility checks ───────────────────────────────────────────────────
    la_complete = len(la_outstanding) == 0
    major_complete = len(major_outstanding) == 0
    gpa_ok = gpa_data["overall_gpa"] >= 2.0
    major_gpa_ok = gpa_data["major_gpa"] >= 2.0
    credits_ok = gpa_data["projected"] >= 120.0
    eligible = la_complete and major_complete and gpa_ok and major_gpa_ok and credits_ok

    # ── Build all_courses list for Course History page ───────────────────────
    all_courses = sorted(course_map.values(), key=lambda c: c.get("raw", ""))

    return AuditResult(
        student_name=student_name,
        student_id=student_id,
        major=major_name,
        catalog_year=catalog_year,
        la_rows=la_rows,
        major_rows=major_rows,
        total_credits_earned=gpa_data["earned"],
        total_credits_in_progress=gpa_data["in_progress"],
        total_credits_projected=gpa_data["projected"],
        overall_gpa=gpa_data["overall_gpa"],
        major_gpa=gpa_data["major_gpa"],
        major_credits_earned=major_credits_earned,
        major_credits_in_progress=major_credits_ip,
        major_credits_required=major_credits_required,
        la_complete=la_complete,
        major_complete=major_complete,
        gpa_ok=gpa_ok,
        major_gpa_ok=major_gpa_ok,
        credits_ok=credits_ok,
        eligible_to_walk=eligible,
        la_outstanding=la_outstanding,
        major_outstanding=major_outstanding,
        all_courses=all_courses,
    )
