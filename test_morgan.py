"""
Test script: Morgan Ferguson — Criminal Justice (2022-23)
Uses the real parse_csv from sport_marketing (same as main.py does).
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

from requirements.non_fsb_programs import get_non_fsb_requirements
from engines.sport_marketing import parse_csv

# ── 1. Parse CSV using the real engine ───────────────────────────────────────
raw_courses = parse_csv("/home/ubuntu/upload/MorganFerguson.csv")

print("=== Morgan Ferguson's Transcript (normalized) ===")
for c in raw_courses:
    print(f"  {c['code']:30s} {c['cr']:4.1f} cr  [{c['status']}]  {c['grade']}")

# ── 2. Load program requirements ──────────────────────────────────────────────
major = "criminal_justice_major"
catalog_year = "2022-23"
prog_reqs = get_non_fsb_requirements(major, catalog_year)
print(f"\n=== Program: {prog_reqs.get('name')} ({catalog_year}) ===")
print(f"Required: {prog_reqs.get('required')}")
print(f"Choose_one: {prog_reqs.get('choose_one')}")
print(f"Elective groups: {prog_reqs.get('elective_groups')}")

# ── 3. Run _build_major_rows ──────────────────────────────────────────────────
sm_mod = importlib.import_module("engines.sport_marketing")
from main import _build_major_rows

rows = _build_major_rows(prog_reqs, raw_courses, sm_mod)

print("\n=== Major Audit Rows ===")
print(f"{'Requirement':<55} {'Status':<15} {'Course'}")
print("-" * 90)
for row in rows:
    req = row.get("label", "")
    status = row.get("status", "")
    course = row.get("course") or {}
    course_code = course.get("raw", "") if course else ""
    print(f"{req:<55} {status:<15} {course_code}")

# ── 4. Summary ────────────────────────────────────────────────────────────────
not_satisfied = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Waived")]
print(f"\n=== NOT Satisfied / Missing ===")
if not_satisfied:
    for r in not_satisfied:
        print(f"  !! {r.get('label')} — {r.get('status')}")
else:
    print("  All requirements satisfied or current!")

# ── 5. Check CRIM elective hours ─────────────────────────────────────────────
crim_courses = [c for c in raw_courses if c["code"].startswith("CRIM_") and c["status"] in ("grade posted", "current")]
print(f"\n=== CRIM courses on transcript ===")
for c in crim_courses:
    print(f"  {c['code']:20s} {c['cr']:4.1f} cr  [{c['status']}]  {c['name']}")
total_crim = sum(c["cr"] for c in crim_courses)
print(f"  Total CRIM credits: {total_crim}")
