"""
Anderson University Degree Audit — PDF Report Generator
Matches the Ethan Scialabba v6 template layout.

Key template rules:
1. Page count is NOT fixed — audits span as many pages as content requires
2. Only layout, colors, and sections must match the v6 template
3. W8 row always displays "BSNS 1050" when auto-satisfied via F1
4. Cross-listed courses shown in each applicable row

Usage:
    generator = AuditPDFGenerator()
    pdf_bytes = generator.generate(audit_result)
"""

from __future__ import annotations
from io import BytesIO
from datetime import date
from engines.audit_engine import AuditResult, RequirementResult

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        KeepTogether, HRFlowable,
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ─────────────────────────────────────────────
# BRAND COLORS (Anderson University)
# ─────────────────────────────────────────────

AU_BLACK      = colors.HexColor("#000000")
AU_GOLD       = colors.HexColor("#C8A84B")
AU_DARK_GOLD  = colors.HexColor("#A08030")
AU_WHITE      = colors.white
AU_LIGHT_GRAY = colors.HexColor("#F5F5F5")
AU_MED_GRAY   = colors.HexColor("#CCCCCC")
AU_DARK_GRAY  = colors.HexColor("#555555")

STATUS_GREEN  = colors.HexColor("#2E7D32")
STATUS_RED    = colors.HexColor("#C62828")
STATUS_YELLOW = colors.HexColor("#F9A825")


class AuditPDFGenerator:
    """Generate PDF audit reports matching the Ethan Scialabba v6 template."""

    PAGE_WIDTH, PAGE_HEIGHT = letter
    MARGIN = 0.65 * inch
    COL_LABEL_WIDTH  = 3.4 * inch
    COL_COURSE_WIDTH = 1.8 * inch
    COL_STATUS_WIDTH = 1.4 * inch
    COL_NOTES_WIDTH  = 1.0 * inch

    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "reportlab is required for PDF generation. "
                "Install with: pip install reportlab"
            )
        self._setup_styles()

    def _setup_styles(self):
        base = getSampleStyleSheet()
        self.styles = {
            "header_title": ParagraphStyle(
                "header_title",
                fontSize=18,
                fontName="Helvetica-Bold",
                textColor=AU_BLACK,
                alignment=TA_LEFT,
                spaceAfter=2,
            ),
            "header_sub": ParagraphStyle(
                "header_sub",
                fontSize=10,
                fontName="Helvetica",
                textColor=AU_DARK_GRAY,
                alignment=TA_LEFT,
                spaceAfter=2,
            ),
            "section_heading": ParagraphStyle(
                "section_heading",
                fontSize=11,
                fontName="Helvetica-Bold",
                textColor=AU_WHITE,
                alignment=TA_LEFT,
                leftIndent=6,
                leading=14,
            ),
            "cell_label": ParagraphStyle(
                "cell_label",
                fontSize=9,
                fontName="Helvetica",
                textColor=AU_BLACK,
                leading=12,
            ),
            "cell_satisfied": ParagraphStyle(
                "cell_satisfied",
                fontSize=9,
                fontName="Helvetica-Bold",
                textColor=STATUS_GREEN,
                leading=12,
            ),
            "cell_not_satisfied": ParagraphStyle(
                "cell_not_satisfied",
                fontSize=9,
                fontName="Helvetica-Bold",
                textColor=STATUS_RED,
                leading=12,
            ),
            "cell_notes": ParagraphStyle(
                "cell_notes",
                fontSize=8,
                fontName="Helvetica-Oblique",
                textColor=AU_DARK_GRAY,
                leading=11,
            ),
            "gpa_label": ParagraphStyle(
                "gpa_label",
                fontSize=9,
                fontName="Helvetica-Bold",
                textColor=AU_BLACK,
                alignment=TA_CENTER,
            ),
            "action_plan_heading": ParagraphStyle(
                "action_plan_heading",
                fontSize=10,
                fontName="Helvetica-Bold",
                textColor=AU_BLACK,
                spaceAfter=4,
            ),
            "action_plan_item": ParagraphStyle(
                "action_plan_item",
                fontSize=9,
                fontName="Helvetica",
                textColor=AU_BLACK,
                leftIndent=12,
                leading=13,
            ),
            "footer": ParagraphStyle(
                "footer",
                fontSize=7,
                fontName="Helvetica",
                textColor=AU_MED_GRAY,
                alignment=TA_CENTER,
            ),
        }

    # ─────────────────────────────────────────────
    # PUBLIC
    # ─────────────────────────────────────────────

    def generate(self, audit_result: AuditResult) -> bytes:
        """Generate PDF bytes from an AuditResult."""
        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=letter,
            leftMargin=self.MARGIN,
            rightMargin=self.MARGIN,
            topMargin=self.MARGIN,
            bottomMargin=self.MARGIN,
        )
        story = []

        story += self._build_header(audit_result)
        story += self._build_gpa_bar(audit_result)
        story.append(Spacer(1, 0.12 * inch))

        if audit_result.liberal_arts:
            story += self._build_section("Liberal Arts Requirements", audit_result.liberal_arts)
            story.append(Spacer(1, 0.1 * inch))

        if audit_result.business_core:
            story += self._build_section("Business Core", audit_result.business_core)
            story.append(Spacer(1, 0.1 * inch))

        if audit_result.major_requirements:
            story += self._build_section(f"{audit_result.major} — Major Requirements", audit_result.major_requirements)
            story.append(Spacer(1, 0.1 * inch))

        if audit_result.minor_requirements:
            story += self._build_section("Minor Requirements", audit_result.minor_requirements)
            story.append(Spacer(1, 0.1 * inch))

        story += self._build_action_plan(audit_result)

        story.append(Spacer(1, 0.15 * inch))
        story.append(self._build_footer(audit_result))

        doc.build(story)
        return buf.getvalue()

    # ─────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────

    def _build_header(self, r: AuditResult) -> list:
        elements = []

        # Gold bar at top
        elements.append(HRFlowable(
            width="100%",
            thickness=6,
            color=AU_GOLD,
            spaceAfter=6,
        ))

        elements.append(Paragraph("Anderson University", self.styles["header_title"]))
        elements.append(Paragraph("Falls School of Business — Degree Audit", self.styles["header_sub"]))

        elements.append(HRFlowable(width="100%", thickness=1, color=AU_MED_GRAY, spaceBefore=4, spaceAfter=6))

        # Student info table
        info_data = [
            [
                Paragraph(f"<b>Student:</b> {r.student_name or '—'}", self.styles["cell_label"]),
                Paragraph(f"<b>ID:</b> {r.student_id or '—'}", self.styles["cell_label"]),
                Paragraph(f"<b>Catalog Year:</b> {r.catalog_year}", self.styles["cell_label"]),
                Paragraph(f"<b>Major:</b> {r.major}", self.styles["cell_label"]),
            ]
        ]
        info_table = Table(info_data, colWidths=["25%", "15%", "25%", "35%"])
        info_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.05 * inch))

        # Print date
        elements.append(Paragraph(
            f"Generated: {date.today().strftime('%B %d, %Y')}  |  "
            f"Status: {'✓ Degree Requirements Met' if r.is_complete else '⚠ Requirements Outstanding'}",
            self.styles["header_sub"],
        ))

        elements.append(HRFlowable(width="100%", thickness=1, color=AU_MED_GRAY, spaceBefore=6, spaceAfter=4))
        return elements

    # ─────────────────────────────────────────────
    # GPA BAR
    # ─────────────────────────────────────────────

    def _build_gpa_bar(self, r: AuditResult) -> list:
        gpa_data = [[
            Paragraph(
                f"<b>Overall GPA:</b> {r.overall_gpa:.2f}",
                self.styles["gpa_label"],
            ),
            Paragraph(
                f"<b>Major GPA:</b> {r.major_gpa:.2f}",
                self.styles["gpa_label"],
            ),
            Paragraph(
                f"<b>Credits Completed:</b> {int(r.total_credits_completed)}",
                self.styles["gpa_label"],
            ),
        ]]
        t = Table(gpa_data, colWidths=["33%", "33%", "34%"])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), AU_LIGHT_GRAY),
            ("BOX", (0, 0), (-1, -1), 1, AU_MED_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return [t]

    # ─────────────────────────────────────────────
    # REQUIREMENTS SECTION TABLE
    # ─────────────────────────────────────────────

    def _build_section(self, heading: str, requirements: list[RequirementResult]) -> list:
        elements = []

        # Section heading row (gold background)
        heading_table = Table(
            [[Paragraph(heading, self.styles["section_heading"])]],
            colWidths=["100%"],
        )
        heading_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), AU_BLACK),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(heading_table)

        # Column headers
        col_header_data = [[
            Paragraph("<b>Requirement</b>", self.styles["cell_label"]),
            Paragraph("<b>Course</b>", self.styles["cell_label"]),
            Paragraph("<b>Status</b>", self.styles["cell_label"]),
            Paragraph("<b>Notes</b>", self.styles["cell_notes"]),
        ]]

        rows = [col_header_data[0]]
        row_colors = []

        for i, req in enumerate(requirements):
            # Status styling
            if req.status == "Satisfied":
                status_style = self.styles["cell_satisfied"]
                status_text = "✓ Satisfied"
            elif req.status == "In Progress":
                status_style = self.styles["cell_notes"]
                status_text = "⟳ In Progress"
            else:
                status_style = self.styles["cell_not_satisfied"]
                status_text = "✗ Not Satisfied"

            course_display = req.satisfying_course or ""
            if req.satisfying_courses and len(req.satisfying_courses) > 1:
                course_display = ", ".join(req.satisfying_courses[:3])

            row = [
                Paragraph(req.label, self.styles["cell_label"]),
                Paragraph(course_display, self.styles["cell_label"]),
                Paragraph(status_text, status_style),
                Paragraph(req.notes[:80] if req.notes else "", self.styles["cell_notes"]),
            ]
            rows.append(row)

            # Alternate row background
            bg = AU_WHITE if i % 2 == 0 else AU_LIGHT_GRAY
            row_colors.append(("BACKGROUND", (0, i + 1), (-1, i + 1), bg))

        col_widths = [
            self.COL_LABEL_WIDTH,
            self.COL_COURSE_WIDTH,
            self.COL_STATUS_WIDTH,
            self.COL_NOTES_WIDTH,
        ]

        table = Table(rows, colWidths=col_widths, repeatRows=1)
        style = TableStyle([
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), AU_DARK_GOLD),
            ("TEXTCOLOR", (0, 0), (-1, 0), AU_WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            # All cells
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, AU_MED_GRAY),
        ])
        for cmd in row_colors:
            style.add(*cmd)
        table.setStyle(style)

        elements.append(KeepTogether([table]))
        return elements

    # ─────────────────────────────────────────────
    # STUDENT ACTION PLAN
    # ─────────────────────────────────────────────

    def _build_action_plan(self, r: AuditResult) -> list:
        elements = []
        plan = r.action_plan

        heading_table = Table(
            [[Paragraph("Student Action Plan", self.styles["section_heading"])]],
            colWidths=["100%"],
        )
        heading_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), AU_BLACK),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(heading_table)

        sections = [
            ("Liberal Arts Outstanding",  plan.get("liberal_arts_outstanding", [])),
            ("Business Core Outstanding", plan.get("core_outstanding", [])),
            ("Major Requirements Outstanding", plan.get("major_outstanding", [])),
            ("Minor Requirements Outstanding", plan.get("minor_outstanding", [])),
            ("GPA Concerns",              plan.get("gpa_concerns", [])),
            ("Other",                     plan.get("other", [])),
        ]

        any_items = False
        for section_name, items in sections:
            if not items:
                continue
            any_items = True
            elements.append(Spacer(1, 0.06 * inch))
            elements.append(Paragraph(section_name, self.styles["action_plan_heading"]))
            for item in items:
                elements.append(Paragraph(f"• {item}", self.styles["action_plan_item"]))

        if not any_items:
            elements.append(Spacer(1, 0.06 * inch))
            elements.append(Paragraph(
                "✓ All requirements satisfied. No outstanding items.",
                self.styles["cell_satisfied"],
            ))

        return elements

    # ─────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────

    def _build_footer(self, r: AuditResult) -> Paragraph:
        return Paragraph(
            f"Anderson University — Falls School of Business  |  "
            f"Catalog Year: {r.catalog_year}  |  "
            f"This document is generated for advising purposes only and does not constitute an official transcript.  |  "
            f"Indy Collab LLC Audit System",
            self.styles["footer"],
        )


# ─────────────────────────────────────────────
# STANDALONE GENERATE FUNCTION
# ─────────────────────────────────────────────

def generate_audit_pdf(audit_result: AuditResult) -> bytes:
    """Generate a PDF audit report. Returns raw bytes."""
    gen = AuditPDFGenerator()
    return gen.generate(audit_result)
