"""
AU Degree Audit — Regression Test Suite
========================================
Run after EVERY change before delivering any files.
ALL tests must pass before files are handed to James.

Usage: python3 run_tests.py
"""

import importlib.util, sys, re, traceback, ast as ast_mod
from collections import defaultdict

sys.path.insert(0, '/home/claude')

PASS = "✓"
FAIL = "✗"

results  = []
failures = []
warnings = []

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def check(condition, label, detail=""):
    if condition:
        results.append(f"  {PASS} {label}")
        return True
    else:
        msg = f"{label}{(' — ' + detail) if detail else ''}"
        results.append(f"  {FAIL} {msg}")
        failures.append(msg)
        return False

def status_of(c):
    if c is None: return 'Not Satisfied'
    g = c['grade'].upper()
    if c['status'] == 'grade posted' and g not in ('','W','DRP','NC','NGL'):
        return 'Satisfied'
    if c['status'] == 'current':   return 'Current'
    if c['status'] == 'scheduled': return 'Scheduled'
    return 'Not Satisfied'

def safe_credits(val, fallback=3):
    if isinstance(val, int):   return val
    if isinstance(val, float): return int(val)
    if isinstance(val, str):
        try: return int(val.split("-")[0])
        except: return fallback
    return fallback

SKIP_KEYS = {
    'name','total_credits','delivery','notes','note','teaching_fields','department',
    'concentration_note','special_rules','same_as','optional_cma','concentrations',
    'tracks','total_major_credits','lead_courses_credits','la_credits','elective_credits',
    'min_level','choose_one','accreditation','prerequisites','dummy_2022_23',
    'dummy_elective','required_old','dept_dummy','upper_div_psyc',
}

COURSE_RE = re.compile(r'^[A-Z]{2,6}[\s_/\-]\d{3,4}', re.IGNORECASE)

# ─────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("AU DEGREE AUDIT — REGRESSION TEST SUITE")
print("=" * 60)

# ── Load modules ──────────────────────────────────────────────────────────────
print("\n[LOAD] Importing modules...")
try:
    sm  = load('/home/claude/sport_marketing.py',   'sport_marketing')
    nfp = load('/home/claude/non_fsb_programs.py',  'nfp')
    print(f"  {PASS} sport_marketing.py")
    print(f"  {PASS} non_fsb_programs.py  ({len(nfp.ALL_NON_FSB_PROGRAMS)} programs)")
except Exception as e:
    print(f"  {FAIL} MODULE LOAD FAILED: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
print("\n[1] SYNTAX — no duplicate dict keys in any file")
# ─────────────────────────────────────────────────────────────────────────────
class DupeKeyChecker(ast_mod.NodeVisitor):
    def __init__(self): self.dupes = []
    def visit_Dict(self, node):
        seen = {}
        for key in node.keys:
            if isinstance(key, ast_mod.Constant):
                k = key.value
                if k in seen:
                    self.dupes.append(f"'{k}' at line {key.lineno}")
                seen[k] = True
        self.generic_visit(node)

for fname in ['non_fsb_programs.py', 'sport_marketing.py', 'main_unified.py',
              'pdf_template.py']:
    try:
        with open(f'/home/claude/{fname}') as f: src = f.read()
        tree = ast_mod.parse(src)
        chk  = DupeKeyChecker()
        chk.visit(tree)
        check(len(chk.dupes) == 0, f"{fname}: no duplicate keys",
              "; ".join(chk.dupes[:3]))
    except FileNotFoundError:
        results.append(f"  — {fname}: not found, skipped")
    except SyntaxError as e:
        check(False, f"{fname}: syntax error", str(e))

# ─────────────────────────────────────────────────────────────────────────────
print("\n[2] PROGRAM INTEGRITY — valid course codes, no empty elective blocks")
# ─────────────────────────────────────────────────────────────────────────────
integrity_issues = []
for prog in sorted(nfp.ALL_NON_FSB_PROGRAMS):
    try:
        req = nfp.get_non_fsb_requirements(prog, '2022-23')
        if not req or not isinstance(req, dict): continue
        for key, val in req.items():
            if key in SKIP_KEYS: continue
            if isinstance(val, list):
                for item in val:
                    if not isinstance(item, str): continue
                    if 'xxx' in item.lower() or item.count('X') >= 3: continue
                    if not COURSE_RE.match(item.strip()):
                        integrity_issues.append(f"{prog}.{key}[]: '{item}'")
            elif isinstance(val, dict):
                if 'credits' not in val: continue
                credits = safe_credits(val.get('credits', 3))
                dept    = val.get('dept', '')
                course  = val.get('course', '')
                choose  = val.get('choose_from', val.get('options', val.get('courses', [])))
                if not course and credits >= 6 and not dept and isinstance(choose, list) and len(choose) == 0:
                    integrity_issues.append(f"{prog}.{key}: {credits}cr, no dept/choose_from")
                if course and not COURSE_RE.match(course.strip()):
                    integrity_issues.append(f"{prog}.{key}.course: '{course}'")
                if isinstance(choose, list):
                    for c in choose:
                        if not isinstance(c, str): continue
                        if 'xxx' in c.lower(): continue
                        if not COURSE_RE.match(c.strip()):
                            integrity_issues.append(f"{prog}.{key}.choose_from: '{c}'")
    except Exception as e:
        integrity_issues.append(f"{prog}: exception — {e}")

check(len(integrity_issues) == 0,
      f"All {len(nfp.ALL_NON_FSB_PROGRAMS)} program definitions structurally valid",
      "; ".join(integrity_issues[:3]) if integrity_issues else "")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[3] ALL PROGRAMS LOAD — no exceptions for any program × year")
# ─────────────────────────────────────────────────────────────────────────────
load_errors = []
for prog in nfp.ALL_NON_FSB_PROGRAMS:
    for yr in ['2022-23', '2023-24', '2024-25', '2025-26']:
        try:
            nfp.get_non_fsb_requirements(prog, yr)
        except Exception as e:
            load_errors.append(f"{prog} [{yr}]: {e}")

check(len(load_errors) == 0,
      f"All {len(nfp.ALL_NON_FSB_PROGRAMS)} programs × 4 years load cleanly",
      "; ".join(load_errors[:3]) if load_errors else "")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[4] MINOR COVERAGE — all 44 catalog minors present in system")
# ─────────────────────────────────────────────────────────────────────────────
CATALOG_MINORS = [
    "Accounting Minor", "Athletic Coaching Minor", "Biblical Studies Minor",
    "Biology Minor", "Chemistry Minor", "Christian Ministries Minor",
    "Christian Spiritual Formation Minor", "Computer Science Minor",
    "Criminal Justice Minor", "Cybersecurity Minor", "Dance Minor",
    "Data Science Minor", "Economics Minor", "English Studies Minor",
    "Ethics Minor", "Family Science Minor", "French/German Studies Minor",
    "History Minor", "History of Christianity Minor", "Humanitarian Engineering Minor",
    "Information Systems Minor", "International Relations Minor", "Legal Studies Minor",
    "Literary Studies Minor", "Mathematics Minor", "Music Minor", "Nutrition Minor",
    "Peace and Conflict Transformation Minor", "Philosophy Minor", "Physics Minor",
    "Political Science Minor", "Psychology Minor", "Public Health Minor",
    "Public History Minor", "Religion Minor", "Social Work Minor",
    "Sociology Minor", "Spanish Minor", "Special Education Minor",
    "Sport and Recreational Leadership Minor", "Statistics Minor",
    "Theatre Minor", "Women's Studies Minor", "Writing Minor",
]

def norm_m(s):
    return (s.lower().replace('(p-12)','').replace('(non-license)','')
              .replace('(pact)','').replace(' minor','').strip())

system_minor_names = []
for k in nfp.ALL_NON_FSB_PROGRAMS:
    if 'minor' in k.lower():
        r = nfp.get_non_fsb_requirements(k, '2022-23')
        if r and isinstance(r, dict):
            system_minor_names.append(r.get('name',''))

missing_minors = [cm for cm in CATALOG_MINORS
                  if not any(norm_m(cm) in norm_m(sn) or norm_m(sn) in norm_m(cm)
                             for sn in system_minor_names)]
check(len(missing_minors) == 0,
      f"All {len(CATALOG_MINORS)} catalog minors present",
      f"missing: {missing_minors}" if missing_minors else "")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[5] STUDENT TRANSCRIPT TESTS")
# ─────────────────────────────────────────────────────────────────────────────

def find_course(courses, code_list):
    normalized = [sm.norm(c.replace(' ','_').replace('-','_')) for c in code_list]
    return sm.best(courses, normalized)

def build_rows(req, courses, concentration=""):
    """Replicate major row building for test validation."""
    rows = []
    SKIP = SKIP_KEYS | {'concentrations'}

    # List keys → individual required rows
    for k, v in req.items():
        if k in SKIP or not isinstance(v, list): continue
        for cid in v:
            if not isinstance(cid, str) or 'xxx' in cid.lower(): continue
            c = find_course(courses, [cid])
            rows.append({'id': sm.norm(cid.replace(' ','_')), 'label': cid,
                         'status': status_of(c), 'course': c})

    # Dict keys with credits → elective/choose rows
    for k, v in req.items():
        if k in SKIP or not isinstance(v, dict) or 'credits' not in v: continue
        credits = safe_credits(v.get('credits', 3))
        dept    = v.get('dept', '')
        course  = v.get('course', '')
        choose  = v.get('choose_from', v.get('options', v.get('courses', [])))
        if not course and not dept and not choose: continue
        opts = [course] if course else (choose if isinstance(choose, list) else [])
        num  = max(1, round(credits / 3)) if not course else 1
        used = set()
        for slot in range(num):
            rem = [o for o in opts
                   if sm.norm(o.replace(' ','_').replace('-','_')) not in used]
            c = find_course(courses, rem) if rem else None
            if c is None and dept:
                dp = tuple(d.upper() for d in ([dept] if isinstance(dept, str) else dept))
                c  = next((x for x in courses
                           if x['raw'].upper().startswith(dp)
                           and x['code'] not in used
                           and status_of(x) in ('Satisfied','Current','Scheduled')), None)
            if c: used.add(c['code'])
            rows.append({'id': f"{k}_{slot+1}" if num > 1 else k,
                         'label': f"{k}[{slot+1}]" if num > 1 else k,
                         'status': status_of(c), 'course': c})

    # Concentration rows
    if concentration:
        conc_data = req.get('concentrations', {}).get(concentration, {})
        if isinstance(conc_data, dict):
            for cid in conc_data.get('required', []):
                c = find_course(courses, [cid])
                rows.append({'id': f"conc_{sm.norm(cid.replace(' ','_'))}",
                             'label': f"[{concentration}] {cid}",
                             'status': status_of(c), 'course': c})
            for sk, sv in conc_data.items():
                if sk in ('required','notes','name'): continue
                if not isinstance(sv, dict) or 'credits' not in sv: continue
                cr   = safe_credits(sv.get('credits', 3))
                dp_r = sv.get('dept', '')
                ch   = sv.get('choose_from', [])
                dp   = tuple(d.upper() for d in ([dp_r] if isinstance(dp_r,str) else dp_r)) if dp_r else ()
                num2 = max(1, round(cr / 3))
                used2 = set()
                for slot in range(num2):
                    rem = [o for o in ch
                           if sm.norm(o.replace(' ','_').replace('-','_')) not in used2]
                    c = find_course(courses, rem) if rem else None
                    if c is None and dp:
                        c = next((x for x in courses
                                  if x['raw'].upper().startswith(dp)
                                  and x['code'] not in used2
                                  and status_of(x) in ('Satisfied','Current','Scheduled')), None)
                    if c: used2.add(c['code'])
                    rows.append({'id': f"conc_{sk}_{slot+1}",
                                 'label': f"[{concentration}] {sk}[{slot+1}]",
                                 'status': status_of(c), 'course': c})
    return rows

# Test cases — each checks specific expected outcomes against real transcripts
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
        "minor_satisfied":     ["BSNS 2710","BSNS 3220"],
        "minor_not_satisfied": ["BSNS 3210","BSNS 4110","BSNS 4330"],
        "choose_row_counts": {},
    },
    {
        "student":  "Landon Bair",
        "csv":      "/mnt/user-data/uploads/Landon_Bair_CVS.csv",
        "major":    "history",
        "catalog":  "2022-23",
        "satisfied": ["HIST 2000","HIST 2300","HIST 2110",
                      "HIST 3420","HIST 3440","HIST 3220","HIST 3240","HIST 3260"],
        "not_satisfied": [],
        "current":  [],
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
        courses = sm.parse_csv(tc["csv"])
        req     = nfp.get_non_fsb_requirements(tc["major"], tc["catalog"])
        assert req and isinstance(req, dict), f"No definition for {tc['major']}"

        rows  = build_rows(req, courses, tc.get("concentration",""))
        ids   = [r['id'] for r in rows]
        dupes = [id for id in set(ids) if ids.count(id) > 1]
        check(len(dupes) == 0, f"{name}: no duplicate rows",
              f"duplicates: {dupes[:5]}")

        # Satisfied checks
        def is_satisfied(code):
            norm_c = sm.norm(code.replace(' ','_'))
            return any(r['course'] and r['course']['code'] == norm_c
                       and r['status'] == 'Satisfied' for r in rows)

        def is_current(code):
            norm_c = sm.norm(code.replace(' ','_'))
            return any(r['course'] and r['course']['code'] == norm_c
                       and r['status'] in ('Current','Scheduled') for r in rows)

        for code in tc.get("satisfied", []):
            check(is_satisfied(code), f"{name}: {code} = Satisfied")

        for code in tc.get("not_satisfied", []):
            check(not is_satisfied(code), f"{name}: {code} = Not Satisfied (correctly)")

        for code in tc.get("current", []):
            check(is_current(code), f"{name}: {code} = Current/Scheduled")

        # Choose-group row count checks
        for group_key, expected_n in tc.get("choose_row_counts", {}).items():
            group_rows = [r for r in rows if r['id'].startswith(group_key)]
            check(len(group_rows) == expected_n,
                  f"{name}: {group_key} has {expected_n} rows",
                  f"found {len(group_rows)}")

        # Minor checks
        minor_key = tc.get("minor")
        if minor_key:
            minor_req  = nfp.get_non_fsb_requirements(minor_key, tc["catalog"])
            assert minor_req, f"No definition for minor {minor_key}"
            minor_rows = build_rows(minor_req, courses)
            minor_ids  = [r['id'] for r in minor_rows]
            minor_dup  = [id for id in set(minor_ids) if minor_ids.count(id) > 1]
            check(len(minor_dup) == 0, f"{name} minor: no duplicate rows",
                  f"duplicates: {minor_dup[:3]}")

            def minor_satisfied(code):
                norm_c = sm.norm(code.replace(' ','_'))
                return any(r['course'] and r['course']['code'] == norm_c
                           and r['status'] == 'Satisfied' for r in minor_rows)

            for code in tc.get("minor_satisfied", []):
                check(minor_satisfied(code), f"{name} minor: {code} = Satisfied")

            for code in tc.get("minor_not_satisfied", []):
                check(not minor_satisfied(code),
                      f"{name} minor: {code} = Not Satisfied (correctly)")

    except Exception as e:
        check(False, f"{name}: EXCEPTION", str(e))
        traceback.print_exc()

# ─────────────────────────────────────────────────────────────────────────────
print("\n[6] LA REQUIREMENTS — spot check against known transcripts")
# ─────────────────────────────────────────────────────────────────────────────
try:
    la_spec = importlib.util.spec_from_file_location(
        "la_req", "/home/claude/liberal_arts_requirements.py")
    la_mod = importlib.util.module_from_spec(la_spec)
    la_spec.loader.exec_module(la_mod)

    req = la_mod.get_la_requirements('2022-23')
    check(req is not None and isinstance(req, dict),
          "LA requirements load for 2022-23")
    check('F1' in req and 'W8' in req and 'WI' in req and 'SI' in req,
          "LA requirements has F1, W8, WI, SI keys")

    # Spot-check WI list has enough courses
    wi_courses = req.get('WI', {}).get('courses', []) or []
    check(len(wi_courses) >= 30,
          f"WI course list has ≥30 courses (has {len(wi_courses)})")

    si_courses = req.get('SI', {}).get('courses', []) or []
    check(len(si_courses) >= 20,
          f"SI course list has ≥20 courses (has {len(si_courses)})")

except Exception as e:
    check(False, "LA framework loaded", str(e))

# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)
total  = len(results)
passed = sum(1 for r in results if r.strip().startswith(PASS))
failed = len(failures)

print(f"  Passed:  {passed}/{total}")
print(f"  Failed:  {failed}")

if failures:
    print(f"\n{'='*60}")
    print("FAILURES — must fix before delivering files:")
    print("=" * 60)
    for f in failures:
        print(f"  {FAIL} {f}")
    print(f"\n{'='*60}")
    print("STATUS: *** DO NOT DELIVER FILES — TESTS FAILING ***")
    print("=" * 60)
    sys.exit(1)
else:
    print(f"\n{'='*60}")
    print("STATUS: ALL TESTS PASSED — safe to deliver files ✓")
    print("=" * 60)
    sys.exit(0)
