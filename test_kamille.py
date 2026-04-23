"""
Test script: Kamille Rinas — Finance Major (2022-23)
Finance is an FSB major — uses sport_marketing.py audit() with MAJOR_KEY=finance.
"""
import sys, importlib
sys.path.insert(0, "/home/ubuntu/au-original-restored")

import engines.sport_marketing as sm
importlib.reload(sm)

raw_courses = sm.parse_csv("/home/ubuntu/upload/KamilleRinas.csv")

# Set FSB major key and catalog year
sm.MAJOR_KEY = "finance"
sm.CATALOG_YEAR = "2022-23"

res = sm.audit(raw_courses)

print(f"=== Finance Major (2022-23) — Kamille Rinas ===\n")

# Major rows
mr = res.get("mr", [])
print(f"{'Requirement':<65} {'Status':<15} {'Course'}")
print("-" * 110)
not_sat = []
for row in mr:
    req = row.get("label", row.get("req", ""))
    status = row.get("status", row.get("s", ""))
    course = row.get("course") or row.get("c") or {}
    course_code = course.get("raw", "") if isinstance(course, dict) else str(course)
    marker = "!!" if status not in ("Satisfied", "Current", "Scheduled", "Waived") else "  "
    if marker == "!!":
        not_sat.append(row)
    print(f"{marker} {req:<63} {status:<15} {course_code}")

print(f"\nTotal unsatisfied major rows: {len(not_sat)}")

# Also show LA rows
la = res.get("la", [])
la_not_sat = [r for r in la if r.get("status", r.get("s", "")) not in ("Satisfied", "Current", "Scheduled", "Waived")]
print(f"\nLA unsatisfied: {len(la_not_sat)}")
for r in la_not_sat:
    req = r.get("label", r.get("req", ""))
    status = r.get("status", r.get("s", ""))
    print(f"  !! {req} [{status}]")
