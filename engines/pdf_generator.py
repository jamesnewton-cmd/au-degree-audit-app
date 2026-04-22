"""
Anderson University — Audit PDF Generator

Replicates the exact layout of the Landon Bair audit PDF:
  Page 1: Header + Summary Stats + Eligibility Check + Liberal Arts table
  Page 2: Liberal Arts continued + LA Hours summary bar
  Page 3: Major table + Major Hours summary bar + Minor table (if applicable)
  Page 4: Course History table
  Page 5: Student Graduation Action Plan

Colors:
  AU Maroon: #7B1C1C (header bars, section titles)
  AU Gold:   #B8962E (section subheadings)
  Table header bg: #7B1C1C (white text)
  Alt row bg: #F5F0E8 (light tan)
  Status colors: Satisfied=#2E7D32 (dark green), In Progress=#E65100 (orange),
                 Scheduled=#1565C0 (blue), Not Satisfied=#C62828 (red)
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─────────────────────────────────────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────────────────────────────────────
AU_MAROON   = colors.HexColor("#7B1C1C")
AU_GOLD     = colors.HexColor("#B8962E")
AU_GOLD_LIGHT = colors.HexColor("#F5F0E8")
AU_DARK_BLUE = colors.HexColor("#1F3864")
WHITE       = colors.white
BLACK       = colors.black
LIGHT_GRAY  = colors.HexColor("#F2F2F2")
MED_GRAY    = colors.HexColor("#CCCCCC")

STATUS_COLORS = {
    "Satisfied":    colors.HexColor("#2E7D32"),
    "In Progress":  colors.HexColor("#E65100"),
    "Scheduled":    colors.HexColor("#1565C0"),
    "Not Satisfied": colors.HexColor("#C62828"),
}

PAGE_W, PAGE_H = letter
MARGIN = 0.5 * inch
CONTENT_W = PAGE_W - 2 * MARGIN


def _status_color(status: str):
    return STATUS_COLORS.get(status, BLACK)


def _status_short(status: str) -> str:
    """Short display for status column."""
    mapping = {
        "Satisfied": "Satisfied",
        "In Progress": "Current",
        "Scheduled": "Scheduled",
        "Not Satisfied": "Not Satisfied",
    }
    return mapping.get(status, status)


# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────

def _make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["header_title"] = ParagraphStyle(
        "header_title", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=10,
        textColor=WHITE, leading=14,
    )
    styles["section_title"] = ParagraphStyle(
        "section_title", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=10,
        textColor=AU_GOLD, leading=14, spaceAfter=4,
    )
    styles["table_header"] = ParagraphStyle(
        "table_header", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8,
        textColor=WHITE, leading=10,
    )
    styles["cell"] = ParagraphStyle(
        "cell", parent=base["Normal"],
        fontName="Helvetica", fontSize=8, leading=10,
    )
    styles["cell_bold"] = ParagraphStyle(
        "cell_bold", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8, leading=10,
    )
    styles["cell_status"] = ParagraphStyle(
        "cell_status", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8, leading=10,
    )
    styles["summary_bar"] = ParagraphStyle(
        "summary_bar", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8,
        textColor=BLACK, leading=10,
    )
    styles["action_header"] = ParagraphStyle(
        "action_header", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8,
        textColor=WHITE, leading=10,
    )
    styles["action_cell"] = ParagraphStyle(
        "action_cell", parent=base["Normal"],
        fontName="Helvetica", fontSize=8, leading=10,
    )
    styles["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"],
        fontName="Helvetica", fontSize=7,
        textColor=colors.HexColor("#666666"), leading=9,
        alignment=TA_CENTER,
    )
    return styles


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: colored status paragraph
# ─────────────────────────────────────────────────────────────────────────────

def _status_para(status: str, styles: dict) -> Paragraph:
    color = _status_color(status)
    hex_color = color.hexval() if hasattr(color, 'hexval') else "#000000"
    display = _status_short(status)
    return Paragraph(
        f'<font color="{hex_color}"><b>{display}</b></font>',
        styles["cell"]
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER BAR
# ─────────────────────────────────────────────────────────────────────────────

def _header_bar(student_name: str, major: str, catalog_year: str, styles: dict) -> Table:
    title = f"Anderson University — Graduation Audit  ·  {student_name}  ·  {major}  ·  {catalog_year} Catalog"
    t = Table(
        [[Paragraph(title, styles["header_title"])]],
        colWidths=[CONTENT_W],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AU_MAROON),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY + ELIGIBILITY TABLE (Page 1)
# ─────────────────────────────────────────────────────────────────────────────

def _summary_eligibility_table(result, styles: dict) -> Table:
    """Two-column table: left=metrics, right=eligibility checks."""
    P = styles["cell"]
    PB = styles["cell_bold"]

    def yn(flag: bool) -> Paragraph:
        color = "#2E7D32" if flag else "#C62828"
        text = "YES" if flag else "NO"
        return Paragraph(f'<font color="{color}"><b>{text}</b></font>', P)

    # Left column: metrics
    metrics = [
        [Paragraph("<b>Metric</b>", PB), Paragraph("<b>Value</b>", PB)],
        [Paragraph("Earned Hours", P), Paragraph(f"<b>{result.total_credits_earned:.1f}</b>", PB)],
        [Paragraph("In-Progress Hours", P), Paragraph(f"<b>{result.total_credits_in_progress:.1f}</b>", PB)],
        [Paragraph("Projected Total Hours", P), Paragraph(f"<b>{result.total_credits_projected:.1f}</b>", PB)],
        [Paragraph("Cumulative GPA", P), Paragraph(f"<b>{result.overall_gpa:.2f}</b>", PB)],
        [Paragraph(f"Major GPA ({result.major[:6]})", P), Paragraph(f"<b>{result.major_gpa:.2f}</b>", PB)],
    ]

    # Right column: eligibility
    wi_ok = sum(1 for r in result.la_rows if r.area == "WI" and r.status == "Satisfied") >= 2
    si_ok = any(r.area == "SI" and r.status == "Satisfied" for r in result.la_rows)

    eligibility = [
        [Paragraph("<b>Eligibility Check</b>", PB), Paragraph("<b>Status</b>", PB)],
        [Paragraph("LA (Projected) satisfied", P), yn(result.la_complete)],
        [Paragraph("Programs satisfied (Projected or Scheduled)", P), yn(result.major_complete)],
        [Paragraph("Projected Hours ≥120", P), yn(result.credits_ok)],
        [Paragraph("Cumulative GPA ≥2.0", P), yn(result.gpa_ok)],
        [Paragraph("Major GPA ≥2.0", P), yn(result.major_gpa_ok)],
        [Paragraph("Writing Intensive (WI) ≥2 courses (≥1 upper-div)", P), yn(wi_ok)],
        [Paragraph("Speaking Intensive (SI) ≥1 beyond COMM-1000", P), yn(si_ok)],
        [Paragraph("Eligible to Graduate — Pending passage of current courses", P),
         yn(result.eligible_to_walk)],
        [Paragraph("Eligible to Walk — Pending passage of current courses", P),
         yn(result.eligible_to_walk)],
    ]

    # Build left sub-table
    left_t = Table(metrics, colWidths=[1.8 * inch, 0.7 * inch])
    left_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, MED_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))

    # Build right sub-table
    right_t = Table(eligibility, colWidths=[3.6 * inch, 0.6 * inch])
    right_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, MED_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]))

    # Combine side by side
    outer = Table([[left_t, right_t]], colWidths=[2.6 * inch, 4.3 * inch])
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return outer


# ─────────────────────────────────────────────────────────────────────────────
# LIBERAL ARTS TABLE
# ─────────────────────────────────────────────────────────────────────────────

def _la_table(la_rows: list, styles: dict) -> Table:
    P = styles["cell"]
    PB = styles["cell_bold"]

    col_widths = [0.45 * inch, 1.8 * inch, 2.9 * inch, 1.0 * inch, 0.4 * inch, 0.45 * inch]

    header = [
        Paragraph("Area", styles["table_header"]),
        Paragraph("Course", styles["table_header"]),
        Paragraph("Requirement", styles["table_header"]),
        Paragraph("Status", styles["table_header"]),
        Paragraph("CR", styles["table_header"]),
        Paragraph("Grade", styles["table_header"]),
    ]

    data = [header]
    for r in la_rows:
        grade = ""
        # Try to get grade from the course display
        status_para = _status_para(r.status, styles)
        cr_display = f"({int(r.credits_required)})" if r.status in ("In Progress", "Scheduled") else str(int(r.credits_required))

        data.append([
            Paragraph(f"<b>{r.area}</b>", PB),
            Paragraph(r.course_display or "", P),
            Paragraph(r.label, P),
            status_para,
            Paragraph(cr_display, P),
            Paragraph(grade, P),
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, MED_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    # Alternate row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


# ─────────────────────────────────────────────────────────────────────────────
# MAJOR TABLE
# ─────────────────────────────────────────────────────────────────────────────

def _major_table(major_rows: list, styles: dict) -> Table:
    P = styles["cell"]
    PB = styles["cell_bold"]

    col_widths = [1.3 * inch, 3.0 * inch, 1.1 * inch, 0.5 * inch, 0.55 * inch]

    header = [
        Paragraph("Course", styles["table_header"]),
        Paragraph("Requirement", styles["table_header"]),
        Paragraph("Status", styles["table_header"]),
        Paragraph("CR", styles["table_header"]),
        Paragraph("Grade", styles["table_header"]),
    ]

    data = [header]
    for r in major_rows:
        status_para = _status_para(r.status, styles)
        cr_display = f"({int(r.credits_required)})" if r.status in ("In Progress", "Scheduled") else str(int(r.credits_required))
        data.append([
            Paragraph(f"<b>{r.course_display}</b>", PB),
            Paragraph(r.label if r.label != r.course_display else r.course_name, P),
            status_para,
            Paragraph(cr_display, P),
            Paragraph("", P),
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, MED_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY BAR (gold background)
# ─────────────────────────────────────────────────────────────────────────────

def _summary_bar(text: str, styles: dict) -> Table:
    t = Table([[Paragraph(text, styles["summary_bar"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AU_GOLD_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, AU_GOLD),
    ]))
    return t


# ─────────────────────────────────────────────────────────────────────────────
# COURSE HISTORY TABLE
# ─────────────────────────────────────────────────────────────────────────────

def _course_history_table(all_courses: list, styles: dict) -> Table:
    P = styles["cell"]
    PB = styles["cell_bold"]

    col_widths = [1.0 * inch, 1.2 * inch, 2.8 * inch, 0.7 * inch, 0.6 * inch, 0.7 * inch]

    header = [
        Paragraph("Term", styles["table_header"]),
        Paragraph("Course Code", styles["table_header"]),
        Paragraph("Course Name", styles["table_header"]),
        Paragraph("Letter Grade", styles["table_header"]),
        Paragraph("Credits", styles["table_header"]),
        Paragraph("Status", styles["table_header"]),
    ]

    data = [header]
    for c in all_courses:
        s = c.get("status", "")
        g = c.get("grade", "")

        if s == "dropped":
            term = "Dropped"
            status_display = "DR"
        elif s == "current":
            term = "Spring, 2025-26"
            status_display = "AC"
        elif s == "scheduled":
            term = "Spring, 2025-26"
            status_display = "AC"
        elif g == "T":
            term = "Transfer Credit"
            status_display = "CG"
        else:
            term = "Completed"
            status_display = "CG"

        # Color the term for transfer credits
        if g == "T":
            term_para = Paragraph(f'<font color="#E65100">{term}</font>', P)
        elif s == "dropped":
            term_para = Paragraph(term, P)
        elif s in ("current", "scheduled"):
            term_para = Paragraph(f'<font color="#1565C0">{term}</font>', P)
        else:
            term_para = Paragraph(term, P)

        data.append([
            term_para,
            Paragraph(f"<b>{c.get('raw', '').replace('_','-')}</b>", PB),
            Paragraph(c.get("name", ""), P),
            Paragraph(g if g != "T" else "T", P),
            Paragraph(str(c.get("cr", "")), P),
            Paragraph(status_display, P),
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, MED_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 1), (-1, -1), 7),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


# ─────────────────────────────────────────────────────────────────────────────
# ACTION PLAN TABLE
# ─────────────────────────────────────────────────────────────────────────────

def _action_section(title: str, items: list, styles: dict, color=None) -> list:
    """Build a section of the action plan."""
    if color is None:
        color = AU_MAROON

    elements = []
    header_t = Table(
        [[Paragraph(title, styles["action_header"])]],
        colWidths=[CONTENT_W],
    )
    header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(header_t)

    P = styles["action_cell"]
    if not items:
        row_t = Table(
            [[Paragraph("Completed", P), Paragraph("", P)]],
            colWidths=[CONTENT_W * 0.5, CONTENT_W * 0.5],
        )
        row_t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Oblique"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2E7D32")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(row_t)
    else:
        col_header = Table(
            [[Paragraph("<b>Course / Area</b>", P), Paragraph("<b>Recommended Action</b>", P)]],
            colWidths=[CONTENT_W * 0.45, CONTENT_W * 0.55],
        )
        col_header.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(col_header)

        for item in items:
            label = item.get("label", str(item))
            action = item.get("action", "Enroll in this course")
            row_t = Table(
                [[Paragraph(f'<font color="#C62828">{label}</font>', P),
                  Paragraph(action, P)]],
                colWidths=[CONTENT_W * 0.45, CONTENT_W * 0.55],
            )
            row_t.setStyle(TableStyle([
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
            ]))
            elements.append(row_t)

    return elements


def _build_action_items(result) -> dict:
    """Categorize outstanding items into Current / Scheduled / Missing."""
    la_current, la_scheduled, la_missing = [], [], []
    for r in result.la_rows:
        if r.status == "In Progress":
            la_current.append({
                "label": f"{r.area} {r.label} — {r.course_display}",
                "action": "Currently enrolled — complete with passing grade this semester",
            })
        elif r.status == "Scheduled":
            la_scheduled.append({
                "label": f"{r.area} {r.label} — {r.course_display}",
                "action": "Scheduled — complete with passing grade",
            })
        elif r.status == "Not Satisfied":
            la_missing.append({
                "label": f"{r.area} {r.label}",
                "action": f"Enroll in {r.area} approved course",
            })

    major_current, major_scheduled, major_missing = [], [], []
    for r in result.major_rows:
        if r.status == "In Progress":
            major_current.append({
                "label": r.course_display or r.label,
                "action": "Currently enrolled — complete with passing grade this semester",
            })
        elif r.status == "Scheduled":
            major_scheduled.append({
                "label": r.course_display or r.label,
                "action": "Scheduled — complete with passing grade",
            })
        elif r.status == "Not Satisfied":
            major_missing.append({
                "label": r.course_display or r.label,
                "action": f"Enroll in {r.course_display or r.label}",
            })

    return {
        "la_current": la_current,
        "la_scheduled": la_scheduled,
        "la_missing": la_missing,
        "major_current": major_current,
        "major_scheduled": major_scheduled,
        "major_missing": major_missing,
    }


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

def _footer_text(student_name: str, catalog_year: str) -> str:
    return f"Anderson University Registrar  ·  Audit Engine v3  ·  {catalog_year} Catalog  ·  {student_name}"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PDF BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def generate_pdf(result, output_path: str) -> str:
    """
    Generate the full graduation audit PDF.

    Args:
        result: AuditResult object from audit_engine.run_audit()
        output_path: File path to write the PDF

    Returns:
        output_path on success
    """
    styles = _make_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=0.6 * inch,
    )

    story = []

    # ── PAGE 1: Header + Summary + LA table ──────────────────────────────────
    story.append(_header_bar(result.student_name, result.major, result.catalog_year, styles))
    story.append(Spacer(1, 8))
    story.append(_summary_eligibility_table(result, styles))
    story.append(Spacer(1, 10))

    # LA section title
    story.append(Paragraph(f"Liberal Arts — {result.catalog_year}", styles["section_title"]))
    story.append(_la_table(result.la_rows, styles))

    # LA summary bar
    la_earned = sum(r.credits_earned for r in result.la_rows if r.status == "Satisfied")
    la_ip = sum(r.credits_earned for r in result.la_rows if r.status in ("In Progress", "Scheduled"))
    la_required = 54  # Standard LA total
    story.append(_summary_bar(
        f"Liberal Arts Hours — Earned: {int(la_earned)} cr  ·  In Progress / Scheduled: {int(la_ip)} cr  ·  Total Required: {la_required} cr",
        styles
    ))

    story.append(Spacer(1, 10))

    # ── MAJOR section ─────────────────────────────────────────────────────────
    story.append(Paragraph(f"{result.major} — {result.catalog_year}", styles["section_title"]))

    # Group major rows by section (Required Courses header)
    major_data = [[Paragraph("Course", styles["table_header"]),
                   Paragraph("Requirement", styles["table_header"]),
                   Paragraph("Status", styles["table_header"]),
                   Paragraph("CR", styles["table_header"]),
                   Paragraph("Grade", styles["table_header"])]]

    # Section header row
    section_row = [Paragraph(f"<b>{result.major} Required Courses</b>", styles["cell_bold"]),
                   Paragraph("", styles["cell"]),
                   Paragraph("", styles["cell"]),
                   Paragraph("", styles["cell"]),
                   Paragraph("", styles["cell"])]

    col_widths = [1.3 * inch, 3.0 * inch, 1.1 * inch, 0.5 * inch, 0.55 * inch]
    major_table_data = [major_data[0], section_row]

    for r in result.major_rows:
        status_para = _status_para(r.status, styles)
        cr_display = f"({int(r.credits_required)})" if r.status in ("In Progress", "Scheduled") else str(int(r.credits_required))
        major_table_data.append([
            Paragraph(f"<b>{r.course_display}</b>", styles["cell_bold"]),
            Paragraph(r.label if r.label != r.course_display else r.course_name, styles["cell"]),
            status_para,
            Paragraph(cr_display, styles["cell"]),
            Paragraph("", styles["cell"]),
        ])

    mt = Table(major_table_data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), AU_MAROON),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, 1), AU_GOLD_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, MED_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("SPAN", (0, 1), (-1, 1)),
    ]
    for i in range(2, len(major_table_data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    mt.setStyle(TableStyle(style_cmds))
    story.append(mt)

    # Major summary bar
    story.append(_summary_bar(
        f"Major Hours — Earned: {int(result.major_credits_earned)} cr  ·  In Progress / Scheduled: {int(result.major_credits_in_progress)} cr  ·  Total Required: {int(result.major_credits_required)} cr",
        styles
    ))

    story.append(Spacer(1, 10))

    # ── COURSE HISTORY ────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(_header_bar(result.student_name, result.major, result.catalog_year, styles))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Course History — Repeats Resolved", styles["section_title"]))
    story.append(_course_history_table(result.all_courses, styles))

    ch_earned = result.total_credits_earned
    ch_ip = result.total_credits_in_progress
    story.append(_summary_bar(
        f"Course History — Earned: {int(ch_earned)} cr  ·  In Progress / Scheduled: {int(ch_ip)} cr  ·  Projected Total: {int(result.total_credits_projected)} cr",
        styles
    ))

    # ── ACTION PLAN ───────────────────────────────────────────────────────────
    story.append(PageBreak())

    # Action plan header
    ap_header_t = Table(
        [[Paragraph(
            f"Anderson University — Student Graduation Action Plan  ·  {result.student_name}  ·  {result.major}",
            styles["header_title"]
        )]],
        colWidths=[CONTENT_W],
    )
    ap_header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AU_MAROON),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ap_header_t)
    story.append(Spacer(1, 4))

    # Sub-header
    story.append(Paragraph(
        f"Major: {result.major}  ·  Projected Hours: {result.total_credits_projected:.1f} / 120  ·  Cumulative GPA: {result.overall_gpa:.2f}",
        styles["cell"]
    ))
    story.append(Spacer(1, 8))

    action_items = _build_action_items(result)

    # LA sections
    story.extend(_action_section("Liberal Arts — Current", action_items["la_current"], styles, AU_GOLD))
    story.extend(_action_section("Liberal Arts — Scheduled", action_items["la_scheduled"], styles, AU_GOLD))
    story.extend(_action_section("Liberal Arts — Missing", action_items["la_missing"], styles, AU_GOLD))

    # Major sections
    story.extend(_action_section("Major — Current", action_items["major_current"], styles, AU_DARK_BLUE))
    story.extend(_action_section("Major — Scheduled", action_items["major_scheduled"], styles, AU_DARK_BLUE))
    story.extend(_action_section("Major — Missing", action_items["major_missing"], styles, AU_DARK_BLUE))

    # Credit hours section
    credits_items = [] if result.credits_ok else [{
        "label": f"Total Credits: {result.total_credits_projected:.0f} / 120",
        "action": "Enroll in additional courses to reach 120 credit hours",
    }]
    story.extend(_action_section("Credit Hours", credits_items, styles, AU_DARK_BLUE))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"Anderson University Registrar  ·  This action plan is auto-generated. Please verify with your academic advisor.  ·  {result.catalog_year} Catalog",
        styles["footer"]
    ))

    # Build PDF
    doc.build(story)
    return output_path
