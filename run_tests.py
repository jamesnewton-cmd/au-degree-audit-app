"""
AU Degree Audit — Regression Test Suite
========================================
Tests run against the ACTUAL code in main_unified.py (via audit_helpers.py).
audit_helpers.py is auto-extracted from main_unified.py — regenerate it
whenever main_unified.py changes by running: python3 extract_helpers.py

ALL tests must pass before any files are delivered.
Usage: python3 run_tests.py
"""

import importlib.util, sys, re, traceback, ast as ast_mod
from collections import defaultdict

sys.path.insert(0, '/home/claude')

PASS = "✓"
FAIL = "✗"
results  = []
failures = []

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def check(condition, label, detail=""):
    if condition:
        results.append(f"  {PASS} {label}")
        return True
    msg = f"{label}{(' — ' + detail) if detail else ''}"
    results.append(f"  {FAIL} {msg}")
    failures.append(msg)
    return False

COURSE_RE = re.compile(r'^[A-Z]{2,6}[\s_/\-]\d{3,4}', re.IGNORECASE)

# ── Load modules ──────────────────────────────────────────────────────────────
print("=" * 60)
print("AU DEGREE AUDIT — REGRESSION TEST SUITE")
print("=" * 60)
print("\n[LOAD] Importing modules...")

try:
    sm  = load('/home/claude/sport_marketing.py',  'sport_marketing')
    nfp = load('/home/claude/non_fsb_programs.py', 'nfp')
    helpers = load('/home/claude/audit_helpers.py', 'audit_helpers')
    print(f"  {PASS} sport_marketing.py")
    print(f"  {PASS} non_fsb_programs.py  ({len(nfp.ALL_NON_FSB_PROGRAMS)} programs)")
    print(f"  {PASS} audit_helpers.py (extracted from main_unified.py)")
    # Verify key symbols are present in helpers
    for sym in ['SKIP_KEYS', '_build_major_rows', '_compute_gpa',
                '_norm_code', '_safe_credits', '_status_of_c']:
        check(hasattr(helpers, sym), f"  audit_helpers has {sym}")
except Exception as e:
    print(f"  {FAIL} LOAD FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# ── [1] Syntax: no duplicate dict keys ───────────────────────────────────────
print("\n[1] SYNTAX — no duplicate dict keys in any file")

class DupeKeyChecker(ast_mod.NodeVisitor):
    def __init__(self): self.dupes = []
    def visit_Dict(self, node):
        seen = {}
        for key in node.keys:
            if isinstance(key, ast_mod.Constant):
                k = key.value
                if k in seen:
                    self.dupes.append(f"'{k}' line {key.lineno}")
                seen[k] = True
        self.generic_visit(node)

for fname in ['main_unified.py', 'non_fsb_programs.py',
              'sport_marketing.py', 'pdf_template.py']:
    try:
        with open(f'/home/claude/{fname}') as f: src = f.read()
        chk = DupeKeyChecker()
        chk.visit(ast_mod.parse(src))
        check(len(chk.dupes) == 0, f"{fname}: no duplicate keys",
              "; ".join(chk.dupes[:3]))
    except FileNotFoundError:
        results.append(f"  — {fname}: not found, skipped")
    except SyntaxError as e:
        check(False, f"{fname}: syntax error", str(e))

# ── [2] Program integrity ─────────────────────────────────────────────────────
print("\n[2] PROGRAM INTEGRITY — valid course codes, no empty elective blocks")

def safe_credits(val, fallback=3):
    if isinstance(val, int): return val
    if isinstance(val, float): return int(val)
    if isinstance(val, str):
        try: return int(val.split("-")[0])
        except: return fallback
    return fallback

issues = []
for prog in sorted(nfp.ALL_NON_FSB_PROGRAMS):
    try:
        req = nfp.get_non_fsb_requirements(prog, '2022-23')
        if not req or not isinstance(req, dict): continue
        for key, val in req.items():
            if key in helpers.SKIP_KEYS: continue
            if isinstance(val, list):
                for item in val:
                    if not isinstance(item, str): continue
                    if 'xxx' in item.lower() or item.count('X') >= 3: continue
                    if not COURSE_RE.match(item.strip()):
                        issues.append(f"{prog}.{key}[]: '{item}'")
            elif isinstance(val, dict):
                if 'credits' not in val: continue
                credits = safe_credits(val.get('credits', 3))
                dept    = val.get('dept', '')
                course  = val.get('course', '')
                choose  = val.get('choose_from', val.get('options', val.get('courses', [])))
                if not course and credits >= 6 and not dept and isinstance(choose, list) and len(choose) == 0:
                    issues.append(f"{prog}.{key}: {credits}cr no dept/choose")
                if course and not COURSE_RE.match(course.strip()):
                    issues.append(f"{prog}.{key}.course: '{course}'")
                if isinstance(choose, list):
                    for c in choose:
                        if isinstance(c, str) and 'xxx' not in c.lower():
                            if not COURSE_RE.match(c.strip()):
                                issues.append(f"{prog}.{key}.choose: '{c}'")
    except Exception as e:
        issues.append(f"{prog}: {e}")

check(len(issues) == 0,
      f"All {len(nfp.ALL_NON_FSB_PROGRAMS)} program definitions valid",
      "; ".join(issues[:3]) if issues else "")

# ── [3] All programs load ─────────────────────────────────────────────────────
print("\n[3] ALL PROGRAMS LOAD — no exceptions for any program × year")

load_errors = []
for prog in nfp.ALL_NON_FSB_PROGRAMS:
    for yr in ['2022-23', '2023-24', '2024-25', '2025-26']:
        try:
            nfp.get_non_fsb_requirements(prog, yr)
        except Exception as e:
            load_errors.append(f"{prog}[{yr}]: {e}")

check(len(load_errors) == 0,
      f"All {len(nfp.ALL_NON_FSB_PROGRAMS)} programs × 4 years load cleanly",
      "; ".join(load_errors[:3]) if load_errors else "")

# ── [4] Minor coverage ────────────────────────────────────────────────────────
print("\n[4] MINOR COVERAGE — all 44 catalog minors present")

CATALOG_MINORS = [
    "Accounting Minor","Athletic Coaching Minor","Biblical Studies Minor",
    "Biology Minor","Chemistry Minor","Christian Ministries Minor",
    "Christian Spiritual Formation Minor","Computer Science Minor",
    "Criminal Justice Minor","Cybersecurity Minor","Dance Minor",
    "Data Science Minor","Economics Minor","English Studies Minor",
    "Ethics Minor","Family Science Minor","French/German Studies Minor",
    "History Minor","History of Christianity Minor","Humanitarian Engineering Minor",
    "Information Systems Minor","International Relations Minor","Legal Studies Minor",
    "Literary Studies Minor","Mathematics Minor","Music Minor","Nutrition Minor",
    "Peace and Conflict Transformation Minor","Philosophy Minor","Physics Minor",
    "Political Science Minor","Psychology Minor","Public Health Minor",
    "Public History Minor","Religion Minor","Social Work Minor",
    "Sociology Minor","Spanish Minor","Special Education Minor",
    "Sport and Recreational Leadership Minor","Statistics Minor",
    "Theatre Minor","Women's Studies Minor","Writing Minor",
]

def norm_m(s):
    return (s.lower().replace('(p-12)','').replace('(non-license)','')
              .replace('(pact)','').replace(' minor','').strip())

system_minor_names = [
    req.get('name','') for k in nfp.ALL_NON_FSB_PROGRAMS
    if 'minor' in k.lower()
    for req in [nfp.get_non_fsb_requirements(k,'2022-23')]
    if req and isinstance(req,dict)
]

missing = [cm for cm in CATALOG_MINORS
           if not any(norm_m(cm) in norm_m(sn) or norm_m(sn) in norm_m(cm)
                      for sn in system_minor_names)]
check(len(missing) == 0,
      f"All {len(CATALOG_MINORS)} catalog minors present",
      f"missing: {missing}" if missing else "")

# ── [5] Student transcript tests using REAL _build_major_rows ─────────────────
print("\n[5] STUDENT TRANSCRIPT TESTS (using actual main_unified code)")

TEST_CASES = [
    {
        "student":       "Joaquin Bautista",
        "csv":           "/mnt/user-data/uploads/Joaquin_B__.csv",
        "major":         "exercise_science",
        "catalog":       "2022-23",
        "concentration": "Sports Performance",
        "minor":         "marketing_minor",
        "satisfied":     ["BIOL 2410","BIOL 2420","EXSC 1360","EXSC 2455","EXSC 2580",
                          "EXSC 3470","EXSC 3480","EXSC 3520","EXSC 4150","EXSC 4800",
                          "EXSC 4910","PEHS 1550","PSYC 2000","CHEM 1000"],
        "current":       ["EXSC 3530","EXSC 4920"],
        "not_satisfied": [],
        # Concentration courses must NOT include any required_core course
        "conc_must_exclude_core": True,
        "minor_satisfied":     ["BSNS 2710","BSNS 3220"],
        "minor_not_satisfied": ["BSNS 3210","BSNS 4110","BSNS 4330"],
        "choose_row_counts":   {},
    },
    {
        "student":  "Landon Bair",
        "csv":      "/mnt/user-data/uploads/Landon_Bair_CVS.csv",
        "major":    "history",
        "catalog":  "2022-23",
        "satisfied":     ["HIST 2000","HIST 2300","HIST 2110",
                          "HIST 3420","HIST 3440","HIST 3220","HIST 3240","HIST 3260"],
        "not_satisfied": [],
        "current":       [],
        "choose_row_counts": {
            "american_hist_choose": 2,
            "european_hist_choose": 2,
            "world_hist_choose":    2,
        },
    },
    {
        "student":  "Olivia Armstrong",
        "csv":      "/mnt/user-data/uploads/Olivia_Armstrong.csv",
        "major":    "biology_ba",
        "catalog":  "2022-23",
        "satisfied":     ["BIOL 2210","BIOL 2220","BIOL 2240","BIOL 3030","BIOL 4050"],
        "not_satisfied": [],
        "current":       [],
        "choose_row_counts": {},
    },
    {
        "student":  "Saniya Fointn",
        "csv":      "/mnt/user-data/uploads/Saniya_Fointn.csv",
        "major":    "christian_ministries",
        "catalog":  "2022-23",
        "satisfied":     ["BIBL 2000","BIBL 2050","RLGN 2000","RLGN 2130",
                          "RLGN 3040","RLGN 3060"],
        "not_satisfied": ["RLGN 2150","RLGN 3300"],
        "current":       [],
        "choose_row_counts": {},
    },
    {
        "student":  "Jakob Surgeon",
        "csv":      "/mnt/user-data/uploads/jakob_surgeon.csv",
        "major":    "cs_ba",
        "catalog":  "2022-23",
        "satisfied":     ["CPSC 1400","CPSC 1500","CPSC 2100","CPSC 2330"],
        "not_satisfied": [],
        "current":       [],
        "choose_row_counts": {},
    },
    {
        "student":  "Jared Spoor",
        "csv":      "/mnt/user-data/uploads/Jared_Spoor.csv",
        "major":    "cinema_media_arts",
        "catalog":  "2022-23",
        "satisfied":     ["COMM 2000","COMM 2010","COMM 2020","COMM 2060",
                          "COMM 2200","COMM 3200","COMM 4000"],
        "not_satisfied": [],
        "current":       [],
        "choose_row_counts": {},
    },
    {
        "student":  "Luke A.",
        "csv":      "/mnt/user-data/uploads/Luke_A_.csv",
        "major":    "music_education_bmus",
        "catalog":  "2022-23",
        "satisfied":     ["MUSC 1010","MUSC 1020","MUSC 1030","MUSC 1040",
                          "MUED 2470","EDUC 2100"],
        "not_satisfied": [],
        "current":       [],
        "choose_row_counts": {},
    },
]

for tc in TEST_CASES:
    name = tc["student"]
    print(f"\n  ── {name} ({tc['major']}, {tc['catalog']}) ──")
    try:
        courses  = sm.parse_csv(tc["csv"])
        req      = nfp.get_non_fsb_requirements(tc["major"], tc["catalog"])
        assert req and isinstance(req, dict), f"No definition for {tc['major']}"

        # Use REAL _build_major_rows from main_unified via audit_helpers
        rows = helpers._build_major_rows(
            req, courses, sm,
            concentration=tc.get("concentration","")
        )

        # No duplicate row IDs
        ids   = [r['id'] for r in rows]
        dupes = [id for id in set(ids) if ids.count(id) > 1]
        check(len(dupes) == 0, f"{name}: no duplicate rows",
              f"duplicates: {dupes[:5]}")

        def is_satisfied(code):
            n = sm.norm(code.replace(' ','_'))
            return any(r['course'] and r['course']['code'] == n
                       and r['status'] == 'Satisfied' for r in rows)

        def is_current(code):
            n = sm.norm(code.replace(' ','_'))
            return any(r['course'] and r['course']['code'] == n
                       and r['status'] in ('Current','Scheduled') for r in rows)

        for code in tc.get("satisfied", []):
            check(is_satisfied(code), f"{name}: {code} = Satisfied")

        for code in tc.get("not_satisfied", []):
            check(not is_satisfied(code), f"{name}: {code} ≠ Satisfied")

        for code in tc.get("current", []):
            check(is_current(code), f"{name}: {code} = Current/Scheduled")

        for group_key, expected_n in tc.get("choose_row_counts", {}).items():
            group_rows = [r for r in rows
                          if r['id'].lower().startswith(group_key.lower())]
            check(len(group_rows) == expected_n,
                  f"{name}: {group_key} has {expected_n} rows",
                  f"found {len(group_rows)}")

        # Concentration must not pull core courses
        if tc.get("conc_must_exclude_core"):
            core_codes = {sm.norm(c.replace(' ','_'))
                          for c in req.get('required_core', [])}
            conc_rows  = [r for r in rows if r['id'].startswith('conc_')]
            conc_course_codes = {r['course']['code'] for r in conc_rows if r['course']}
            overlap = conc_course_codes & core_codes
            check(len(overlap) == 0,
                  f"{name}: concentration rows don't repeat core courses",
                  f"overlap: {overlap}")

        # Minor checks
        minor_key = tc.get("minor")
        if minor_key:
            minor_req  = nfp.get_non_fsb_requirements(minor_key, tc["catalog"])
            assert minor_req, f"No definition for minor {minor_key}"
            minor_rows = helpers._build_major_rows(minor_req, courses, sm)
            minor_ids  = [r['id'] for r in minor_rows]
            minor_dup  = [id for id in set(minor_ids) if minor_ids.count(id) > 1]
            check(len(minor_dup) == 0, f"{name} minor: no duplicate rows",
                  f"duplicates: {minor_dup[:3]}")

            def minor_satisfied(code):
                n = sm.norm(code.replace(' ','_'))
                return any(r['course'] and r['course']['code'] == n
                           and r['status'] == 'Satisfied' for r in minor_rows)

            for code in tc.get("minor_satisfied", []):
                check(minor_satisfied(code), f"{name} minor: {code} = Satisfied")
            for code in tc.get("minor_not_satisfied", []):
                check(not minor_satisfied(code), f"{name} minor: {code} ≠ Satisfied")

    except Exception as e:
        check(False, f"{name}: EXCEPTION", str(e))
        traceback.print_exc()

# ── [6] FSB ENGINE TESTS ─────────────────────────────────────────────────────
print("\n[6] FSB ENGINES — all 10 majors run without crashing")
import os

FSB_TESTS = [
    ('sport_marketing',               'engines/sport_marketing.py',  'sport_marketing',   True),
    ('management',                    'engines/management.py',        'management',        False),
    ('marketing',                     'engines/fsb_engine.py',        'fsb_engine',        True),
    ('accounting',                    'engines/fsb_engine.py',        'fsb_engine',        True),
    ('finance',                       'engines/fsb_engine.py',        'fsb_engine',        True),
    ('business_analytics',            'engines/fsb_engine.py',        'fsb_engine',        True),
    ('engineering_management',        'engines/fsb_engine.py',        'fsb_engine',        True),
    ('global_business',               'engines/fsb_engine.py',        'fsb_engine',        True),
    ('music_entertainment_business',  'engines/fsb_engine.py',        'fsb_engine',        True),
    ('business_integrative_leadership','engines/fsb_engine.py',       'fsb_engine',        True),
]

_fsb_courses = sm.parse_csv('/mnt/user-data/uploads/Joaquin_B__.csv')
for major_key, engine_path, engine_name, has_minor in FSB_TESTS:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), engine_path)
    try:
        eng = load(full_path, engine_name)
        if hasattr(eng, 'MAJOR_KEY'):
            eng.MAJOR_KEY    = major_key
            eng.CATALOG_YEAR = '2022-23'
        res = eng.audit(_fsb_courses, minor_key=None) if has_minor else eng.audit(_fsb_courses)
        check('mr' in res and 'la' in res,
              f"FSB {major_key}: audit() returns mr and la rows")
    except Exception as e:
        check(False, f"FSB {major_key}: audit() runs without error", str(e))

# ── [7] ALL NON-FSB PROGRAMS PRODUCE ROWS ────────────────────────────────────
print("\n[7] ALL NON-FSB PROGRAMS — scanner produces rows for all 151 programs")
_all_crashes = []
_zero_rows   = []
for prog in sorted(nfp.ALL_NON_FSB_PROGRAMS):
    try:
        req = nfp.get_non_fsb_requirements(prog, '2022-23')
        if not req or not isinstance(req, dict): continue
        rows = helpers._build_major_rows(req, _fsb_courses, sm)
        if len(rows) == 0 and prog != 'honors_program':
            _zero_rows.append(prog)
    except Exception as e:
        _all_crashes.append(f"{prog}: {e}")

check(len(_all_crashes) == 0,
      f"All {len(nfp.ALL_NON_FSB_PROGRAMS)} programs scan without crashing",
      "; ".join(_all_crashes[:3]) if _all_crashes else "")
check(len(_zero_rows) == 0,
      "No programs produce zero rows (except honors_program)",
      f"zero-row: {_zero_rows}" if _zero_rows else "")

# ── [8] LA requirements ───────────────────────────────────────────────────────
print("\n[8] LA REQUIREMENTS — framework and course lists")
try:
    la = load('/home/claude/liberal_arts_requirements.py', 'la')
    req_la = la.get_la_requirements('2022-23')
    check(isinstance(req_la, dict), "LA requirements load for 2022-23")
    check(all(k in req_la for k in ['F1','W8','WI','SI']),
          "LA has F1, W8, WI, SI keys")
    wi = req_la.get('WI',{}).get('courses',[]) or []
    si = req_la.get('SI',{}).get('courses',[]) or []
    check(len(wi) >= 30, f"WI has ≥30 courses (has {len(wi)})")
    check(len(si) >= 20, f"SI has ≥20 courses (has {len(si)})")
except Exception as e:
    check(False, "LA framework loaded", str(e))

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)
total  = len(results)
passed = sum(1 for r in results if r.strip().startswith(PASS))
failed = len(failures)
print(f"  Passed: {passed}/{total}")
print(f"  Failed: {failed}")

if failures:
    print(f"\n{'='*60}")
    print("FAILURES — fix before delivering files:")
    print("=" * 60)
    for f in failures:
        print(f"  {FAIL} {f}")
    print(f"\nSTATUS: *** DO NOT DELIVER FILES ***")
    sys.exit(1)
else:
    print(f"\nSTATUS: ALL TESTS PASSED — safe to deliver ✓")
    sys.exit(0)
