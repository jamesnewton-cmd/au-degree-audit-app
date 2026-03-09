"""
Anderson University Degree Audit — FastAPI Route Handlers
Drop these routes into the existing main.py (or import as a router).

Endpoints:
  POST /audit              — Run an audit for any major/year
  GET  /majors/{year}      — List available majors for a catalog year
  GET  /minors/{year}      — List available minors for a catalog year
  GET  /catalog-years      — List all supported catalog years
  POST /audit/batch        — Batch audit from CSV data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from engines.audit_engine import (
    AuditEngine,
    AuditResult,
    CourseRecord,
    parse_courses_from_dict,
    run_audit_from_dict,
    MAJOR_DISPLAY_NAMES,
    VALID_CATALOG_YEARS,
)
from requirements.fsb_minors import FSB_MINORS

router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────

class CourseInput(BaseModel):
    code: str
    name: str = ""
    credits: float = 3.0
    grade: str = ""
    term: str = ""
    is_exception: bool = False
    is_transfer: bool = False


class AuditRequest(BaseModel):
    student_name: str = ""
    student_id: str = ""
    catalog_year: str           # e.g. "2022-23"
    major: str                  # Display name e.g. "Management" or key e.g. "management"
    minor: Optional[str] = None
    icc_exempt: bool = False
    courses: list[CourseInput]


class RequirementResultOut(BaseModel):
    label: str
    status: str
    satisfying_course: Optional[str] = None
    satisfying_courses: list = []
    credits_earned: float = 0
    credits_required: float = 0
    notes: str = ""


class AuditResultOut(BaseModel):
    student_name: str
    student_id: str
    catalog_year: str
    major: str
    overall_gpa: float
    major_gpa: float
    total_credits_completed: float
    liberal_arts: list
    business_core: list
    major_requirements: list
    minor_requirements: list
    action_plan: dict
    is_complete: bool
    summary: str


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def resolve_major_key(major_display: str, catalog_year: str) -> str:
    """Convert a display name or key to the internal major key."""
    # Try direct key first
    if major_display in MAJOR_DISPLAY_NAMES.get(catalog_year, {}):
        return MAJOR_DISPLAY_NAMES[catalog_year][major_display]
    # Try treating it as an already-resolved key
    from requirements.fsb_majors import FSB_MAJORS
    if major_display in FSB_MAJORS:
        return major_display
    raise HTTPException(
        status_code=400,
        detail=f"Major '{major_display}' not found for catalog year {catalog_year}. "
               f"Available: {list(MAJOR_DISPLAY_NAMES.get(catalog_year, {}).keys())}"
    )


def resolve_minor_key(minor_display: str | None) -> str | None:
    if not minor_display:
        return None
    # Normalize to snake_case key
    normalized = minor_display.lower().replace(" ", "_").replace("&", "and").replace("-", "_")
    if normalized in FSB_MINORS:
        return normalized
    # Try suffix search
    for key in FSB_MINORS:
        if normalized in key or key in normalized:
            return key
    return None  # Don't crash — just skip minor


def audit_result_to_dict(r: AuditResult) -> dict:
    """Serialize AuditResult to JSON-safe dict."""
    def req_to_dict(req):
        return {
            "label": req.label,
            "status": req.status,
            "satisfying_course": req.satisfying_course,
            "satisfying_courses": req.satisfying_courses,
            "credits_earned": req.credits_earned,
            "credits_required": req.credits_required,
            "notes": req.notes,
        }
    return {
        "student_name": r.student_name,
        "student_id": r.student_id,
        "catalog_year": r.catalog_year,
        "major": r.major,
        "overall_gpa": r.overall_gpa,
        "major_gpa": r.major_gpa,
        "total_credits_completed": r.total_credits_completed,
        "liberal_arts": [req_to_dict(req) for req in r.liberal_arts],
        "business_core": [req_to_dict(req) for req in r.business_core],
        "major_requirements": [req_to_dict(req) for req in r.major_requirements],
        "minor_requirements": [req_to_dict(req) for req in r.minor_requirements],
        "action_plan": r.action_plan,
        "is_complete": r.is_complete,
        "summary": r.summary,
    }


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.get("/catalog-years")
def get_catalog_years():
    """List all supported catalog years."""
    return {"catalog_years": VALID_CATALOG_YEARS}


@router.get("/majors/{catalog_year}")
def get_majors(catalog_year: str):
    """List available majors for a given catalog year."""
    if catalog_year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=404, detail=f"Unknown catalog year: {catalog_year}")
    return {
        "catalog_year": catalog_year,
        "majors": list(MAJOR_DISPLAY_NAMES.get(catalog_year, {}).keys()),
    }


@router.get("/minors/{catalog_year}")
def get_minors(catalog_year: str):
    """List available minors for a given catalog year."""
    if catalog_year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=404, detail=f"Unknown catalog year: {catalog_year}")
    available = []
    for key in FSB_MINORS:
        req = FSB_MINORS[key].get(catalog_year)
        if req is not None:
            name = req.get("name", key) if isinstance(req, dict) else key
            if isinstance(req, dict) and "same_as" in req:
                base = FSB_MINORS[key].get(req["same_as"], {})
                name = req.get("name", base.get("name", key))
            available.append({"key": key, "name": name})
    return {"catalog_year": catalog_year, "minors": available}


@router.post("/audit")
def run_audit(request: AuditRequest):
    """
    Run a degree audit for a single student.

    Body:
        student_name, student_id, catalog_year, major, minor (optional),
        icc_exempt (optional, 2025-26 only), courses: [{code, name, credits, grade, term}]
    """
    if request.catalog_year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid catalog year: {request.catalog_year}")

    major_key = resolve_major_key(request.major, request.catalog_year)
    minor_key = resolve_minor_key(request.minor)

    course_dicts = [c.dict() for c in request.courses]
    result = run_audit_from_dict(
        courses=course_dicts,
        catalog_year=request.catalog_year,
        major_key=major_key,
        minor_key=minor_key,
        icc_exempt=request.icc_exempt,
        student_name=request.student_name,
        student_id=request.student_id,
    )

    return audit_result_to_dict(result)


class BatchAuditRequest(BaseModel):
    catalog_year: str
    major: str
    minor: Optional[str] = None
    icc_exempt: bool = False
    students: list[dict]   # Each dict: {student_name, student_id, courses: [...]}


@router.post("/audit/batch")
def run_batch_audit(request: BatchAuditRequest):
    """
    Run audits for multiple students at once.
    All students share the same catalog_year and major.
    """
    if request.catalog_year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid catalog year: {request.catalog_year}")

    major_key = resolve_major_key(request.major, request.catalog_year)
    minor_key = resolve_minor_key(request.minor)

    engine = AuditEngine(
        catalog_year=request.catalog_year,
        major_key=major_key,
        minor_key=minor_key,
        icc_exempt=request.icc_exempt,
    )

    results = []
    for student in request.students:
        courses = parse_courses_from_dict(student.get("courses", []))
        result = engine.run_audit(
            courses,
            student_name=student.get("student_name", ""),
            student_id=student.get("student_id", ""),
        )
        results.append(audit_result_to_dict(result))

    return {
        "batch_size": len(results),
        "catalog_year": request.catalog_year,
        "major": request.major,
        "results": results,
    }


# ─────────────────────────────────────────────
# NON-FSB PROGRAMS INTEGRATION
# ─────────────────────────────────────────────

from engines.non_fsb_audit_engine import (
    run_non_fsb_audit,
    get_all_available_programs,
    CourseRecord as NonFSBCourseRecord,
)
from requirements.non_fsb_programs import (
    ALL_NON_FSB_PROGRAMS,
    list_programs_by_year,
)


class NonFSBAuditRequest(BaseModel):
    student_name: str = ""
    student_id: str = ""
    catalog_year: str
    program_key: str          # e.g. "biology_ba", "theatre", "nursing_bsn"
    courses: list[CourseInput]


class NonFSBAuditResultOut(BaseModel):
    student_id: str
    name: str
    major: str
    catalog_year: str
    requirements: list
    major_gpa: float
    total_major_credits: float
    all_satisfied: bool
    outstanding: list[str]


@router.post("/audit/non-fsb", response_model=NonFSBAuditResultOut)
async def run_non_fsb_audit_endpoint(request: NonFSBAuditRequest):
    """Run a degree audit for any non-FSB program."""
    from requirements.non_fsb_programs import program_exists_in_year

    if request.catalog_year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid catalog year: {request.catalog_year}")

    if not program_exists_in_year(request.program_key, request.catalog_year):
        raise HTTPException(
            status_code=404,
            detail=f"Program '{request.program_key}' not available in {request.catalog_year}"
        )

    transcript = [
        NonFSBCourseRecord(
            course_id=c.code,
            grade=c.grade,
            credits=c.credits,
            term=c.term,
        )
        for c in request.courses
    ]

    result = run_non_fsb_audit(
        program_key=request.program_key,
        catalog_year=request.catalog_year,
        student={"id": request.student_id, "name": request.student_name},
        transcript=transcript,
    )

    return NonFSBAuditResultOut(
        student_id=result.student_id,
        name=result.name,
        major=result.major,
        catalog_year=result.catalog_year,
        requirements=[
            {
                "label": r.label,
                "status": r.status,
                "course_used": r.course_used,
                "notes": r.notes,
            }
            for r in result.requirements
        ],
        major_gpa=result.major_gpa,
        total_major_credits=result.total_major_credits,
        all_satisfied=result.all_satisfied,
        outstanding=result.outstanding,
    )


@router.get("/programs/non-fsb/{year}")
async def list_non_fsb_programs(year: str):
    """List all non-FSB programs available for a given catalog year."""
    if year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid catalog year: {year}")

    programs = get_all_available_programs(catalog_year=year)
    return {
        "catalog_year": year,
        "count": len(programs),
        "programs": programs,
    }


@router.get("/programs/all/{year}")
async def list_all_programs(year: str):
    """List ALL programs (FSB + non-FSB) for a given catalog year."""
    if year not in VALID_CATALOG_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid catalog year: {year}")

    fsb = {k: v for k, v in MAJOR_DISPLAY_NAMES.items()}
    non_fsb = get_all_available_programs(catalog_year=year)

    return {
        "catalog_year": year,
        "fsb_programs": fsb,
        "non_fsb_programs": non_fsb,
        "total_programs": len(fsb) + len(non_fsb),
    }
