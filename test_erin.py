"""
Test script: Erin Powell — Dance Major (2022-23)
Tests all four track concentrations to identify which one she satisfies.
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

import engines.sport_marketing as sm
importlib.reload(sm)
from requirements.non_fsb_programs import get_non_fsb_requirements
from main import _build_major_rows

# ── 1. Parse CSV ──────────────────────────────────────────────────────────────
raw_courses = sm.parse_csv("/home/ubuntu/upload/ErinPowell.csv")

print("=== Erin Powell's Transcript (DANC courses only) ===")
for c in sorted(raw_courses, key=lambda x: x['code']):
    if c['code'].startswith('DANC_') or c['code'].startswith('ACCT_') or c['code'].startswith('BSNS_') or c['code'].startswith('NURS_') or c['code'].startswith('PEHS_'):
        print(f"  {c['code']:30s} {c['cr']:4.1f} cr  [{c['status']:15s}]  {c['grade']}  {c['name']}")

# ── 2. Load program requirements ──────────────────────────────────────────────
major = "dance_major"
catalog_year = "2022-23"
prog_reqs = get_non_fsb_requirements(major, catalog_year)
print(f"\n=== Program: {prog_reqs.get('name')} ({catalog_year}) ===")
print(f"Tracks available: {list(prog_reqs.get('concentrations', {}).keys())}")

# ── 3. Run audit for each track ───────────────────────────────────────────────
tracks = list(prog_reqs.get("concentrations", {}).keys())
for track in tracks:
    rows = _build_major_rows(prog_reqs, raw_courses, sm, concentration=track)
    not_sat = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Scheduled", "Waived")]
    print(f"\n=== Track: {track} — {len(not_sat)} unsatisfied ===")
    print(f"{'Requirement':<65} {'Status':<15} {'Course'}")
    print("-" * 110)
    for row in rows:
        req = row.get("label", "")
        status = row.get("status", "")
        course = row.get("course") or {}
        course_code = course.get("raw", "") if course else ""
        marker = "!!" if status not in ("Satisfied", "Current", "Scheduled", "Waived") else "  "
        print(f"{marker} {req:<63} {status:<15} {course_code}")

# ── 4. Summary ────────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
for track in tracks:
    rows = _build_major_rows(prog_reqs, raw_courses, sm, concentration=track)
    not_sat = [r for r in rows if r.get("status") not in ("Satisfied", "Current", "Scheduled", "Waived")]
    print(f"  {track:15s}: {len(not_sat):2d} unsatisfied — {[r['label'] for r in not_sat]}")
