"""
Anderson University — Non-FSB Audit Engine
Handles audit logic for all non-business-school programs.

For FSB majors, use engines/audit_engine.py.
This module is designed to be invoked from audit_engine.py's dispatch logic.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import re
from requirements.non_fsb_programs import (
    get_non_fsb_requirements,
    program_exists_in_year,
    ALL_NON_FSB_PROGRAMS,
)

# ─────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────


@dataclass
class CourseRecord:
    course_id: str  # e.g. "BIOL 2210"
    grade: str  # "A", "B+", "C", "IP", "TR", etc.
    credits: float
    term: str = ""

    @property
    def is_passing(self) -> bool:
        failing = {"F", "W", "WF", "NC", "I", "AU"}
        grade_upper = self.grade.upper().strip()
        return grade_upper not in failing and grade_upper != ""

    @property
    def is_in_progress(self) -> bool:
        return self.grade.upper() in {"IP", "CR/IP", "IN PROGRESS", "ENROLLED"}

    @property
    def grade_points(self) -> float:
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
        return gp_map.get(self.grade.upper(), 0.0)


@dataclass
class RequirementStatus:
    label: str  # e.g. "BIOL 2210 Foundations of Modern Biology I"
    status: str  # "Satisfied", "In Progress", "Not Met"
    course_used: Optional[str] = None
    notes: str = ""


@dataclass
class NonFSBAuditResult:
    student_id: str
    name: str
    major: str
    catalog_year: str
    requirements: list[RequirementStatus] = field(default_factory=list)
    major_gpa: float = 0.0
    total_major_credits: float = 0.0
    all_satisfied: bool = False
    outstanding: list[str] = field(default_factory=list)


# ─────────────────────────────────────────────
# Core engine
# ─────────────────────────────────────────────


class NonFSBAuditEngine:

    def __init__(self, program_key: str, catalog_year: str):
        self.program_key = program_key
        self.catalog_year = catalog_year
        self.requirements = get_non_fsb_requirements(program_key, catalog_year)
        if self.requirements is None:
            raise ValueError(
                f"Program '{program_key}' does not exist in catalog year {catalog_year}"
            )

    def _normalize_id(self, course_id: str) -> str:
        """Normalize course ID for matching: 'BIOL2210' → 'BIOL 2210'."""
        m = re.match(r"([A-Za-z]+)\s*(\d+)", course_id.strip())
        if m:
            return f"{m.group(1).upper()} {m.group(2)}"
        return course_id.strip().upper()

    def _build_completed_set(self, transcript: list[CourseRecord]) -> dict:
        """
        Build a dict of {normalized_course_id: CourseRecord} for passing courses.
        Also includes IP (in-progress) courses separately.
        """
        completed = {}
        in_progress = {}
        for rec in transcript:
            nid = self._normalize_id(rec.course_id)
            if rec.is_in_progress:
                in_progress[nid] = rec
            elif rec.is_passing:
                if nid not in completed:
                    completed[nid] = rec
        return completed, in_progress

    def _check_course(
        self, course_id: str, completed: dict, in_progress: dict, alternatives: list[str] = None
    ) -> RequirementStatus:
        """
        Check if a single course (or one of its alternatives) is satisfied.
        """
        courses_to_check = [course_id]
        if alternatives:
            courses_to_check.extend(alternatives)

        for cid in courses_to_check:
            nid = self._normalize_id(cid)
            if nid in completed:
                rec = completed[nid]
                return RequirementStatus(
                    label=cid,
                    status="Satisfied",
                    course_used=nid,
                    notes=f"Grade: {rec.grade} ({rec.credits} cr)",
                )
            elif nid in in_progress:
                return RequirementStatus(
                    label=cid,
                    status="In Progress",
                    course_used=nid,
                )

        return RequirementStatus(
            label=course_id,
            status="Not Met",
        )

    def _check_elective_block(
        self,
        label: str,
        required_credits: float,
        completed: dict,
        elective_config: dict,
    ) -> RequirementStatus:
        """
        Check if enough elective credits from a pool are completed.
        """
        dept = elective_config.get("dept")
        min_level = elective_config.get("min_level", 0)
        choose_from = elective_config.get("choose_from", [])

        earned = 0.0
        courses_counted = []

        for nid, rec in completed.items():
            # Match by dept prefix
            if dept:
                depts = [dept] if isinstance(dept, str) else dept
                prefix = nid.split(" ")[0] if " " in nid else ""
                if prefix not in depts:
                    continue
            # Match by explicit list
            if choose_from:
                if nid not in [self._normalize_id(c) for c in choose_from]:
                    continue
            # Match by level
            if min_level:
                try:
                    level = int(nid.split(" ")[1]) if " " in nid else 0
                    if level < min_level:
                        continue
                except (ValueError, IndexError):
                    continue
            earned += rec.credits
            courses_counted.append(nid)

        if earned >= required_credits:
            return RequirementStatus(
                label=label,
                status="Satisfied",
                notes=f"{earned:.0f}/{required_credits:.0f} cr ({', '.join(courses_counted[:4])})",
            )
        else:
            return RequirementStatus(
                label=label,
                status="Not Met",
                notes=f"{earned:.0f}/{required_credits:.0f} cr needed",
            )

    def audit(self, student: dict, transcript: list[CourseRecord]) -> NonFSBAuditResult:
        """
        Run degree audit for a non-FSB student.
        student: dict with 'id', 'name', 'major', 'catalog_year'
        transcript: list of CourseRecord
        """
        completed, in_progress = self._build_completed_set(transcript)
        req = self.requirements
        results: list[RequirementStatus] = []

        # ── Required individual courses ──────────────────────
        for course_id in req.get("required", []):
            results.append(self._check_course(course_id, completed, in_progress))

        # ── Foundation blocks ─────────────────────────────────
        for block_key in [
            "foundation",
            "core",
            "dept_core",
            "ministry_core",
            "required_science",
            "required_exsc",
        ]:
            for course_id in req.get(block_key, []):
                results.append(self._check_course(course_id, completed, in_progress))

        # ── Choose one from list ──────────────────────────────
        for key in req:
            if key.startswith("choose_one") or key == "choose_one":
                options = req[key]
                if isinstance(options, list):
                    satisfied = any(self._normalize_id(c) in completed for c in options)
                    in_prog = (
                        any(self._normalize_id(c) in in_progress for c in options)
                        if not satisfied
                        else False
                    )
                    status = "Satisfied" if satisfied else ("In Progress" if in_prog else "Not Met")
                    used = next(
                        (
                            self._normalize_id(c)
                            for c in options
                            if self._normalize_id(c) in completed
                        ),
                        None,
                    )
                    results.append(
                        RequirementStatus(
                            label=f"One of: {', '.join(options[:3])}{'...' if len(options)>3 else ''}",
                            status=status,
                            course_used=used,
                        )
                    )

        # ── Distribution groups (e.g. Political Science American Politics / International) ──
        dist_groups = req.get("dist_groups", [])
        for group in dist_groups:
            group_name = group.get("name", "Distribution Group")
            credits_needed = float(group.get("credits", 3))
            min_courses = int(group.get("min_courses", 1))
            choose_from = group.get("choose_from", [])
            # Count earned and in-progress credits/courses from the pool
            earned_credits = 0.0
            ip_credits = 0.0
            courses_earned = []
            courses_ip = []
            for c in choose_from:
                nid = self._normalize_id(c)
                if nid in completed:
                    earned_credits += completed[nid].credits
                    courses_earned.append(nid)
                elif nid in in_progress:
                    ip_credits += in_progress[nid].credits
                    courses_ip.append(nid)
            courses_met = len(courses_earned)
            courses_in_prog = len(courses_ip)
            if earned_credits >= credits_needed and courses_met >= min_courses:
                status = "Satisfied"
            elif (earned_credits + ip_credits) >= credits_needed or (courses_met + courses_in_prog) >= min_courses:
                status = "In Progress"
            else:
                status = "Not Met"
            used = courses_earned[0] if courses_earned else (courses_ip[0] if courses_ip else None)
            results.append(
                RequirementStatus(
                    label=f"{group_name} — {int(credits_needed)} cr, choose {min_courses} from: {', '.join(choose_from[:3])}{'...' if len(choose_from) > 3 else ''}",
                    status=status,
                    course_used=used,
                    notes=f"{earned_credits:.0f}/{credits_needed:.0f} cr earned"
                    + (f", {ip_credits:.0f} cr in progress" if ip_credits else ""),
                )
            )

        # ── Elective blocks ───────────────────────────────────
        for elective_key in [
            "elective_upper",
            "elective_upper_div",
            "elective",
            "math",
            "elective_chem",
            "elective_lit",
            "elective_writing",
        ]:
            elective_conf = req.get(elective_key)
            if elective_conf and isinstance(elective_conf, dict):
                credits_needed = elective_conf.get("credits", 0)
                if isinstance(credits_needed, str):
                    # Handle ranges like "3-4"; use minimum
                    try:
                        credits_needed = float(credits_needed.split("-")[0])
                    except ValueError:
                        credits_needed = 0
                if credits_needed:
                    results.append(
                        self._check_elective_block(
                            label=f"Elective: {credits_needed} cr",
                            required_credits=float(credits_needed),
                            completed=completed,
                            elective_config=elective_conf,
                        )
                    )

        # ── Applied music / ensembles (Music programs) ────────
        for music_key in [
            "applied",
            "applied_primary",
            "applied_voice",
            "applied_music",
            "major_ensemble",
            "ensembles",
        ]:
            music_conf = req.get(music_key)
            if music_conf and isinstance(music_conf, dict):
                credits_needed = music_conf.get("credits", 0)
                if isinstance(credits_needed, int) and credits_needed:
                    # Check for MUPF/ensemble courses
                    dept = "MUPF" if "applied" in music_key else "MUSC"
                    results.append(
                        self._check_elective_block(
                            label=f"{music_key.replace('_', ' ').title()}: {credits_needed} cr",
                            required_credits=float(credits_needed),
                            completed=completed,
                            elective_config={"dept": dept},
                        )
                    )

        # ── Concentrations: check at least one track satisfied ──
        concentrations = req.get("concentrations") or req.get("tracks")
        if concentrations and isinstance(concentrations, dict):
            track_results = []
            for track_name, track_req in concentrations.items():
                if isinstance(track_req, list):
                    satisfied_count = sum(
                        1 for c in track_req if self._normalize_id(c) in completed
                    )
                    track_results.append((track_name, satisfied_count, len(track_req)))

            if track_results:
                best = max(track_results, key=lambda x: x[1])
                status = (
                    "Satisfied"
                    if best[1] == best[2]
                    else ("In Progress" if best[1] > 0 else "Not Met")
                )
                results.append(
                    RequirementStatus(
                        label=f"Concentration/Track ({best[0]})",
                        status=status,
                        notes=f"{best[1]}/{best[2]} courses in best track",
                    )
                )

        # ── Calculate major GPA ───────────────────────────────
        major_credits = 0.0
        major_grade_points = 0.0
        for nid, rec in completed.items():
            prefix = nid.split(" ")[0] if " " in nid else ""
            # Rough major GPA: all courses with the major's primary dept prefix
            major_prefixes = self._get_major_prefixes()
            if prefix in major_prefixes:
                major_credits += rec.credits
                major_grade_points += rec.credits * rec.grade_points

        major_gpa = round(major_grade_points / major_credits, 3) if major_credits else 0.0

        # ── Outstanding ──────────────────────────────────────
        outstanding = [r.label for r in results if r.status == "Not Met"]

        result = NonFSBAuditResult(
            student_id=student.get("id", ""),
            name=student.get("name", ""),
            major=req.get("name", self.program_key),
            catalog_year=self.catalog_year,
            requirements=results,
            major_gpa=major_gpa,
            total_major_credits=major_credits,
            all_satisfied=len(outstanding) == 0,
            outstanding=outstanding,
        )
        return result

    def _get_major_prefixes(self) -> list[str]:
        """
        Return the primary dept course prefixes for this program.
        Used to compute major GPA.
        """
        prefix_map = {
            "biology": ["BIOL"],
            "biochemistry": ["BIOL", "CHEM"],
            "chemistry": ["CHEM"],
            "physics": ["PHYS"],
            "cs": ["CPSC"],
            "cybersecurity": ["CPSC", "POSC"],
            "data_science": ["CPSC", "MATH"],
            "math": ["MATH"],
            "communication": ["COMM"],
            "cinema_media_arts": ["COMM"],
            "journalism": ["COMM"],
            "public_relations": ["COMM"],
            "visual_communication": ["ARTS", "ARTH"],
            "literary_studies": ["ENGL"],
            "writing": ["ENGL"],
            "songwriting": ["ENGL", "MUBS"],
            "history": ["HIST"],
            "political_science": ["POSC"],
            "spanish": ["SPAN"],
            "music": ["MUSC", "MUPF", "MUED", "MUBS"],
            "musical_theatre": ["MUTR", "THEA"],
            "theatre": ["THEA"],
            "dance": ["DANC"],
            "christian_ministries": ["CMIN", "RLGN", "BIBL"],
            "exercise_science": ["EXSC", "PEHS", "PETE"],
            "sport_recreational": ["SPRL", "PETE"],
            "nursing": ["NURS"],
            "psychology": ["PSYC"],
            "public_health": ["PUBH"],
            "social_work": ["SOWK"],
            "criminal_justice": ["CRIM"],
            "family_science": ["SOCI"],
            "elementary_education": ["EDUC"],
            "electrical_engineering": ["ENGR"],
            "computer_engineering": ["ENGR"],
            "mechanical_engineering": ["ENGR"],
        }
        # Find matching key
        for k, prefixes in prefix_map.items():
            if k in self.program_key.lower():
                return prefixes
        # Default: use first word of program_key
        return [self.program_key.split("_")[0].upper()]


# ─────────────────────────────────────────────
# Convenience function (mirrors FSB engine interface)
# ─────────────────────────────────────────────


def run_non_fsb_audit(
    program_key: str,
    catalog_year: str,
    student: dict,
    transcript: list[CourseRecord],
) -> NonFSBAuditResult:
    """
    Top-level function to run a non-FSB audit.
    Drop-in replacement for the FSB audit_engine.run_audit().
    """
    engine = NonFSBAuditEngine(program_key=program_key, catalog_year=catalog_year)
    return engine.audit(student, transcript)


def get_all_available_programs(catalog_year: str = None) -> dict:
    """
    Return dict of all available programs, optionally filtered by catalog year.
    Format: {program_key: program_name}
    """
    results = {}
    for key in ALL_NON_FSB_PROGRAMS:
        if catalog_year:
            req = get_non_fsb_requirements(key, catalog_year)
            if req is not None:
                name = req.get("name", key) if isinstance(req, dict) else key
                results[key] = name
        else:
            results[key] = key
    return results
