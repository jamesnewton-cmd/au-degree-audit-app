"""
Test script — run a full audit for Jennifer Eisinger (Political Science 2022-23)
and generate the PDF to verify the output.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from engines.csv_parser import parse_csv, get_student_info
from engines.audit_engine import run_audit
from engines.pdf_generator import generate_pdf

CSV_PATH = "/home/ubuntu/upload/JenniferEisinger-PoliticalScience22-23.csv"
OUTPUT_PDF = "/home/ubuntu/au-audit-rebuild/test_output_jennifer.pdf"

def main():
    print("=== STEP 1: Parse CSV ===")
    course_map = parse_csv(CSV_PATH)
    print(f"  Parsed {len(course_map)} courses")
    for code, c in sorted(course_map.items())[:10]:
        print(f"  {code:25s} | {c['status']:15s} | {c['grade']:5s} | {c['cr']} cr | {c['name'][:40]}")
    print(f"  ... and {max(0, len(course_map)-10)} more")

    print("\n=== STEP 2: Run Audit ===")
    result = run_audit(
        course_map=course_map,
        student_name="Jennifer Eisinger",
        student_id="",
        major_key="political_science",
        catalog_year="2022-23",
    )

    print(f"  Student: {result.student_name}")
    print(f"  Major:   {result.major}")
    print(f"  Catalog: {result.catalog_year}")
    print(f"  Earned:  {result.total_credits_earned} cr")
    print(f"  IP:      {result.total_credits_in_progress} cr")
    print(f"  GPA:     {result.overall_gpa}")
    print(f"  Major GPA: {result.major_gpa}")
    print(f"  LA Complete: {result.la_complete}")
    print(f"  Major Complete: {result.major_complete}")
    print(f"  Eligible: {result.eligible_to_walk}")

    print("\n=== LIBERAL ARTS RESULTS ===")
    for r in result.la_rows:
        status_icon = "✓" if r.status == "Satisfied" else ("~" if r.status in ("In Progress", "Scheduled") else "✗")
        print(f"  {status_icon} {r.area:4s} | {r.status:15s} | {r.course_display[:45]}")

    print("\n=== MAJOR REQUIREMENT RESULTS ===")
    for r in result.major_rows:
        status_icon = "✓" if r.status == "Satisfied" else ("~" if r.status in ("In Progress", "Scheduled") else "✗")
        print(f"  {status_icon} {r.course_display[:20]:20s} | {r.status:15s} | {r.label[:50]}")

    if result.la_outstanding:
        print(f"\n=== LA OUTSTANDING ({len(result.la_outstanding)}) ===")
        for item in result.la_outstanding:
            print(f"  ✗ {item}")

    if result.major_outstanding:
        print(f"\n=== MAJOR OUTSTANDING ({len(result.major_outstanding)}) ===")
        for item in result.major_outstanding:
            print(f"  ✗ {item}")

    print("\n=== STEP 3: Generate PDF ===")
    generate_pdf(result, OUTPUT_PDF)
    print(f"  PDF written to: {OUTPUT_PDF}")
    import os
    size = os.path.getsize(OUTPUT_PDF)
    print(f"  File size: {size:,} bytes ({size//1024} KB)")
    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    main()
