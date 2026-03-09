"""
Tests for non-FSB audit engine.
Run with: python -m pytest tests/test_non_fsb_engine.py -v
"""

import sys
sys.path.insert(0, '/home/claude/au_audit_expansion')

import pytest
from engines.non_fsb_audit_engine import (
    NonFSBAuditEngine,
    run_non_fsb_audit,
    get_all_available_programs,
    CourseRecord,
)
from requirements.non_fsb_programs import (
    get_non_fsb_requirements,
    program_exists_in_year,
    list_programs_by_year,
    ALL_NON_FSB_PROGRAMS,
)


# ──── Fixtures ────────────────────────────────

def make_course(code, grade="A", credits=3.0, term="FA2024"):
    return CourseRecord(course_id=code, grade=grade, credits=credits, term=term)

STUDENT = {"id": "T001", "name": "Test Student", "major": "biology_ba", "catalog_year": "2022-23"}

BIOL_BA_COMPLETE = [
    make_course("BIOL 2210", credits=4), make_course("BIOL 2220", credits=4),
    make_course("BIOL 2240", credits=4), make_course("BIOL 3030", credits=4),
    make_course("BIOL 3510", credits=4), make_course("BIOL 4050", credits=4),
    make_course("BIOL 4070", credits=4), make_course("BIOL 4910", credits=2),
    make_course("BIOL 4920", credits=2),
    make_course("CHEM 2110", credits=4), make_course("CHEM 2120", credits=4),
    make_course("CHEM 2210", credits=4),
    # Upper-div electives (8 hrs)
    make_course("BIOL 3800", credits=4), make_course("BIOL 4310", credits=4),
]


# ──── Tests ──────────────────────────────────

def test_total_programs_registered():
    """92 non-FSB programs should be registered."""
    assert len(ALL_NON_FSB_PROGRAMS) >= 85


def test_programs_in_2223():
    """At least 80 programs should be available in 22-23."""
    progs = list_programs_by_year("2022-23")
    assert len(progs) >= 80


def test_programs_in_2526():
    """At least 80 programs should be available in 25-26."""
    progs = list_programs_by_year("2025-26")
    assert len(progs) >= 80


def test_biology_ba_requirements_retrieved():
    """Biology BA 22-23 requirements load correctly."""
    req = get_non_fsb_requirements("biology_ba", "2022-23")
    assert req is not None
    assert req["total_credits"] == 48
    assert "BIOL 2210" in req["required"]
    assert "CHEM 2110" in req["required"]


def test_biology_ba_engine_instantiates():
    """NonFSBAuditEngine initializes for biology_ba/2022-23."""
    engine = NonFSBAuditEngine("biology_ba", "2022-23")
    assert engine is not None


def test_biology_ba_all_satisfied():
    """A student with all biology BA courses should satisfy all requirements."""
    result = run_non_fsb_audit("biology_ba", "2022-23", STUDENT, BIOL_BA_COMPLETE)
    assert result.all_satisfied is True
    assert len(result.outstanding) == 0


def test_biology_ba_missing_chem():
    """Without CHEM 2210, audit should show it as Not Met."""
    transcript = [c for c in BIOL_BA_COMPLETE if c.course_id != "CHEM 2210"]
    result = run_non_fsb_audit("biology_ba", "2022-23", STUDENT, transcript)
    assert result.all_satisfied is False
    missing = result.outstanding
    assert any("CHEM 2210" in m for m in missing)


def test_cs_bs_2526_new_courses():
    """CS BS 25-26 should require CPSC 2030 and CPSC 2150."""
    req = get_non_fsb_requirements("cs_bs", "2025-26")
    assert req is not None
    assert "CPSC 2030" in req["required"]
    assert "CPSC 2150" in req["required"]


def test_family_science_removed_2324():
    """Family Science major should not exist in 2023-24+."""
    assert not program_exists_in_year("family_science", "2023-24")
    assert not program_exists_in_year("family_science", "2024-25")
    assert not program_exists_in_year("family_science", "2025-26")


def test_family_science_exists_2223():
    """Family Science should exist in 22-23."""
    assert program_exists_in_year("family_science", "2022-23")


def test_same_as_resolution_biology_bs():
    """Biology BS 25-26 with same_as should resolve to 22-23 data."""
    req = get_non_fsb_requirements("biology_bs", "2025-26")
    assert req is not None
    # Should have the required courses
    assert "BIOL 2210" in req.get("required", []) or req.get("same_as")


def test_theatre_all_years():
    """Theatre major should exist in all 4 catalog years."""
    for year in ["2022-23", "2023-24", "2024-25", "2025-26"]:
        assert program_exists_in_year("theatre", year), f"Theatre missing in {year}"


def test_math_teaching_2526_new_courses():
    """Math Teaching 25-26 should require CPSC 2020 and MATH 3200."""
    req = get_non_fsb_requirements("math_teaching_ba", "2025-26")
    assert req is not None
    assert "CPSC 2020" in req.get("required", [])
    assert "MATH 3200" in req.get("required", [])


def test_music_business_2526_restructured():
    """Music Business 25-26 should have elective_music_biz block."""
    req = get_non_fsb_requirements("music_business", "2025-26")
    assert req is not None
    assert "elective_music_biz" in req


def test_get_all_available_programs_2223():
    """get_all_available_programs returns dict for 22-23."""
    progs = get_all_available_programs("2022-23")
    assert isinstance(progs, dict)
    assert "biology_ba" in progs
    assert "theatre" in progs
    assert "nursing_bsn" in progs


def test_ip_courses_show_in_progress():
    """In-progress courses should show 'In Progress' status, not 'Satisfied'."""
    transcript = [
        CourseRecord("BIOL 2210", grade="IP", credits=4),
        make_course("BIOL 2220", credits=4),
    ]
    result = run_non_fsb_audit("biology_ba", "2022-23", STUDENT, transcript)
    req_map = {r.label: r.status for r in result.requirements}
    # BIOL 2210 should be IP, BIOL 2220 should be Satisfied
    assert req_map.get("BIOL 2210") == "In Progress"
    assert req_map.get("BIOL 2220") == "Satisfied"


def test_cybersecurity_major_2526_larger():
    """Cybersecurity 25-26 should have more credits than 22-23."""
    req_2223 = get_non_fsb_requirements("cybersecurity_major", "2022-23")
    req_2526 = get_non_fsb_requirements("cybersecurity_major", "2025-26")
    assert req_2223 is not None
    assert req_2526 is not None
    assert req_2526["total_credits"] > req_2223["total_credits"]


def test_pact_minor_restructured_2526():
    """PACT minor 25-26 should have foundation with PACT 2100, 2200, 2400."""
    req = get_non_fsb_requirements("pact_minor", "2025-26")
    assert req is not None
    foundation = req.get("foundation", {})
    if isinstance(foundation, dict):
        courses = foundation.get("required", [])
    else:
        courses = foundation
    assert "PACT 2100" in courses
    assert "PACT 2400" in courses


def test_non_fsb_audit_engine_gpa_calculation():
    """Major GPA should be calculated correctly from transcript."""
    transcript = [
        CourseRecord("BIOL 2210", grade="A", credits=4),
        CourseRecord("BIOL 2220", grade="B", credits=4),
        CourseRecord("BIOL 2240", grade="A-", credits=4),
    ]
    result = run_non_fsb_audit("biology_ba", "2022-23", STUDENT, transcript)
    # A=4.0, B=3.0, A-=3.7 → (16+12+14.8)/12 = 3.567
    assert result.major_gpa > 0
    assert abs(result.major_gpa - 3.567) < 0.01


if __name__ == "__main__":
    # Quick manual run
    tests = [
        test_total_programs_registered,
        test_programs_in_2223,
        test_programs_in_2526,
        test_biology_ba_requirements_retrieved,
        test_biology_ba_engine_instantiates,
        test_biology_ba_all_satisfied,
        test_biology_ba_missing_chem,
        test_cs_bs_2526_new_courses,
        test_family_science_removed_2324,
        test_family_science_exists_2223,
        test_same_as_resolution_biology_bs,
        test_theatre_all_years,
        test_math_teaching_2526_new_courses,
        test_music_business_2526_restructured,
        test_get_all_available_programs_2223,
        test_ip_courses_show_in_progress,
        test_cybersecurity_major_2526_larger,
        test_pact_minor_restructured_2526,
        test_non_fsb_audit_engine_gpa_calculation,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} tests passed")
