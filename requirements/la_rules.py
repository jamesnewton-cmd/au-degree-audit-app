"""
Anderson University — Liberal Arts Requirements Rules Engine
Catalog Year: 2022-23 (also applies to 2023-24, 2024-25 unless overridden)

This module is the ONLY place where LA logic lives.
It is deterministic — no AI inference at runtime.

Rules encoded:
  - F1–F7 Foundational Skills
  - W1–W8 Ways of Knowing
  - WI Advanced Writing Competency (2 courses, ≥1 upper-div)
  - SI Speaking Intensive (1 course beyond COMM-1000)
  - Crossover AND/OR rules (from LiberalArtsCrossOverClasses.pdf)
  - Honors Program exceptions (HNRS prefix courses)
  - W8 major-specific course mapping (from W8-ExperientialWaysofKnowing.xlsx)
  - POSC-2840 two-semester rule for W8
"""

from __future__ import annotations
from dataclasses import dataclass, field
import re


# ─────────────────────────────────────────────────────────────────────────────
# NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def norm(code: str) -> str:
    """Normalize course code to DEPT_NNNN uppercase format."""
    c = code.strip().upper().replace("-", "_").replace(" ", "_")
    c = re.sub(r"_\d{2}$", "", c)
    return c


def course_status(code: str, course_map: dict) -> str:
    """
    Return canonical status for a course code.
    Returns: "Satisfied" | "In Progress" | "Scheduled" | "Not Satisfied"
    """
    c = course_map.get(norm(code))
    if c is None:
        return "Not Satisfied"
    s = c.get("status", "")
    g = c.get("grade", "").upper()
    if s == "grade posted":
        if g in ("W", "DRP", "F", "NC"):
            return "Not Satisfied"
        # F3 requires C- or better — enforced in F3 logic below
        return "Satisfied"
    if s == "current":
        return "In Progress"
    if s == "scheduled":
        return "Scheduled"
    return "Not Satisfied"


def course_credits(code: str, course_map: dict) -> float:
    c = course_map.get(norm(code))
    return float(c.get("cr", 0)) if c else 0.0


def course_grade(code: str, course_map: dict) -> str:
    c = course_map.get(norm(code))
    return c.get("grade", "") if c else ""


def course_display(code: str, course_map: dict) -> str:
    """Return 'DEPT-NNNN CourseName' for display."""
    c = course_map.get(norm(code))
    if c:
        raw = c.get("raw", code.replace("_", "-"))
        name = c.get("name", "")
        return f"{raw} {name}".strip()
    return code.replace("_", "-")


# ─────────────────────────────────────────────────────────────────────────────
# RESULT DATACLASS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LAResult:
    area: str                   # "F1", "W3", "WI", "SI", etc.
    label: str                  # Requirement description
    course_display: str         # Course code + name shown in audit
    status: str                 # "Satisfied" | "In Progress" | "Scheduled" | "Not Satisfied"
    credits_required: float
    credits_earned: float
    grade: str = ""
    note: str = ""              # e.g., "Assigned to F3 (W3 also satisfied)"


# ─────────────────────────────────────────────────────────────────────────────
# CROSSOVER RULES
# ─────────────────────────────────────────────────────────────────────────────
# Source: LiberalArtsCrossOverClasses.pdf
# "AND" = course satisfies BOTH simultaneously (allowed because one is WI or SI)
# "OR"  = course can only satisfy ONE — system assigns to first unmet requirement

CROSSOVER_AND = {
    # course_code: [list of areas it satisfies simultaneously]
    norm("ARTH-3040"):      ["W4", "SI"],
    norm("BIBL-3000"):      ["W1", "WI"],
    norm("RLGN-3000"):      ["W1", "WI"],
    norm("BSNS-3120"):      ["W7", "WI"],
    norm("ENGL-2220"):      ["W7", "SI"],
    norm("ENGL-2500"):      ["W4", "WI"],
    norm("ENGL-3190"):      ["F2", "WI"],
    norm("ENGL-3580"):      ["F2", "WI"],
    norm("ENGR-2090"):      ["W7", "WI"],
    norm("HIST-2300"):      ["F2", "SI"],
    norm("HIST-3260"):      ["W7", "WI"],
    norm("HIST-3300"):      ["W7", "WI"],
    norm("HIST-3425"):      ["W7", "WI"],
    norm("HNRS-2125"):      ["F2", "SI"],
    norm("POSC-3320"):      ["W7", "WI"],
    norm("POSC-3450"):      ["W7", "WI"],
    norm("PSYC-3200"):      ["F2", "SI"],
    norm("SPAN-3010"):      ["W6", "WI"],
    norm("SPAN-3020"):      ["W7", "SI"],
}

CROSSOVER_OR = {
    # course_code: [area_option_1, area_option_2]
    # System assigns to first unmet area
    norm("HNRS-2110"):  ["F3", "W3"],
    norm("MLAN-2000"):  ["W6", "W7"],
    norm("SOCI-2450"):  ["F2", "W7"],
}

# Honors Program: HNRS-2110 satisfies F3 AND W3 AND F1 simultaneously for Honors students
# (overrides the OR rule above for Honors students)


# ─────────────────────────────────────────────────────────────────────────────
# W8 MAJOR-SPECIFIC COURSE MAPPING
# Source: W8-ExperientialWaysofKnowing(updated11.23).xlsx
# ─────────────────────────────────────────────────────────────────────────────

W8_MAJOR_COURSES = {
    # key: list of course codes that satisfy W8 for this major
    "political_science":        ["POSC_2810", "POSC_4800", "POSC_4810", "POSC_4820",
                                  "POSC_4860", "POSC_4915", "POSC_2840"],
    "polsci_philosophy_economics": ["POSC_2810", "POSC_4800", "POSC_4810", "POSC_4820",
                                     "POSC_4860", "POSC_4915", "POSC_2840"],
    "international_relations":  ["POSC_2810", "POSC_4800", "POSC_4810", "POSC_4820",
                                  "POSC_4860", "POSC_4915", "POSC_2840"],
    "accounting":               ["ACCT_2020", "ACCT_3500", "ACCT_3860", "ACCT_4020",
                                  "ACCT_4800", "BSNS_1050", "BSNS_4800"],
    "management":               ["BSNS_4800", "BSNS_4810", "BSNS_4820", "BSNS_4850"],
    "marketing":                ["BSNS_4800", "BSNS_4810", "BSNS_4820", "BSNS_4850"],
    "finance":                  ["BSNS_4800", "BSNS_4810", "BSNS_4820", "BSNS_4850"],
    "sport_marketing":          ["BSNS_4800", "BSNS_4810", "BSNS_4820", "BSNS_4850",
                                  "SPRL_4800"],
    "visual_communication":     ["ARTH_4800"],
    "communication":            ["COMM_4800", "COMM_4810", "COMM_4820"],
    "psychology":               ["PSYC_4800", "PSYC_4810", "PSYC_4820", "PSYC_4900"],
    "biology":                  ["BIOL_4800", "BIOL_4810", "BIOL_4820", "BIOL_4900"],
    "chemistry":                ["CHEM_4800", "CHEM_4810", "CHEM_4820", "CHEM_4900"],
    "nursing":                  ["NURS_4800", "NURS_4810", "NURS_4820"],
    "education":                ["EDUC_4800", "EDUC_4810", "EDUC_4820"],
    "elementary_education":     ["EDUC_4800", "EDUC_4810", "EDUC_4820"],
    "history":                  ["HIST_4800", "HIST_4810", "HIST_4820"],
    "math":                     ["MATH_4800", "MATH_4810", "MATH_4820"],
    "computer_science":         ["CPSC_4800", "CPSC_4810", "CPSC_4820"],
    "criminal_justice":         ["CRIM_4800", "CRIM_4810", "CRIM_4820"],
    "social_work":              ["SOWK_4800", "SOWK_4810", "SOWK_4820"],
    "exercise_science":         ["EXSC_4800", "EXSC_4810", "EXSC_4820"],
    "music":                    ["MUSC_4800", "MUSC_4810", "MUSC_4820", "MUPF_4800"],
    "theatre":                  ["THEA_4800", "THEA_4810", "THEA_4820"],
    "spanish":                  ["SPAN_4800", "SPAN_4810", "SPAN_4820"],
    "engineering":              ["ENGR_4800", "ENGR_4810", "ENGR_4820"],
    # Fallback for any major not listed
    "_default":                 ["LAWK_18EC"],
}

# POSC-2840 (Model UN) requires TWO semesters to satisfy W8
W8_TWO_SEMESTER_COURSES = {norm("POSC-2840")}


def _get_w8_courses(major_key: str) -> list:
    key = major_key.lower()
    for k, v in W8_MAJOR_COURSES.items():
        if k == key:
            return v
    # Partial match
    for k, v in W8_MAJOR_COURSES.items():
        if k in key or key in k:
            return v
    return W8_MAJOR_COURSES["_default"]


# ─────────────────────────────────────────────────────────────────────────────
# HONORS DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def is_honors_student(course_map: dict) -> bool:
    """Detect Honors enrollment by presence of HNRS-prefix courses."""
    return any(k.startswith("HNRS_") for k in course_map)


# ─────────────────────────────────────────────────────────────────────────────
# REQUIREMENT LISTS
# ─────────────────────────────────────────────────────────────────────────────

F2_COURSES = [
    "BIOL_3510", "PUBH_3510", "BSNS_3420", "CMIN_2270", "ENGL_3190", "ENGL_3580",
    "ENGR_2060", "HIST_2300", "HNRS_2125", "LART_1100", "MUED_1000", "PHIL_2000",
    "PHIL_2120", "POSC_2020", "PSYC_3200", "RLGN_3120", "SOCI_2450", "SPED_2400",
]

F5_COURSES = [
    "CPSC_1100", "CPSC_1200", "CPSC_1400", "LEAD_3100", "MATH_1100", "MATH_1250",
    "MATH_1300", "MATH_1400", "MATH_2010", "MATH_2120", "PSYC_2440",
]

F7_COURSES = ["DANC_3060", "NURS_1210", "PEHS_1000"]

W1_COURSES = [
    "BIBL_3000", "RLGN_3000", "BIBL_3410", "HNRS_3325", "PHIL_3250", "RLGN_3250",
    "RLGN_3010", "RLGN_3020", "RLGN_3100",
]

W2_COURSES = [
    "BIOL_1000", "BIOL_2070", "BIOL_2080", "BIOL_2210", "CHEM_1000", "CHEM_2110",
    "EXSC_2140", "HNRS_2210", "PHYS_1000", "PHYS_1020", "PHYS_1140", "PHYS_1240",
    "PHYS_2140", "PHYS_2240", "PSYC_3210",
]

W3_COURSES = [
    "HIST_2000", "HIST_2030", "HIST_2040", "HNRS_2110", "HIST_2110", "HIST_2120",
    "POSC_2100",
]

W4_AE_COURSES = [
    "ARTS_1210", "ARTS_1230", "ARTS_1250", "ARTH_2000", "COMM_2550",
    "ENGL_3590", "MUSC_2210",
]
W4_AP_COURSES = [
    "DANC_3510", "ENGL_2500", "MUED_2110", "MUSC_2110", "MUSC_2220", "THEA_2350",
]
W4_AX_COURSES = [
    "DANC_1120", "DANC_2120", "DANC_3120", "DANC_4120",
    "DANC_1220", "DANC_2220", "DANC_3220", "DANC_4220",
    "DANC_1320", "DANC_2320", "DANC_3320", "DANC_4320",
    "DANC_1420", "DANC_2420", "DANC_3420", "DANC_4420",
    "ENGL_2510",
    "MUPF_1010", "MUPF_1030", "MUPF_1070", "MUPF_1110", "MUPF_1220",
    "MUPF_1410", "MUPF_1420", "MUPF_1700", "MUPF_4890",
]

W5_COURSES = [
    "ECON_2010", "SOCI_2020", "EDUC_2110", "PSYC_2110", "LEAD_2300",
    "SOCI_2010", "SOCI_2100", "PSYC_2000", "HNRS_3311",
]

W6_COURSES = [
    "FREN_1010", "FREN_1020", "FREN_2010", "FREN_2020",
    "GERM_1010", "GERM_1020", "GERM_2010",
    "SPAN_1010", "SPAN_1020", "SPAN_2010", "SPAN_2020",
    "MLAN_2000", "SPAN_3010",
    "BIBL_2110", "BIBL_2120", "BIBL_2210", "BIBL_2220",
]

W7_COURSES = [
    "BIBL_3310", "BSNS_3120", "COMM_3050", "DANC_3000", "EDUC_3550",
    "ENGL_2220", "ENGR_2080", "ENGR_2090",
    "HIST_3100", "HIST_3190", "HIST_3240", "HIST_3250", "HIST_3260",
    "HIST_3280", "HIST_3320", "HIST_3300", "HIST_3360", "HIST_3370", "HIST_3425",
    "HNRS_3221", "LEAD_4550", "MLAN_2000", "MLAN_3400", "MUSC_2330",
    "POSC_3320", "POSC_3450", "SOCI_2450", "SOCI_3470",
    "SPAN_3020", "SPAN_3101", "SPAN_3102",
    # Additional foreign language courses from W6 list also count for W7
    "FREN_1010", "FREN_1020", "FREN_2010", "FREN_2020",
    "GERM_1010", "GERM_1020", "GERM_2010",
    "SPAN_1010", "SPAN_1020", "SPAN_2010", "SPAN_2020",
    "SPAN_3010",
    "BIBL_2110", "BIBL_2120", "BIBL_2210", "BIBL_2220",
]

WI_COURSES = [
    "ACCT_4900", "ARTH_3030", "ATRG_3440", "ATRG_4550",
    "BIBL_3000", "RLGN_3000", "BIOL_4050",
    "BIOL_4910", "BIOL_4920", "CHEM_4910", "CHEM_4920", "PHYS_4910", "PHYS_4920",
    "BSNS_3120", "BSNS_3330", "BSNS_4910", "CHEM_3100",
    "CMIN_4250", "COMM_2130", "COMM_2160", "COMM_3130", "COMM_3220", "COMM_3230",
    "COMM_3340", "CPSC_4950", "CRIM_2510", "SOCI_2510",
    "DANC_3010", "EDUC_3120", "EDUC_4120", "EDUC_4710",
    "ENGL_2500", "ENGL_3050", "ENGL_3110", "ENGL_3120", "ENGL_3140", "ENGL_3160",
    "ENGL_3180", "ENGL_3190", "ENGL_3500", "ENGL_3551", "ENGL_3580",
    "ENGL_4550", "ENGL_4700", "ENGL_4910",
    "ENGR_2090", "ENGR_4950", "ENGR_4960",
    "EXSC_4910",
    "HIST_3260", "HIST_3300", "HIST_3310", "HIST_3320", "HIST_3340",
    "HIST_3360", "HIST_3370", "HIST_3425", "HIST_3440", "HIST_3451",
    "HIST_3452", "HIST_3470", "HIST_3510",
    "HNRS_3221", "LEAD_4990", "MLAN_4900",
    "MUBS_3350", "MUBS_3500",
    "MUSC_3110", "MUSC_3120", "MUSC_3130", "MUSC_3140",
    "MUSC_3150", "MUSC_3160", "MUSC_3170", "MUSC_3180",
    "NURS_3391", "NURS_4470",
    "PEHS_3340", "PETE_2250", "PETE_4300", "PHYS_3100",
    "POSC_2400", "POSC_3211", "POSC_3310", "POSC_3320", "POSC_3450",
    "PSYC_2010", "PSYC_4510",
    "PUBH_3010", "PSYC_3010", "SOCI_3010",
    "PUBH_3700", "SOCI_3700",
    "RLGN_3300", "SPAN_3010", "SPED_3120",
]

SI_COURSES = [
    "ARTS_4950", "ATRG_4910", "BSNS_3210", "BSNS_4480",
    "CHEM_4910", "CHEM_4920", "BIOL_4910", "BIOL_4920", "PHYS_4910", "PHYS_4920",
    "CMIN_3910", "COMM_2550", "COMM_3420", "CRIM_4900", "CPSC_4960",
    "DANC_3050", "EDUC_4120", "EDUC_4710",
    "ENGL_3050", "ENGL_2220", "ENGR_4960",
    "EXSC_4920", "MLAN_4900",
    "HIST_2300", "HIST_2350", "HIST_4930",
    "HNRS_2125", "LART_4500", "LEAD_4990",
    "MATH_4000", "MUBS_3350", "BSNS_3330", "MUED_3110", "MUED_3350",
    "MUSC_4955", "MUTR_3210", "NURS_4960", "PETE_4900",
    "POSC_3211", "POSC_3212", "POSC_3370",
    "PSYC_3200", "PSYC_4110", "PSYC_4210", "PSYC_4520",
    "SOCI_4200", "SOCI_4950", "SOWK_4850",
    "SPAN_3020", "THEA_3210",
    "ARTH_3040",
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: find first satisfied course from a list
# ─────────────────────────────────────────────────────────────────────────────

def _find_best(course_list: list, course_map: dict, exclude: set = None) -> tuple:
    """
    Find the best course from a list that the student has taken.
    Priority: Satisfied > In Progress > Scheduled > Not Satisfied
    Returns (code, status) or (None, "Not Satisfied")
    Excludes codes already assigned to another requirement.
    """
    if exclude is None:
        exclude = set()
    best_code = None
    best_status = "Not Satisfied"
    priority = {"Satisfied": 0, "In Progress": 1, "Scheduled": 2, "Not Satisfied": 3}

    for code in course_list:
        n = norm(code)
        if n in exclude:
            continue
        s = course_status(code, course_map)
        if s != "Not Satisfied":
            if priority.get(s, 3) < priority.get(best_status, 3):
                best_code = code
                best_status = s

    return best_code, best_status


def _find_all_satisfied(course_list: list, course_map: dict, exclude: set = None) -> list:
    """Return all courses from list that are Satisfied, In Progress, or Scheduled."""
    if exclude is None:
        exclude = set()
    result = []
    for code in course_list:
        n = norm(code)
        if n in exclude:
            continue
        s = course_status(code, course_map)
        if s != "Not Satisfied":
            result.append((code, s))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# MAIN LA EVALUATOR
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_la(course_map: dict, catalog_year: str, major_key: str) -> list:
    """
    Evaluate all Liberal Arts requirements for a student.

    Args:
        course_map: Output of csv_parser.parse_csv()
        catalog_year: "2022-23", "2023-24", or "2024-25"
        major_key: Lowercase underscore major key (e.g. "political_science")

    Returns:
        List of LAResult objects in display order.
    """
    rows: list[LAResult] = []
    honors = is_honors_student(course_map)

    # Track which course codes have been "consumed" by a requirement
    # to enforce OR rules (a course can only satisfy one OR requirement)
    assigned: set = set()  # set of norm(code) strings

    def _assign(code: str):
        assigned.add(norm(code))

    def _is_assigned(code: str) -> bool:
        return norm(code) in assigned

    # ── F1 — Understanding College ───────────────────────────────────────────
    if honors and course_status("HNRS-2110", course_map) != "Not Satisfied":
        # Honors: HNRS-2110 satisfies F1, F3-I, F3-II, and W3 simultaneously
        f1_status = course_status("HNRS-2110", course_map)
        f1_display = course_display("HNRS-2110", course_map)
        f1_note = "Honors: HNRS-2110 satisfies F1, F3, and W3"
        # Do NOT assign HNRS-2110 yet — it will be assigned in F3 block
    else:
        lart_status = course_status("LART-1050", course_map)
        f1_display = course_display("LART-1050", course_map) if lart_status != "Not Satisfied" else "LART-1050"
        f1_status = lart_status
        f1_note = ""
        if lart_status != "Not Satisfied":
            _assign("LART-1050")

    rows.append(LAResult(
        area="F1",
        label="F1 LART-1050 Understanding College",
        course_display=f1_display,
        status=f1_status,
        credits_required=1,
        credits_earned=course_credits("LART-1050", course_map) if f1_status != "Not Satisfied" else 0,
        grade=course_grade("LART-1050", course_map),
        note=f1_note,
    ))

    # ── F2 — Civil Discourse & Critical Reasoning ────────────────────────────
    f2_code, f2_status = _find_best(F2_COURSES, course_map, assigned)
    # Check SOCI-2450 OR rule: if SOCI-2450 is assigned to W7 later, don't use it for F2
    # We handle this by checking OR courses last
    # For now, find best non-OR course first
    f2_non_or = [c for c in F2_COURSES if norm(c) not in {norm("SOCI-2450")}]
    f2_code_safe, f2_status_safe = _find_best(f2_non_or, course_map, assigned)
    if f2_status_safe != "Not Satisfied":
        f2_code, f2_status = f2_code_safe, f2_status_safe
    # If no non-OR course found, fall back to SOCI-2450 for F2 (it won't be available for W7)
    elif course_status("SOCI-2450", course_map) != "Not Satisfied" and not _is_assigned("SOCI-2450"):
        f2_code, f2_status = "SOCI-2450", course_status("SOCI-2450", course_map)

    if f2_code:
        _assign(f2_code)
        f2_display = course_display(f2_code, course_map)
    else:
        f2_display = "F2 course required"

    rows.append(LAResult(
        area="F2",
        label="F2 Civil Discourse & Critical Reasoning",
        course_display=f2_display,
        status=f2_status,
        credits_required=3,
        credits_earned=course_credits(f2_code, course_map) if f2_code and f2_status != "Not Satisfied" else 0,
        grade=course_grade(f2_code, course_map) if f2_code else "",
    ))

    # ── F3 — Written Communication (two rows: Writing I and Writing II) ──────
    # Honors: HNRS-2110 satisfies both F3-I and F3-II and W3 simultaneously
    if honors and course_status("HNRS-2110", course_map) != "Not Satisfied":
        hnrs2110_status = course_status("HNRS-2110", course_map)
        hnrs2110_display = course_display("HNRS-2110", course_map)
        _assign("HNRS-2110")

        rows.append(LAResult(
            area="F3",
            label="F3 Writing I — HNRS-2110 (Honors: satisfies F3 + W3 + F1)",
            course_display=hnrs2110_display,
            status=hnrs2110_status,
            credits_required=5,
            credits_earned=course_credits("HNRS-2110", course_map),
            grade=course_grade("HNRS-2110", course_map),
            note="Honors: HNRS-2110 satisfies F3-I, F3-II, and W3",
        ))
        rows.append(LAResult(
            area="F3",
            label="F3 Writing II — HNRS-2110 (Honors: satisfies F3-II)",
            course_display=hnrs2110_display,
            status=hnrs2110_status,
            credits_required=3,
            credits_earned=0,  # credits already counted in F3-I row
            grade=course_grade("HNRS-2110", course_map),
            note="Satisfied by HNRS-2110 above",
        ))
        # W3 will be marked satisfied by HNRS-2110 in W3 block below
        hnrs2110_satisfies_w3 = True
    else:
        hnrs2110_satisfies_w3 = False
        # Writing I: ENGL-1100 (4 cr) or ENGL-1110 (3 cr)
        w1_options = ["ENGL-1100", "ENGL-1110"]
        f3i_code, f3i_status = _find_best(w1_options, course_map, assigned)
        # Check grade requirement: C- or better
        if f3i_code and f3i_status == "Satisfied":
            g = course_grade(f3i_code, course_map).upper()
            grade_ok = g in ("A", "A-", "B+", "B", "B-", "C+", "C", "C-", "T")
            if not grade_ok:
                f3i_status = "Not Satisfied"
                f3i_code = None

        if f3i_code:
            _assign(f3i_code)
            f3i_display = course_display(f3i_code, course_map)
        else:
            f3i_display = "ENGL-1110 (or ENGL-1100)"

        rows.append(LAResult(
            area="F3",
            label="F3 Writing I — ENGL-1110 (or ENGL-1100 / HNRS-2110)",
            course_display=f3i_display,
            status=f3i_status,
            credits_required=3,
            credits_earned=course_credits(f3i_code, course_map) if f3i_code and f3i_status != "Not Satisfied" else 0,
            grade=course_grade(f3i_code, course_map) if f3i_code else "",
            note="Grade of C- or better required",
        ))

        # Writing II: ENGL-1120
        f3ii_status = course_status("ENGL-1120", course_map)
        if f3ii_status == "Satisfied":
            g = course_grade("ENGL-1120", course_map).upper()
            grade_ok = g in ("A", "A-", "B+", "B", "B-", "C+", "C", "C-", "T")
            if not grade_ok:
                f3ii_status = "Not Satisfied"
        f3ii_display = course_display("ENGL-1120", course_map) if f3ii_status != "Not Satisfied" else "ENGL-1120"
        if f3ii_status != "Not Satisfied":
            _assign("ENGL-1120")

        rows.append(LAResult(
            area="F3",
            label="F3 Writing II — ENGL-1120 (or HNRS-2110)",
            course_display=f3ii_display,
            status=f3ii_status,
            credits_required=3,
            credits_earned=course_credits("ENGL-1120", course_map) if f3ii_status != "Not Satisfied" else 0,
            grade=course_grade("ENGL-1120", course_map),
            note="Grade of C- or better required",
        ))

    # ── F4 — Speaking and Listening ──────────────────────────────────────────
    f4_status = course_status("COMM-1000", course_map)
    f4_display = course_display("COMM-1000", course_map) if f4_status != "Not Satisfied" else "COMM-1000"
    if f4_status != "Not Satisfied":
        _assign("COMM-1000")

    rows.append(LAResult(
        area="F4",
        label="F4 Speaking and Listening",
        course_display=f4_display,
        status=f4_status,
        credits_required=3,
        credits_earned=course_credits("COMM-1000", course_map) if f4_status != "Not Satisfied" else 0,
        grade=course_grade("COMM-1000", course_map),
    ))

    # ── F5 — Quantitative Reasoning ──────────────────────────────────────────
    f5_code, f5_status = _find_best(F5_COURSES, course_map, assigned)
    if f5_code:
        _assign(f5_code)
        f5_display = course_display(f5_code, course_map)
    else:
        f5_display = "F5 Quantitative Reasoning course required"

    rows.append(LAResult(
        area="F5",
        label="F5 Quantitative Reasoning",
        course_display=f5_display,
        status=f5_status,
        credits_required=3,
        credits_earned=course_credits(f5_code, course_map) if f5_code and f5_status != "Not Satisfied" else 0,
        grade=course_grade(f5_code, course_map) if f5_code else "",
    ))

    # ── F6 — Biblical Literacy ───────────────────────────────────────────────
    f6_status = course_status("BIBL-2000", course_map)
    f6_display = course_display("BIBL-2000", course_map) if f6_status != "Not Satisfied" else "BIBL-2000"
    if f6_status != "Not Satisfied":
        _assign("BIBL-2000")

    rows.append(LAResult(
        area="F6",
        label="F6 Biblical Literacy",
        course_display=f6_display,
        status=f6_status,
        credits_required=3,
        credits_earned=course_credits("BIBL-2000", course_map) if f6_status != "Not Satisfied" else 0,
        grade=course_grade("BIBL-2000", course_map),
    ))

    # ── F7 — Personal Wellness ───────────────────────────────────────────────
    f7_code, f7_status = _find_best(F7_COURSES, course_map, assigned)
    if f7_code:
        _assign(f7_code)
        f7_display = course_display(f7_code, course_map)
    else:
        f7_display = "F7 Personal Wellness course required"

    rows.append(LAResult(
        area="F7",
        label="F7 Personal Wellness",
        course_display=f7_display,
        status=f7_status,
        credits_required=2,
        credits_earned=course_credits(f7_code, course_map) if f7_code and f7_status != "Not Satisfied" else 0,
        grade=course_grade(f7_code, course_map) if f7_code else "",
    ))

    # ── W1 — Christian Ways of Knowing ───────────────────────────────────────
    if honors and course_status("HNRS-3325", course_map) != "Not Satisfied":
        w1_code, w1_status = "HNRS-3325", course_status("HNRS-3325", course_map)
    else:
        w1_code, w1_status = _find_best(W1_COURSES, course_map, assigned)

    # AND rule: BIBL/RLGN-3000 satisfies W1 AND WI simultaneously
    w1_also_wi = w1_code and norm(w1_code) in {norm("BIBL-3000"), norm("RLGN-3000")}

    if w1_code:
        _assign(w1_code)
        w1_display = course_display(w1_code, course_map)
    else:
        w1_display = "W1 Christian Ways of Knowing course required"

    rows.append(LAResult(
        area="W1",
        label="W1 Christian Ways of Knowing",
        course_display=w1_display,
        status=w1_status,
        credits_required=3,
        credits_earned=course_credits(w1_code, course_map) if w1_code and w1_status != "Not Satisfied" else 0,
        grade=course_grade(w1_code, course_map) if w1_code else "",
        note="Also satisfies WI" if w1_also_wi else "",
    ))

    # ── W2 — Scientific Ways of Knowing ──────────────────────────────────────
    if honors and course_status("HNRS-2210", course_map) != "Not Satisfied":
        w2_code, w2_status = "HNRS-2210", course_status("HNRS-2210", course_map)
    else:
        w2_code, w2_status = _find_best(W2_COURSES, course_map, assigned)

    if w2_code:
        _assign(w2_code)
        w2_display = course_display(w2_code, course_map)
    else:
        w2_display = "W2 Scientific Ways of Knowing course required (4 cr)"

    rows.append(LAResult(
        area="W2",
        label="W2 Scientific Ways of Knowing",
        course_display=w2_display,
        status=w2_status,
        credits_required=4,
        credits_earned=course_credits(w2_code, course_map) if w2_code and w2_status != "Not Satisfied" else 0,
        grade=course_grade(w2_code, course_map) if w2_code else "",
    ))

    # ── W3 — Civic Ways of Knowing ────────────────────────────────────────────
    if hnrs2110_satisfies_w3:
        w3_status = course_status("HNRS-2110", course_map)
        w3_display = course_display("HNRS-2110", course_map)
        w3_note = "Satisfied by HNRS-2110 (Honors)"
    else:
        # HNRS-2110 is an OR course for non-Honors: F3 OR W3
        # If HNRS-2110 was not used for F3 (non-honors), check if it's available for W3
        w3_candidates = [c for c in W3_COURSES if not _is_assigned(norm(c))]
        w3_code, w3_status = _find_best(w3_candidates, course_map, assigned)
        if w3_code:
            _assign(w3_code)
            w3_display = course_display(w3_code, course_map)
        else:
            w3_display = "W3 Civic Ways of Knowing course required"
        w3_note = ""

    rows.append(LAResult(
        area="W3",
        label="W3 Civic Ways of Knowing",
        course_display=w3_display,
        status=w3_status,
        credits_required=3,
        credits_earned=course_credits("HNRS-2110", course_map) if hnrs2110_satisfies_w3 else
                       (course_credits(w3_code if not hnrs2110_satisfies_w3 else "HNRS-2110", course_map)
                        if w3_status != "Not Satisfied" else 0),
        grade=course_grade("HNRS-2110" if hnrs2110_satisfies_w3 else
                           (w3_code if not hnrs2110_satisfies_w3 else ""), course_map),
        note=w3_note,
    ))

    # ── W5 — Social and Behavioral Ways of Knowing ───────────────────────────
    # (W4 comes after W5 in the display order based on the Landon Bair audit)
    if honors and course_status("HNRS-3311", course_map) != "Not Satisfied":
        w5_code, w5_status = "HNRS-3311", course_status("HNRS-3311", course_map)
    else:
        w5_code, w5_status = _find_best(W5_COURSES, course_map, assigned)

    if w5_code:
        _assign(w5_code)
        w5_display = course_display(w5_code, course_map)
    else:
        w5_display = "W5 Social & Behavioral Ways of Knowing course required"

    rows.append(LAResult(
        area="W5",
        label="W5 Social and Behavioral Ways of Knowing",
        course_display=w5_display,
        status=w5_status,
        credits_required=3,
        credits_earned=course_credits(w5_code, course_map) if w5_code and w5_status != "Not Satisfied" else 0,
        grade=course_grade(w5_code, course_map) if w5_code else "",
    ))

    # ── W6 — Modern Languages ─────────────────────────────────────────────────
    # MLAN-2000 is an OR course: W6 OR W7 — assign to W6 first
    w6_candidates = [c for c in W6_COURSES if not _is_assigned(norm(c))]
    w6_code, w6_status = _find_best(w6_candidates, course_map, assigned)
    if w6_code:
        _assign(w6_code)
        w6_display = course_display(w6_code, course_map)
    else:
        w6_display = "W6 Modern Languages course required (4 cr)"

    rows.append(LAResult(
        area="W6",
        label="W6 Modern Languages",
        course_display=w6_display,
        status=w6_status,
        credits_required=4,
        credits_earned=course_credits(w6_code, course_map) if w6_code and w6_status != "Not Satisfied" else 0,
        grade=course_grade(w6_code, course_map) if w6_code else "",
    ))

    # ── W7 — Global/Intercultural Ways of Knowing ─────────────────────────────
    if honors and course_status("HNRS-3221", course_map) != "Not Satisfied":
        w7_code, w7_status = "HNRS-3221", course_status("HNRS-3221", course_map)
        w7_also_wi = True
    else:
        w7_candidates = [c for c in W7_COURSES if not _is_assigned(norm(c))]
        w7_code, w7_status = _find_best(w7_candidates, course_map, assigned)
        w7_also_wi = w7_code and norm(w7_code) in {
            norm(c) for c in ["BSNS-3120", "ENGR-2090", "HIST-3260", "HIST-3300",
                               "HIST-3425", "HNRS-3221", "POSC-3320", "POSC-3450"]
        }

    if w7_code:
        _assign(w7_code)
        w7_display = course_display(w7_code, course_map)
    else:
        w7_display = "W7 Global/Intercultural Ways of Knowing course required"

    rows.append(LAResult(
        area="W7",
        label="W7 Global/Intercultural Ways of Knowing",
        course_display=w7_display,
        status=w7_status,
        credits_required=3,
        credits_earned=course_credits(w7_code, course_map) if w7_code and w7_status != "Not Satisfied" else 0,
        grade=course_grade(w7_code, course_map) if w7_code else "",
        note="Also satisfies WI" if w7_also_wi else "",
    ))

    # ── W4 — Aesthetic Ways of Knowing ───────────────────────────────────────
    # AE (Integrative) takes priority; if not available, need AP + AX
    w4_ae_candidates = [c for c in W4_AE_COURSES if not _is_assigned(norm(c))]
    w4_ae_code, w4_ae_status = _find_best(w4_ae_candidates, course_map, assigned)

    if w4_ae_code and w4_ae_status != "Not Satisfied":
        _assign(w4_ae_code)
        w4_display = course_display(w4_ae_code, course_map)
        w4_status = w4_ae_status
        w4_credits = course_credits(w4_ae_code, course_map)
        w4_grade = course_grade(w4_ae_code, course_map)
    else:
        # Try AP + AX
        w4_ap_candidates = [c for c in W4_AP_COURSES if not _is_assigned(norm(c))]
        w4_ax_candidates = [c for c in W4_AX_COURSES if not _is_assigned(norm(c))]
        ap_code, ap_status = _find_best(w4_ap_candidates, course_map, assigned)
        ax_code, ax_status = _find_best(w4_ax_candidates, course_map, assigned)

        if ap_code and ax_code:
            _assign(ap_code)
            _assign(ax_code)
            w4_display = f"{course_display(ap_code, course_map)} + {course_display(ax_code, course_map)}"
            if ap_status == "Satisfied" and ax_status == "Satisfied":
                w4_status = "Satisfied"
            elif "Not Satisfied" not in (ap_status, ax_status):
                w4_status = "In Progress"
            else:
                w4_status = "In Progress"
            w4_credits = course_credits(ap_code, course_map) + course_credits(ax_code, course_map)
            w4_grade = ""
        elif ap_code or ax_code:
            code = ap_code or ax_code
            _assign(code)
            w4_display = course_display(code, course_map) + " (need AP + AX pair)"
            w4_status = "In Progress"
            w4_credits = course_credits(code, course_map)
            w4_grade = course_grade(code, course_map)
        else:
            w4_display = "W4 Aesthetic Ways of Knowing course required"
            w4_status = "Not Satisfied"
            w4_credits = 0
            w4_grade = ""

    rows.append(LAResult(
        area="W4",
        label="W4 Aesthetic Ways of Knowing",
        course_display=w4_display,
        status=w4_status,
        credits_required=3,
        credits_earned=w4_credits if w4_status != "Not Satisfied" else 0,
        grade=w4_grade,
    ))

    # ── W8 — Experiential Ways of Knowing ────────────────────────────────────
    w8_options = _get_w8_courses(major_key)
    w8_code = None
    w8_status = "Not Satisfied"
    w8_note = ""

    for code in w8_options:
        n = norm(code)
        s = course_status(code, course_map)
        if s == "Not Satisfied":
            continue

        # Special rule: POSC-2840 requires TWO semesters
        if n in W8_TWO_SEMESTER_COURSES:
            # Count how many times this course appears in the raw CSV
            # (The parser deduplicates, so we need to check the raw count)
            # Since parser deduplicates, we check if credits >= 6 (2 semesters × 3 cr)
            cr = course_credits(code, course_map)
            if cr < 6:
                w8_note = "POSC-2840 requires 2 semesters (6 cr) to satisfy W8"
                continue  # Not yet satisfied

        w8_code = code
        w8_status = s
        break

    if w8_code:
        _assign(w8_code)
        w8_display = course_display(w8_code, course_map)
    else:
        w8_display = f"W8 Experiential course required ({', '.join(w8_options[:3])}...)"

    rows.append(LAResult(
        area="W8",
        label="W8 Experiential Ways of Knowing",
        course_display=w8_display,
        status=w8_status,
        credits_required=3,
        credits_earned=course_credits(w8_code, course_map) if w8_code and w8_status != "Not Satisfied" else 0,
        grade=course_grade(w8_code, course_map) if w8_code else "",
        note=w8_note,
    ))

    # ── WI — Advanced Writing Competency (2 courses, ≥1 upper-div) ───────────
    # AND rule: some courses satisfy both another requirement AND WI simultaneously
    # We collect WI courses from the full WI list, but AND-rule courses are already assigned
    # They still count for WI — the AND rule allows this

    wi_satisfied = []
    wi_all = list(WI_COURSES)

    # Add AND-rule courses that were already assigned (they still count for WI)
    and_wi_codes = [
        c for c, areas in CROSSOVER_AND.items()
        if "WI" in areas and c in assigned
    ]
    # Also check if HNRS-3221 was assigned (it satisfies W7 AND WI)
    if honors and norm("HNRS-3221") in assigned:
        and_wi_codes.append(norm("HNRS-3221"))

    for code in and_wi_codes:
        s = course_status(code, course_map)
        if s in ("Satisfied", "In Progress", "Scheduled"):
            wi_satisfied.append((code, s))

    # Find additional WI courses not yet assigned
    for code in wi_all:
        n = norm(code)
        if n in assigned:
            continue  # Skip already-assigned non-AND courses
        s = course_status(code, course_map)
        if s in ("Satisfied", "In Progress", "Scheduled"):
            wi_satisfied.append((code, s))
            if len(wi_satisfied) >= 3:
                break

    # Need at least 2 WI courses, at least 1 upper-division (3000+)
    wi_count = len(wi_satisfied)
    wi_upper = sum(1 for code, _ in wi_satisfied
                   if re.search(r"_[34]\d{3}", norm(code)))

    for i, (code, s) in enumerate(wi_satisfied[:3]):
        wi_num = i + 1
        upper_flag = bool(re.search(r"_[34]\d{3}", norm(code)))
        rows.append(LAResult(
            area="WI",
            label=f"WI Writing Intensive #{wi_num} — {'must be upper-div (3000+)' if wi_num == 2 else 'must be from approved WI list'}",
            course_display=course_display(code, course_map),
            status=s,
            credits_required=3,
            credits_earned=course_credits(code, course_map) if s != "Not Satisfied" else 0,
            grade=course_grade(code, course_map),
            note="Upper-division" if upper_flag else "",
        ))

    # If fewer than 2 WI courses found, add placeholder rows
    for i in range(len(wi_satisfied), 2):
        wi_num = i + 1
        rows.append(LAResult(
            area="WI",
            label=f"WI Writing Intensive #{wi_num} — {'must be upper-div (3000+)' if wi_num >= 2 else 'must be from approved WI list'}",
            course_display="WI approved course required",
            status="Not Satisfied",
            credits_required=3,
            credits_earned=0,
            grade="",
        ))

    # ── SI — Speaking Intensive ───────────────────────────────────────────────
    # Honors: HNRS-2125 satisfies F2 AND SI simultaneously
    si_code = None
    si_status = "Not Satisfied"

    # Check AND-rule SI courses already assigned
    and_si_codes = [
        c for c, areas in CROSSOVER_AND.items()
        if "SI" in areas and c in assigned
    ]
    if and_si_codes:
        si_code = and_si_codes[0]
        si_status = course_status(si_code, course_map)

    if si_status == "Not Satisfied":
        # Find SI course not yet assigned (excluding COMM-1000 itself)
        si_candidates = [c for c in SI_COURSES
                         if norm(c) != norm("COMM-1000") and not _is_assigned(norm(c))]
        si_code, si_status = _find_best(si_candidates, course_map, assigned)
        if si_code:
            _assign(si_code)

    si_display = course_display(si_code, course_map) if si_code and si_status != "Not Satisfied" else "SI approved course required (beyond COMM-1000)"

    rows.append(LAResult(
        area="SI",
        label="SI Speaking Intensive — 1 course required from approved SI list",
        course_display=si_display,
        status=si_status,
        credits_required=3,
        credits_earned=course_credits(si_code, course_map) if si_code and si_status != "Not Satisfied" else 0,
        grade=course_grade(si_code, course_map) if si_code else "",
    ))

    return rows
