"""
Anderson University Degree Audit — PDF Report Generator
Matches Ethan Scialabba v6 template exactly.

Sections:
  Page 1+: Running page header
  1. Title bar
  2. Metrics table (Earned/In-Progress/Projected/GPA Hours/Quality Points/Cum GPA/Major GPA)
  3. Eligibility Check table
  4. Liberal Arts table (ALL rows — satisfied, current, not satisfied — in one table)
  5. Major Requirements table (Business Core sub-header + Major sub-header + Notes footer)
  6. Course History table
  Action Plan page: Title bar, sub-line, then sections:
    Liberal Arts — Current / Scheduled / Missing
    Advanced Competency — WI (if applicable)
    Major — Current / Scheduled / Missing
    Credit Hours (if < 120)
  Footer line
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

# ── Brand palette ─────────────────────────────────────────────────────────────
MAROON  = colors.HexColor("#6B0F1A")
GOLD    = colors.HexColor("#C8942A")
BLACK   = colors.HexColor("#191918")
LGRAY   = colors.HexColor("#F5F3EF")
MGRAY   = colors.HexColor("#CCCCCC")
DGRAY   = colors.HexColor("#555555")
GREEN   = colors.HexColor("#2E7D32")
RED     = colors.HexColor("#C62828")
ORANGE  = colors.HexColor("#E65100")
WHITE   = colors.white

MARGIN  = 0.55 * inch
PW      = letter[0] - 2 * MARGIN   # usable page width ≈ 7.4 in


# ── Style factory ─────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=7.5, leading=10, textColor=BLACK)
    base.update(kw)
    return ParagraphStyle(name, **base)


STYLES = {
    "hdr_white" : S("hdr_white",  fontName="Helvetica-Bold", fontSize=9,
                    textColor=WHITE, leading=12),
    "hdr_sub"   : S("hdr_sub",    fontName="Helvetica",      fontSize=7.5,
                    textColor=colors.HexColor("#DDDDDD"), leading=10),
    "sec_hdr"   : S("sec_hdr",    fontName="Helvetica-Bold", fontSize=8,
                    textColor=WHITE, leading=11),
    "col_hdr"   : S("col_hdr",    fontName="Helvetica-Bold", fontSize=7.5,
                    textColor=BLACK, leading=10),
    "normal"    : S("normal"),
    "bold"      : S("bold",       fontName="Helvetica-Bold"),
    "satisfied" : S("satisfied",  fontName="Helvetica-Bold", textColor=GREEN),
    "current"   : S("current",    fontName="Helvetica-Bold", textColor=ORANGE),
    "missing"   : S("missing",    fontName="Helvetica-Bold", textColor=RED),
    "ap_course" : S("ap_course",  fontName="Helvetica-Bold", textColor=MAROON),
    "ap_action" : S("ap_action"),
    "footer"    : S("footer",     fontSize=6.5, textColor=MGRAY,
                    alignment=1, leading=9),
    "note"      : S("note",       fontSize=7, textColor=DGRAY, leading=9),
}


def p(text, style="normal"):
    return Paragraph(str(text), STYLES[style])


def status_p(status):
    if status == "Satisfied":
        return p("Satisfied", "satisfied")
    elif status in ("In Progress", "Current"):
        return p("Current",   "current")
    else:
        return p("Not Satisfied", "missing")


# ── Table helpers ──────────────────────────────────────────────────────────────
BASE_STYLE = [
    ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("BOX",           (0, 0), (-1, -1), 0.4, MGRAY),
    ("INNERGRID",     (0, 0), (-1, -1), 0.2, MGRAY),
]

def alt_rows(tbl_style, n_rows, start=1):
    """Append alternating row background commands."""
    for i in range(start, n_rows):
        bg = LGRAY if i % 2 == 1 else WHITE
        tbl_style.append(("BACKGROUND", (0, i), (-1, i), bg))


def title_bar(text, sub=None, color=MAROON):
    content = [p(text, "hdr_white")]
    if sub:
        content.append(p(sub, "hdr_sub"))
    t = Table([[c] for c in content], colWidths=[PW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), color),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    return t


def section_bar(text, color=MAROON):
    t = Table([[p(text, "sec_hdr")]], colWidths=[PW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), color),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    return t


# ── Main class ────────────────────────────────────────────────────────────────
class AuditPDFGenerator:

    def generate(self, audit_result, advisor_notes="", waiver_notes="",
                 raw_courses=None) -> bytes:
        r = audit_result
        buf = BytesIO()

        pg_hdr = (f"Anderson University Registrar  \u00b7  Audit Engine v2  \u00b7  "
                  f"{r.catalog_year} Catalog  \u00b7  {r.student_name}")

        def on_page(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 6.5)
            canvas.setFillColor(MGRAY)
            canvas.drawString(MARGIN, letter[1] - 0.35 * inch, pg_hdr)
            canvas.restoreState()

        doc = SimpleDocTemplate(buf, pagesize=letter,
                                leftMargin=MARGIN, rightMargin=MARGIN,
                                topMargin=0.5 * inch, bottomMargin=0.45 * inch)

        # Compute hours from raw_courses
        earned   = r.total_credits_completed
        in_prog  = sum(
            float(c.get("credits", 0)) for c in (raw_courses or [])
            if str(c.get("grade", "")).upper() == "IP"
        )
        projected = earned + in_prog

        # GPA hours & quality points (graded letter grades only)
        gpa_hrs = 0.0
        quality_pts = 0.0
        GRADE_POINTS = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,
                        "C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"F":0.0}
        for c in (raw_courses or []):
            g = str(c.get("grade","")).strip().upper()
            cr = float(c.get("credits", 0))
            if g in GRADE_POINTS:
                gpa_hrs    += cr
                quality_pts += GRADE_POINTS[g] * cr

        story = []
        story += self._title(r)
        story.append(Spacer(1, 0.1*inch))
        story += self._metrics(r, earned, in_prog, projected, gpa_hrs, quality_pts)
        story.append(Spacer(1, 0.08*inch))
        story += self._eligibility(r, projected)
        story.append(Spacer(1, 0.08*inch))
        story += self._liberal_arts(r)
        story.append(Spacer(1, 0.08*inch))
        story += self._major(r)
        if raw_courses:
            story.append(Spacer(1, 0.08*inch))
            story += self._course_history(raw_courses)

        story.append(PageBreak())
        story += self._action_plan(r, projected)
        story.append(Spacer(1, 0.08*inch))
        story.append(p(
            f"Anderson University Registrar  \u00b7  This action plan is auto-generated. "
            f"Please verify with your academic advisor.  \u00b7  {r.catalog_year} Catalog",
            "footer"
        ))

        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        return buf.getvalue()

    # ── 1. Title ──────────────────────────────────────────────────────────────
    def _title(self, r):
        return [title_bar(
            f"Anderson University \u2014 Graduation Audit  \u00b7  "
            f"{r.student_name}  \u00b7  {r.major}  \u00b7  {r.catalog_year} Catalog"
        )]

    # ── 2. Metrics ────────────────────────────────────────────────────────────
    def _metrics(self, r, earned, in_prog, projected, gpa_hrs, quality_pts):
        rows = [
            [p("Metric", "col_hdr"),     p("Value", "col_hdr")],
            [p("Earned Hours"),           p(f"{earned:.1f}")],
            [p("In-Progress Hours"),      p(f"{in_prog:.1f}")],
            [p("Projected Total Hours"),  p(f"{projected:.1f}")],
            [p("GPA Hours"),              p(f"{gpa_hrs:.1f}")],
            [p("Quality Points"),         p(f"{quality_pts:.1f}")],
            [p("Cumulative GPA"),         p(f"{r.overall_gpa:.2f}")],
            [p(f"Major GPA ({r.major[:4]})"), p(f"{r.major_gpa:.2f}")],
        ]
        cw = [3.5*inch, 1.2*inch]
        ts = TableStyle(BASE_STYLE + [
            ("BACKGROUND", (0, 0), (-1, 0), MAROON),
            ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
        alt_rows(ts._cmds if hasattr(ts, '_cmds') else [], len(rows))
        t = Table(rows, colWidths=cw)
        # Build style list manually so alt_rows works
        style_cmds = list(BASE_STYLE) + [
            ("BACKGROUND", (0, 0), (-1, 0), MAROON),
            ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
        for i in range(1, len(rows)):
            style_cmds.append(("BACKGROUND", (0,i), (-1,i), LGRAY if i%2==1 else WHITE))
        t.setStyle(TableStyle(style_cmds))
        return [t]

    # ── 3. Eligibility ────────────────────────────────────────────────────────
    def _eligibility(self, r, projected):
        la  = r.liberal_arts or []
        core = (r.business_core or []) + (r.major_requirements or [])

        la_proj     = all(rq.status in ("Satisfied","In Progress","Current") for rq in la)
        prog_proj   = all(rq.status in ("Satisfied","In Progress","Current") for rq in core)
        hrs_ok      = projected >= 120
        gpa_ok      = r.overall_gpa >= 2.0
        mgpa_ok     = r.major_gpa   >= 2.0
        wi_reqs     = [rq for rq in la if "WI" in rq.label or "Writing Intensive" in rq.label]
        wi_sat_cnt  = sum(1 for w in wi_reqs if w.status == "Satisfied")
        wi_ok       = wi_sat_cnt >= 2
        si_ok       = any(rq.status in ("Satisfied","Current")
                          for rq in la if "SI" in rq.label or "Speaking Intensive" in rq.label)
        eligible    = la_proj and prog_proj and hrs_ok and gpa_ok and mgpa_ok and wi_ok

        def yn(v): return p("YES","satisfied") if v else p("NO","missing")

        rows = [
            [p("Eligibility Check","col_hdr"),                                    p("Status","col_hdr")],
            [p("LA (Projected) satisfied"),                                        yn(la_proj)],
            [p("Programs satisfied (Projected or Scheduled)"),                     yn(prog_proj)],
            [p("Projected Hours \u2265120"),                                       yn(hrs_ok)],
            [p("Cumulative GPA \u22652.0"),                                        yn(gpa_ok)],
            [p("Major GPA \u22652.0"),                                             yn(mgpa_ok)],
            [p("Writing Intensive (WI) \u22652 courses (\u22651 upper-div)"),      yn(wi_ok)],
            [p("Speaking Intensive (SI) \u22651 beyond COMM-1000"),                yn(si_ok)],
            [p("Eligible to Graduate (all requirements met)"),                     yn(eligible)],
            [p("Eligible to Walk (projected or scheduled)"),
             yn(la_proj and prog_proj and gpa_ok and mgpa_ok)],
        ]
        cw = [5.0*inch, 0.9*inch]
        cmds = list(BASE_STYLE) + [
            ("BACKGROUND", (0,0), (-1,0), MAROON),
            ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
        for i in range(1, len(rows)):
            cmds.append(("BACKGROUND", (0,i), (-1,i), LGRAY if i%2==1 else WHITE))
        t = Table(rows, colWidths=cw)
        t.setStyle(TableStyle(cmds))
        return [t]

    # ── 4. Liberal Arts ───────────────────────────────────────────────────────
    def _liberal_arts(self, r):
        reqs = r.liberal_arts or []

        # Column widths: Area | Course | Requirement | Status | CR | Grade
        cw = [1.4*inch, 1.4*inch, 2.2*inch, 1.1*inch, 0.4*inch, 0.5*inch]

        col_hdr_row = [
            p("Area",            "col_hdr"),
            p("Course",          "col_hdr"),
            p("Requirement",     "col_hdr"),
            p("Status",          "col_hdr"),
            p("CR",              "col_hdr"),
            p("Grade",           "col_hdr"),
        ]

        rows = [col_hdr_row]
        for rq in reqs:
            # Area code = first token of label (F1, W2, WI, SI …)
            parts = rq.label.split(" ", 1)
            area  = parts[0]
            req_label = parts[1] if len(parts) > 1 else rq.label

            course = rq.satisfying_course or ""

            # For WI rows get count note into label
            if rq.notes and rq.status != "Satisfied":
                req_label = f"{req_label} — {rq.notes}"

            rows.append([
                p(area),
                p(course),
                p(req_label),
                status_p(rq.status),
                p(str(int(rq.credits_required)) if rq.credits_required else ""),
                p(""),   # grade not stored on req — left blank (matches template look)
            ])

        cmds = list(BASE_STYLE) + [
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8E0D0")),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
        for i in range(1, len(rows)):
            cmds.append(("BACKGROUND", (0,i), (-1,i), LGRAY if i%2==1 else WHITE))

        t = Table(rows, colWidths=cw)
        t.setStyle(TableStyle(cmds))
        return [section_bar("Liberal Arts \u2014 Current"), t]

    # ── 5. Major Requirements ─────────────────────────────────────────────────
    def _major(self, r):
        cw = [1.4*inch, 2.6*inch, 1.1*inch, 0.4*inch, 0.5*inch]

        col_hdr_row = [
            p("Course",      "col_hdr"),
            p("Requirement", "col_hdr"),
            p("Status",      "col_hdr"),
            p("CR",          "col_hdr"),
            p("Grade",       "col_hdr"),
        ]

        rows = [col_hdr_row]
        sub_rows = []   # indices of sub-header rows

        def sub_row(label):
            sub_rows.append(len(rows))
            rows.append([p(label, "bold"), p(""), p(""), p(""), p("")])

        def req_row(rq):
            code = rq.satisfying_course or rq.label.split(" \u2014 ")[0]
            label = rq.label
            if rq.notes:
                label = f"{label}   ({rq.notes})"
            cr = str(int(rq.credits_required)) if rq.credits_required else "3"
            rows.append([p(code), p(label), status_p(rq.status), p(cr), p("")])

        # Business Core
        if r.business_core:
            total_core_cr = sum(rq.credits_required for rq in r.business_core if rq.credits_required)
            sub_row(f"\u25a0 Business Core Requirements ({int(total_core_cr)} hrs) \u25a0")
            for rq in r.business_core:
                req_row(rq)

        # Major Required
        if r.major_requirements:
            sub_row(f"\u25a0 {r.major} Required Courses \u25a0")
            for rq in r.major_requirements:
                req_row(rq)

        # Minor
        if r.minor_requirements:
            sub_row(f"\u25a0 Minor Requirements \u25a0")
            for rq in r.minor_requirements:
                req_row(rq)

        cmds = list(BASE_STYLE) + [
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8E0D0")),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
        for i in range(1, len(rows)):
            if i in sub_rows:
                cmds += [
                    ("BACKGROUND", (0,i), (-1,i), BLACK),
                    ("TEXTCOLOR",  (0,i), (-1,i), WHITE),
                    ("FONTNAME",   (0,i), (-1,i), "Helvetica-Bold"),
                    ("SPAN",       (0,i), (-1,i)),
                ]
            else:
                cmds.append(("BACKGROUND", (0,i), (-1,i), LGRAY if i%2==1 else WHITE))

        t = Table(rows, colWidths=cw)
        t.setStyle(TableStyle(cmds))

        # Notes footer
        elements = [section_bar(f"{r.major} Major \u2014 {r.catalog_year}"), t]

        # Collect cross-listing notes from major reqs
        notes = [rq.notes for rq in (r.major_requirements or []) if rq.notes]
        if notes:
            elements.append(Spacer(1, 0.04*inch))
            elements.append(p("Note: " + "  \u00b7  ".join(notes), "note"))

        return elements

    # ── 6. Course History ─────────────────────────────────────────────────────
    def _course_history(self, raw_courses):
        cw = [1.3*inch, 1.1*inch, 2.2*inch, 0.65*inch, 0.55*inch, 0.55*inch]

        col_hdr_row = [
            p("Term",         "col_hdr"),
            p("Course Code",  "col_hdr"),
            p("Course Name",  "col_hdr"),
            p("Letter Grade", "col_hdr"),
            p("Credits",      "col_hdr"),
            p("Status",       "col_hdr"),
        ]

        rows = [col_hdr_row]
        for c in sorted(raw_courses, key=lambda x: x.get("code","")):
            grade  = str(c.get("grade","")).upper()
            term   = c.get("term","")
            code   = c.get("code","").replace(" ","-")
            name   = c.get("name","")
            creds  = c.get("credits", 0)
            is_tr  = c.get("is_transfer", False)

            if is_tr or grade == "T":
                term_disp  = "Transfer Credit"
                status_str = "CG"
            elif grade == "IP":
                term_disp  = term
                status_str = "AC"
            elif grade in ("CR","P","S"):
                term_disp  = term
                status_str = "CG"
            elif grade == "DRP" or grade == "W":
                term_disp  = "Dropped"
                status_str = "DR"
            else:
                term_disp  = "Completed"
                status_str = "CG"

            cr_disp = str(int(creds)) if creds else "0"
            rows.append([
                p(term_disp),
                p(code, "bold"),
                p(name),
                p(grade if grade not in ("IP","") else ("IP" if grade=="IP" else "")),
                p(cr_disp),
                p(status_str),
            ])

        cmds = list(BASE_STYLE) + [
            ("BACKGROUND", (0,0), (-1,0), MAROON),
            ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 7),
        ]
        for i in range(1, len(rows)):
            cmds.append(("BACKGROUND", (0,i), (-1,i), LGRAY if i%2==1 else WHITE))

        t = Table(rows, colWidths=cw)
        t.setStyle(TableStyle(cmds))
        return [section_bar("Course History \u2014 Repeats Resolved", color=GOLD), t]

    # ── 7. Action Plan ────────────────────────────────────────────────────────
    def _action_plan(self, r, projected):
        elements = []

        elements.append(title_bar(
            f"Anderson University \u2014 Student Graduation Action Plan  "
            f"\u00b7  {r.student_name}  \u00b7  {r.major}"
        ))
        elements.append(Spacer(1, 0.05*inch))
        elements.append(p(
            f"Major: {r.major}  \u00b7  Projected Hours: {projected:.1f} / 120  "
            f"\u00b7  Cumulative GPA: {r.overall_gpa:.2f}",
            "bold"
        ))
        elements.append(Spacer(1, 0.08*inch))

        la    = r.liberal_arts        or []
        core  = r.business_core       or []
        major = r.major_requirements  or []
        plan  = r.action_plan         or {}

        la_current  = [rq for rq in la    if rq.status in ("In Progress","Current")]
        la_missing  = [rq for rq in la    if rq.status == "Not Satisfied"]
        maj_current = [rq for rq in core+major if rq.status in ("In Progress","Current")]
        maj_missing = [rq for rq in core+major if rq.status == "Not Satisfied"]

        # WI status
        wi_reqs = [rq for rq in la if "WI" in rq.label or "Writing Intensive" in rq.label]
        wi_satisfied = [w for w in wi_reqs if w.status == "Satisfied"]
        wi_in_prog   = [w for w in wi_reqs if w.status in ("In Progress","Current")]
        show_wi = len(wi_satisfied) < 2

        def ap_section(label, rows_data, color=MAROON):
            """rows_data: list of (course_label, action_text)"""
            elements.append(section_bar(label, color=color))
            if not rows_data:
                t = Table([[p("\u2713 Completed", "satisfied")]], colWidths=[PW])
                t.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,-1),LGRAY),
                    ("LEFTPADDING",(0,0),(-1,-1),8),
                    ("TOPPADDING",(0,0),(-1,-1),3),
                    ("BOTTOMPADDING",(0,0),(-1,-1),3),
                    ("BOX",(0,0),(-1,-1),0.25,MGRAY),
                ]))
                elements.append(t)
                return

            tbl_rows = [[p("Course / Area","col_hdr"), p("Recommended Action","col_hdr")]]
            for (course_lbl, action) in rows_data:
                tbl_rows.append([
                    p(f"\u2717{course_lbl}", "ap_course"),
                    p(action, "ap_action"),
                ])
            cmds = list(BASE_STYLE) + [
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8E0D0")),
                ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ]
            for i in range(1, len(tbl_rows)):
                cmds.append(("BACKGROUND",(0,i),(-1,i), LGRAY if i%2==1 else WHITE))
            t = Table(tbl_rows, colWidths=[3.0*inch, 3.5*inch])
            t.setStyle(TableStyle(cmds))
            elements.append(t)

        # Liberal Arts — Current
        ap_section("Liberal Arts \u2014 Current", [
            (rq.label + (" \u2014 " + rq.satisfying_course if rq.satisfying_course else ""),
             "Currently enrolled \u2014 complete with passing grade this semester")
            for rq in la_current
        ])
        # Liberal Arts — Scheduled
        ap_section("Liberal Arts \u2014 Scheduled", [])
        # Liberal Arts — Missing
        ap_section("Liberal Arts \u2014 Missing", [
            (rq.label, "See advisor \u2014 enroll in required course")
            for rq in la_missing
        ], color=GOLD)

        # Advanced Competency — WI
        if show_wi:
            sat_list = ", ".join(w.satisfying_course or w.label for w in wi_satisfied) or "none"
            ip_list  = ", ".join(w.satisfying_course or w.label for w in wi_in_prog)
            lbl = f"Writing Intensive: {len(wi_satisfied)} of 2 satisfied ({sat_list})"
            if ip_list:
                lbl += f" | Currently enrolled: {ip_list}"
            ap_section("Advanced Competency \u2014 WI", [
                (lbl, "Still need 2 WI-designated courses (at least 1 upper-division 3000+) \u2014 see advisor")
            ], color=DGRAY)

        # Major — Current
        ap_section("Major \u2014 Current", [
            (rq.label, "Currently enrolled \u2014 complete with passing grade this semester")
            for rq in maj_current
        ])
        # Major — Scheduled
        ap_section("Major \u2014 Scheduled", [])
        # Major — Missing
        ap_section("Major \u2014 Missing", [
            (rq.label,
             f"Enroll in {rq.satisfying_course or rq.label.split(' \u2014 ')[0]} \u2014 {rq.label}"
             if rq.satisfying_course else "See advisor \u2014 enroll in required course")
            for rq in maj_missing
        ], color=GOLD)

        # Credit Hours
        if projected < 120:
            needed = 120 - projected
            ap_section("Credit Hours", [
                (f"Projected total: {projected:.1f} hrs \u2014 need 120 hrs",
                 f"Must complete {needed:.1f} additional credit hours before graduation")
            ], color=GOLD)

        # GPA concerns
        if plan.get("gpa_concerns"):
            ap_section("GPA", [
                (concern, "See advisor \u2014 GPA improvement plan required")
                for concern in plan["gpa_concerns"]
            ], color=RED)

        return elements


# ── Convenience wrapper ───────────────────────────────────────────────────────
def generate_audit_pdf(audit_result, raw_courses=None) -> bytes:
    return AuditPDFGenerator().generate(audit_result, raw_courses=raw_courses)
