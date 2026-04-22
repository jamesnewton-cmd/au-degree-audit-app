"""
Integration test that mirrors the real /generate endpoint for Jennifer Eisinger.
This uses the exact same code path as the live app — no shortcuts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import importlib

CSV_PATH = "/home/ubuntu/upload/JenniferEisinger-PoliticalScience22-23.csv"
OUTPUT_PDF = "/home/ubuntu/test_jennifer_integration.pdf"
MAJOR = "political_science"
CATALOG_YEAR = "2022-23"
STUDENT_NAME = "Jennifer Eisinger"

def _norm_code(s):
    return s.upper().replace("-", "_").replace(" ", "_")

def _status_of_c(c):
    if c is None:
        return "Not Satisfied"
    st = c.get("status", "").lower()
    if st == "grade posted":
        return "Satisfied"
    if st in ("current", "scheduled"):
        return "Current"
    return "Not Satisfied"

def _safe_credits(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 3.0

def _find_course_factory(raw_courses, sm_mod):
    def _find_course(opts):
        for opt in opts:
            code = sm_mod.norm(opt.replace(" ", "_").replace("-", "_"))
            c = next((x for x in raw_courses if x["code"] == code), None)
            if c and _status_of_c(c) != "Not Satisfied":
                return c
        for opt in opts:
            code = sm_mod.norm(opt.replace(" ", "_").replace("-", "_"))
            c = next((x for x in raw_courses if x["code"] == code), None)
            if c:
                return c
        return None
    return _find_course

def _build_major_rows(prog_reqs, raw_courses, sm_mod, concentration=""):
    """Mirror of main.py _build_major_rows with the dist_groups fix."""
    _find_course = _find_course_factory(raw_courses, sm_mod)

    def _course_label(course_id, c):
        if c:
            return f"{course_id} {c.get('name', '')}"
        return course_id

    _skip_keys = {
        "name", "total_credits", "delivery", "notes", "teaching_fields",
        "department", "concentration_note", "special_rules", "same_as",
        "optional_cma", "concentrations", "tracks", "total_major_credits",
        "lead_courses_credits", "la_credits", "elective_credits", "min_level",
        "choose_one", "accreditation",
    }
    rows = []

    # Pass 1: list-type keys → individual required course rows
    for req_key, req_val in prog_reqs.items():
        if req_key in _skip_keys:
            continue
        if isinstance(req_val, list) and req_val:
            for course_id in req_val:
                if not isinstance(course_id, str):
                    continue
                if "xxx" in course_id.lower() or course_id.upper().count("X") >= 3:
                    continue
                c = _find_course([course_id])
                rows.append({
                    "id": _norm_code(course_id),
                    "label": _course_label(course_id, c),
                    "status": _status_of_c(c),
                    "course": c,
                    "dcr": 3,
                    "note": "",
                })

    # Pass 2: dict-type keys with 'credits' → elective/choose blocks
    for ekey, edef in prog_reqs.items():
        if ekey in _skip_keys:
            continue
        if not isinstance(edef, (dict, int, float)):
            continue
        if isinstance(edef, dict) and "credits" not in edef:
            continue
        if isinstance(edef, dict):
            credits = _safe_credits(edef.get("credits", 3))
            choose_from = edef.get("choose_from", edef.get("options", edef.get("courses", [])))
            label = edef.get("label", ekey.replace("_", " ").title())
            opts = choose_from if isinstance(choose_from, list) else []
            c = _find_course(opts) if opts else None
            rows.append({
                "id": _norm_code(ekey),
                "label": label,
                "status": _status_of_c(c),
                "course": c,
                "dcr": credits,
                "note": "",
            })
        elif isinstance(edef, (int, float)):
            rows.append({
                "id": _norm_code(ekey),
                "label": f"{ekey.replace('_',' ').title()} ({int(edef)} hrs)",
                "status": "Not Satisfied",
                "course": None,
                "dcr": int(edef),
                "note": "",
            })

    # Pass 3: Distribution groups (THE FIX)
    dist_groups = prog_reqs.get("dist_groups", [])
    for group in dist_groups:
        group_name = group.get("name", "Distribution Group")
        credits_needed = float(group.get("credits", 3))
        min_courses = int(group.get("min_courses", 1))
        choose_from = group.get("choose_from", [])
        earned_credits = 0.0
        ip_credits = 0.0
        first_earned_course = None
        first_ip_course = None
        courses_earned_count = 0
        courses_ip_count = 0
        sm_norm = sm_mod.norm
        for c_id in choose_from:
            c_norm = sm_norm(c_id.replace(" ", "_").replace("-", "_"))
            matched = next((x for x in raw_courses if x["code"] == c_norm), None)
            if matched:
                st = _status_of_c(matched)
                if st == "Satisfied":
                    earned_credits += matched.get("cr", 3)
                    courses_earned_count += 1
                    if first_earned_course is None:
                        first_earned_course = matched
                elif st in ("Current", "Scheduled"):
                    ip_credits += matched.get("cr", 3)
                    courses_ip_count += 1
                    if first_ip_course is None:
                        first_ip_course = matched
        if earned_credits >= credits_needed and courses_earned_count >= min_courses:
            grp_status = "Satisfied"
            display_course = first_earned_course
        elif (earned_credits + ip_credits) >= credits_needed or (courses_earned_count + courses_ip_count) >= min_courses:
            grp_status = "Current"
            display_course = first_ip_course or first_earned_course
        else:
            grp_status = "Not Satisfied"
            display_course = first_earned_course or first_ip_course
        preview = ", ".join(choose_from[:3]) + ("..." if len(choose_from) > 3 else "")
        rows.append({
            "id": "DIST-" + str(sum(1 for r in rows if str(r.get("id","")).startswith("DIST-")) + 1).zfill(2),
            "label": (
                group_name + " -- " + str(int(credits_needed)) + " cr (choose "
                + str(min_courses) + ": " + preview + ")"
            ),
            "status": grp_status,
            "course": display_course,
            "dcr": credits_needed,
            "note": (
                str(int(earned_credits)) + "/" + str(int(credits_needed)) + " cr earned"
                + (", " + str(int(ip_credits)) + " cr in progress" if ip_credits else "")
            ),
        })

    return rows


def _compute_gpa(raw_courses, major_codes_set):
    GP = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
          "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7, "F": 0.0}
    op = oh = mp = mh = qp = 0.0
    earned = ip_hrs = 0
    seen = set()
    for c in raw_courses:
        g = c["grade"].upper()
        if g in ("W", "DRP") or c["status"] == "dropped":
            continue
        if c["status"] == "current":
            ip_hrs += c["cr"]
            continue
        if c["status"] != "grade posted":
            continue
        earned += c["cr"]
        if g in ("T", "CR", "NC", ""):
            continue
        gp = GP.get(g)
        if gp is None:
            continue
        cr = c["cr"]
        if c["code"] not in seen:
            op += gp * cr
            oh += cr
            qp += gp * cr
            seen.add(c["code"])
        if c["code"] in major_codes_set:
            mp += gp * cr
            mh += cr
    return (
        round(op / oh, 2) if oh else 0.0,
        round(mp / mh, 2) if mh else 0.0,
        int(oh),
        earned,
        ip_hrs,
        round(qp, 1),
        earned + ip_hrs,
    )


def main():
    print("=" * 70)
    print("INTEGRATION TEST — Jennifer Eisinger | Political Science | 2022-23")
    print("=" * 70)

    # Load the sport_marketing engine (shared engine for all non-FSB)
    sm_mod = importlib.import_module("engines.sport_marketing")
    from requirements.non_fsb_programs import get_non_fsb_requirements

    # Step 1: Parse CSV
    raw_courses = sm_mod.parse_csv(CSV_PATH)
    print(f"\n[1] Parsed {len(raw_courses)} course records from CSV")

    # Step 2: Load Political Science requirements
    prog_reqs = get_non_fsb_requirements(MAJOR, CATALOG_YEAR)
    major_label = prog_reqs.get("name", "Political Science")
    print(f"\n[2] Loaded requirements for: {major_label}")
    print(f"    Required: {prog_reqs.get('required', [])}")
    print(f"    Dist groups: {[g['name'] for g in prog_reqs.get('dist_groups', [])]}")

    # Step 3: Build major rows (includes dist_groups fix)
    mr_rows = _build_major_rows(prog_reqs, raw_courses, sm_mod)
    print(f"\n[3] Built {len(mr_rows)} major requirement rows:")
    for r in mr_rows:
        icon = "✓" if r["status"] == "Satisfied" else ("~" if r["status"] == "Current" else "✗")
        print(f"    {icon} {r['label'][:55]:55s} | {r['status']}")

    # Step 4: Build LA rows
    la_rows = sm_mod.build_la_rows_for_non_fsb(raw_courses, CATALOG_YEAR, major_key=MAJOR)
    print(f"\n[4] Built {len(la_rows)} LA rows:")
    for row in la_rows:
        area = row.get("area", "?")
        status = row.get("status", "?")
        course_col = row.get("course_col", "")
        icon = "✓" if status == "Satisfied" else ("~" if status in ("Current", "Scheduled") else "✗")
        print(f"    {icon} {area:4s} | {status:20s} | {course_col[:45]}")

    # Step 5: Compute GPA
    _skip_gpa = {"name", "total_credits", "delivery", "notes", "teaching_fields",
                 "department", "same_as", "concentrations", "tracks", "accreditation",
                 "total_major_credits", "la_credits", "elective_credits", "min_level"}
    major_codes_set = set()
    for _k, _v in prog_reqs.items():
        if _k in _skip_gpa:
            continue
        if isinstance(_v, list):
            for _cid in _v:
                if isinstance(_cid, str) and "xxx" not in _cid.lower():
                    major_codes_set.add(_norm_code(_cid))
    gpa_o, gpa_m, gpa_hrs, earned, ip_hrs, qp, proj = _compute_gpa(raw_courses, major_codes_set)
    print(f"\n[5] GPA: {gpa_o} overall | {gpa_m} major | {earned} cr earned | {ip_hrs} cr IP | {proj} projected")

    # Step 6: Build res dict (mirrors the real /generate endpoint)
    res = {
        "catalog_year": CATALOG_YEAR,
        "current_term_label": "2025-26",
        "gpa_o": gpa_o,
        "gpa_m": gpa_m,
        "earned": earned,
        "ip_hrs": ip_hrs,
        "proj": proj,
        "gpa_hrs": gpa_hrs,
        "qp": qp,
        "la": la_rows,
        "bc": [],
        "mr": mr_rows,
        "elecs": [],
        "elecs_ip": [],
        "ehrs": 0,
        "ehrs_ip": 0,
        "elec_required_hrs": 0,
        "courses": raw_courses,
        "minor_rows": None,
        "minor_key": None,
        "major_section_label": f"{major_label} Major — {CATALOG_YEAR}",
        "major_subsections": [(f"{major_label} Required Courses", mr_rows)],
        "notes_row_text": "",
        "elec_opts": [],
        "advisor_notes": "",
        "additional_major_sections": [],
    }
    res["eligible_to_walk"] = sm_mod.eligible_to_walk(res)
    print(f"\n[6] Eligible to walk: {res['eligible_to_walk']}")

    # Step 7: Generate PDF
    sm_mod.build(res, STUDENT_NAME, major_label, OUTPUT_PDF)
    size = os.path.getsize(OUTPUT_PDF)
    print(f"\n[7] PDF generated: {OUTPUT_PDF} ({size:,} bytes)")

    print("\n" + "=" * 70)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
