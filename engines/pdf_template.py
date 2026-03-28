"""
Anderson University — Shared PDF Template
Canonical graduation audit layout extracted from sport_marketing.py build().
All majors — FSB and non-FSB — must use this template. No exceptions.

Call: build(res, student_name, major_label, out, exceptions='')

res dict shape:
  gpa_o, gpa_m, earned, ip_hrs, proj, gpa_hrs, qp  — floats/strings
  la        — list of LA row dicts (see sport_marketing.py audit() for shape)
  bc        — list of business core row dicts (empty list for non-FSB)
  mr        — list of major requirement row dicts
  elecs     — list of course dicts (empty list for non-FSB)
  elecs_ip  — list of course dicts (empty list for non-FSB)
  ehrs      — float, elective hours earned
  ehrs_ip   — float, elective hours in-progress
  courses   — full course list for Course History section
  minor_rows — list or None
  minor_key  — str or None
  major_section_label — str, e.g. "Sport Marketing Major — 2023-24"
  major_subsections   — list of (label, rows) tuples for sub-section headers
  notes_row_text      — str, shown in the notes row below major section (or '')
  elec_section_label  — str, e.g. "Sport Marketing Electives — 6 hrs required"
  elec_opts           — list of elective option strings (for "still needed" msg)
  elec_required_hrs   — int, total elective hours required (default 0 = no elec section)
"""

import re
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

# ── EXACT COLORS FROM ISAAC BAIR TEMPLATE ────────────────────────────────────
MAROON = colors.HexColor("#8B1A2B")
GOLD_HEAD = colors.HexColor("#B8860B")
GOLD_BAR = colors.HexColor("#C9A84C")
BLUE_BAR = colors.HexColor("#1F3864")
COL_HDR_BG = colors.HexColor("#8B1A2B")
COL_HDR_TXT = colors.white
SUB_HDR_BG = colors.HexColor("#D4C5A0")
SUB_HDR_TXT = colors.HexColor("#3B2A00")
ROW_ODD = colors.HexColor("#F5F2EC")
ROW_EVEN = colors.white
SATISFIED = colors.HexColor("#375623")
CURRENT_CLR = colors.HexColor("#7F4700")
NOT_SAT = colors.HexColor("#8B1A2B")
TERM_CLR = colors.HexColor("#1A1A1A")
TRANSFER_CLR = colors.HexColor("#8B6914")
XMARK_CLR = colors.HexColor("#CC3300")
DARK = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#F0F0F0")
BORDER = colors.HexColor("#CCCCCC")
WHITE = colors.white
THIN = colors.HexColor("#CCCCCC")

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
    "title": ps("title", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, leading=13),
    "sec_gold": ps(
        "sec_gold", fontName="Helvetica-Bold", fontSize=10, textColor=GOLD_HEAD, leading=13
    ),
    "col_hdr": ps("col_hdr", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11),
    "sub_hdr": ps(
        "sub_hdr",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=SUB_HDR_TXT,
        leading=11,
        alignment=TA_CENTER,
    ),
    "cell": ps("cell", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=11),
    "cell_b": ps("cell_b", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, leading=11),
    "sat": ps("sat", fontName="Helvetica-Bold", fontSize=8.5, textColor=SATISFIED, leading=11),
    "cur": ps("cur", fontName="Helvetica-Bold", fontSize=8.5, textColor=CURRENT_CLR, leading=11),
    "nos": ps("nos", fontName="Helvetica-Bold", fontSize=8.5, textColor=NOT_SAT, leading=11),
    "term": ps("term", fontName="Helvetica", fontSize=8, textColor=TERM_CLR, leading=10),
    "term_tr": ps(
        "term_tr", fontName="Helvetica-Oblique", fontSize=8, textColor=TRANSFER_CLR, leading=10
    ),
    "code_b": ps("code_b", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=10),
    "hist_cell": ps("hist_cell", fontName="Helvetica", fontSize=8, textColor=DARK, leading=10),
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
    "footer": ps(
        "footer", fontName="Helvetica", fontSize=7, textColor=GRAY, leading=9, alignment=TA_CENTER
    ),
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


def _int(v):
    """Safely convert dcr/credits to int regardless of type."""
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str):
        try:
            return int(v.split("-")[0])
        except ValueError:
            return 0
    return 0


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


# ── COURSE HELPERS ────────────────────────────────────────────────────────────
def done(c):
    return c["status"] == "grade posted" and c["grade"].upper() not in ("", "W", "DRP", "NC")


def ip(c):
    return c["status"] == "current"


def sched(c):
    return c["status"] == "scheduled"


def xfer(c):
    return c["grade"].upper() == "T"


def drop(c):
    return c["grade"].upper() in ("DRP", "W") or c["status"] == "dropped"


def status_para(s):
    if s == "Satisfied":
        return Paragraph("✓ Satisfied", P["sat"])
    if s == "Current":
        return Paragraph("✓ Satisfied (pending)", P["sat"])
    if s == "Scheduled":
        return Paragraph("✓ Satisfied (pending)", P["sat"])
    return Paragraph("✗ Not Satisfied", P["nos"])


def grade_disp(c):
    if not c:
        return ""
    g = c["grade"].upper()
    if g == "T":
        return "T"
    if ip(c):
        return "IP"
    if sched(c):
        return ""
    return g


def cr_disp(c, fallback=""):
    if not c:
        return str(fallback)
    if done(c) or xfer(c):
        return str(c["cr"])
    if ip(c) or sched(c):
        return f"({c['cr']})"
    return str(fallback)


# ── MAIN BUILD FUNCTION ───────────────────────────────────────────────────────
def build(res, student_name, major_label, out, exceptions=""):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GRAY)
        canvas.drawCentredString(
            PAGE_W / 2,
            0.3 * inch,
            f"Anderson University Registrar  ·  Audit Engine v2  ·  {res.get('catalog_year','2023-24')} Catalog  ·  {student_name}",
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
    catalog_year = res.get("catalog_year", "2023-24")
    title_t = Table(
        [
            [
                Paragraph(
                    f"Anderson University — Graduation Audit  ·  {student_name}  ·  {major_label}  ·  {catalog_year} Catalog",
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

    # Metrics table
    gpa_o = res["gpa_o"]
    gpa_m = res["gpa_m"]
    earned = res["earned"]
    ip_hrs = res["ip_hrs"]
    proj = res["proj"]

    met_total = CW * 0.26
    gap_w = 0.12 * inch
    elig_total = CW - met_total - gap_w

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
        [
            Paragraph(f"Major GPA ({major_label})", P["met_lbl"]),
            Paragraph(str(gpa_m), P["met_val"]),
        ],
    ]

    mw = [met_total * 0.72, met_total * 0.28]
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

    # Eligibility table
    elec_required_hrs = res.get("elec_required_hrs", 0)
    ehrs = res.get("ehrs", 0)
    ehrs_ip = res.get("ehrs_ip", 0)
    elecs = res.get("elecs", [])
    elecs_ip = res.get("elecs_ip", [])

    la_ok = all(r["status"] == "Satisfied" for r in res["la"])
    bc_ok = all(r["status"] == "Satisfied" for r in res.get("bc", []))
    mr_ok = all(r["status"] == "Satisfied" for r in res["mr"])
    elec_ok = (elec_required_hrs == 0) or (ehrs + ehrs_ip >= elec_required_hrs)
    prog_ok = bc_ok and mr_ok and elec_ok

    bc_ok_proj = all(
        r["status"] in ("Satisfied", "Current", "Scheduled") for r in res.get("bc", [])
    )
    mr_ok_proj = all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["mr"])
    prog_ok = prog_ok or (bc_ok_proj and mr_ok_proj and elec_ok)

    proj120 = proj >= 120
    gpa_ok = gpa_o >= 2.0
    mgpa_ok = gpa_m >= 2.0
    wi_ok = sum(1 for r in res["la"] if r["area"] == "WI" and r["status"] == "Satisfied") >= 2
    si_ok = any(r["area"] == "SI" and r["status"] == "Satisfied" for r in res["la"])
    elig = la_ok and prog_ok and proj120 and gpa_ok and mgpa_ok and wi_ok and si_ok

    la_ok_pend = all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["la"])
    bc_ok_pend = all(
        r["status"] in ("Satisfied", "Current", "Scheduled") for r in res.get("bc", [])
    )
    mr_ok_pend = all(r["status"] in ("Satisfied", "Current", "Scheduled") for r in res["mr"])
    elec_ok_pend = (elec_required_hrs == 0) or (ehrs + ehrs_ip >= elec_required_hrs)
    prog_ok_pend = bc_ok_pend and mr_ok_pend and elec_ok_pend
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

    def yn(b):
        sty = P["elig_yes"] if b else P["elig_no"]
        return Paragraph("YES" if b else "NO", sty)

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

    elig_rows = [
        [Paragraph("Eligibility Check", P["elig_hdr"]), Paragraph("Status", P["elig_hdr_r"])],
        [Paragraph("LA (Projected) satisfied", P["elig_lbl"]), yn(la_ok or la_ok_pend)],
        [Paragraph("Programs satisfied (Projected or Scheduled)", P["elig_lbl"]), yn(prog_ok)],
        [Paragraph("Projected Hours ≥120", P["elig_lbl"]), yn(proj120)],
        [Paragraph("Cumulative GPA ≥2.0", P["elig_lbl"]), yn(gpa_ok)],
        [Paragraph("Major GPA ≥2.0", P["elig_lbl"]), yn(mgpa_ok)],
        [Paragraph("Writing Intensive (WI) ≥2 courses (≥1 upper-div)", P["elig_lbl"]), yn(wi_ok)],
        [Paragraph("Speaking Intensive (SI) ≥1 beyond COMM-1000", P["elig_lbl"]), yn(si_ok)],
        [Paragraph(grad_lbl, P["elig_lbl"]), yn(elig or elig_pend)],
        [Paragraph(walk_lbl, P["elig_lbl"]), yn(res.get("eligible_to_walk", (elig or elig_pend)))],
    ]

    ew = [elig_total * 0.78, elig_total * 0.22]
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

    side = Table([[met_t, Spacer(gap_w, 1), elig_t]], colWidths=[met_total, gap_w, elig_total])
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
    # Exceptions note
    if exceptions and exceptions.strip():
        exc_lines = [
            l.strip()
            for l in exceptions.strip().splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
        if exc_lines:
            exc_text = "  ·  ".join(exc_lines)
            exc_row = Table(
                [[Paragraph(f"<b>Advisor Exceptions Applied:</b>  {exc_text}", P["note"])]],
                colWidths=[CW],
            )
            exc_row.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF3CD")),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E6A817")),
                    ]
                )
            )
            story.append(exc_row)
            story.append(Spacer(1, 8))

    # ── ADVISOR NOTES ─────────────────────────────────────────────────────────
    advisor_notes = res.get("advisor_notes", "")
    if advisor_notes and advisor_notes.strip():
        notes_lines = [l.strip() for l in advisor_notes.strip().splitlines() if l.strip()]
        notes_text = "<br/>".join(notes_lines)
        notes_row = Table(
            [[Paragraph(f"<b>Advisor Notes:</b>  {notes_text}", P["note"])]], colWidths=[CW]
        )
        notes_row.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#1F3864")),
                ]
            )
        )
        story.append(notes_row)
        story.append(Spacer(1, 8))

    # ── LA SECTION ────────────────────────────────────────────────────────────
    story.append(Paragraph("Liberal Arts — Current", P["sec_gold"]))
    story.append(Spacer(1, 4))

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

    # LA hour totals row
    la_earned = sum(_int(r["dcr"]) for r in res["la"] if r["status"] == "Satisfied")
    la_ip = sum(_int(r["dcr"]) for r in res["la"] if r["status"] in ("Current", "Scheduled"))
    la_total = sum(_int(r["dcr"]) for r in res["la"])
    la_total_row = Table(
        [
            [
                Paragraph(
                    f"Liberal Arts Hours — Earned: {la_earned} cr  ·  In Progress / Scheduled: {la_ip} cr  ·  Total Required: {la_total} cr",
                    ps("la_tot", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=10),
                )
            ]
        ],
        colWidths=[CW],
    )
    la_total_row.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SUB_HDR_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(la_total_row)
    story.append(Spacer(1, 10))

    # ── PAGE 2: MAJOR SECTION ─────────────────────────────────────────────────
    major_section_label = res.get("major_section_label", f"{major_label} Major")
    story.append(Paragraph(major_section_label, P["sec_gold"]))
    story.append(Spacer(1, 4))

    mj_cw = [CW * 0.13, CW * 0.54, CW * 0.16, CW * 0.07, CW * 0.10]
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

    # Render major_subsections: list of (subsection_label, rows)
    # Each row in rows is a dict with keys: id, label, status, course, dcr, note (optional)
    for subsection_label, subsection_rows in res.get("major_subsections", []):
        story.append(sub_section_row(subsection_label))
        for i, r in enumerate(subsection_rows):
            c = r["course"]
            code = c["raw"] if c else r["id"].replace("_", "-")
            note = r.get("note", "")
            story.append(
                mj_row(code, r["label"] + note, r["status"], cr_disp(c, r["dcr"]), grade_disp(c), i)
            )

    # Electives section (only if elec_required_hrs > 0)
    if elec_required_hrs > 0:
        elec_label = res.get(
            "elec_section_label",
            f"Electives — {elec_required_hrs} hrs required  (earned: {ehrs} hrs)",
        )
        story.append(sub_section_row(elec_label))
        row_i = 0
        if elecs:
            for c in elecs:
                story.append(
                    mj_row(c["raw"], c["name"], "Satisfied", str(c["cr"]), c["grade"], row_i)
                )
                row_i += 1
        if elecs_ip:
            for c in elecs_ip:
                s = "Current" if ip(c) else "Scheduled"
                story.append(mj_row(c["raw"], c["name"], s, str(c["cr"]), grade_disp(c), row_i))
                row_i += 1
        if not elecs and not elecs_ip:
            story.append(
                mj_row(
                    "",
                    f"Electives needed — {elec_required_hrs} hrs required",
                    "Not Satisfied",
                    str(elec_required_hrs),
                    "",
                    0,
                )
            )
        elif ehrs + ehrs_ip < elec_required_hrs:
            enrolled_codes = {c["raw"].upper() for c in elecs + elecs_ip}
            elec_opts = res.get("elec_opts", [])
            remaining = [o for o in elec_opts if o not in enrolled_codes]
            if remaining:
                story.append(
                    mj_row(
                        "",
                        f"Additional electives needed from: {' / '.join(remaining)}",
                        "Not Satisfied",
                        str(elec_required_hrs - ehrs - ehrs_ip),
                        "",
                        row_i,
                    )
                )

    # Notes row
    notes_text = res.get("notes_row_text", "")
    if notes_text:
        notes_row = Table([[Paragraph(notes_text, P["note"])]], colWidths=[CW])
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

    # Major hour totals row
    mj_earned = sum(
        _int(r["dcr"])
        for r in list(res.get("bc", [])) + list(res["mr"])
        if r["status"] == "Satisfied"
    )
    mj_ip = sum(
        _int(r["dcr"])
        for r in list(res.get("bc", [])) + list(res["mr"])
        if r["status"] in ("Current", "Scheduled")
    )
    mj_req = sum(_int(r["dcr"]) for r in list(res.get("bc", [])) + list(res["mr"]))
    if elec_required_hrs > 0:
        mj_earned += ehrs
        mj_ip += ehrs_ip
        mj_req += elec_required_hrs
    mj_total_row = Table(
        [
            [
                Paragraph(
                    f"Major Hours — Earned: {mj_earned} cr  ·  In Progress / Scheduled: {mj_ip} cr  ·  Total Required: {mj_req} cr",
                    ps("mj_tot", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=10),
                )
            ]
        ],
        colWidths=[CW],
    )
    mj_total_row.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SUB_HDR_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(mj_total_row)
    story.append(Spacer(1, 6))

    # ── ADDITIONAL MAJOR SECTIONS (2nd and 3rd majors) ────────────────────────
    for extra_label, extra_rows in res.get("additional_major_sections", []):
        story.append(Paragraph(f"{extra_label}", P["sec_gold"]))
        story.append(Spacer(1, 4))
        extra_hdr = Table(
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
        extra_hdr.setStyle(
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
        story.append(extra_hdr)
        for i, r in enumerate(extra_rows):
            c = r.get("course")
            code = c["raw"] if c else r["id"].replace("_", "-")
            note = r.get("note", "")
            story.append(
                mj_row(code, r["label"] + note, r["status"], cr_disp(c, r["dcr"]), grade_disp(c), i)
            )
        # Hour totals for extra major
        ex_earned = sum(_int(r["dcr"]) for r in extra_rows if r["status"] == "Satisfied")
        ex_ip = sum(_int(r["dcr"]) for r in extra_rows if r["status"] in ("Current", "Scheduled"))
        ex_req = sum(_int(r["dcr"]) for r in extra_rows)
        ex_tot = Table(
            [
                [
                    Paragraph(
                        f"Major Hours — Earned: {ex_earned} cr  ·  In Progress / Scheduled: {ex_ip} cr  ·  Total Required: {ex_req} cr",
                        ps(
                            "ex_tot",
                            fontName="Helvetica-Bold",
                            fontSize=8,
                            textColor=DARK,
                            leading=10,
                        ),
                    )
                ]
            ],
            colWidths=[CW],
        )
        ex_tot.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SUB_HDR_BG),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(ex_tot)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ── MINOR SECTION ─────────────────────────────────────────────────────────
    minor_rows = res.get("minor_rows")
    minor_key = res.get("minor_key", "")
    if minor_rows:
        minor_name = res.get("minor_name", "Minor")
        story.append(Paragraph(minor_name, P["sec_gold"]))
        story.append(Spacer(1, 4))

        minor_hdr = Table(
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
        minor_hdr.setStyle(
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
        story.append(minor_hdr)

        row_i = 0
        for r in minor_rows:
            c = r["course"]
            if r["id"] == "ELEC":
                elec_rows = r["elec_done"] + r["elec_ip"]
                if elec_rows:
                    for ec in elec_rows:
                        es = "Satisfied" if done(ec) else ("Current" if ip(ec) else "Scheduled")
                        story.append(
                            mj_row(ec["raw"], ec["name"], es, str(ec["cr"]), grade_disp(ec), row_i)
                        )
                        row_i += 1
                    elec_hrs_total = r["elec_hrs"] + sum(ec["cr"] for ec in r["elec_ip"])
                    if elec_hrs_total < 4:
                        story.append(
                            mj_row(
                                "",
                                f"Coaching elective — {4 - elec_hrs_total} more hrs needed (PEHS/EXSC/SPRL 3000+)",
                                "Not Satisfied",
                                str(4 - elec_hrs_total),
                                "",
                                row_i,
                            )
                        )
                        row_i += 1
                else:
                    story.append(mj_row("", r["label"], "Not Satisfied", str(r["dcr"]), "", row_i))
                    row_i += 1
            else:
                code = c["raw"] if c else r["id"].replace("_", "-")
                story.append(
                    mj_row(
                        code, r["label"], r["status"], cr_disp(c, r["dcr"]), grade_disp(c), row_i
                    )
                )
                row_i += 1

        story.append(Spacer(1, 10))

    # ── COURSE HISTORY ────────────────────────────────────────────────────────
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
        raw = c.get("reg_date", "")
        m = re.match(r"(\d+)/(\d+)/(\d{4})", raw)
        if not m:
            return "Scheduled"
        month, day, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if month >= 8:
            return f"Spring, {year}-{str(year+1)[2:]}"
        else:
            return f"Fall, {year}-{str(year+1)[2:]}"

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
            return f"Spring, {res.get('current_term_label','2025-26')}"
        if s == "scheduled":
            return sched_term(c)
        if s == "grade posted":
            return "Completed"
        if s == "dropped":
            return "Dropped"
        if s == "not started":
            return "Not Started"
        return ""

    all_c = sorted(
        [c for c in res["courses"] if not (c["status"] == "not started" and not c["grade"])],
        key=lambda c: c["raw"],
    )

    for i, c in enumerate(all_c):
        bg = ROW_ODD if i % 2 == 0 else ROW_EVEN
        is_tr = xfer(c)
        row = Table(
            [
                [
                    Paragraph(term_str(c), P["term_tr"] if is_tr else P["term"]),
                    Paragraph(c["raw"], P["code_b"]),
                    Paragraph(c["name"], P["hist_cell"]),
                    Paragraph(
                        (
                            c["grade"]
                            if c["grade"] and c["grade"] != "T"
                            else ("T" if is_tr else ("IP" if ip(c) else ""))
                        ),
                        P["hist_cell"],
                    ),
                    Paragraph(str(c["cr"]), P["hist_cell"]),
                    Paragraph(hist_status(c), P["hist_cell"]),
                ]
            ],
            colWidths=ch_cw,
        )
        row.setStyle(padded(("BACKGROUND", (0, 0), (-1, -1), bg)))
        story.append(row)

    # Course history totals
    ch_earned_hrs = sum(c["cr"] for c in all_c if done(c) and not drop(c))
    ch_ip_hrs = sum(c["cr"] for c in all_c if ip(c) or sched(c))
    ch_tot = Table(
        [
            [
                Paragraph(
                    f"Course History — Earned: {ch_earned_hrs} cr  ·  In Progress / Scheduled: {ch_ip_hrs} cr  ·  Projected Total: {ch_earned_hrs + ch_ip_hrs} cr",
                    ps("ch_tot", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=10),
                )
            ]
        ],
        colWidths=[CW],
    )
    ch_tot.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SUB_HDR_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(ch_tot)

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

    # Build action plan items from la, bc, mr, elecs
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
    all_major_rows = list(res.get("bc", [])) + list(res["mr"])
    for r in all_major_rows:
        code = r["id"].replace("_", "-")
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

    if elec_required_hrs > 0 and ehrs + ehrs_ip < elec_required_hrs:
        enrolled_codes = {c["raw"].upper() for c in elecs + elecs_ip}
        elec_opts = res.get("elec_opts", [])
        remaining = [o for o in elec_opts if o not in enrolled_codes]
        hrs_still_needed = elec_required_hrs - ehrs - ehrs_ip
        opt_str = ", ".join(remaining) if remaining else "see advisor"
        maj_miss.append(
            (
                f"Electives — {hrs_still_needed} hrs still needed",
                f"Enroll in elective from: {opt_str}",
            )
        )
    for c in elecs_ip:
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
    wi_rows = [r for r in res["la"] if r["area"] == "WI"]
    wi_sat = sum(1 for r in wi_rows if r["status"] == "Satisfied")
    wi_pend = sum(1 for r in wi_rows if r["status"] in ("Current", "Scheduled"))
    if wi_sat + wi_pend < 2:
        # Show each WI slot separately
        for i, r in enumerate(wi_rows, 1):
            slot_label = f"WI Writing Intensive #{i}"
            if r.get("course"):
                course_str = f"{r['course']['raw']} {r['course']['name']}"
                if r["status"] == "Satisfied":
                    action = f"✓ Satisfied — {course_str}"
                elif r["status"] in ("Current", "Scheduled"):
                    action = f"⟳ In Progress — {course_str} — complete with passing grade"
                else:
                    action = (
                        "Enroll in a WI-designated course (at least 1 must be upper-division 3000+)"
                    )
            else:
                action = (
                    "Enroll in a WI-designated course (at least 1 must be upper-division 3000+)"
                )
            wi_items.append((slot_label, action))
    elif wi_sat < 2 and wi_pend > 0:
        # Has enough combined but not all fully satisfied yet
        for i, r in enumerate(wi_rows, 1):
            if r["status"] in ("Current", "Scheduled") and r.get("course"):
                course_str = f"{r['course']['raw']} {r['course']['name']}"
                wi_items.append(
                    (
                        f"WI Writing Intensive #{i}",
                        f"⟳ In Progress — {course_str} — complete with passing grade",
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

    # Minor action plan
    if minor_rows:
        minor_miss = []
        minor_cur = []
        minor_sched = []
        for r in minor_rows:
            if r["id"] == "ELEC":
                elec_hrs_total = r["elec_hrs"] + sum(ec["cr"] for ec in r["elec_ip"])
                if elec_hrs_total < 4:
                    for ec in r["elec_ip"]:
                        s = "Current" if ip(ec) else "Scheduled"
                        lbl = f"{ec['raw']} {ec['name']}"
                        if s == "Current":
                            minor_cur.append(
                                (lbl, "Currently enrolled — complete with passing grade")
                            )
                        else:
                            minor_sched.append((lbl, "Scheduled — confirm enrollment"))
                    if elec_hrs_total == 0 and not r["elec_ip"]:
                        minor_miss.append(
                            (
                                "Coaching Elective — 4 hrs needed",
                                "Enroll in upper-division PEHS/EXSC/SPRL elective (3000+)",
                            )
                        )
            else:
                if r["status"] == "Not Satisfied":
                    minor_miss.append((r["label"], f"Enroll in {r['id'].replace('_','-')}"))
                elif r["status"] == "Current":
                    c = r["course"]
                    minor_cur.append(
                        (
                            f"{c['raw']} {c['name']}" if c else r["label"],
                            "Currently enrolled — complete with passing grade",
                        )
                    )
                elif r["status"] == "Scheduled":
                    c = r["course"]
                    minor_sched.append(
                        (
                            f"{c['raw']} {c['name']}" if c else r["label"],
                            "Scheduled — confirm enrollment",
                        )
                    )
        mn = res.get("minor_name", "Minor")
        ap_section(f"Minor — Current ({mn})", minor_cur, GOLD_BAR)
        ap_section(f"Minor — Scheduled ({mn})", minor_sched, GOLD_BAR)
        ap_section(f"Minor — Missing ({mn})", minor_miss, GOLD_BAR)

    # ── ELECTIVES action plan section ─────────────────────────────────────────
    elec_cur = []
    elec_sched = []
    elec_miss = []
    for c in elecs:
        elec_cur.append(
            (f"{c['raw']} {c['name']}", "Completed — counts toward elective requirement")
        )
    for c in elecs_ip:
        if ip(c):
            elec_cur.append(
                (f"{c['raw']} {c['name']}", "Currently enrolled — complete with passing grade")
            )
        else:
            elec_sched.append(
                (f"{c['raw']} {c['name']}", "Scheduled — confirm enrollment and complete")
            )
    if elec_required_hrs > 0 and ehrs + ehrs_ip < elec_required_hrs:
        still_needed = elec_required_hrs - ehrs - ehrs_ip
        elec_opts_list = res.get("elec_opts", [])
        enrolled_codes = {c["raw"].upper() for c in elecs + elecs_ip}
        remaining_opts = [o for o in elec_opts_list if o not in enrolled_codes]
        opt_str = ", ".join(remaining_opts) if remaining_opts else "see advisor"
        elec_miss.append(
            (f"{still_needed} hrs still needed", f"Enroll in approved elective: {opt_str}")
        )
    if elec_required_hrs > 0:
        ap_section("Electives — Current", elec_cur, GOLD_BAR)
        ap_section("Electives — Scheduled", elec_sched, GOLD_BAR)
        ap_section("Electives — Missing", elec_miss, GOLD_BAR)

    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            f"Anderson University Registrar  ·  This action plan is auto-generated. Please verify with your academic advisor.  ·  {catalog_year} Catalog",
            P["footer"],
        )
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
