"""
Anderson University Degree Audit Engine
Universal engine covering all FSB majors, minors, and LA frameworks
for catalog years 2022-23 through 2025-26.

Usage:
    engine = AuditEngine(catalog_year="2022-23", major_key="management")
    result = engine.run_audit(completed_courses)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from requirements.business_core import get_business_core
from requirements.fsb_majors import get_major_requirements, FSB_MAJORS
from requirements.fsb_minors import get_minor_requirements
from requirements.liberal_arts_requirements import (
    get_la_framework,
    LA_OLD_FRAMEWORK,
    LA_RAVEN_CORE_2526,
)


VALID_CATALOG_YEARS = ["2022-23", "2023-24", "2024-25", "2025-26"]

# Map display names → internal keys for the UI/API
MAJOR_DISPLAY_NAMES = {
    "2022-23": {
        "Sport Marketing":               "sport_marketing",
        "Marketing":                     "marketing",
        "Management":                    "management",
        "Accounting":                    "accounting",
        "Finance":                       "finance",
        "Engineering Management":        "engineering_management",
        "Global Business":               "global_business",
        "Music & Entertainment Business":"music_entertainment_business",
        "Business & Integrative Leadership": "business_integrative_leadership",
    },
    "2023-24": {
        "Sport Marketing":               "sport_marketing",
        "Marketing":                     "marketing",
        "Management":                    "management",
        "Accounting":                    "accounting",
        "Finance":                       "finance",
        "Business Analytics":            "business_analytics",
        "Engineering Management":        "engineering_management",
        "Global Business":               "global_business",
        "Business & Integrative Leadership": "business_integrative_leadership",
    },
    "2024-25": {
        "Sport Marketing":               "sport_marketing",
        "Marketing":                     "marketing",
        "Management":                    "management",
        "Accounting":                    "accounting",
        "Finance":                       "finance",
        "Business Analytics":            "business_analytics",
        "Engineering Management":        "engineering_management",
        "Business & Integrative Leadership": "business_integrative_leadership",
    },
    "2025-26": {
        "Sports Management":             "sport_marketing",  # renamed
        "Marketing":                     "marketing",
        "Management":                    "management",
        "Accounting":                    "accounting",
        "Finance":                       "finance",
        "Business Analytics":            "business_analytics",
        "Engineering Management":        "engineering_management",
        "Business & Integrative Leadership": "business_integrative_leadership",
    },
}


@dataclass
class CourseRecord:
    """A single completed course from a student transcript."""
    code: str
    name: str = ""
    credits: float = 0.0
    grade: str = ""
    term: str = ""
    is_exception: bool = False   # Waiver/exception flag
    is_transfer: bool = False

    @property
    def numeric_grade(self) -> float:
        grade_map = {
            "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "D-": 0.7,
            "F": 0.0,
        }
        return grade_map.get(self.grade.upper(), 0.0)

    @property
    def passing(self) -> bool:
        return self.numeric_grade >= 1.0 and self.grade.upper() not in ("F", "W", "WF")


@dataclass
class RequirementResult:
    """Result of checking a single requirement."""
    label: str
    status: str          # "Satisfied" | "In Progress" | "Not Satisfied"
    satisfying_course: Optional[str] = None
    satisfying_courses: list = field(default_factory=list)
    credits_earned: float = 0.0
    credits_required: float = 0.0
    notes: str = ""


@dataclass
class AuditResult:
    """Full audit result for one student."""
    student_name: str = ""
    student_id: str = ""
    catalog_year: str = ""
    major: str = ""
    overall_gpa: float = 0.0
    major_gpa: float = 0.0
    total_credits_completed: float = 0.0

    # Sections
    liberal_arts: list = field(default_factory=list)
    business_core: list = field(default_factory=list)
    major_requirements: list = field(default_factory=list)
    minor_requirements: list = field(default_factory=list)

    # Student Action Plan (6 categories)
    action_plan: dict = field(default_factory=lambda: {
        "liberal_arts_outstanding":  [],
        "core_outstanding":          [],
        "major_outstanding":         [],
        "minor_outstanding":         [],
        "gpa_concerns":              [],
        "other":                     [],
    })

    is_complete: bool = False
    summary: str = ""


class AuditEngine:
    """
    Unified audit engine for all AU FSB majors across all 4 catalog years.

    Parameters:
        catalog_year: One of "2022-23", "2023-24", "2024-25", "2025-26"
        major_key: Internal major key (e.g., "management", "sport_marketing")
        minor_key: Optional internal minor key
        icc_exempt: For 2025-26 — student completed Indiana College Core
    """

    def __init__(
        self,
        catalog_year: str,
        major_key: str,
        minor_key: str | None = None,
        icc_exempt: bool = False,
    ):
        if catalog_year not in VALID_CATALOG_YEARS:
            raise ValueError(f"Invalid catalog year: {catalog_year}")

        self.catalog_year = catalog_year
        self.major_key = major_key
        self.minor_key = minor_key
        self.icc_exempt = icc_exempt
        self.la_framework = get_la_framework(catalog_year)

        # Load requirement sets
        self.core_reqs = get_business_core(catalog_year)
        self.major_reqs = get_major_requirements(major_key, catalog_year)
        self.minor_reqs = get_minor_requirements(minor_key, catalog_year) if minor_key else None

    # ─────────────────────────────────────────────
    # PUBLIC ENTRY POINT
    # ─────────────────────────────────────────────

       def run_audit(
        self,
        completed_courses: list[CourseRecord],
        student_name: str = "",
        student_id: str = "",
    ) -> AuditResult:
        """Run a full degree audit and return an AuditResult."""

        result = AuditResult(
            student_name=student_name,
            student_id=student_id,
            catalog_year=self.catalog_year,
            major=self.major_reqs.get("name", self.major_key) if self.major_reqs else self.major_key,
        )

        completed_codes = {
            self._norm(c.code)
            for c in completed_courses if c.passing
        }

        # Compute GPAs
        result.overall_gpa = self._compute_gpa(completed_courses)
        result.major_gpa = self._compute_major_gpa(completed_courses, completed_codes)
        result.total_credits_completed = sum(c.credits for c in completed_courses if c.passing)

        # Run each section
        result.liberal_arts = self._check_liberal_arts(completed_courses, completed_codes)
        result.business_core = self._check_business_core(completed_courses, completed_codes)
        result.major_requirements = self._check_major(completed_courses, completed_codes)
        if self.minor_reqs:
            result.minor_requirements = self._check_minor(completed_courses, completed_codes)

        # Build action plan
        result.action_plan = self._build_action_plan(result)

        # Overall completion
        all_reqs = result.liberal_arts + result.business_core + result.major_requirements + result.minor_requirements
        result.is_complete = all(r.status == "Satisfied" for r in all_reqs)
        result.summary = self._build_summary(result, all_reqs)

        return result

    # ─────────────────────────────────────────────
    # LIBERAL ARTS CHECKER
    # ─────────────────────────────────────────────

    def _check_liberal_arts(
        self,
        courses: list[CourseRecord],
        completed_codes: set,
    ) -> list[RequirementResult]:
        """Check all LA requirements for the catalog year."""
        if self.la_framework == "OLD_FRAMEWORK":
            return self._check_old_la(courses, completed_codes)
        else:
            return self._check_raven_core(courses, completed_codes)

    def _check_old_la(self, courses, completed_codes) -> list[RequirementResult]:
        results = []
        year = self.catalog_year

        # F1 — Understanding College
        f1 = self._check_single_course("F1 Understanding College", "LART 1050", completed_codes)
        results.append(f1)

        # F1 → W8 auto-satisfy rule
        f1_satisfied = f1.status == "Satisfied"

        # F2 — Civil Discourse
        f2_courses = LA_OLD_FRAMEWORK["F2"]["courses"][year]
        f2 = self._check_any_course("F2 Civil Discourse & Critical Reasoning", f2_courses, completed_codes)
        results.append(f2)

        # F3 — Written Communication (ENGL + 2 WI)
        f3 = self._check_f3(completed_codes, courses, year)
        results.append(f3)

        # F4 — Speaking and Listening (COMM 1000 + 1 SI)
        f4 = self._check_f4(completed_codes, year)
        results.append(f4)

        # F5 — Quantitative Reasoning
        f5_courses = LA_OLD_FRAMEWORK["F5"]["courses"][year]
        f5 = self._check_any_course("F5 Quantitative Reasoning", f5_courses, completed_codes)
        results.append(f5)

        # F6 — Biblical Literacy
        f6 = self._check_single_course("F6 Biblical Literacy", "BIBL 2000", completed_codes)
        results.append(f6)

        # F7 — Personal Wellness
        f7_courses = [self._norm(c) for c in LA_OLD_FRAMEWORK["F7"]["courses"][year]]

        f7_found = None
        for c in courses:
            c_code = self._norm(c.code)
            if c_code in f7_courses and c.passing:
                f7_found = c
                break

        f7 = RequirementResult(
            label="F7 Personal Wellness",
            status="Satisfied" if f7_found else "Not Satisfied",
            satisfying_course=f7_found.code if f7_found else None,
            satisfying_courses=[f7_found.code] if f7_found else [],
            credits_earned=f7_found.credits if f7_found else 0.0,
            credits_required=2.0,
            notes="" if f7_found else f"Options: {', '.join(f7_courses)}",
        )
        results.append(f7)
        
        # W1 — Christian Ways of Knowing
        w1_courses = LA_OLD_FRAMEWORK["W1"]["courses"][year]
        w1 = self._check_any_course("W1 Christian Ways of Knowing", w1_courses, completed_codes)
        results.append(w1)

        # W2 — Scientific Ways of Knowing
        w2_courses = LA_OLD_FRAMEWORK["W2"]["courses"][year]
        w2 = self._check_any_course("W2 Scientific Ways of Knowing (Lab)", w2_courses, completed_codes)
        results.append(w2)

        # W3 — Civic Ways of Knowing
        w3_courses = LA_OLD_FRAMEWORK["W3"]["courses"][year]
        w3 = self._check_any_course("W3 Civic Ways of Knowing", w3_courses, completed_codes)
        results.append(w3)

        # W4 — Aesthetic Ways of Knowing
        w4 = self._check_w4(completed_codes, year)
        results.append(w4)

        # W5 — Social & Behavioral
        w5_courses = LA_OLD_FRAMEWORK["W5"]["courses"][year]
        w5 = self._check_any_course("W5 Social & Behavioral Ways of Knowing", w5_courses, completed_codes)
        results.append(w5)

        # W6 — Modern Languages
        w6_courses = LA_OLD_FRAMEWORK["W6"]["courses"][year]
        w6 = self._check_any_course("W6 Modern Languages (4 hrs)", w6_courses, completed_codes)
        results.append(w6)

        # W7 — Global/Intercultural
        w7_courses = LA_OLD_FRAMEWORK["W7"]["courses"][year]
        w7 = self._check_any_course("W7 Global/Intercultural Ways of Knowing", w7_courses, completed_codes)
        results.append(w7)

        # W8 — Experiential (auto-satisfied if F1 done)
        if f1_satisfied:
            w8 = RequirementResult(
                label="W8 Experiential Ways of Knowing",
                status="Satisfied",
                satisfying_course="BSNS 1050",  # Display rule from v6 template
                notes="Auto-satisfied: LART 1050 (F1) completed",
            )
        else:
            w8_courses = LA_OLD_FRAMEWORK["W8"]["courses"][year]
            w8 = self._check_any_course("W8 Experiential Ways of Knowing", w8_courses, completed_codes)
            if w8.status != "Satisfied":
                w8.notes = "Can also be satisfied when F1 (LART 1050) is completed"
        results.append(w8)

        return results

    def _check_raven_core(self, courses, completed_codes) -> list[RequirementResult]:
        """Check 2025-26 Raven Core + AU Experience."""
        results = []
        rc = LA_RAVEN_CORE_2526

        if not self.icc_exempt:
            # RC1–RC6
            for rc_key in ["RC1", "RC2", "RC3", "RC4", "RC5", "RC6"]:
                section = rc["RAVEN_CORE"][rc_key]
                r = self._check_any_course(section["label"], section["courses"], completed_codes)
                results.append(r)
        else:
            results.append(RequirementResult(
                label="Raven Core (RC1–RC6)",
                status="Satisfied",
                notes="ICC exemption applied — Indiana College Core completed",
            ))

        # AU1–AU6
        for au_key in ["AU1", "AU2", "AU3", "AU4", "AU5", "AU6"]:
            section = rc["AU_EXPERIENCE"][au_key]
            r = self._check_any_course(section["label"], section["courses"], completed_codes)
            results.append(r)

        return results

    def _check_f3(self, completed_codes, courses, year) -> RequirementResult:
        """F3: ENGL 1100/1110 + ENGL 1120 + 2 WI courses."""
        engl_base = ("ENGL 1100" in completed_codes or "ENGL 1110" in completed_codes)
        engl_1120 = "ENGL 1120" in completed_codes
        wi_courses = LA_OLD_FRAMEWORK["F3"]["wi_courses"][year]
        wi_found = [c for c in wi_courses if c in completed_codes and c != "ENGL 1120"]
        wi_satisfied = len(wi_found) >= 2

        all_good = engl_base and engl_1120 and wi_satisfied
        status = "Satisfied" if all_good else "Not Satisfied"
        missing_parts = []
        if not engl_base:
            missing_parts.append("ENGL 1100 or ENGL 1110")
        if not engl_1120:
            missing_parts.append("ENGL 1120")
        if not wi_satisfied:
            missing_parts.append(f"2 WI courses (found {len(wi_found)})")

        return RequirementResult(
            label="F3 Written Communication",
            status=status,
            satisfying_courses=wi_found,
            notes="; ".join(missing_parts) if missing_parts else "",
        )

    def _check_f4(self, completed_codes, year) -> RequirementResult:
        """F4: COMM 1000 + 1 SI course."""
        comm1000 = "COMM 1000" in completed_codes
        si_courses = LA_OLD_FRAMEWORK["F4"]["si_courses"][year]
        si_found = [c for c in si_courses if c in completed_codes]

        all_good = comm1000 and len(si_found) >= 1
        status = "Satisfied" if all_good else "Not Satisfied"
        notes = []
        if not comm1000:
            notes.append("COMM 1000 required")
        if not si_found:
            notes.append(f"1 SI course required (options: {', '.join(si_courses)})")

        return RequirementResult(
            label="F4 Speaking and Listening",
            status=status,
            satisfying_courses=(["COMM 1000"] if comm1000 else []) + si_found,
            notes="; ".join(notes),
        )

    def _check_w4(self, completed_codes, year) -> RequirementResult:
        """W4: Integrative AE course OR AP + AX combo."""
        w4_data = LA_OLD_FRAMEWORK["W4"]["courses"][year]
        integrative = w4_data.get("integrative", [])
        found_integrative = [c for c in integrative if c in completed_codes]

        # For simplicity, check integrative courses; AP/AX logic requires course flags
        # Future enhancement: parse AP/AX course attributes from transcript data
        if found_integrative:
            return RequirementResult(
                label="W4 Aesthetic Ways of Knowing",
                status="Satisfied",
                satisfying_course=found_integrative[0],
                satisfying_courses=found_integrative,
            )

        # Check if any AP-designated course exists (requires course attribute flagging)
        # Placeholder — full AP/AX logic requires course attribute data
        return RequirementResult(
            label="W4 Aesthetic Ways of Knowing",
            status="Not Satisfied",
            notes="Requires integrative AE course or AP+AX combination. See advisor.",
        )

    # ─────────────────────────────────────────────
    # BUSINESS CORE CHECKER
    # ─────────────────────────────────────────────

    def _check_business_core(self, courses, completed_codes) -> list[RequirementResult]:
        results = []
        core = self.core_reqs

        # Engineering Management 2022-23 uses standalone_core from major, not FSB core
        major_uses_fsb_core = True
        if self.major_reqs and not self.major_reqs.get("uses_business_core", True):
            major_uses_fsb_core = False
            standalone = self.major_reqs.get("standalone_core", [])
            for course in standalone:
                code = course["code"]
                status = "Satisfied" if code in completed_codes else "Not Satisfied"
                results.append(RequirementResult(
                    label=f"{code} — {course.get('name', '')}",
                    status=status,
                    satisfying_course=code if status == "Satisfied" else None,
                    credits_required=course.get("credits", 3),
                    credits_earned=course.get("credits", 3) if status == "Satisfied" else 0,
                ))
            return results

        for course in core.get("required", []):
            code = course["code"]
            status = "Satisfied" if code in completed_codes else "Not Satisfied"
            also = ", ".join(course.get("also_satisfies", []))
            results.append(RequirementResult(
                label=f"{code} — {course.get('name', '')}",
                status=status,
                satisfying_course=code if status == "Satisfied" else None,
                credits_required=course["credits"],
                credits_earned=course["credits"] if status == "Satisfied" else 0,
                notes=f"Also satisfies: {also}" if also else "",
            ))

        # Math requirement (22-23 through 24-25 only)
        math_req = core.get("math_requirement")
        if math_req:
            math_options = [c["code"] for c in math_req["choose_one"]]
            math_found = [c for c in math_options if c in completed_codes]
            results.append(RequirementResult(
                label=f"Math Requirement (one of: {', '.join(math_options)})",
                status="Satisfied" if math_found else "Not Satisfied",
                satisfying_course=math_found[0] if math_found else None,
                notes=math_req["note"],
            ))

        return results

    # ─────────────────────────────────────────────
    # MAJOR CHECKER
    # ─────────────────────────────────────────────

    def _check_major(self, courses, completed_codes) -> list[RequirementResult]:
        if not self.major_reqs:
            return [RequirementResult(
                label="Major",
                status="Not Satisfied",
                notes=f"Major '{self.major_key}' not available for {self.catalog_year}",
            )]

        results = []

        # Required courses
        for course in self.major_reqs.get("required_courses", []):
            code = course["code"]
            status = "Satisfied" if code in completed_codes else "Not Satisfied"
            also = ", ".join(course.get("also_satisfies", []))
            results.append(RequirementResult(
                label=f"{code} — {course.get('name', '')}",
                status=status,
                satisfying_course=code if status == "Satisfied" else None,
                credits_required=course.get("credits", 3),
                credits_earned=course.get("credits", 3) if status == "Satisfied" else 0,
                notes=f"Also satisfies: {also}" if also else "",
            ))

        # Major courses (Sport Marketing style)
        for course in self.major_reqs.get("major_courses", []):
            code = course["code"]
            status = "Satisfied" if code in completed_codes else "Not Satisfied"
            also = ", ".join(course.get("also_satisfies", []))
            results.append(RequirementResult(
                label=f"{code} — {course.get('name', '')}",
                status=status,
                satisfying_course=code if status == "Satisfied" else None,
                credits_required=course.get("credits", 3),
                credits_earned=course.get("credits", 3) if status == "Satisfied" else 0,
                notes=f"Also satisfies: {also}" if also else "",
            ))

        # Choose-one block
        choose_one = self.major_reqs.get("choose_one")
        if choose_one:
            options = choose_one.get("options", [])
            found = [o for o in options if o["code"] in completed_codes]
            results.append(RequirementResult(
                label=f"Choose One: {choose_one.get('note', '')}",
                status="Satisfied" if found else "Not Satisfied",
                satisfying_course=found[0]["code"] if found else None,
                notes=f"Options: {', '.join(o['code'] for o in options)}",
            ))

        # Elective block
        elective = self.major_reqs.get("elective")
        if elective:
            choose_from = elective.get("choose_from", [])
            needed_credits = elective.get("credits", 3)
            found = [c for c in choose_from if c in completed_codes]
            earned = sum(3 for _ in found)  # Assume 3 cr each
            results.append(RequirementResult(
                label=f"Elective ({needed_credits} cr from approved list)",
                status="Satisfied" if earned >= needed_credits else "Not Satisfied",
                satisfying_courses=found,
                credits_required=needed_credits,
                credits_earned=earned,
                notes=f"Options: {', '.join(choose_from)}",
            ))

        # Electives block (Management style — 6 cr choose from list)
        electives = self.major_reqs.get("electives")
        if electives:
            choose_from = electives.get("choose_from", [])
            needed_credits = electives.get("credits", 6)
            found = [c for c in choose_from if c in completed_codes]
            earned = sum(3 for _ in found)
            results.append(RequirementResult(
                label=f"Major Electives ({needed_credits} cr)",
                status="Satisfied" if earned >= needed_credits else "Not Satisfied",
                satisfying_courses=found,
                credits_required=needed_credits,
                credits_earned=earned,
                notes=f"Options: {', '.join(choose_from)}",
            ))

        # Concentration handling (Marketing 22-23)
        concentrations = self.major_reqs.get("concentrations")
        if concentrations and isinstance(concentrations, dict):
            # Skip if it's a string-only note (e.g., Engineering Management)
            first_val = next(iter(concentrations.values()), None)
            if isinstance(first_val, str):
                # It's a {note: str, options: list} style — just note it
                results.append(RequirementResult(
                    label=f"Concentration: {concentrations.get('note', 'see advisor')}",
                    status="Not Satisfied",
                    notes=f"Options: {', '.join(concentrations.get('options', []))}",
                ))
            else:
                # Check if any concentration is fully satisfied
                concentration_found = False
                for conc_name, conc_courses in concentrations.items():
                    if not isinstance(conc_courses, list):
                        continue
                    conc_codes = [c["code"] for c in conc_courses if isinstance(c, dict)]
                    found = [c for c in conc_codes if c in completed_codes]
                    if len(found) == len(conc_codes) and len(conc_codes) > 0:
                        concentration_found = True
                        results.append(RequirementResult(
                            label=f"Concentration: {conc_name}",
                            status="Satisfied",
                            satisfying_courses=found,
                            notes="Concentration requirement met",
                        ))
                        break
                if not concentration_found:
                    results.append(RequirementResult(
                        label="Concentration (choose one)",
                        status="Not Satisfied",
                        notes=f"Available: {', '.join(k for k in concentrations.keys() if k not in ('note','options'))}",
                    ))

        return results

    # ─────────────────────────────────────────────
    # MINOR CHECKER
    # ─────────────────────────────────────────────

    def _check_minor(self, courses, completed_codes) -> list[RequirementResult]:
        if not self.minor_reqs:
            return []

        results = []
        required = self.minor_reqs.get("required", [])
        for code in required:
            results.append(RequirementResult(
                label=f"Minor: {code}",
                status="Satisfied" if code in completed_codes else "Not Satisfied",
                satisfying_course=code if code in completed_codes else None,
            ))

        # Elective/choose_from blocks
        for key in ["choose_6_from", "choose_9_from", "elective"]:
            block = self.minor_reqs.get(key)
            if not block:
                continue
            if isinstance(block, dict):
                choose_from = block.get("choose_from", [])
                needed = block.get("credits", 3)
            elif isinstance(block, list):
                choose_from = block
                needed = 6 if "6" in key else 9
            else:
                continue
            found = [c for c in choose_from if c in completed_codes]
            earned = sum(3 for _ in found)
            results.append(RequirementResult(
                label=f"Minor Elective ({needed} cr)",
                status="Satisfied" if earned >= needed else "Not Satisfied",
                satisfying_courses=found,
                credits_required=needed,
                credits_earned=earned,
            ))

        return results

    # ─────────────────────────────────────────────
    # GPA CALCULATORS
    # ─────────────────────────────────────────────

    def _compute_gpa(self, courses: list[CourseRecord]) -> float:
        gradeable = [c for c in courses if c.grade.upper() not in ("W", "WF", "P", "NP", "TR")]
        if not gradeable:
            return 0.0
        total_points = sum(c.numeric_grade * c.credits for c in gradeable)
        total_credits = sum(c.credits for c in gradeable)
        return round(total_points / total_credits, 2) if total_credits else 0.0

    def _compute_major_gpa(self, courses: list[CourseRecord], completed_codes: set) -> float:
        """GPA for courses that count toward the major."""
        major_codes = set()
        if self.major_reqs:
            for c in self.major_reqs.get("required_courses", []):
                major_codes.add(c["code"])
            for c in self.major_reqs.get("major_courses", []):
                major_codes.add(c["code"])
        # Also include business core
        for c in self.core_reqs["required"]:
            major_codes.add(c["code"])

        major_courses = [c for c in courses if c.code in major_codes and c.grade.upper() not in ("W", "WF")]
        if not major_courses:
            return 0.0
        total_points = sum(c.numeric_grade * c.credits for c in major_courses)
        total_credits = sum(c.credits for c in major_courses)
        return round(total_points / total_credits, 2) if total_credits else 0.0

    # ─────────────────────────────────────────────
    # ACTION PLAN BUILDER
    # ─────────────────────────────────────────────

    def _build_action_plan(self, result: AuditResult) -> dict:
        plan = {
            "liberal_arts_outstanding":  [],
            "core_outstanding":          [],
            "major_outstanding":         [],
            "minor_outstanding":         [],
            "gpa_concerns":              [],
            "other":                     [],
        }
        for r in result.liberal_arts:
            if r.status != "Satisfied":
                plan["liberal_arts_outstanding"].append(r.label)
        for r in result.business_core:
            if r.status != "Satisfied":
                plan["core_outstanding"].append(r.label)
        for r in result.major_requirements:
            if r.status != "Satisfied":
                plan["major_outstanding"].append(r.label)
        for r in result.minor_requirements:
            if r.status != "Satisfied":
                plan["minor_outstanding"].append(r.label)
        if result.major_gpa < 2.0:
            plan["gpa_concerns"].append(f"Major GPA {result.major_gpa:.2f} — minimum 2.0 required")
        if result.overall_gpa < 2.0:
            plan["gpa_concerns"].append(f"Overall GPA {result.overall_gpa:.2f} — minimum 2.0 required for graduation")
        return plan

    # ─────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────

    def _build_summary(self, result: AuditResult, all_reqs: list) -> str:
        total = len(all_reqs)
        satisfied = sum(1 for r in all_reqs if r.status == "Satisfied")
        outstanding = total - satisfied
        if result.is_complete:
            return f"All {total} requirements satisfied. Student is eligible for graduation pending GPA verification."
        return (
            f"{satisfied}/{total} requirements satisfied. "
            f"{outstanding} outstanding. "
            f"See Student Action Plan for details."
        )

       # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    def _norm(self, code: str) -> str:
        return code.split()[0].upper().replace("-", "_").replace(" ", "_").strip()

    def _check_single_course(self, label: str, code: str, completed: set) -> RequirementResult:
        norm_code = self._norm(code)
        status = "Satisfied" if norm_code in completed else "Not Satisfied"
        return RequirementResult(
            label=label,
            status=status,
            satisfying_course=norm_code if status == "Satisfied" else None,
        )

    def _check_any_course(self, label: str, options: list, completed: set) -> RequirementResult:
        found = [c for c in options if self._norm(c) in completed]
        status = "Satisfied" if found else "Not Satisfied"

        return RequirementResult(
            label=label,
            status=status,
            satisfying_course=found[0] if found else None,
            satisfying_courses=found,
            notes=f"Options: {', '.join(options)}" if not found else "",
        )

      


# ─────────────────────────────────────────────
# CONVENIENCE: CSV/DICT PARSER
# ─────────────────────────────────────────────

def parse_courses_from_dict(course_list: list[dict]) -> list[CourseRecord]:
    """
    Convert a list of dicts (from CSV or API) into CourseRecord objects.
    Expected keys: code, name, credits, grade, term
    """
    records = []
    for item in course_list:
        records.append(CourseRecord(
            code=item.get("code", "").strip().upper(),
            name=item.get("name", ""),
            credits=float(item.get("credits", 0)),
            grade=item.get("grade", ""),
            term=item.get("term", ""),
            is_exception=bool(item.get("is_exception", False)),
            is_transfer=bool(item.get("is_transfer", False)),
        ))
    return records


def run_audit_from_dict(
    courses: list[dict],
    catalog_year: str,
    major_key: str,
    minor_key: str | None = None,
    icc_exempt: bool = False,
    student_name: str = "",
    student_id: str = "",
) -> AuditResult:
    """
    One-call audit function. Pass raw course dicts and get back an AuditResult.
    """
    engine = AuditEngine(
        catalog_year=catalog_year,
        major_key=major_key,
        minor_key=minor_key,
        icc_exempt=icc_exempt,
    )
    records = parse_courses_from_dict(courses)
    return engine.run_audit(records, student_name=student_name, student_id=student_id)
