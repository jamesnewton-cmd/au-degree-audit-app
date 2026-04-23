"""
Test script: Kade Hill — Exercise Science (2022-23)
Tests all three concentrations using the proper concentration= parameter.
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

import engines.sport_marketing as sm
importlib.reload(sm)
from requirements.non_fsb_programs import get_non_fsb_requirements
from main import _build_major_rows

raw_courses = sm.parse_csv("/home/ubuntu/upload/KadeHill-ExerciseScience.csv")

major = "exercise_science"
catalog_year = "2022-23"
prog_reqs = get_non_fsb_requirements(major, catalog_year)

concentrations = list(prog_reqs.get("concentrations", {}).keys())
print(f"Available concentrations: {concentrations}\n")

for conc in concentrations:
    rows = _build_major_rows(prog_reqs, raw_courses, sm, concentration=conc)
    not_sat = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Scheduled", "Waived")]
    print(f"=== Concentration: {conc} — {len(not_sat)} unsatisfied ===")
    for r in not_sat:
        print(f"  !! {r['label']}")
    print()

# Full audit for Pre-Health
print("\n=== FULL AUDIT: Pre-Health Concentration ===")
rows = _build_major_rows(prog_reqs, raw_courses, sm, concentration="Pre-Health")
print(f"{'Requirement':<65} {'Status':<15} {'Course'}")
print("-" * 110)
for row in rows:
    req = row.get("label", "")
    status = row.get("status", "")
    course = row.get("course") or {}
    course_code = course.get("raw", "") if course else ""
    marker = "!!" if status not in ("Satisfied", "Current", "Scheduled", "Waived") else "  "
    print(f"{marker} {req:<63} {status:<15} {course_code}")
