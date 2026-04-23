"""
Test script: Michael Baylor — Electrical Engineering BS (2022-23)
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

import engines.sport_marketing as sm
importlib.reload(sm)
from requirements.non_fsb_programs import get_non_fsb_requirements
from main import _build_major_rows

# ── 1. Parse CSV ──────────────────────────────────────────────────────────────
raw_courses = sm.parse_csv("/home/ubuntu/upload/MichaelBaylor.csv")

# ── 2. Load program requirements ──────────────────────────────────────────────
major = "electrical_engineering_bs"
catalog_year = "2022-23"
prog_reqs = get_non_fsb_requirements(major, catalog_year)
print(f"=== Program: {prog_reqs.get('name')} ({catalog_year}) ===")

# ── 3. Run audit ──────────────────────────────────────────────────────────────
rows = _build_major_rows(prog_reqs, raw_courses, sm)

print(f"\n{'Requirement':<65} {'Status':<15} {'Course'}")
print("-" * 110)
for row in rows:
    req = row.get("label", "")
    status = row.get("status", "")
    course = row.get("course") or {}
    course_code = course.get("raw", "") if course else ""
    marker = "!!" if status not in ("Satisfied", "Current", "Scheduled", "Waived") else "  "
    print(f"{marker} {req:<63} {status:<15} {course_code}")

not_sat = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Scheduled", "Waived")]
print(f"\n=== SUMMARY: {len(not_sat)} unsatisfied ===")
for r in not_sat:
    print(f"  !! {r['label']}")

# ── 4. Check ENGR-4240 specifically ──────────────────────────────────────────
print("\n=== ENGR-4240 on transcript ===")
for c in raw_courses:
    if '4240' in c['code']:
        print(f"  {c['code']:30s} {c['cr']:4.1f} cr  [{c['status']:15s}]  {c['grade']}")
