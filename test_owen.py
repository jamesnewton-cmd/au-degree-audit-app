"""Test Owen Reenie's Biochemistry BS (2022-23) audit using main.py's approach."""
import sys
sys.path.insert(0, '/home/ubuntu/au-original-restored')

import importlib
from engines import sport_marketing as sm_mod
from requirements.non_fsb_programs import get_non_fsb_requirements
from main import _build_major_rows, _compute_gpa, _norm_code

csv_path = '/home/ubuntu/upload/OwenReenie.csv'
major = 'biochemistry_bs'
catalog_year = '2022-23'

raw_courses = sm_mod.parse_csv(csv_path)
prog_reqs = get_non_fsb_requirements(major, catalog_year) or {}

print("=" * 70)
print(f"Program requirements found: {prog_reqs.get('name', 'N/A')}")
print(f"Total credits: {prog_reqs.get('total_credits', '?')}")
print("=" * 70)

# Build major rows
mr_rows = _build_major_rows(prog_reqs, raw_courses, sm_mod)

# Compute GPA
_skip_gpa = {"name","total_credits","delivery","notes","teaching_fields","department",
             "same_as","concentrations","tracks","accreditation","total_major_credits",
             "la_credits","elective_credits","min_level"}
major_codes_set = set()
for _k, _v in prog_reqs.items():
    if _k in _skip_gpa:
        continue
    if isinstance(_v, list):
        for _cid in _v:
            if isinstance(_cid, str) and "xxx" not in _cid.lower():
                major_codes_set.add(_norm_code(_cid))

gpa_o, gpa_m, gpa_hrs, earned, ip_hrs, qp, proj = _compute_gpa(raw_courses, major_codes_set)

# LA rows
la_rows = sm_mod.build_la_rows_for_non_fsb(raw_courses, catalog_year, major_key=major)

print(f"\nEarned Hours: {earned}")
print(f"In-Progress Hours: {ip_hrs}")
print(f"Projected Hours: {earned + ip_hrs}")
print(f"Cumulative GPA: {gpa_o:.2f}")
print(f"Major GPA: {gpa_m:.2f}")

print("\n--- LIBERAL ARTS ROWS ---")
for r in la_rows:
    area = r.get('area', '')
    course = r.get('course_col', '')
    req = r.get('req', '')
    status = r.get('status', '')
    cr = r.get('cr', '')
    grade = r.get('grade', '')
    print(f"  {area:4} | {course:40} | {req:45} | {status:20} | {cr} | {grade}")

print("\n--- MAJOR REQUIREMENT ROWS ---")
for r in mr_rows:
    course = r.get('course_col', '')
    req = r.get('req', '')
    status = r.get('status', '')
    cr = r.get('cr', '')
    grade = r.get('grade', '')
    print(f"  {course:40} | {req:45} | {status:20} | {cr} | {grade}")
