"""
Anderson University — Degree Audit Generator
Exact match to Isaac Bair template.
"""

import csv, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── EXACT COLORS FROM ISAAC BAIR ─────────────────────────────────────────────
MAROON = colors.HexColor("#8B1A2B")  # title bar / page 4 section headers
GOLD_HEAD = colors.HexColor("#B8860B")  # section headings text (gold/olive)
GOLD_BAR = colors.HexColor("#C9A84C")  # page 4 LA/Major section bar bg
BLUE_BAR = colors.HexColor("#1F3864")  # page 4 Credit/WI section bar bg
COL_HDR_BG = colors.HexColor("#8B1A2B")  # table column header bg (maroon)
COL_HDR_TXT = colors.white
SUB_HDR_BG = colors.HexColor("#D4C5A0")  # sub-section row (tan/gold)
SUB_HDR_TXT = colors.HexColor("#3B2A00")
ROW_ODD = colors.HexColor("#F5F2EC")  # alternating row (warm off-white)
ROW_EVEN = colors.white
SATISFIED = colors.HexColor("#375623")  # green text
CURRENT_CLR = colors.HexColor("#7F4700")  # amber/orange text
NOT_SAT = colors.HexColor("#8B1A2B")  # red/maroon text
TERM_CLR = colors.HexColor("#1A1A1A")  # term column color (black)
TRANSFER_CLR = colors.HexColor("#8B6914")  # italic gold for Transfer
XMARK_CLR = colors.HexColor("#CC3300")  # red-orange ✗ items
DARK = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#F0F0F0")
BORDER = colors.HexColor("#CCCCCC")
WHITE = colors.white

PAGE_W, PAGE_H = letter
LM = RM = 0.5 * inch
TM = BM = 0.5 * inch
CW = PAGE_W - LM - RM


# ── STYLES ────────────────────────────────────────────────────────────────────
def ps(name, **kw):
    d = dict(
        fontName="Helvetica", fontSize=9, leading=11, textColor=DARK, spaceAfter=0, spaceBefore=0
    )
    d.update(kw)
    return ParagraphStyle(name, **d)


P = {
    # Title bar
    "title": ps("title", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, leading=13),
    # Section headings (gold, outside tables)
    "sec_gold": ps(
        "sec_gold", fontName="Helvetica-Bold", fontSize=10, textColor=GOLD_HEAD, leading=13
    ),
    # Table column headers
    "col_hdr": ps("col_hdr", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11),
    # Sub-section rows inside tables
    "sub_hdr": ps(
        "sub_hdr",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=SUB_HDR_TXT,
        leading=11,
        alignment=TA_CENTER,
    ),
    # Normal cell
    "cell": ps("cell", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "cell_b": ps("cell_b", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, leading=11),
    # Status colors
    "sat": ps("sat", fontName="Helvetica-Bold", fontSize=8.5, textColor=SATISFIED, leading=11),
    "cur": ps("cur", fontName="Helvetica-Bold", fontSize=8.5, textColor=CURRENT_CLR, leading=11),
    "nos": ps("nos", fontName="Helvetica-Bold", fontSize=8.5, textColor=NOT_SAT, leading=11),
    # Course history term
    "term": ps("term", fontName="Helvetica", fontSize=8, textColor=TERM_CLR, leading=10),
    "term_tr": ps(
        "term_tr", fontName="Helvetica-Oblique", fontSize=8, textColor=TRANSFER_CLR, leading=10
    ),
    "code_b": ps("code_b", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=10),
    "hist_cell": ps("hist_cell", fontName="Helvetica", fontSize=8, textColor=DARK, leading=10),
    # Eligibility table
    "elig_lbl": ps("elig_lbl", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "elig_val": ps(
        "elig_val",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=DARK,
        leading=11,
        alignment=TA_RIGHT,
    ),
    "elig_yes": ps(
        "elig_yes",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=SATISFIED,
        leading=11,
        alignment=TA_RIGHT,
    ),
    "elig_no": ps(
        "elig_no",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=NOT_SAT,
        leading=11,
        alignment=TA_RIGHT,
    ),
    "elig_hdr": ps(
        "elig_hdr", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11
    ),
    "elig_hdr_r": ps(
        "elig_hdr_r",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=WHITE,
        leading=11,
        alignment=TA_RIGHT,
    ),
    # Action plan
    "ap_cat_lbl": ps("ap_cat_lbl", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "ap_cat_hdr": ps(
        "ap_cat_hdr", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, leading=11
    ),
    "ap_x": ps("ap_x", fontName="Helvetica", fontSize=8.5, textColor=XMARK_CLR, leading=11),
    "ap_rec": ps("ap_rec", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "ap_title": ps(
        "ap_title", fontName="Helvetica-Bold", fontSize=9.5, textColor=WHITE, leading=12
    ),
    "ap_bar_gold": ps(
        "ap_bar_gold", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12
    ),
    "ap_bar_blue": ps(
        "ap_bar_blue", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12
    ),
    "summary": ps("summary", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    # Footer
    "footer": ps(
        "footer", fontName="Helvetica", fontSize=7, textColor=GRAY, leading=9, alignment=TA_CENTER
    ),
    # Metrics
    "met_lbl": ps("met_lbl", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "met_val": ps(
        "met_val",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=DARK,
        leading=11,
        alignment=TA_RIGHT,
    ),
    "met_hdr_l": ps(
        "met_hdr_l", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11
    ),
    "met_hdr_r": ps(
        "met_hdr_r",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=WHITE,
        leading=11,
        alignment=TA_RIGHT,
    ),
    "note": ps("note", fontName="Helvetica-Oblique", fontSize=7.5, textColor=GRAY, leading=10),
}

THIN = colors.HexColor("#CCCCCC")
PAD = dict(TOPPADDING=3, BOTTOMPADDING=3, LEFTPADDING=6, RIGHTPADDING=6)


def padded(*extra):
    base = [
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, THIN),
    ]
    base.extend(extra)
    return TableStyle(base)


# ── CSV ───────────────────────────────────────────────────────────────────────
def norm(c):
    return c.strip().upper().replace("-", "_")


def parse_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append(
                {
                    "code": norm(r.get("Course Code", "")),
                    "raw": r.get("Course Code", "").strip().upper(),
                    "name": r.get("Course Name", "").strip(),
                    "cr": _int(r.get("Credits", "0")),
                    "status": r.get("Status", "").strip().lower(),
                    "grade": r.get("Letter Grade", "").strip(),
                    "reg_date": r.get("Registration Date", "").strip(),
                }
            )
    # PEHS-1200 note: Co-Curricular Activity courses (PEHS-1200) are student-athlete
    # participation credits — 1 credit, earned once. NC grade = not satisfactory, excluded
    # by done() logic. These courses are never tracked as degree requirements.
    # Remove fully blank rows (no status AND no grade — phantom duplicates from export)
    rows = [c for c in rows if c["status"] or c["grade"]]
    # Deduplicate: for each course code keep the best record
    # Priority: grade posted > current > dropped > not started/blank
    seen = {}

    def priority(c):
        if c["status"] == "grade posted" and c["grade"].upper() not in ("", "W", "WF", "DRP", "NC"):
            return 0
        if c["status"] == "current":
            return 1
        if c["status"] == "scheduled":
            return 2
        if c["status"] == "grade posted" and c["grade"].upper() == "NC":
            return 3
        if c["status"] == "dropped" or c["grade"].upper() in ("DRP", "W"):
            return 4
        return 5

    for c in rows:
        k = c["code"]
        if k not in seen or priority(c) < priority(seen[k]):
            seen[k] = c
    return list(seen.values())


def _int(v):
    try:
        return int(str(v).strip())
    except:
        return 0


def done(c):
    return c["status"] == "grade posted" and c["grade"].upper() not in ("", "W", "WF", "DRP", "NC")


def ip(c):
    return c["status"] == "current"


def sched(c):
    return c["status"] == "scheduled"


def xfer(c):
    return c["grade"].upper() == "T"


def drop(c):
    return c["grade"].upper() in ("DRP", "W", "WF") or c["status"] == "dropped"


def best(courses, codes):
    norms = [norm(x) for x in codes]
    found = [c for c in courses if c["code"] in norms and not drop(c)]
    for f in found:
        if done(f):
            return f
    for f in found:
        if ip(f):
            return f
    # Scheduled courses satisfy requirements pending final grade
    for f in found:
        if sched(f):
            return f
    return found[0] if found else None


def cmap(courses):
    m = {}
    for c in courses:
        k = c["code"]
        if k not in m:
            m[k] = c
        else:
            e = m[k]
            if done(c) and not done(e):
                m[k] = c
            elif ip(c) and not done(e) and not ip(e):
                m[k] = c
            elif sched(c) and not done(e) and not ip(e) and not sched(e):
                m[k] = c
    return m


# ── STATUS ────────────────────────────────────────────────────────────────────
def status_of(c):
    if c is None:
        return "Not Satisfied"
    if done(c):
        return "Satisfied"
    if ip(c):
        return "Current"
    if sched(c):
        return "Scheduled"
    return "Not Satisfied"


def status_para(s):
    if s == "Satisfied":
        return Paragraph(s, P["sat"])
    if s == "Current":
        return Paragraph(s, P["cur"])
    if s == "Scheduled":
        return Paragraph(s, P["cur"])  # same amber as Current
    return Paragraph(s, P["nos"])


def grade_disp(c):
    if c is None:
        return ""
    if ip(c):
        return "IP"
    return c["grade"] if c["grade"] else ""


def cr_disp(c, fallback=""):
    if c is None:
        return str(fallback) if fallback else ""
    return str(c["cr"])


# ── REQUIREMENT LISTS ─────────────────────────────────────────────────────────
MATH_OPTS = ["MATH_1300", "MATH_1400", "MATH_2010"]

BUS_CORE = [
    ("MATH_1300", "MATH-1300 Finite Mathematics (or MATH-1400/2010)", MATH_OPTS, 3),
    ("ACCT_2010", "ACCT-2010 Principles of Accounting I", ["ACCT_2010"], 3),
    ("ACCT_2020", "ACCT-2020 Principles of Accounting II", ["ACCT_2020"], 3),
    ("BSNS_1050", "BSNS-1050 Business as a Profession", ["BSNS_1050"], 2),
    ("BSNS_2310", "BSNS-2310 Business Analytics", ["BSNS_2310"], 3),
    ("BSNS_2450", "BSNS-2450 Data Analytics and Decision Making", ["BSNS_2450"], 3),
    ("BSNS_2510", "BSNS-2510 Principles of Finance", ["BSNS_2510"], 3),
    ("BSNS_2710", "BSNS-2710 Principles of Management", ["BSNS_2710"], 3),
    ("BSNS_2810", "BSNS-2810 Principles of Marketing", ["BSNS_2810"], 3),
    ("BSNS_3270", "BSNS-3270 Project Management", ["BSNS_3270"], 3),
    ("BSNS_3420", "BSNS-3420 Business Law", ["BSNS_3420"], 3),
    ("BSNS_4500", "BSNS-4500 Strategic Management", ["BSNS_4500"], 3),
    ("BSNS_4910", "BSNS-4910 Senior Seminar in Business / Ethics & Leadership", ["BSNS_4910"], 2),
    ("ECON_2010", "ECON-2010 Principles of Macroeconomics", ["ECON_2010"], 3),
    ("ECON_2020", "ECON-2020 Principles of Microeconomics", ["ECON_2020"], 3),
]

MGMT_REQ = [
    ("BSNS_3120", "BSNS-3120 Global Business", ["BSNS_3120"], 3),
    ("BSNS_3230", "BSNS-3230 Human Resource Management", ["BSNS_3230"], 3),
    ("BSNS_4010", "BSNS-4010 Organizational Behavior and Theory", ["BSNS_4010"], 3),
    ("BSNS_4480", "BSNS-4480 Leadership", ["BSNS_4480"], 3),
    ("BSNS_PRAC", "BSNS-3850 Practicum / BSNS-4800 Internship", ["BSNS_3850", "BSNS_4800"], 2),
]

ELEC_OPTS = [
    "BSNS_3100",
    "BSNS_3240",
    "BSNS_3510",
    "BSNS_4050",
    "BSNS_4120",
    "BSNS_4240",
    "BSNS_4310",
    "BSNS_4310_23",
]

# Liberal Arts rows (Area label, Course display, Requirement text, option codes, default_cr)
LA_ROWS = [
    (
        "F1",
        "LART-1050 First-Year Exper Seminar",
        "F1 LART-1050 Understanding College",
        ["LART_1050"],
        1,
    ),
    (
        "F2",
        "BSNS-3420 Business Law",
        "F2 BSNS-3420 Civil Discourse & Critical Reasoning",
        ["BSNS_3420", "ENGL_3190", "ENGL_3580", "HIST_2300", "HNRS_2125", "PSYC_3200", "SOCI_2450"],
        3,
    ),
    (
        "F3",
        "ENGL-1110 Rhetoric and Composition",
        "F3 ENGL-1110 Writing I — ENGL-1110 (or ENGL-1100/HNRS-2110)",
        ["ENGL_1110", "ENGL_1100", "HNRS_2110"],
        3,
    ),
    (
        "F3",
        "ENGL-1120 Rhetoric and Research",
        "F3 ENGL-1120 Writing II — ENGL-1120 (grade of C- or better required)",
        ["ENGL_1120"],
        3,
    ),
    (
        "F4",
        "COMM-1000 Intro to Speech Communication",
        "F4 COMM-1000 Speaking & Listening (COMM-1000 + 1 SI)",
        ["COMM_1000"],
        3,
    ),
    ("F5", "MATH-1300 Finite Mathematics", "F5 MATH-1300 Quantitative Reasoning", MATH_OPTS, 3),
    ("F6", "BIBL-2000 Intro to the Bible", "F6 BIBL-2000 Biblical Literacy", ["BIBL_2000"], 3),
    (
        "F7",
        "PEHS-1000 Fitness/Wellness for Life",
        "F7 PEHS-1000 Personal Wellness",
        ["PEHS_1000"],
        2,
    ),
    (
        "W1",
        None,
        "W1 BIBL-3410 Christian Ways of Knowing",
        ["BIBL_3410", "RELI_3000", "BIBL_3000", "RLGN_3000"],
        3,
    ),
    (
        "W2",
        None,
        "W2 Scientific Ways of Knowing (4 hrs)",
        ["BIOL_1000", "CHEM_1000", "PHYS_1000", "EXSC_2140", "ENVS_1000"],
        4,
    ),
    (
        "W3",
        None,
        "W3 Civic Ways of Knowing",
        ["HIST_2030", "HIST_2110", "POLS_1000", "SOCI_1000", "CRIM_2520", "HNRS_2110"],
        3,
    ),
    (
        "W4",
        None,
        "W4 Aesthetic Ways of Knowing",
        [
            "ARTS_1250",
            "MUSC_2210",
            "THEA_1000",
            "ARTS_1210",
            "ARTS_1230",
            "MUSC_1000",
            "ARTS_1000",
            "ARTH_3040",
        ],
        3,
    ),
    (
        "W5",
        None,
        "W5 Social & Behavioral Ways of Knowing",
        ["ECON_2010", "PSYC_1000", "SOCI_1000"],
        3,
    ),
    (
        "W6",
        None,
        "W6 Modern Language (1 course, placement-based)",
        ["GERM_1010", "SPAN_1010", "SPAN_1020", "FREN_1010", "GERM_1020", "MLAN_2000", "SPAN_3010"],
        4,
    ),
    (
        "W7",
        None,
        "W7 Global/Intercultural Ways of Knowing",
        [
            "BSNS_3120",
            "COMM_3050",
            "HIST_3260",
            "HIST_3300",
            "HIST_3425",
            "POSC_3320",
            "POSC_3450",
            "ENGR_2090",
            "ENGL_2220",
            "MLAN_2000",
            "SPAN_3020",
            "SOCI_2450",
        ],
        3,
    ),
    (
        "W8",
        None,
        "W8 Experiential Ways of Knowing",
        ["BSNS_1050", "BSNS_2550", "BSNS_4240", "BSNS_4310", "BSNS_4500", "BSNS_4800"],
        2,
    ),
    (
        "WI",
        None,
        "WI BSNS-3120 Writing Intensive #1 — must be from approved WI list",
        [
            "BSNS_3120",
            "BSNS_4910",
            "ENGL_3110",
            "COMM_3130",
            "HIST_3260",
            "BIBL_3000",
            "RLGN_3000",
            "ENGL_2500",
            "ENGL_3190",
            "ENGL_3580",
            "ENGR_2090",
            "HIST_3300",
            "HIST_3425",
            "POSC_3320",
            "POSC_3450",
            "SPAN_3010",
        ],
        3,
    ),
    ("WI", None, "WI Writing Intensive #2 — at least one must be upper-division (3000+)", [], 3),
    (
        "SI",
        None,
        "SI BSNS-3210 Speaking Intensive — 1 course required from approved SI list | Found: 1",
        [
            "BSNS_3210",
            "BSNS_4480",
            "COMM_2000",
            "ARTH_3040",
            "ENGL_2220",
            "HIST_2300",
            "HNRS_2125",
            "PSYC_3200",
            "SPAN_3020",
        ],
        3,
    ),
]


# ── AUDIT ─────────────────────────────────────────────────────────────────────
def audit(courses):
    cm = cmap(courses)

    def find(codes):
        return best(courses, codes)

    # ── EXCEPTION RULE 1: ENGL-1110 tested out ──────────────────────────────────
    # If ENGL-1120 is present but ENGL-1110 is absent, the student tested out of
    # ENGL-1110. Inject a synthetic "Satisfied" record for ENGL-1110 (3 cr, T grade).
    has_1110 = cm.get("ENGL_1110") or cm.get("ENGL_1100")
    has_1120 = cm.get("ENGL_1120")
    if not has_1110 and has_1120:
        synthetic_1110 = {
            "code": "ENGL_1110",
            "raw": "ENGL-1110",
            "name": "Rhetoric and Composition (tested out)",
            "cr": 3,
            "status": "grade posted",
            "grade": "T",
            "reg_date": "",
        }
        courses = courses + [synthetic_1110]
        cm["ENGL_1110"] = synthetic_1110

    # ── EXCEPTION RULE 2: LART-1050 exemption ────────────────────────────────────
    # If LART-1050 is entirely absent from the uploaded transcript, the student
    # is exempt. Inject a synthetic Satisfied record so F1 shows as satisfied
    # and the W8 auto-satisfy chain fires correctly.
    has_lart = cm.get("LART_1050")
    if not has_lart:
        synthetic_lart = {
            "code": "LART_1050",
            "raw": "LART-1050",
            "name": "First-Year Seminar (exempt)",
            "cr": 0,
            "status": "grade posted",
            "grade": "T",
            "reg_date": "",
        }
        courses = courses + [synthetic_lart]
        cm["LART_1050"] = synthetic_lart

    # F1 for W8 auto-satisfy
    f1 = find(["LART_1050"])
    f1_ok = f1 is not None and done(f1)

    # W8 satisfying courses for Management major (per Registrar 11/14/2023)
    W8_COURSES = ["BSNS_1050", "BSNS_2550", "BSNS_4240", "BSNS_4310", "BSNS_4500", "BSNS_4800"]

    # LA rows
    la = []
    for row in LA_ROWS:
        area, course_col, req_txt, opts, dcr = row
        if area == "W8":
            if f1_ok:
                # F1 complete: auto-satisfy, display as BSNS-1050
                c = cm.get("BSNS_1050")
                s = "Satisfied"
            else:
                # Check if any W8 course is completed/in-progress/scheduled
                c = None
                s = "Not Satisfied"
                for code in W8_COURSES:
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
            # WI #2 upper division — BSNS-4910 double-dips here first;
            # BSNS-3120 also qualifies as a WI-designated 3000+ course
            c4910 = cm.get("BSNS_4910")
            c3120 = cm.get("BSNS_3120")
            if c4910 and done(c4910):
                c = c4910
                s = "Satisfied"
            elif c4910 and ip(c4910):
                c = c4910
                s = "Current"
            elif c4910 and sched(c4910):
                c = c4910
                s = "Scheduled"
            elif c3120 and done(c3120):
                c = c3120
                s = "Satisfied"
            elif c3120 and ip(c3120):
                c = c3120
                s = "Current"
            elif c3120 and sched(c3120):
                c = c3120
                s = "Scheduled"
            else:
                c = None
                s = "Not Satisfied"
        else:
            c = find(opts) if opts else None
            s = status_of(c)
        # course_col override for W rows
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

    # Business core
    bc = []
    for rid, label, opts, dcr in BUS_CORE:
        c = find(opts)
        s = status_of(c)
        bc.append({"id": rid, "label": label, "opts": opts, "status": s, "course": c, "dcr": dcr})

    # Mgmt required
    mr = []
    for rid, label, opts, dcr in MGMT_REQ:
        if rid == "BSNS_PRAC":
            c4 = cm.get("BSNS_4800")
            c3 = cm.get("BSNS_3850")
            if c4 and done(c4):
                c = c4
            elif c3 and done(c3):
                c = c3
            elif c4 and ip(c4):
                c = c4
            elif c3 and ip(c3):
                c = c3
            elif c4 and sched(c4):
                c = c4
            elif c3 and sched(c3):
                c = c3
            else:
                c = None
        else:
            c = find(opts)
        s = status_of(c)
        mr.append({"id": rid, "label": label, "status": s, "course": c, "dcr": dcr})

    # Electives
    elecs = []
    elecs_ip = []
    ehrs = 0
    ehrs_ip = 0
    for opt in ELEC_OPTS:
        c = cm.get(norm(opt))
        if c and done(c):
            elecs.append(c)
            ehrs += c["cr"]
        elif c and (ip(c) or sched(c)):
            elecs_ip.append(c)
            ehrs_ip += c["cr"]

    # GPA
    major_codes = set()
    for _, _, opts, _ in BUS_CORE:
        major_codes.update([norm(o) for o in opts])
    for _, _, opts, _ in MGMT_REQ:
        major_codes.update([norm(o) for o in opts])
    for o in ELEC_OPTS:
        major_codes.add(norm(o))

    op, oh, mp, mh, qp = 0.0, 0, 0.0, 0, 0.0
    earned = 0
    ip_hrs = 0
    GP = {
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
    seen = set()
    for c in courses:
        if drop(c):
            continue
        if ip(c) or sched(c):
            ip_hrs += c["cr"]
            continue
        if not done(c):
            continue
        earned += c["cr"]
        if xfer(c):
            continue
        g = GP.get(c["grade"].upper())
        if g is None:
            continue
        cr = c["cr"]
        if c["code"] not in seen:
            op += g * cr
            oh += cr
            qp += g * cr
            seen.add(c["code"])
        if c["code"] in major_codes:
            mp += g * cr
            mh += cr

    gpa_o = round(op / oh, 2) if oh else 0.0
    gpa_m = round(mp / mh, 2) if mh else 0.0
    proj = earned + ip_hrs

    return dict(
        la=la,
        bc=bc,
        mr=mr,
        elecs=elecs,
        elecs_ip=elecs_ip,
        ehrs=ehrs,
        ehrs_ip=ehrs_ip,
        gpa_o=gpa_o,
        gpa_m=gpa_m,
        qp=round(qp, 1),
        gpa_hrs=oh,
        earned=earned,
        ip_hrs=ip_hrs,
        proj=proj,
        courses=courses,
    )


# ── BUILD PDF ─────────────────────────────────────────────────────────────────
def build(res, student_name, major_label, out):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GRAY)
        canvas.drawCentredString(
            PAGE_W / 2,
            0.3 * inch,
            f"Anderson University Registrar  ·  Audit Engine v2  ·  2023–24 Catalog  ·  {student_name}",
        )
        canvas.restoreState()

    doc = SimpleDocTemplate(
        out,
        pagesize=letter,
        leftMargin=LM,
        rightMargin=RM,
        topMargin=TM,
        bottomMargin=0.6 * inch,
        title=f"Anderson University — Graduation Audit — {student_name}",
    )

    story = []

    # ── PAGE 1 ────────────────────────────────────────────────────────────────
    # Title bar
    title_t = Table(
        [
            [
                Paragraph(
                    f"Anderson University — Graduation Audit  ·  {student_name}  ·  {major_label}  ·  2023–24 Catalog",
                    P["title"],
                )
            ]
        ],
        colWidths=[CW],
    )
    title_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MAROON),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(title_t)
    story.append(Spacer(1, 8))

    # Two-column: Metrics (left) | Eligibility (right)
    # --- Metrics table ---
    gpa_o = res["gpa_o"]
    gpa_m = res["gpa_m"]
    earned = res["earned"]
    ip_hrs = res["ip_hrs"]
    proj = res["proj"]
    met_rows = [
        [Paragraph("Metric", P["met_hdr_l"]), Paragraph("Value", P["met_hdr_r"])],
        [Paragraph("Earned Hours", P["met_lbl"]), Paragraph(str(float(earned)), P["met_val"])],
        [Paragraph("In-Progress Hours", P["met_lbl"]), Paragraph(str(float(ip_hrs)), P["met_val"])],
        [
            Paragraph("Projected Total Hours", P["met_lbl"]),
            Paragraph(str(float(proj)), P["met_val"]),
        ],
        [Paragraph("GPA Hours", P["met_lbl"]), Paragraph(str(float(res["gpa_hrs"])), P["met_val"])],
        [Paragraph("Quality Points", P["met_lbl"]), Paragraph(str(res["qp"]), P["met_val"])],
        [Paragraph("Cumulative GPA", P["met_lbl"]), Paragraph(str(gpa_o), P["met_val"])],
        [Paragraph("Major GPA (Mgmt)", P["met_lbl"]), Paragraph(str(gpa_m), P["met_val"])],
    ]
    mw = [CW * 0.20, CW * 0.11]
    met_t = Table(met_rows, colWidths=mw)
    met_sty = [
        ("BACKGROUND", (0, 0), (-1, 0), MAROON),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, THIN),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, THIN),
    ]
    for i in range(1, len(met_rows)):
        met_sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ODD if i % 2 == 1 else ROW_EVEN))
    met_t.setStyle(TableStyle(met_sty))

    # --- Eligibility table ---
    la_ok = all(r["status"] == "Satisfied" for r in res["la"])
    prog_ok = (
        all(r["status"] == "Satisfied" for r in res["bc"])
        and all(r["status"] == "Satisfied" for r in res["mr"])
        and res["ehrs"] + res["ehrs_ip"] >= 6
    )
    proj120 = proj >= 120
    gpa_ok = gpa_o >= 2.0
    mgpa_ok = gpa_m >= 2.0
    wi_ok = sum(1 for r in res["la"] if r["area"] == "WI" and r["status"] == "Satisfied") >= 2
    si_ok = any(r["area"] == "SI" and r["status"] == "Satisfied" for r in res["la"])
    elig = la_ok and prog_ok and proj120 and gpa_ok and mgpa_ok and wi_ok and si_ok

    # Pending eligibility: would be eligible if all Current/Scheduled classes pass
    la_ok_pend = all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["la"])
    prog_ok_pend = (
        all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["bc"])
        and all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["mr"])
        and res["ehrs"] + res["ehrs_ip"] >= 6
    )
    wi_ok_pend = (
        sum(
            1
            for r in res["la"]
            if r["area"] == "WI" and r["status"] in ("Satisfied", "Current", "Scheduled")
        )
        >= 2
    )
    si_ok_pend = any(
        r["area"] == "SI" and r["status"] in ("Satisfied", "Current", "Scheduled")
        for r in res["la"]
    )
    elig_pend = (
        (not elig)
        and la_ok_pend
        and prog_ok_pend
        and proj120
        and gpa_ok
        and mgpa_ok
        and wi_ok_pend
        and si_ok_pend
    )

    def yn(b, right=True):
        sty = P["elig_yes"] if b else P["elig_no"]
        return Paragraph("YES" if b else "NO", sty)

    ew = [CW * 0.45, CW * 0.13]
    grad_lbl = (
        "Eligible to Graduate — Pending passage of current courses"
        if elig_pend
        else "Eligible to Graduate (all requirements met)"
    )
    walk_lbl = (
        "Eligible to Walk — Pending passage of current courses"
        if elig_pend
        else "Eligible to Walk (projected or scheduled)"
    )
    grad_val = yn(elig or elig_pend)
    walk_val = yn(elig or elig_pend)

    elig_rows = [
        [Paragraph("Eligibility Check", P["elig_hdr"]), Paragraph("Status", P["elig_hdr_r"])],
        [Paragraph("LA (Projected) satisfied", P["elig_lbl"]), yn(la_ok)],
        [Paragraph("Programs satisfied (Projected or Scheduled)", P["elig_lbl"]), yn(prog_ok)],
        [Paragraph("Projected Hours ≥120", P["elig_lbl"]), yn(proj120)],
        [Paragraph("Cumulative GPA ≥2.0", P["elig_lbl"]), yn(gpa_ok)],
        [Paragraph("Major GPA ≥2.0", P["elig_lbl"]), yn(mgpa_ok)],
        [Paragraph("Writing Intensive (WI) ≥2 courses (≥1 upper-div)", P["elig_lbl"]), yn(wi_ok)],
        [Paragraph("Speaking Intensive (SI) ≥1 beyond COMM-1000", P["elig_lbl"]), yn(si_ok)],
        [Paragraph(grad_lbl, P["elig_lbl"]), grad_val],
        [Paragraph(walk_lbl, P["elig_lbl"]), walk_val],
    ]
    elig_t = Table(elig_rows, colWidths=ew)
    elig_sty = [
        ("BACKGROUND", (0, 0), (-1, 0), MAROON),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, THIN),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, THIN),
    ]
    for i in range(1, len(elig_rows)):
        elig_sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ODD if i % 2 == 1 else ROW_EVEN))
    elig_t.setStyle(TableStyle(elig_sty))

    # Side by side
    side = Table(
        [[met_t, Spacer(0.15 * inch, 1), elig_t]], colWidths=[sum(mw), 0.15 * inch, sum(ew)]
    )
    side.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(side)
    story.append(Spacer(1, 10))

    # Liberal Arts heading
    story.append(Paragraph("Liberal Arts — Current", P["sec_gold"]))
    story.append(Spacer(1, 4))

    # LA table
    la_cw = [CW * 0.06, CW * 0.22, CW * 0.40, CW * 0.15, CW * 0.06, CW * 0.11]
    la_hdr = Table(
        [
            [
                Paragraph("Area", P["col_hdr"]),
                Paragraph("Course", P["col_hdr"]),
                Paragraph("Requirement", P["col_hdr"]),
                Paragraph("Status", P["col_hdr"]),
                Paragraph("CR", P["col_hdr"]),
                Paragraph("Grade", P["col_hdr"]),
            ]
        ],
        colWidths=la_cw,
    )
    la_hdr.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MAROON),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(la_hdr)

    for i, r in enumerate(res["la"]):
        bg = ROW_ODD if i % 2 == 0 else ROW_EVEN
        c = r["course"]
        cr_val = cr_disp(c, r["dcr"]) if r["status"] != "Not Satisfied" or c else ""
        grade = grade_disp(c)
        row = Table(
            [
                [
                    Paragraph(r["area"], P["cell_b"]),
                    Paragraph(r["course_col"] or "", P["cell"]),
                    Paragraph(r["req"], P["cell"]),
                    status_para(r["status"]),
                    Paragraph(cr_val, P["cell"]),
                    Paragraph(grade, P["cell_b"]),
                ]
            ],
            colWidths=la_cw,
        )
        row.setStyle(padded(("BACKGROUND", (0, 0), (-1, -1), bg)))
        story.append(row)

    story.append(Spacer(1, 10))

    # ── PAGE 2: MANAGEMENT MAJOR ──────────────────────────────────────────────
    story.append(Paragraph(f"Management Major — 2023–24", P["sec_gold"]))
    story.append(Spacer(1, 4))

    mj_cw = [CW * 0.13, CW * 0.54, CW * 0.16, CW * 0.07, CW * 0.10]

    # Column header
    mj_hdr = Table(
        [
            [
                Paragraph("Course", P["col_hdr"]),
                Paragraph("Requirement", P["col_hdr"]),
                Paragraph("Status", P["col_hdr"]),
                Paragraph("CR", P["col_hdr"]),
                Paragraph("Grade", P["col_hdr"]),
            ]
        ],
        colWidths=mj_cw,
    )
    mj_hdr.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MAROON),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(mj_hdr)

    def sub_section_row(label):
        # Small colored square + centered bold text + small square (matches Isaac exactly)
        sq = "\u25a0"
        t = Table(
            [
                [
                    Paragraph(
                        sq,
                        ps("sq", fontName="Symbol", fontSize=8, textColor=SUB_HDR_BG, leading=10),
                    ),
                    Paragraph(label, P["sub_hdr"]),
                    Paragraph(
                        sq,
                        ps(
                            "sq2",
                            fontName="Symbol",
                            fontSize=8,
                            textColor=SUB_HDR_BG,
                            leading=10,
                            alignment=TA_RIGHT,
                        ),
                    ),
                ]
            ],
            colWidths=[0.18 * inch, CW - 0.36 * inch, 0.18 * inch],
        )
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SUB_HDR_BG),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        return t

    def mj_row(code_str, req_label, status, cr_str, grade_str, idx):
        bg = ROW_ODD if idx % 2 == 0 else ROW_EVEN
        row = Table(
            [
                [
                    Paragraph(code_str, P["cell_b"]),
                    Paragraph(req_label, P["cell"]),
                    status_para(status),
                    Paragraph(cr_str, P["cell"]),
                    Paragraph(grade_str, P["cell_b"]),
                ]
            ],
            colWidths=mj_cw,
        )
        row.setStyle(padded(("BACKGROUND", (0, 0), (-1, -1), bg)))
        return row

    # Business Core
    story.append(sub_section_row("Business Core Requirements (43 hrs)"))
    for i, r in enumerate(res["bc"]):
        c = r["course"]
        code = c["raw"] if c else r["id"].replace("_", "-")
        note = ""
        if r["id"] == "BSNS_4910":
            note = " (WI)"
        story.append(
            mj_row(code, r["label"] + note, r["status"], cr_disp(c, r["dcr"]), grade_disp(c), i)
        )

    # Management Required
    story.append(sub_section_row("Management Required Courses"))
    for i, r in enumerate(res["mr"]):
        c = r["course"]
        code = c["raw"] if c else r["id"].replace("_", "-")
        note = ""
        if r["id"] == "BSNS_4480":
            note = " (SI)"
        if r["id"] == "BSNS_3120":
            note = " (WI #1 · W7 Liberal Arts)"
        story.append(
            mj_row(code, r["label"] + note, r["status"], cr_disp(c, r["dcr"]), grade_disp(c), i)
        )

    # Management Electives
    story.append(
        sub_section_row(f"Management Electives — 6 hrs required  (earned: {res['ehrs']} hrs)")
    )
    row_i = 0
    if res["elecs"]:
        for c in res["elecs"]:
            story.append(mj_row(c["raw"], c["name"], "Satisfied", str(c["cr"]), c["grade"], row_i))
            row_i += 1
    if res["elecs_ip"]:
        for c in res["elecs_ip"]:
            s = "Current" if ip(c) else "Scheduled"
            story.append(mj_row(c["raw"], c["name"], s, str(c["cr"]), grade_disp(c), row_i))
            row_i += 1
    if not res["elecs"] and not res["elecs_ip"]:
        story.append(
            mj_row(
                "",
                "Electives needed from: BSNS 3100/3240/3510/4050/4120/4240/4310",
                "Not Satisfied",
                "6",
                "",
                0,
            )
        )
    elif res["ehrs"] + res["ehrs_ip"] < 6:
        enrolled_codes = {c["raw"].upper() for c in res["elecs"] + res["elecs_ip"]}
        all_opts = [
            "BSNS-3100",
            "BSNS-3240",
            "BSNS-3510",
            "BSNS-4050",
            "BSNS-4120",
            "BSNS-4240",
            "BSNS-4310",
        ]
        remaining = [o for o in all_opts if o not in enrolled_codes]
        if remaining:
            story.append(
                mj_row(
                    "",
                    f"Additional electives needed from: {' / '.join(remaining)}",
                    "Not Satisfied",
                    str(6 - res["ehrs"] - res["ehrs_ip"]),
                    "",
                    row_i,
                )
            )

    # Notes row
    notes_row = Table(
        [
            [
                Paragraph(
                    "Note: BSNS-4480 (Leadership) = SI  ·  BSNS-3120 (Global Business) = WI #1 (Liberal Arts Program)  ·  "
                    "BSNS-4910 (Senior Seminar) = WI  ·  W8 satisfied by: BSNS-1050, 2550, 4240, 4310, 4500, 4800  ·  W8 auto-satisfied when F1 (LART-1050) complete",
                    P["note"],
                )
            ]
        ],
        colWidths=[CW],
    )
    notes_row.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ROW_ODD),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(notes_row)
    story.append(PageBreak())

    # ── PAGE 3: COURSE HISTORY ────────────────────────────────────────────────
    story.append(Paragraph("Course History — Repeats Resolved", P["sec_gold"]))
    story.append(Spacer(1, 4))

    ch_cw = [CW * 0.18, CW * 0.14, CW * 0.40, CW * 0.10, CW * 0.09, CW * 0.09]
    ch_hdr = Table(
        [
            [
                Paragraph("Term", P["col_hdr"]),
                Paragraph("Course Code", P["col_hdr"]),
                Paragraph("Course Name", P["col_hdr"]),
                Paragraph("Letter\nGrade", P["col_hdr"]),
                Paragraph("Credits", P["col_hdr"]),
                Paragraph("Status", P["col_hdr"]),
            ]
        ],
        colWidths=ch_cw,
    )
    ch_hdr.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MAROON),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(ch_hdr)

    def sched_term(c):
        """Derive the scheduled semester label from the registration date."""
        import re

        raw = c.get("reg_date", "")
        # Parse M/D/YYYY from date string
        m = re.match(r"(\d+)/(\d+)/(\d{4})", raw)
        if not m:
            return "Scheduled"
        month, day, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # AU academic year: Fall = Aug–Dec, Spring = Jan–May, Summer = Jun–Jul
        # Registration for a term typically opens the semester before.
        # Map registration date → likely scheduled term:
        #   Registered Aug–Dec  → Spring of that academic year (next calendar year)
        #   Registered Jan–May  → Fall of that same academic year (next Aug)
        #   Registered Jun–Jul  → Fall of that same academic year
        if month >= 8:  # Registered fall → scheduled for spring
            acad_start = year
            acad_end = year + 1
            return f"Spring, {acad_start}-{str(acad_end)[2:]}"
        else:  # Registered spring/summer → scheduled for fall
            acad_start = year
            acad_end = year + 1
            return f"Fall, {acad_start}-{str(acad_end)[2:]}"

    def hist_status(c):
        if xfer(c):
            return "CG"
        if drop(c):
            return "DR"
        if ip(c):
            return "AC"
        if sched(c):
            return "SC"
        if done(c):
            return "CG"
        return "NS"

    def term_str(c):
        if xfer(c):
            return "Transfer Credit"
        s = c["status"]
        if s == "current":
            return "Spring, 2025-26"
        if s == "scheduled":
            return sched_term(c)
        if s == "grade posted":
            return "Completed"
        if s == "dropped":
            return "Dropped"
        if s == "not started":
            return "Not Started"
        return ""

    # Sort: by code alphabetically, skip blank not-started
    all_c = sorted(
        [c for c in res["courses"] if not (c["status"] == "not started" and not c["grade"])],
        key=lambda c: c["raw"],
    )

    for i, c in enumerate(all_c):
        bg = ROW_ODD if i % 2 == 0 else ROW_EVEN
        is_tr = xfer(c)
        term_p = Paragraph(term_str(c), P["term_tr"] if is_tr else P["term"])
        code_p = Paragraph(c["raw"], P["code_b"])
        name_p = Paragraph(c["name"], P["hist_cell"])
        grade_p = Paragraph(
            (
                c["grade"]
                if c["grade"] and c["grade"] != "T"
                else ("T" if is_tr else ("IP" if ip(c) else ""))
            ),
            P["hist_cell"],
        )
        cr_p = Paragraph(str(c["cr"]), P["hist_cell"])
        stat_p = Paragraph(hist_status(c), P["hist_cell"])

        row = Table([[term_p, code_p, name_p, grade_p, cr_p, stat_p]], colWidths=ch_cw)
        row.setStyle(padded(("BACKGROUND", (0, 0), (-1, -1), bg)))
        story.append(row)

    story.append(PageBreak())

    # ── PAGE 4: ACTION PLAN ───────────────────────────────────────────────────
    ap_title = Table(
        [
            [
                Paragraph(
                    f"Anderson University — Student Graduation Action Plan  ·  {student_name}  ·  {major_label}",
                    P["ap_title"],
                )
            ]
        ],
        colWidths=[CW],
    )
    ap_title.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MAROON),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(ap_title)
    story.append(Spacer(1, 6))

    # Summary line
    summ = Table(
        [
            [
                Paragraph(
                    f"Major: {major_label}  ·  Projected Hours: {float(proj)} / 120  ·  Cumulative GPA: {gpa_o}",
                    P["summary"],
                )
            ]
        ],
        colWidths=[CW],
    )
    summ.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BOX", (0, 0), (-1, -1), 0.5, THIN),
            ]
        )
    )
    story.append(summ)
    story.append(Spacer(1, 8))

    ap_cw = [CW * 0.38, CW * 0.62]

    def ap_section(title, items, bar_color=GOLD_BAR):
        bar_sty = P["ap_bar_gold"] if bar_color == GOLD_BAR else P["ap_bar_blue"]
        bar = Table([[Paragraph(title, bar_sty)]], colWidths=[CW])
        bar.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), bar_color),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(bar)

        if not items:
            # Section is complete — show Completed row
            comp_row = Table(
                [
                    [
                        Paragraph(
                            "\u2713 Completed",
                            ps(
                                "comp",
                                fontName="Helvetica-Bold",
                                fontSize=8.5,
                                textColor=SATISFIED,
                                leading=11,
                            ),
                        ),
                        Paragraph("", P["ap_rec"]),
                    ]
                ],
                colWidths=ap_cw,
            )
            comp_row.setStyle(
                padded(
                    ("BACKGROUND", (0, 0), (-1, -1), ROW_ODD),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                )
            )
            story.append(comp_row)
            story.append(Spacer(1, 6))
            return

        # Column header row
        col_h = Table(
            [
                [
                    Paragraph("Course / Area", P["ap_cat_hdr"]),
                    Paragraph("Recommended Action", P["ap_cat_hdr"]),
                ]
            ],
            colWidths=ap_cw,
        )
        col_h.setStyle(
            padded(
                ("BACKGROUND", (0, 0), (-1, -1), ROW_EVEN),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, THIN),
            )
        )
        story.append(col_h)

        for i, (label, action) in enumerate(items):
            bg = ROW_ODD if i % 2 == 0 else ROW_EVEN
            row = Table(
                [
                    [
                        Paragraph(f"\u2717{label}", P["ap_x"]),
                        Paragraph(action, P["ap_rec"]),
                    ]
                ],
                colWidths=ap_cw,
            )
            row.setStyle(
                padded(("BACKGROUND", (0, 0), (-1, -1), bg), ("VALIGN", (0, 0), (-1, -1), "TOP"))
            )
            story.append(row)
        story.append(Spacer(1, 6))

    # Collect items
    la_miss = []
    la_cur = []
    la_sched = []
    for r in res["la"]:
        area = r["area"]
        req = r["req"]
        if r["status"] == "Not Satisfied":
            if area == "W4":
                la_miss.append(
                    (
                        "W4 Aesthetic Ways of Knowing",
                        "Enroll in an Aesthetic course: ARTH-3040, ARTS-1210/1230/1250, MUSC-2210, THEA-2350, or a MUPF/DANC performance course",
                    )
                )
            elif "WI #2" in req:
                la_miss.append(
                    (
                        "WI Writing Intensive #2 — at least one must be upper-division (3000+)",
                        "See advisor",
                    )
                )
            else:
                la_miss.append(
                    (
                        req.split("—")[0].strip() if "—" in req else req,
                        "See advisor — enroll in required course",
                    )
                )
        elif r["status"] == "Current":
            c = r["course"]
            cname = f" — {c['raw']} {c['name']}" if c else ""
            disp = req.split("—")[0].strip() if "—" in req else req
            la_cur.append(
                (f"{disp}{cname}", "Currently enrolled — complete with passing grade this semester")
            )
        elif r["status"] == "Scheduled":
            c = r["course"]
            cname = f" — {c['raw']} {c['name']}" if c else ""
            disp = req.split("—")[0].strip() if "—" in req else req
            la_sched.append(
                (f"{disp}{cname}", "Scheduled — confirm enrollment and complete with passing grade")
            )

    maj_miss = []
    maj_cur = []
    maj_sched = []
    for r in res["bc"] + res["mr"]:
        code = "BSNS-4800" if r["id"] == "BSNS_PRAC" else r["id"].replace("_", "-")
        full_label = r["label"]
        if r["status"] == "Not Satisfied":
            maj_miss.append((full_label, f"Enroll in {code} — {r['label']}"))
        elif r["status"] == "Current":
            maj_cur.append(
                (full_label, "Currently enrolled — complete with passing grade this semester")
            )

        elif r["status"] == "Scheduled":
            maj_sched.append(
                (full_label, "Scheduled — confirm enrollment and complete with passing grade")
            )
    if res["ehrs"] + res["ehrs_ip"] < 6:
        enrolled_codes = {c["raw"].upper() for c in res["elecs"] + res["elecs_ip"]}
        all_opts = [
            "BSNS-3100",
            "BSNS-3240",
            "BSNS-3510",
            "BSNS-4050",
            "BSNS-4120",
            "BSNS-4240",
            "BSNS-4310",
        ]
        remaining = [o for o in all_opts if o not in enrolled_codes]
        hrs_still_needed = 6 - res["ehrs"] - res["ehrs_ip"]
        opt_str = ", ".join(remaining) if remaining else "see advisor"
        maj_miss.append(
            (
                f"Management Electives — {hrs_still_needed} hrs still needed",
                f"Enroll in elective from: {opt_str}",
            )
        )
    for c in res["elecs_ip"]:
        s = "Current" if ip(c) else "Scheduled"
        label = f"{c['raw']} {c['name']}"
        if s == "Current":
            maj_cur.append(
                (label, "Currently enrolled — complete with passing grade this semester")
            )
        else:
            maj_sched.append(
                (label, "Scheduled — confirm enrollment and complete with passing grade")
            )

    credit_items = []
    short = max(0, 120 - proj)
    if short > 0:
        credit_items.append(
            (
                f"Projected total: {float(proj)} hrs — need 120 hrs",
                f"Must complete {float(short)} additional credit hours before graduation",
            )
        )

    wi_items = []
    wi_sat = sum(1 for r in res["la"] if r["area"] == "WI" and r["status"] == "Satisfied")
    wi_cur_rows = [
        r for r in res["la"] if r["area"] == "WI" and r["status"] in ("Current", "Scheduled")
    ]
    if wi_sat < 2:
        wi_courses = [r for r in res["la"] if r["area"] == "WI" and r["status"] == "Satisfied"]
        completed_str = (
            ", ".join(
                f"{r['course']['raw']} {r['course']['name']}" for r in wi_courses if r.get("course")
            )
            if wi_courses
            else "none"
        )
        cur_str = ""
        if wi_cur_rows:
            cur_parts = [
                f"{r['course']['raw']} {r['course']['name']}"
                for r in wi_cur_rows
                if r.get("course")
            ]
            cur_str = f" | Currently enrolled: {', '.join(cur_parts)}" if cur_parts else ""
        wi_items.append(
            (
                f"Writing Intensive: {wi_sat} of 2 satisfied ({completed_str}){cur_str}",
                "Still need 2 WI-designated courses (at least 1 upper-division 3000+) — see advisor",
            )
        )

    ap_section("Liberal Arts — Current", la_cur, GOLD_BAR)
    ap_section("Liberal Arts — Scheduled", la_sched, GOLD_BAR)
    ap_section("Liberal Arts — Missing", la_miss, GOLD_BAR)
    ap_section("Advanced Competency — WI", wi_items, GOLD_BAR)
    ap_section("Major — Current", maj_cur, BLUE_BAR)
    ap_section("Major — Scheduled", maj_sched, BLUE_BAR)
    ap_section("Major — Missing", maj_miss, BLUE_BAR)
    ap_section("Credit Hours", credit_items, BLUE_BAR)

    # Disclaimer
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "Anderson University Registrar  ·  This action plan is auto-generated. Please verify with your academic advisor.  ·  2023–24 Catalog",
            P["footer"],
        )
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✓ {out}")


# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    courses = parse_csv("/mnt/user-data/uploads/Jenna_Miller.csv")
    res = audit(courses)
    build(
        res,
        "Jenna Miller",
        "Management",
        "/mnt/user-data/outputs/Jenna_Miller_Management_Audit_Final.pdf",
    )
