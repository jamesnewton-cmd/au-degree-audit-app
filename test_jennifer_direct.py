"""
Direct test of the original app's audit pipeline for Jennifer Eisinger.
Bypasses FastAPI and calls the engine functions directly.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Load the sport_marketing engine (the main audit engine for non-FSB)
from engines.sport_marketing import (
    parse_csv,
    build_la_rows_for_non_fsb,
    norm,
    done,
    ip,
    status_of,
    best,
    cmap,
)
from requirements.non_fsb_programs import get_non_fsb_requirements

CSV_PATH = "/home/ubuntu/upload/JenniferEisinger-PoliticalScience22-23.csv"
OUTPUT_PDF = "/home/ubuntu/test_jennifer_fixed.pdf"
MAJOR = "political_science"
CATALOG_YEAR = "2022-23"
STUDENT_NAME = "Jennifer Eisinger"

def main():
    print("=" * 60)
    print("ANDERSON UNIVERSITY AUDIT TEST — Jennifer Eisinger")
    print("Major: Political Science | Catalog: 2022-23")
    print("=" * 60)

    # Step 1: Parse CSV
    print("\n[1] Parsing CSV...")
    courses = parse_csv(CSV_PATH)
    print(f"    Parsed {len(courses)} course records")

    # Step 2: Get major requirements
    print("\n[2] Loading Political Science requirements...")
    prog_reqs = get_non_fsb_requirements(MAJOR, CATALOG_YEAR)
    print(f"    Required courses: {prog_reqs.get('required', [])}")
    print(f"    Dist groups: {[g['name'] for g in prog_reqs.get('dist_groups', [])]}")

    # Step 3: Evaluate required courses
    print("\n[3] Evaluating required courses...")
    cm = cmap(courses)
    required = prog_reqs.get("required", [])
    for cid in required:
        code = norm(cid.replace("-", "_").replace(" ", "_"))
        c = cm.get(code)
        st = status_of(c) if c else "Not Satisfied"
        print(f"    {cid:20s} -> {st}")

    # Step 4: Evaluate distribution groups (THE FIX)
    print("\n[4] Evaluating distribution groups (FIXED)...")
    dist_groups = prog_reqs.get("dist_groups", [])
    if not dist_groups:
        print("    WARNING: No dist_groups found in requirements!")
    for group in dist_groups:
        group_name = group.get("name")
        credits_needed = float(group.get("credits", 3))
        min_courses = int(group.get("min_courses", 1))
        choose_from = group.get("choose_from", [])
        earned = 0.0
        ip_cr = 0.0
        earned_list = []
        ip_list = []
        for cid in choose_from:
            code = norm(cid.replace("-", "_").replace(" ", "_"))
            c = cm.get(code)
            if c:
                if done(c):
                    earned += c.get("cr", 3)
                    earned_list.append(cid)
                elif ip(c):
                    ip_cr += c.get("cr", 3)
                    ip_list.append(cid)
        if earned >= credits_needed and len(earned_list) >= min_courses:
            grp_status = "SATISFIED"
        elif (earned + ip_cr) >= credits_needed or (len(earned_list) + len(ip_list)) >= min_courses:
            grp_status = "IN PROGRESS"
        else:
            grp_status = "NOT MET"
        print(f"    {group_name}:")
        print(f"      Required: {credits_needed} cr, {min_courses} courses from {choose_from}")
        print(f"      Earned:   {earned} cr ({earned_list})")
        print(f"      IP:       {ip_cr} cr ({ip_list})")
        print(f"      Status:   {grp_status}")

    # Step 5: Build LA rows
    print("\n[5] Building Liberal Arts rows...")
    la_rows = build_la_rows_for_non_fsb(courses, CATALOG_YEAR, major_key=MAJOR)
    print(f"    Built {len(la_rows)} LA rows")
    for row in la_rows:
        area = row.get("area", "?")
        status = row.get("status", "?")
        course_col = row.get("course_col", "")
        icon = "✓" if status == "Satisfied" else ("~" if status in ("Current", "Scheduled") else "✗")
        print(f"    {icon} {area:4s} | {status:15s} | {course_col[:45]}")

    # Step 6: Generate PDF using the original build function
    print("\n[6] Generating PDF...")
    from engines.sport_marketing import audit, build

    # Build the res dict that build() expects
    res = audit(courses, minor_key=None)
    build(res, STUDENT_NAME, "Political Science", OUTPUT_PDF)
    size = os.path.getsize(OUTPUT_PDF)
    print(f"    PDF written: {OUTPUT_PDF} ({size:,} bytes)")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
