"""
Test script: Griffin Craig — Cybersecurity Major (2022-23)
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

import engines.sport_marketing as sm
importlib.reload(sm)
from requirements.non_fsb_programs import get_non_fsb_requirements
from main import _build_major_rows

# ── 1. Parse CSV ──────────────────────────────────────────────────────────────
raw_courses = sm.parse_csv("/home/ubuntu/upload/GriffinCraig.csv")

print("=== Griffin Craig's Transcript (normalized) ===")
for c in raw_courses:
    print(f"  {c['code']:40s} {c['cr']:4.1f} cr  [{c['status']}]  {c['grade']}")

# ── 2. Load program requirements ──────────────────────────────────────────────
major = "cybersecurity_major"
catalog_year = "2022-23"
prog_reqs = get_non_fsb_requirements(major, catalog_year)
print(f"\n=== Program: {prog_reqs.get('name')} ({catalog_year}) ===")
print(f"Required: {prog_reqs.get('required')}")
print(f"Choose_one: {prog_reqs.get('choose_one')}")
print(f"Elective groups: {prog_reqs.get('elective_groups')}")

# ── 3. Run _build_major_rows ──────────────────────────────────────────────────
rows = _build_major_rows(prog_reqs, raw_courses, sm)

print("\n=== Major Audit Rows ===")
print(f"{'Requirement':<60} {'Status':<15} {'Course'}")
print("-" * 100)
for row in rows:
    req = row.get("label", "")
    status = row.get("status", "")
    course = row.get("course") or {}
    course_code = course.get("raw", "") if course else ""
    print(f"{req:<60} {status:<15} {course_code}")

# ── 4. Summary ────────────────────────────────────────────────────────────────
not_satisfied = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Waived")]
print(f"\n=== NOT Satisfied / Missing ===")
if not_satisfied:
    for r in not_satisfied:
        print(f"  !! {r.get('label')} — {r.get('status')}")
else:
    print("  All requirements satisfied or current!")

# ── 5. Check elective hours ───────────────────────────────────────────────────
print(f"\n=== CPSC/POSC/CRIM elective-eligible courses ===")
elective_eligible = [
    c for c in raw_courses
    if (c["code"].startswith("CPSC_") and int(c["code"].split("_")[1][:4]) >= 2000
        or c["code"] in ("CRIM_2520", "POSC_3310", "POSC_3250"))
    and c["status"] in ("grade posted", "current")
]
for c in elective_eligible:
    print(f"  {c['code']:30s} {c['cr']:4.1f} cr  [{c['status']}]  {c['name']}")

# ── 6. Check MATH-2200 vs CPSC-2250 ──────────────────────────────────────────
print(f"\n=== MATH-2200 / CPSC-2250 check ===")
for code in ["MATH_2200", "CPSC_2250"]:
    c = next((x for x in raw_courses if x["code"] == code), None)
    if c:
        print(f"  {code}: status={c['status']}  grade={c['grade']}  cr={c['cr']}")
    else:
        print(f"  {code}: NOT on transcript")
