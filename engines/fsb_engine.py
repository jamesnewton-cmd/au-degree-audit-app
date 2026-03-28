"""
Anderson University — Generic FSB Major Engine
Handles: Marketing, Accounting, Finance, Business Analytics,
         Engineering Management, Global Business,
         Music & Entertainment Business, Business & Integrative Leadership

Uses fsb_majors.py for major-specific requirements and shares all
parsing/audit helpers with sport_marketing.py.
The major key is passed in at runtime via the MAJOR_KEY module-level variable,
which main.py sets before calling audit() and build().
"""

# ── Import shared helpers from sport_marketing ────────────────────────────────
from engines.sport_marketing import (
    parse_csv,
    apply_exceptions,
    cmap,
    norm,
    best,
    done,
    ip,
    sched,
    xfer,
    drop,
    status_of,
    grade_disp,
    cr_disp,
    build_la_rows_for_non_fsb,
    MINOR_DEFS,
    BUS_CORE,
    BUS_CORE_2526,
    LA_ROWS,
    MATH_OPTS,
)
from engines.pdf_template import build as template_build
from requirements.fsb_majors import FSB_MAJORS
from requirements.fsb_minors import FSB_MINORS

# ── Set by main.py before each call ──────────────────────────────────────────
MAJOR_KEY = None  # e.g. 'marketing'
CATALOG_YEAR = "2023-24"


def _get_req(catalog_year):
    """Return the requirement dict for the current major + catalog year."""
    major_data = FSB_MAJORS.get(MAJOR_KEY)
    if major_data is None:
        raise ValueError(f"Unknown FSB major key: {MAJOR_KEY}")

    req = major_data.get(catalog_year)
    if req is None:
        raise ValueError(f"FSB major '{MAJOR_KEY}' is not available in catalog year {catalog_year}")

    return req


def _norm_code(code_str):
    return code_str.strip().upper().replace(" ", "_").replace("-", "_")


FSB_W8_BY_MAJOR = {
    # Source: W8_-_Crosslist.csv (11/14/2023)
    "sport_marketing": ["BSNS_1050", "BSNS_4110", "BSNS_4330", "BSNS_4560", "BSNS_4800"],
    "marketing": ["BSNS_1050", "BSNS_2810", "BSNS_3130", "BSNS_3210", "BSNS_4110", "BSNS_4550", "BSNS_4800"],
    "accounting": ["BSNS_1050", "ACCT_2020", "ACCT_3500", "ACCT_3860", "ACCT_4020", "BSNS_4800"],
    "business_analytics": ["BSNS_1050"],
    "finance": ["BSNS_1050", "BSNS_4150", "BSNS_4800"],
    "global_business": ["BSNS_1050", "BSNS_3850", "BSNS_4800"],
    "management": ["BSNS_1050", "BSNS_2550", "BSNS_4240", "BSNS_4310", "BSNS_4500", "BSNS_4800"],
    "engineering_management": ["BSNS_1050"],
    "music_entertainment_business": ["MUBS_4800", "BSNS_4810"],
    "business_integrative_leadership": ["LEAD_4990"],
}


def audit(courses, minor_key=None):
    cm = cmap(courses)

    # ── Exception rules (same as sport_marketing) ─────────────────────────────
    has_1110 = cm.get("ENGL_1110") or cm.get("ENGL_1100")
    has_1120 = cm.get("ENGL_1120")
    if not has_1110 and has_1120:
        synthetic = {
            "code": "ENGL_1110",
            "raw": "ENGL-1110",
            "name": "Rhetoric and Composition (tested out)",
            "cr": 3,
            "status": "grade posted",
            "grade": "T",
            "reg_date": "",
        }
        courses = courses + [synthetic]
        cm["ENGL_1110"] = synthetic

    has_lart = cm.get("LART_1050")
    if not has_lart:
        synthetic = {
            "code": "LART_1050",
            "raw": "LART-1050",
            "name": "First-Year Seminar (exempt)",
            "cr": 0,
            "status": "grade posted",
            "grade": "T",
            "reg_date": "",
        }
        courses = courses + [synthetic]
        cm["LART_1050"] = synthetic

    def find(opts):
        return best(courses, opts)

    # F1 for W8 auto-satisfy
    f1 = find(["LART_1050"])
    f1_ok = f1 is not None and done(f1)

    # ── LA rows (use the FSB-specific LA_ROWS same as sport_marketing) ─────────
    w8_courses = FSB_W8_BY_MAJOR.get(MAJOR_KEY, FSB_W8_BY_MAJOR["sport_marketing"])
    la = []
    for row in LA_ROWS:
        area, course_col, req_txt, opts, dcr = row
        if area == "W8":
            if f1_ok:
                c = cm.get("BSNS_1050")
                s = "Satisfied"
            else:
                c = None
                s = "Not Satisfied"
                for code in w8_courses:
                    candidate = cm.get(code)
                    if candidate and done(candidate):
                        c = candidate
                        s = "Satisfied"
                        break
                    elif candidate and ip(candidate) and s != "Satisfied":
                        c = candidate
                        s = "Current"
                    elif candidate and sched(candidate) and s not in ("Satisfied", "Current"):
                        c = candidate
                        s = "Scheduled"
        elif area == "WI" and not opts:
            # WI #2 — check for any upper-div WI course
            wi_upper = [
                "BSNS_4910",
                "BSNS_3120",
                "BSNS_4110",
                "ENGL_3110",
                "ENGL_3190",
                "ENGL_3580",
                "COMM_3130",
                "HIST_3260",
            ]
            c = None
            s = "Not Satisfied"
            for code in wi_upper:
                candidate = cm.get(code)
                if candidate and done(candidate):
                    c = candidate
                    s = "Satisfied"
                    break
                elif candidate and ip(candidate) and s != "Satisfied":
                    c = candidate
                    s = "Current"
                elif candidate and sched(candidate) and s not in ("Satisfied", "Current"):
                    c = candidate
                    s = "Scheduled"
        else:
            c = find(opts) if opts else None
            s = status_of(c)
        if course_col is None and c is not None:
            course_col = f"{c['raw']} {c['name']}"
        la.append(
            {
                "area": area,
                "course_col": course_col or "",
                "req": req_txt,
                "status": s,
                "course": c,
                "dcr": dcr,
            }
        )

    # ── Business Core ─────────────────────────────────────────────────────────
    req = _get_req(CATALOG_YEAR)
    uses_2526_core = CATALOG_YEAR == "2025-26"
    core_rows_def = BUS_CORE_2526 if uses_2526_core else BUS_CORE
    bc = []
    for rid, label, opts, dcr in core_rows_def:
        c = find(opts)
        s = status_of(c)
        bc.append({"id": rid, "label": label, "opts": opts, "status": s, "course": c, "dcr": dcr})

    # ── Major Required Courses ────────────────────────────────────────────────
    mr = []
    major_name = req.get("name", MAJOR_KEY.replace("_", " ").title())

    # Standard required_courses list
    for course_def in req.get("required_courses", []):
        if isinstance(course_def, dict):
            code = course_def["code"]
            name = course_def.get("name", code)
            dcr = course_def.get("credits", 3)
        else:
            code = course_def
            name = code
            dcr = 3
        rid = _norm_code(code)
        c = find([rid])
        note = ""
        if course_def.get("also_satisfies"):
            sats = course_def["also_satisfies"]
            if "F4 SI" in sats or "SI" in sats:
                note = " (SI)"
            elif any("WI" in x for x in sats):
                note = " (WI)"
        mr.append(
            {
                "id": rid,
                "label": f"{code} {name}",
                "status": status_of(c),
                "course": c,
                "dcr": dcr,
                "note": note,
            }
        )

    # Standalone core (Engineering Management 22-23)
    for course_def in req.get("standalone_core", []):
        code = course_def["code"]
        dcr = course_def.get("credits", 3)
        rid = _norm_code(code)
        c = find([rid])
        mr.append(
            {"id": rid, "label": code, "status": status_of(c), "course": c, "dcr": dcr, "note": ""}
        )

    # lead_courses (Business & Integrative Leadership)
    for code in req.get("lead_courses", []):
        rid = _norm_code(code)
        c = find([rid])
        mr.append(
            {"id": rid, "label": code, "status": status_of(c), "course": c, "dcr": 3, "note": ""}
        )

    # Choose-one blocks
    for key in req:
        if key.startswith("choose_one"):
            opts_raw = req[key].get("options", req[key]) if isinstance(req[key], dict) else req[key]
            if isinstance(opts_raw, list):
                nids = [_norm_code(o) for o in opts_raw]
                c = find(nids)
                label = (
                    f"Choose one of: {', '.join(opts_raw[:3])}{'...' if len(opts_raw) > 3 else ''}"
                )
                mr.append(
                    {
                        "id": "CHOOSE_ONE",
                        "label": label,
                        "status": status_of(c),
                        "course": c,
                        "dcr": 3,
                        "note": "",
                    }
                )

    # Electives
    elecs = []
    elecs_ip = []
    ehrs = 0
    ehrs_ip = 0
    elec_required_hrs = 0
    elec_opts = []
    elec_def = req.get("elective") or req.get("electives")
    if elec_def and isinstance(elec_def, dict):
        elec_required_hrs = elec_def.get("credits", 0)
        choose_from = elec_def.get("choose_from", elec_def.get("courses", []))
        elec_opts = [c.replace(" ", "-") for c in choose_from]
        for opt in choose_from:
            rid = _norm_code(opt)
            c2 = cm.get(rid)
            if c2 and done(c2):
                elecs.append(c2)
                ehrs += c2["cr"]
            elif c2 and (ip(c2) or sched(c2)):
                elecs_ip.append(c2)
                ehrs_ip += c2["cr"]

    # ── Minor ─────────────────────────────────────────────────────────────────
    minor_rows = None
    if minor_key and minor_key in MINOR_DEFS:
        from engines.sport_marketing import audit_minor

        minor_rows = audit_minor(courses, minor_key, find, status_of)

    # ── GPA ───────────────────────────────────────────────────────────────────
    gp_map = {
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "D-": 0.7,
        "F": 0.0,
    }

    major_codes = set()
    for r in mr:
        major_codes.add(r["id"])
    for r in bc:
        major_codes.add(r["id"])

    gpa_hrs = 0
    qp = 0.0
    mgpa_hrs = 0
    mqp = 0.0
    earned = 0
    ip_hrs = 0
    for c in courses:
        g = c["grade"].upper()
        if done(c) and g not in ("", "T", "CR"):
            pts = gp_map.get(g, 0.0)
            gpa_hrs += c["cr"]
            qp += c["cr"] * pts
            if _norm_code(c["raw"]) in major_codes:
                mgpa_hrs += c["cr"]
                mqp += c["cr"] * pts
        if done(c) and g not in ("", "W", "DRP", "NC", "F"):
            earned += c["cr"]
        if ip(c):
            ip_hrs += c["cr"]

    sched_hrs = sum(c["cr"] for c in courses if sched(c))
    proj = earned + ip_hrs + sched_hrs
    gpa_o = round(qp / gpa_hrs, 2) if gpa_hrs else 0.0
    gpa_m = round(mqp / mgpa_hrs, 2) if mgpa_hrs else 0.0

    return {
        "catalog_year": CATALOG_YEAR,
        "gpa_o": gpa_o,
        "gpa_m": gpa_m,
        "earned": earned,
        "ip_hrs": ip_hrs,
        "proj": proj,
        "gpa_hrs": gpa_hrs,
        "qp": round(qp, 1),
        "la": la,
        "bc": bc,
        "mr": mr,
        "elecs": elecs,
        "elecs_ip": elecs_ip,
        "ehrs": ehrs,
        "ehrs_ip": ehrs_ip,
        "elec_required_hrs": elec_required_hrs,
        "elec_opts": elec_opts,
        "courses": courses,
        "minor_rows": minor_rows,
        "minor_key": minor_key,
        "major_name": major_name,
        "advisor_notes": "",
        "additional_major_sections": [],
    }


def build(res, student_name, major_label, out, exceptions=""):
    """Delegate to shared PDF template."""
    yr = res.get("catalog_year", CATALOG_YEAR)
    req = _get_req(yr)
    major_name = req.get("name", major_label)
    uses_2526_core = yr == "2025-26"
    core_hrs = 48 if uses_2526_core else 43

    res.setdefault("catalog_year", yr)
    res.setdefault("current_term_label", "2025-26")
    res.setdefault("major_section_label", f"{major_name} — {yr}")
    res.setdefault("advisor_notes", "")
    res.setdefault("additional_major_sections", [])

    elec_required_hrs = res.get("elec_required_hrs", 0)
    ehrs = res.get("ehrs", 0)
    res.setdefault(
        "elec_section_label",
        f"{major_name} Electives — {elec_required_hrs} hrs required  (earned: {ehrs} hrs)",
    )

    # Determine notes row
    notes_parts = []
    for r in res.get("mr", []):
        note = r.get("note", "")
        if " (SI)" in note:
            notes_parts.append(f"{r['id'].replace('_','-')} = SI")
        if " (WI)" in note:
            notes_parts.append(f"{r['id'].replace('_','-')} = WI")
    w8_codes_for_major = FSB_W8_BY_MAJOR.get(MAJOR_KEY, FSB_W8_BY_MAJOR["sport_marketing"])
    w8_label = ", ".join(code.replace("_", "-") for code in w8_codes_for_major)
    notes_parts.append(
        f"W8 satisfied by: {w8_label}  ·  W8 auto-satisfied when F1 (LART-1050) complete"
    )
    res.setdefault("notes_row_text", "  ·  ".join(notes_parts))

    # Build major_subsections
    if "major_subsections" not in res:
        bc_rows = [dict(r, note=r.get("note", "")) for r in res.get("bc", [])]
        mr_rows = [dict(r, note=r.get("note", "")) for r in res.get("mr", [])]
        res["major_subsections"] = []
        if bc_rows:
            res["major_subsections"].append(
                (f"Business Core Requirements ({core_hrs} hrs)", bc_rows)
            )
        if mr_rows:
            res["major_subsections"].append((f"{major_name} Required Courses", mr_rows))

    # Minor name
    minor_key = res.get("minor_key", "")
    if res.get("minor_rows") and minor_key:
        res.setdefault("minor_name", FSB_MINORS.get(minor_key, {}).get("name", "Minor"))

    template_build(res, student_name, major_label, out, exceptions=exceptions)
