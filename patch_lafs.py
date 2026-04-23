"""
Patch sport_marketing.py to handle LAFS-style transfer codes.

LAFS codes (e.g. 'LAFS- 15QR-1631788-MATH-125') are used by the registrar
to indicate a transfer course that satisfies a specific Liberal Arts Framework
area. The area code is embedded in the course code:
  - QR -> F5 (Quantitative Reasoning)
  - WR -> WI (Writing Intensive)
  - SP -> SI (Speaking Intensive)
  - etc.

The fix adds a helper _extract_lafs_area() and annotates LAFS courses in
parse_csv with __map_area__ so they flow through the existing map_by_area
mechanism in build_la_rows_for_non_fsb.
"""

with open('/home/ubuntu/au-original-restored/engines/sport_marketing.py', 'r') as f:
    content = f.read()

# ── 1. Add LAFS_AREA_MAP constant and helper after _resolve_transfer_code ─────
ANCHOR_AFTER = '''def _resolve_transfer_code(course_code, equiv_course):
    """
    For ELCT-style transfer codes, try to extract the real AU course code.
    e.g. 'ELCT-1000-1628902-CHEM-119' -> try equiv_course field first,
    otherwise return original. Non-ELCT codes pass through unchanged.
    """
    code_upper = course_code.strip().upper()
    if not code_upper.startswith("ELCT"):
        return course_code
    if equiv_course and equiv_course.strip():
        eq = equiv_course.strip().upper()
        import re as _re
        if _re.match(r"^[A-Z]{2,6}[-\\x20]\\d{3,4}", eq):
            return eq
    import re as _re
    m = _re.search(r"-([A-Z]{2,6})-(\\d{3,4}[A-Z]?)$", code_upper)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return course_code'''

LAFS_HELPER = '''
# ── LAFS area code -> LA framework area key mapping ───────────────────────────
# LAFS codes (e.g. 'LAFS- 15QR-1631788-MATH-125') indicate transfer courses
# that satisfy a specific Liberal Arts Framework area. The area code is embedded
# in the course code: QR=F5, WR=WI, SP=SI, etc.
_LAFS_AREA_MAP = {
    "QR": "F5",   # Quantitative Reasoning
    "WR": "WI",   # Writing Intensive
    "SP": "SI",   # Speaking Intensive
    "AW": "W4",   # Aesthetic Ways of Knowing
    "CW": "W3",   # Christian Ways of Knowing
    "GW": "W8",   # Global/Intercultural Ways of Knowing
    "SW": "W2",   # Scientific Ways of Knowing
    "BW": "W1",   # Biblical/Theological Ways of Knowing
}
def _extract_lafs_area(raw_code):
    """
    For LAFS-style transfer codes, extract the LA framework area key.
    e.g. 'LAFS- 15QR-1631788-MATH-125' -> 'F5'
    Returns None if not a LAFS code or area not recognized.
    """
    code_upper = (raw_code or "").strip().upper()
    if not code_upper.startswith("LAFS"):
        return None
    import re as _re
    m = _re.search(r"LAFS[- ]+\\d*([A-Z]+)-", code_upper)
    if m:
        return _LAFS_AREA_MAP.get(m.group(1))
    return None
'''

if ANCHOR_AFTER not in content:
    print("ERROR: Anchor for _resolve_transfer_code not found!")
else:
    content = content.replace(ANCHOR_AFTER, ANCHOR_AFTER + LAFS_HELPER)
    print("Step 1: Added LAFS helper after _resolve_transfer_code")

# ── 2. In parse_csv, annotate LAFS courses with __map_area__ ──────────────────
OLD_ROWS_APPEND = '''            rows.append(
                {
                    "code": norm(resolved),
                    "raw": resolved.upper(),
                    "name": r.get("Course Name", "").strip(),
                    "cr": _int(r.get("Credits", "0")),
                    "status": status_raw,
                    "grade": grade_raw,
                    "reg_date": r.get("Registration Date", "").strip(),
                }'''

NEW_ROWS_APPEND = '''            _row = {
                    "code": norm(resolved),
                    "raw": resolved.upper(),
                    "name": r.get("Course Name", "").strip(),
                    "cr": _int(r.get("Credits", "0")),
                    "status": status_raw,
                    "grade": grade_raw,
                    "reg_date": r.get("Registration Date", "").strip(),
                }
            # Annotate LAFS transfer codes with their LA area for map_by_area lookup
            _lafs_area = _extract_lafs_area(raw_code)
            if _lafs_area:
                _row["__map_area__"] = _lafs_area
                _row["__map_taken_code__"] = _row["code"]
            rows.append(_row'''

if OLD_ROWS_APPEND not in content:
    print("ERROR: Anchor for rows.append not found!")
else:
    content = content.replace(OLD_ROWS_APPEND, NEW_ROWS_APPEND)
    print("Step 2: Annotated LAFS courses with __map_area__ in parse_csv")

with open('/home/ubuntu/au-original-restored/engines/sport_marketing.py', 'w') as f:
    f.write(content)

# Verify
with open('/home/ubuntu/au-original-restored/engines/sport_marketing.py', 'r') as f:
    verify = f.read()
if '_LAFS_AREA_MAP' in verify and '_extract_lafs_area' in verify and '__map_area__' in verify:
    print("VERIFIED: LAFS handling added to sport_marketing.py")
else:
    print("ERROR: Verification failed")
