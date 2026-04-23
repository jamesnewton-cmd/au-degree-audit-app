import sys
sys.path.insert(0, '/home/ubuntu/au-original-restored')

from engines import sport_marketing as sm
from engines import fsb_engine

fsb_engine.MAJOR_KEY = 'accounting'
fsb_engine.CATALOG_YEAR = '2022-23'

courses = sm.parse_csv('/home/ubuntu/upload/CarterKnobloch-Accounting.csv')
print(f"Total courses parsed: {len(courses)}")

try:
    result = fsb_engine.audit(courses, minor_key=None)
except TypeError:
    result = fsb_engine.audit(courses)

# Summary stats
print(f"\n=== SUMMARY ===")
print(f"  Earned Hours:    {result.get('earned')}")
print(f"  Projected Hours: {result.get('proj')}")
print(f"  Cumulative GPA:  {result.get('gpa_o')}")
print(f"  Major GPA:       {result.get('gpa_m')}")

# LA rows
print("\n=== LIBERAL ARTS (la) ===")
for row in result.get('la', []):
    area = row.get('area', '')
    status = row.get('status', '')
    course = row.get('course', {})
    course_str = f"{course.get('raw','')} {course.get('name','')}" if course else ''
    req = row.get('req', '')
    print(f"  {area:4} | {status:15} | {course_str[:38]:38} | {req[:45]}")

# Business core
print("\n=== BUSINESS CORE (bc) ===")
for row in result.get('bc', []):
    status = row.get('status', '')
    label = row.get('label', '')
    course = row.get('course', {})
    course_str = f"{course.get('raw','')} {course.get('name','')}" if course else '(not satisfied)'
    print(f"  {status:15} | {course_str[:38]:38} | {label[:45]}")

# Major requirements
print("\n=== MAJOR REQUIREMENTS (mr) ===")
for row in result.get('mr', []):
    status = row.get('status', '')
    label = row.get('label', '')
    course = row.get('course', {})
    course_str = f"{course.get('raw','')} {course.get('name','')}" if course else '(not satisfied)'
    note = row.get('note', '')
    print(f"  {status:15} | {course_str[:38]:38} | {label[:40]} {note}")

# Electives
print(f"\n=== ELECTIVES ===")
print(f"  Elective hours earned: {result.get('ehrs')}")
print(f"  Elective hours required: {result.get('elec_required_hrs')}")
for row in result.get('elecs', []):
    course = row.get('course', {})
    course_str = f"{course.get('raw','')} {course.get('name','')}" if course else ''
    print(f"  {course_str}")
