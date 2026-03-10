"""
Anderson University Degree Audit — PDF Report Generator
Canvas-based, pixel-matched to Isaiah Rhodes / Registrar v2 reference.

COORDINATE SYSTEM:
- All y values are "from page top" (pdfplumber convention)
- text() helper converts: rl_y_from_bottom = H - y_top_for_baseline
- For 7.5pt text in a 17pt row: baseline = row_top + 12 (text visually centered)
- filled_rect(x0, y_top, x1, y_bot) draws rect from y_top to y_bot
"""
from __future__ import annotations
from io import BytesIO
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth

def clip(txt, max_pts, font="Helvetica", size=7.5):
    """Truncate text to fit within max_pts width."""
    txt = str(txt)
    while txt and stringWidth(txt, font, size) > max_pts:
        txt = txt[:-1]
    return txt

H, W_PAGE = 792, 612
MARGIN = 36
PW = W_PAGE - 2 * MARGIN  # 540

# Colors (r,g,b 0-1)
MAROON = (0.5412, 0.1020, 0.1647)
GOLD   = (0.7843, 0.6588, 0.2941)
TAN    = (0.8314, 0.7686, 0.6275)
ALT    = (0.9569, 0.9490, 0.9216)
BLACK  = (0.098,  0.098,  0.094)
WHITE  = (1.0,    1.0,    1.0)
GRAY   = (0.6,    0.6,    0.6)
LGRAY  = (0.94,   0.94,   0.94)
GREEN  = (0.18,   0.49,   0.20)
RED    = (0.776,  0.157,  0.157)
ORANGE = (0.902,  0.318,  0.0)
BLUE   = (0.082,  0.322,  0.753)

GRADE_PTS = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,
             "C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"D-":0.7,"F":0.0}

def fc(code):
    """'BSNS 3420' -> 'BSNS-3420'"""
    if not code: return ""
    p = str(code).strip().split()
    return f"{p[0]}-{p[1]}" if len(p) == 2 else str(code)

def status_str(s):
    if s == "Satisfied": return "Satisfied", GREEN
    if s in ("In Progress", "Current"): return "Current", ORANGE
    if s == "Scheduled": return "Scheduled", BLUE
    return "Not Satisfied", RED


class Draw:
    """Thin wrapper around ReportLab canvas with top-origin coordinates."""

    def __init__(self, canvas):
        self.c = canvas

    def rect(self, x0, y_top, x1, y_bot, fill=WHITE, stroke=True):
        self.c.setFillColorRGB(*fill)
        if stroke:
            self.c.setStrokeColorRGB(*GRAY)
            self.c.setLineWidth(0.25)
        self.c.rect(x0, H - y_bot, x1 - x0, y_bot - y_top,
                    fill=1, stroke=1 if stroke else 0)

    def text(self, txt, x, y_baseline_from_top, font="Helvetica", size=7.5,
             color=BLACK, align="left"):
        """y_baseline_from_top: y from page top to text baseline."""
        self.c.setFillColorRGB(*color)
        self.c.setFont(font, size)
        rl_y = H - y_baseline_from_top
        if align == "left":
            self.c.drawString(x, rl_y, str(txt))
        elif align == "center":
            self.c.drawCentredString(x, rl_y, str(txt))
        elif align == "right":
            self.c.drawRightString(x, rl_y, str(txt))

    def new_page(self):
        self.c.showPage()

    def save(self):
        self.c.save()


class AuditPDFGenerator:

    def generate(self, r, advisor_notes="", waiver_notes="", raw_courses=None):
        buf = BytesIO()
        cv = rl_canvas.Canvas(buf, pagesize=letter)
        d = Draw(cv)

        # Build lookups from raw course list
        grade_map, name_map = {}, {}
        for crs in (raw_courses or []):
            k = str(crs.get("code","")).strip().upper()
            if k:
                grade_map[k] = str(crs.get("grade","")).strip()
                name_map[k]  = str(crs.get("name","")).strip()

        def gf(code): return grade_map.get(str(code).strip().upper(), "") if code else ""
        def nf(code): return name_map.get(str(code).strip().upper(), "") if code else ""

        # Stats
        earned   = r.total_credits_completed
        in_prog  = sum(float(x.get("credits",0) or 0)
                       for x in (raw_courses or []) if x.get("grade","") == "IP")
        gpa_hrs  = qual_pts = 0.0
        for x in (raw_courses or []):
            g = str(x.get("grade","")).strip().upper()
            cr = float(x.get("credits",0) or 0)
            if g in GRADE_PTS: gpa_hrs += cr; qual_pts += GRADE_PTS[g] * cr
        projected = earned + in_prog

        footer = (f"Anderson University Registrar  \u00b7  Audit Engine v2  \u00b7  "
                  f"{r.catalog_year} Catalog  \u00b7  {r.student_name}")

        # ── Row/bar constants (all in points from page top) ──────────────────
        TITLE_H    = 27   # title bar height
        TITLE_TOP  = 42   # title bar starts here
        SEC_H      = 19   # section bar height
        COL_H      = 19   # column header height
        ROW_H      = 17   # standard data row height
        ROW2_H     = 28   # two-line data row height
        SUB_H      = 20   # sub-header (black) row height
        FOOTER_Y   = 764  # footer baseline from top
        BOTTOM     = 756  # last y before footer

        def draw_footer():
            d.text(footer, W_PAGE/2, FOOTER_Y, size=6.5, color=GRAY, align="center")

        def title_bar(txt, y_top=TITLE_TOP):
            d.rect(MARGIN, y_top, W_PAGE-MARGIN, y_top+TITLE_H, fill=MAROON, stroke=False)
            d.text(txt, 44, y_top + 18, "Helvetica-Bold", 9.5, WHITE)

        def sec_bar(txt, y_top, color=MAROON):
            d.rect(MARGIN, y_top, W_PAGE-MARGIN, y_top+SEC_H, fill=color, stroke=False)
            d.text(txt, 44, y_top + 13, "Helvetica-Bold", 8, WHITE)
            return y_top + SEC_H

        def col_hdr(cols, y_top):
            """cols: list of (label, x). Draws tan header row."""
            d.rect(MARGIN, y_top, W_PAGE-MARGIN, y_top+COL_H, fill=TAN, stroke=True)
            for lbl, x in cols:
                d.text(lbl, x, y_top + 13, "Helvetica-Bold", 7.5)
            return y_top + COL_H

        def data_row(cells, y_top, row_h=ROW_H, i=0):
            """cells: list of (txt, x, font, size, color). Alternating bg."""
            bg = ALT if i % 2 == 0 else WHITE
            d.rect(MARGIN, y_top, W_PAGE-MARGIN, y_top+row_h, fill=bg, stroke=True)
            for cell in cells:
                txt, x = cell[0], cell[1]
                font  = cell[2] if len(cell) > 2 else "Helvetica"
                size  = cell[3] if len(cell) > 3 else 7.5
                color = cell[4] if len(cell) > 4 else BLACK
                # Baseline at row center for ROW_H, slightly higher for ROW2_H first line
                baseline = y_top + 12
                d.text(txt, x, baseline, font, size, color)
            return y_top + row_h

        def check_page(y, needed, d, draw_footer):
            if y + needed > BOTTOM:
                draw_footer(); d.new_page(); return MARGIN
            return y

        # ════════════════════════════════════════════════════════════════════
        # PAGE 1
        # ════════════════════════════════════════════════════════════════════
        title_bar(f"Anderson University \u2014 Graduation Audit  \u00b7  "
                  f"{r.student_name}  \u00b7  {r.major}  \u00b7  {r.catalog_year} Catalog")

        # ── Metrics table (x0=60, x1=228, 167pt wide) ──────────────────────
        mx0, mx1 = 60.3, 227.7
        my = TITLE_TOP + TITLE_H   # = 69

        d.rect(mx0, my, mx1, my+17, fill=MAROON, stroke=True)
        d.text("Metric", mx0+5, my+12, "Helvetica-Bold", 7.5, WHITE)
        d.text("Value",  mx0+140, my+12, "Helvetica-Bold", 7.5, WHITE)

        abbr = (r.major or "")[:4]
        m_rows = [
            ("Earned Hours",          f"{earned:.1f}"),
            ("In-Progress Hours",     f"{in_prog:.1f}"),
            ("Projected Total Hours", f"{projected:.1f}"),
            ("GPA Hours",             f"{gpa_hrs:.1f}"),
            ("Quality Points",        f"{qual_pts:.1f}"),
            ("Cumulative GPA",        f"{r.overall_gpa:.2f}" if r.overall_gpa else "0.00"),
            (f"Major GPA ({abbr})",   f"{r.major_gpa:.2f}"   if r.major_gpa   else "0.00"),
        ]
        for i, (lbl, val) in enumerate(m_rows):
            yr = my + 17 + i * 17
            bg = ALT if i % 2 == 0 else WHITE
            d.rect(mx0, yr, mx1, yr+17, fill=bg, stroke=True)
            d.text(lbl, mx0+5, yr+12)
            d.text(val, mx0+143, yr+12)

        # ── Eligibility table (x0=238, x1=552, 313pt wide) ─────────────────
        ex0, ex1 = 238.5, 551.7
        ey = my

        la   = r.liberal_arts or []
        core = (r.business_core or []) + (r.major_requirements or [])
        la_ok   = all(rq.status in ("Satisfied","In Progress","Current","Scheduled") for rq in la)
        prg_ok  = all(rq.status in ("Satisfied","In Progress","Current","Scheduled") for rq in core)
        hrs_ok  = projected >= 120
        gpa_ok  = (r.overall_gpa or 0) >= 2.0
        mgpa_ok = (r.major_gpa   or 0) >= 2.0
        wi_ok   = sum(1 for rq in la
                      if ("WI" in rq.label or "Writing Intensive" in rq.label)
                      and rq.status == "Satisfied") >= 2
        si_ok   = any(rq.status in ("Satisfied","Current")
                      for rq in la if "SI" in rq.label or "Speaking Intensive" in rq.label)
        eligible = la_ok and prg_ok and hrs_ok and gpa_ok and mgpa_ok and wi_ok

        d.rect(ex0, ey, ex1, ey+17, fill=MAROON, stroke=True)
        d.text("Eligibility Check", ex0+5, ey+12, "Helvetica-Bold", 7.5, WHITE)
        d.text("Status", 519, ey+12, "Helvetica-Bold", 7.5, WHITE)

        e_rows = [
            ("LA (Projected) satisfied",                                   la_ok),
            ("Programs satisfied (Projected or Scheduled)",                prg_ok),
            (f"Projected Hours \u2265120",                                 hrs_ok),
            ("Cumulative GPA \u22652.0",                                   gpa_ok),
            ("Major GPA \u22652.0",                                        mgpa_ok),
            ("Writing Intensive (WI) \u22652 courses (\u22651 upper-div)", wi_ok),
            ("Speaking Intensive (SI) \u22651 beyond COMM-1000",           si_ok),
            ("Eligible to Graduate (all requirements met)",                eligible),
            ("Eligible to Walk (projected or scheduled)",
             la_ok and prg_ok and gpa_ok and mgpa_ok),
        ]
        for i, (lbl, val) in enumerate(e_rows):
            yr = ey + 17 + i * 17
            bg = ALT if i % 2 == 0 else WHITE
            d.rect(ex0, yr, ex1, yr+17, fill=bg, stroke=True)
            d.text(lbl, ex0+5, yr+12)
            yn_txt = "YES"; yn_col = GREEN
            if not val: yn_txt = "NO"; yn_col = RED
            d.text(yn_txt, 529, yr+12, "Helvetica-Bold", 7.5, yn_col)

        # ── Liberal Arts ────────────────────────────────────────────────────
        # LA cols: Area=41, Course=73.4, Requirement=192.2,
        #          Status=408.2, CR=489.2, Grade=521.6
        y = my + 17 + len(m_rows) * 17 + 6   # below metrics table + gap
        y = check_page(y, SEC_H + COL_H, d, draw_footer)
        y = sec_bar("Liberal Arts \u2014 Current", y)
        y = col_hdr([("Area",41),("Course",73.4),("Requirement",192.2),
                     ("Status",408.2),("CR",489.2),("Grade",521.6)], y)

        for i, rq in enumerate(r.liberal_arts or []):
            parts = rq.label.split(" ", 1)
            area     = parts[0]
            req_txt  = parts[1] if len(parts) > 1 else rq.label
            codes    = rq.satisfying_courses if rq.satisfying_courses else (
                       [rq.satisfying_course] if rq.satisfying_course else [])
            row_h    = ROW2_H if (codes and nf(codes[0])) else ROW_H

            y = check_page(y, row_h, d, draw_footer)
            bg = ALT if i % 2 == 0 else WHITE
            d.rect(MARGIN, y, W_PAGE-MARGIN, y+row_h, fill=bg, stroke=True)

            d.text(area, 42, y+12)
            if codes:
                d.text(fc(codes[0]), 74.4, y+8,  "Helvetica", 6.8, GRAY)
                nm = nf(codes[0])
                if nm: d.text(nm, 74.4, y+18, "Helvetica", 6.8, GRAY)
            d.text(req_txt, 193.2, y+12)
            s_txt, s_col = status_str(rq.status)
            d.text(s_txt, 409.2, y+12, "Helvetica-Bold", 7.5, s_col)
            cr_v = rq.credits_earned or rq.credits_required or 0
            if cr_v:
                cr_s = str(int(cr_v)) if float(cr_v) == int(float(cr_v)) else str(cr_v)
                d.text(cr_s, 490.2, y+12)
            if codes: d.text(gf(codes[0]), 522.6, y+12)
            y += row_h

        # ── Major Requirements ──────────────────────────────────────────────
        # Major cols: Course=41, Requirement=111.2, Status=402.8, CR=489.2, Grade=527
        y += 6
        y = check_page(y, SEC_H + COL_H, d, draw_footer)
        y = sec_bar(f"{r.major} Major \u2014 {r.catalog_year}", y)
        y = col_hdr([("Course",41),("Requirement",111.2),
                     ("Status",402.8),("CR",489.2),("Grade",527.0)], y)

        row_i = 0

        def major_sub(label, y):
            y = check_page(y, SUB_H, d, draw_footer)
            d.rect(MARGIN, y, W_PAGE-MARGIN, y+SUB_H, fill=BLACK, stroke=False)
            d.text(label, W_PAGE/2, y+14, "Helvetica-Bold", 7.5, WHITE, "center")
            return y + SUB_H

        def major_row(rq, y, i):
            y = check_page(y, ROW_H, d, draw_footer)
            # Extract code: use satisfying_course, or first word(s) of label that look like a code
            if rq.satisfying_course:
                code = rq.satisfying_course
            else:
                # Label format: "BSNS-4910 Full Name" — take the first token as code
                first_token = rq.label.split()[0] if rq.label else ""
                code = first_token if ('-' in first_token and first_token[:4].isalpha()) else rq.label.split()[0]
            # The requirement column shows full label; code column shows just the code
            req_label = rq.label
            # Strip leading "CODE-XXXX " from label if it starts with the code
            code_prefix = fc(code) + " "
            if req_label.startswith(code_prefix):
                req_label = req_label[len(code_prefix):]
            cr    = str(int(rq.credits_required)) if rq.credits_required else "3"
            grade = gf(code)
            bg    = ALT if i % 2 == 0 else WHITE
            d.rect(MARGIN, y, W_PAGE-MARGIN, y+ROW_H, fill=bg, stroke=True)
            d.text(fc(code),   42,    y+12)
            d.text(clip(req_label, 278), 112.2, y+12)
            s_txt, s_col = status_str(rq.status)
            d.text(s_txt,      403.8, y+12, "Helvetica-Bold", 7.5, s_col)
            d.text(cr,         490.2, y+12)
            d.text(grade,      528.0, y+12)
            return y + ROW_H

        if r.business_core:
            cr_tot = int(sum(rq.credits_required or 3 for rq in r.business_core))
            y = major_sub(f"Business Core Requirements ({cr_tot} hrs)", y)
            for rq in r.business_core:
                y = major_row(rq, y, row_i); row_i += 1

        if r.major_requirements:
            y = major_sub(f"{r.major} Required Courses", y)
            for rq in r.major_requirements:
                y = major_row(rq, y, row_i); row_i += 1

        electives = (r.action_plan or {}).get("electives_outstanding", [])
        if electives:
            y = major_sub(f"{r.major} Electives", y)
            for rq in electives:
                y = major_row(rq, y, row_i); row_i += 1

        if r.minor_requirements:
            y = major_sub("Minor Requirements", y)
            for rq in r.minor_requirements:
                y = major_row(rq, y, row_i); row_i += 1

        # Notes line
        notes = []
        for rq in (r.major_requirements or []):
            if rq.notes and any(k in rq.notes for k in ("SI","WI","Also")):
                c2 = (rq.satisfying_course or rq.label.split("\u2014")[0].split("—")[0]).strip()
                notes.append(f"{fc(c2)} ({rq.notes})")
        if notes:
            y += 3
            y = check_page(y, 10, d, draw_footer)
            note = "Note: " + "  \u00b7  ".join(notes)
            d.text(note, 42, y+8, size=6.5, color=GRAY)
            y += 12

        # ── Course History ──────────────────────────────────────────────────
        # CH cols: Term=41, Code=138.2, Name=213.8, Grade=429.8, Credits=483.8, Status=532.4
        if raw_courses:
            y += 6
            y = check_page(y, SEC_H + 28, d, draw_footer)
            y = sec_bar("Course History \u2014 Repeats Resolved", y)
            # Two-line header
            d.rect(MARGIN, y, W_PAGE-MARGIN, y+28, fill=MAROON, stroke=True)
            for lbl, x in [("Term",41),("Course Code",138.2),("Course Name",213.8),
                            ("Credits",483.8),("Status",532.4)]:
                d.text(lbl, x, y+20, "Helvetica-Bold", 7.5, WHITE)
            d.text("Letter", 429.8, y+10, "Helvetica-Bold", 7.5, WHITE)
            d.text("Grade",  429.8, y+20, "Helvetica-Bold", 7.5, WHITE)
            y += 28

            for i, crs in enumerate(sorted(raw_courses,
                                    key=lambda x:(x.get("code",""), x.get("term","")))):
                grade = str(crs.get("grade","")).strip().upper()
                term  = crs.get("term","")
                code  = fc(crs.get("code",""))
                name  = crs.get("name","")
                creds = float(crs.get("credits",0) or 0)
                is_tr = crs.get("is_transfer", False)

                if grade in ("DRP","W"):      term_d, stat = "Dropped",       "DR"
                elif is_tr or grade == "T":   term_d, stat = "Transfer Credit","CG"
                elif grade == "IP":            term_d, stat = term,             "AC"
                elif grade in ("CR","P","S"):  term_d, stat = "Completed",     "CG"
                else:
                    term_d = "Completed" if (not term or term == "Transfer Credit") else term
                    stat   = "CG"

                # For long ELCT/LAWK transfer codes, show just the local code portion
                raw_code = crs.get("code","")
                disp_code = code
                if len(code) > 12 or raw_code.startswith("ELCT") or raw_code.startswith("LAWK"):
                    # Try to extract just the last meaningful segment
                    parts = raw_code.replace("LAWK--","LAWK-").split("-")
                    # Show max 14 chars
                    disp_code = clip(code, 70, "Helvetica-Bold", 7)

                y = check_page(y, 16, d, draw_footer)
                bg = ALT if i % 2 == 0 else WHITE
                d.rect(MARGIN, y, W_PAGE-MARGIN, y+16, fill=bg, stroke=True)
                d.text(clip(term_d, 90, size=7),  42,    y+11, size=7)
                d.text(disp_code,                 139.2, y+11, "Helvetica-Bold", 7)
                d.text(clip(name, 200, size=7),   214.8, y+11, size=7)
                d.text(grade,                     430.8, y+11, size=7)
                d.text(str(int(creds)) if creds else "0", 484.8, y+11, size=7)
                d.text(stat,                      533.4, y+11, size=7)
                y += 16

        draw_footer()
        d.new_page()

        # ════════════════════════════════════════════════════════════════════
        # ACTION PLAN PAGE
        # ════════════════════════════════════════════════════════════════════
        title_bar(f"Anderson University \u2014 Student Graduation Action Plan  "
                  f"\u00b7  {r.student_name}  \u00b7  {r.major}")

        ap_y = TITLE_TOP + TITLE_H + 10
        d.text(f"Major: {r.major}  \u00b7  Projected Hours: {projected:.1f} / 120  "
               f"\u00b7  Cumulative GPA: {r.overall_gpa:.1f}",
               44, ap_y, "Helvetica-Bold", 7.5)
        ap_y += 22

        la2   = r.liberal_arts       or []
        core2 = (r.business_core     or []) + (r.major_requirements or [])
        plan  = r.action_plan        or {}

        la_cur  = [rq for rq in la2   if rq.status in ("In Progress","Current")]
        la_sch  = [rq for rq in la2   if rq.status == "Scheduled"]
        la_mis  = [rq for rq in la2   if rq.status == "Not Satisfied"]
        m_cur   = [rq for rq in core2 if rq.status in ("In Progress","Current")]
        m_sch   = [rq for rq in core2 if rq.status == "Scheduled"]
        m_mis   = [rq for rq in core2 if rq.status == "Not Satisfied"]

        wi_sat  = [w for w in la2 if ("WI" in w.label or "Writing Intensive" in w.label)
                   and w.status == "Satisfied"]
        wi_ip   = [w for w in la2 if ("WI" in w.label or "Writing Intensive" in w.label)
                   and w.status in ("In Progress","Current")]

        def ap_section(title, rows_data, color=MAROON):
            nonlocal ap_y
            ap_y = check_page(ap_y, SEC_H + ROW_H, d, draw_footer)
            ap_y = sec_bar(title, ap_y, color)

            if not rows_data:
                ap_y = check_page(ap_y, 18, d, draw_footer)
                d.rect(MARGIN, ap_y, W_PAGE-MARGIN, ap_y+18, fill=LGRAY, stroke=True)
                d.text("\u2713 Completed", 42, ap_y+13, "Helvetica-Bold", 7.5, GREEN)
                ap_y += 18
            else:
                ap_y = check_page(ap_y, COL_H, d, draw_footer)
                d.rect(MARGIN, ap_y, W_PAGE-MARGIN, ap_y+COL_H, fill=TAN, stroke=True)
                d.text("Course / Area",      42,    ap_y+13, "Helvetica-Bold", 7.5)
                d.text("Recommended Action", 247.2, ap_y+13, "Helvetica-Bold", 7.5)
                ap_y += COL_H
                for i, (lbl, act) in enumerate(rows_data):
                    ap_y = check_page(ap_y, ROW_H, d, draw_footer)
                    bg = ALT if i % 2 == 0 else WHITE
                    d.rect(MARGIN, ap_y, W_PAGE-MARGIN, ap_y+ROW_H, fill=bg, stroke=True)
                    d.text(clip(f"\u2717{lbl}", 190), 42,    ap_y+12, "Helvetica-Bold", 7.5, MAROON)
                    d.text(clip(act, 300),              247.2, ap_y+12)
                    ap_y += ROW_H
            ap_y += 16  # gap

        ap_section("Liberal Arts \u2014 Current",
                   [(rq.label, "Currently enrolled \u2014 complete with passing grade this semester")
                    for rq in la_cur])
        ap_section("Liberal Arts \u2014 Scheduled",
                   [(rq.label, "Scheduled \u2014 confirm enrollment and complete with passing grade")
                    for rq in la_sch])
        ap_section("Liberal Arts \u2014 Missing",
                   [(rq.label, "See advisor \u2014 enroll in required course")
                    for rq in la_mis], color=GOLD)

        if len(wi_sat) < 2:
            sat_n = ", ".join(w.satisfying_course or w.label for w in wi_sat) or "none"
            ip_n  = ", ".join(w.satisfying_course or w.label for w in wi_ip)
            wi_lbl = f"Writing Intensive: {len(wi_sat)} of 2 satisfied ({sat_n})"
            if ip_n: wi_lbl += f" | Currently enrolled: {ip_n}"
            ap_section("Advanced Competency \u2014 WI",
                       [(wi_lbl, "Still need 2 WI-designated courses (at least 1 upper-division 3000+)")])
        else:
            ap_section("Advanced Competency \u2014 WI", [])

        ap_section("Major \u2014 Current",
                   [(rq.label, "Currently enrolled \u2014 complete with passing grade this semester")
                    for rq in m_cur])
        ap_section("Major \u2014 Scheduled",
                   [(rq.label, "Scheduled \u2014 confirm enrollment and complete with passing grade")
                    for rq in m_sch])
        ap_section("Major \u2014 Missing",
                   [(rq.label,
                     f"Enroll in {fc((rq.satisfying_course or rq.label.split()[0]).strip())}")
                    for rq in m_mis], color=GOLD)

        if projected < 120:
            ap_section("Credit Hours",
                       [(f"Projected total: {projected:.1f} hrs \u2014 need 120 hrs",
                         f"Must complete {120.0-projected:.1f} additional credit hours before graduation")],
                       color=GOLD)

        gpa_concerns = plan.get("gpa_concerns", [])
        if gpa_concerns:
            ap_section("GPA",
                       [(c2, "See advisor \u2014 GPA improvement plan required")
                        for c2 in gpa_concerns], color=RED)

        # Action plan special footer
        ap_y = check_page(ap_y, 12, d, draw_footer)
        d.text(f"Anderson University Registrar  \u00b7  This action plan is auto-generated. "
               f"Please verify with your academic advisor.  \u00b7  {r.catalog_year} Catalog",
               W_PAGE/2, ap_y+8, size=6.5, color=GRAY, align="center")

        draw_footer()
        d.save()
        return buf.getvalue()


def generate_audit_pdf(audit_result, raw_courses=None) -> bytes:
    return AuditPDFGenerator().generate(audit_result, raw_courses=raw_courses)
