"""
Anderson University — Degree Audit Web App
Indy Collab, LLC

Unified engine: all majors (FSB and non-FSB) route through one /generate endpoint.
FSB majors use their dedicated audit() functions for business core + major rows.
Non-FSB majors use the dynamic scanner against non_fsb_programs.py definitions.
All majors share: parse_csv, apply_exceptions, build_la_rows_for_non_fsb, pdf_template.
"""

import os, io, csv, json, datetime, tempfile, importlib.util, smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import secrets

# ── CONFIG ────────────────────────────────────────────────────────────────────
LOG_FILE = Path("logs/audit_log.json")
ENGINES_DIR = Path("engines")
MAX_PULLS = int(os.environ.get("MAX_PULLS", 1000))
ALLOWED_EMAIL_DOMAIN = os.environ.get("ALLOWED_EMAIL_DOMAIN", "anderson.edu").lower().strip()

AUTH_CODE_TTL_SECONDS = int(os.environ.get("AUTH_CODE_TTL_SECONDS", "600"))
AUTH_SESSION_TTL_SECONDS = int(os.environ.get("AUTH_SESSION_TTL_SECONDS", "43200"))
AUTH_CODE_RESEND_SECONDS = int(os.environ.get("AUTH_CODE_RESEND_SECONDS", "45"))
AUTH_CODE_MAX_ATTEMPTS = int(os.environ.get("AUTH_CODE_MAX_ATTEMPTS", "6"))
# Test/development bypass: when set, OTP delivery email is skipped.
AUTH_STATIC_TEST_CODE = os.environ.get("AUTH_STATIC_TEST_CODE", "").strip()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
# Backward compatibility: previous deployments used GMAIL_USER/GMAIL_PASS.
SMTP_USER = os.environ.get("SMTP_USER") or os.environ.get("GMAIL_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS") or os.environ.get("GMAIL_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)

CATALOG_YEARS = ["2022-23", "2023-24", "2024-25", "2025-26"]

# ── PROGRAM ENGINE MAP (FSB majors only) ──────────────────────────────────────
# Non-FSB programs are defined in requirements/non_fsb_programs.py and are
# loaded dynamically by year. Keeping engine mapping separate avoids duplicated
# label/year logic in this file.
FSB_ENGINE_MAP = {
    "management": "management",
    "sport_marketing": "sport_marketing",
    "marketing": "fsb_engine",
    "accounting": "fsb_engine",
    "finance": "fsb_engine",
    "business_analytics": "fsb_engine",
    "engineering_management": "fsb_engine",
    "global_business": "fsb_engine",
    "music_entertainment_business": "fsb_engine",
    "business_integrative_leadership": "fsb_engine",
}


def _pretty_program_key(program_key: str) -> str:
    return program_key.replace("_", " ").title()


def get_fsb_program_labels_for_year(catalog_year: str) -> dict[str, str]:
    """Return {program_key: display_label} for FSB majors offered in a year."""
    from requirements.fsb_majors import FSB_MAJORS as FSB_MAJOR_CATALOG

    labels = {}
    for key in FSB_ENGINE_MAP:
        req = FSB_MAJOR_CATALOG.get(key, {}).get(catalog_year)
        if isinstance(req, dict):
            labels[key] = req.get("name", _pretty_program_key(key))
    return labels


def is_fsb_program_key(program_key: str, catalog_year: str) -> bool:
    """True when a key maps to an FSB major in the given catalog year."""
    return program_key in get_fsb_program_labels_for_year(catalog_year)


def program_bucket(program_key: str, catalog_year: str) -> str | None:
    """
    Resolve a program key to a year-valid bucket:
    - "FSB"
    - "NON_FSB"
    - None (unknown or unavailable in year)
    """
    if is_fsb_program_key(program_key, catalog_year):
        return "FSB"

    from requirements.non_fsb_programs import program_exists_in_year

    return "NON_FSB" if program_exists_in_year(program_key, catalog_year) else None


def resolve_program_label(program_key: str, catalog_year: str) -> str:
    """Resolve a stable display label for a valid program key/year."""
    if program_key in FSB_ENGINE_MAP:
        fsb_labels = get_fsb_program_labels_for_year(catalog_year)
        return fsb_labels.get(program_key, _pretty_program_key(program_key))

    from requirements.non_fsb_programs import get_non_fsb_requirements

    req = get_non_fsb_requirements(program_key, catalog_year) or {}
    if isinstance(req, dict):
        return req.get("name", _pretty_program_key(program_key))
    return _pretty_program_key(program_key)


def list_all_programs_for_year(catalog_year: str) -> list[dict]:
    """Return unified, year-valid program list with key/label/type."""
    programs = []
    fsb_labels = get_fsb_program_labels_for_year(catalog_year)
    for key, label in fsb_labels.items():
        programs.append({"key": key, "label": label, "type": "FSB"})

    from requirements.non_fsb_programs import ALL_NON_FSB_PROGRAMS

    for key in ALL_NON_FSB_PROGRAMS:
        if program_bucket(key, catalog_year) == "NON_FSB":
            programs.append(
                {"key": key, "label": resolve_program_label(key, catalog_year), "type": "non-FSB"}
            )
    return programs


# ── APP ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="AU Degree Audit", docs_url="/docs", redoc_url=None)
bearer_security = HTTPBearer(auto_error=False)

from engines.audit_routes import router


# ── AUTH ──────────────────────────────────────────────────────────────────────
AUTH_CODES: dict[str, dict[str, Any]] = {}
AUTH_SESSIONS: dict[str, dict[str, Any]] = {}


class AuthRequest(BaseModel):
    email: str


class AuthVerifyRequest(BaseModel):
    email: str
    code: str


def _now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _normalize_anderson_email(email: str) -> str:
    normalized = (email or "").strip().lower()
    if normalized.count("@") != 1:
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    if not normalized.endswith(f"@{ALLOWED_EMAIL_DOMAIN}"):
        raise HTTPException(
            status_code=403,
            detail=f"Access is restricted to @{ALLOWED_EMAIL_DOMAIN} email accounts.",
        )
    return normalized


def _cleanup_auth_state() -> None:
    now = _now_utc()
    for email, payload in list(AUTH_CODES.items()):
        if payload.get("expires_at") and payload["expires_at"] <= now:
            AUTH_CODES.pop(email, None)
    for token, payload in list(AUTH_SESSIONS.items()):
        if payload.get("expires_at") and payload["expires_at"] <= now:
            AUTH_SESSIONS.pop(token, None)


def _smtp_send(msg: EmailMessage) -> None:
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP credentials are not configured.")
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        return
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def _generate_auth_code() -> str:
    if AUTH_STATIC_TEST_CODE:
        return AUTH_STATIC_TEST_CODE
    return f"{secrets.randbelow(1_000_000):06d}"


def _send_login_code_email(to_email: str, code: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Anderson Degree Audit Login Verification Code"
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = to_email
    msg.set_content(
        "Your Anderson Degree Audit login verification code is:\n\n"
        f"{code}\n\n"
        f"This code expires in {AUTH_CODE_TTL_SECONDS // 60} minutes.\n"
        "If you did not request this code, you can ignore this message."
    )
    _smtp_send(msg)


def verify(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
):
    # Auth disabled — open access per registrar request
    return "open"


@app.post("/auth/request-code")
def auth_request_code(payload: AuthRequest):
    email = _normalize_anderson_email(payload.email)
    _cleanup_auth_state()
    now = _now_utc()
    existing = AUTH_CODES.get(email)
    if existing:
        delta = (now - existing["sent_at"]).total_seconds()
        if delta < AUTH_CODE_RESEND_SECONDS:
            return {
                "ok": True,
                "message": "Verification code recently sent.",
                "retry_after_seconds": int(AUTH_CODE_RESEND_SECONDS - delta),
            }
    code = _generate_auth_code()
    AUTH_CODES[email] = {
        "code": code,
        "sent_at": now,
        "expires_at": now + datetime.timedelta(seconds=AUTH_CODE_TTL_SECONDS),
        "attempts_left": AUTH_CODE_MAX_ATTEMPTS,
    }
    try:
        # In test mode we intentionally skip SMTP.
        if not AUTH_STATIC_TEST_CODE:
            _send_login_code_email(email, code)
    except Exception:
        AUTH_CODES.pop(email, None)
        raise HTTPException(status_code=500, detail="Unable to send verification code right now.")
    return {"ok": True, "message": "Verification code sent."}


@app.post("/auth/verify-code")
def auth_verify_code(payload: AuthVerifyRequest):
    email = _normalize_anderson_email(payload.email)
    _cleanup_auth_state()
    challenge = AUTH_CODES.get(email)
    if not challenge:
        raise HTTPException(status_code=401, detail="Invalid or expired verification code.")
    if challenge["expires_at"] <= _now_utc():
        AUTH_CODES.pop(email, None)
        raise HTTPException(status_code=401, detail="Verification code expired.")
    incoming = "".join(ch for ch in (payload.code or "") if ch.isdigit())
    if not secrets.compare_digest(incoming, challenge["code"]):
        challenge["attempts_left"] -= 1
        if challenge["attempts_left"] <= 0:
            AUTH_CODES.pop(email, None)
            raise HTTPException(status_code=429, detail="Too many failed attempts.")
        raise HTTPException(status_code=401, detail="Invalid verification code.")

    AUTH_CODES.pop(email, None)
    token = secrets.token_urlsafe(32)
    expires_at = _now_utc() + datetime.timedelta(seconds=AUTH_SESSION_TTL_SECONDS)
    AUTH_SESSIONS[token] = {"email": email, "expires_at": expires_at}
    resp = JSONResponse(
        {
        "access_token": token,
        "token_type": "bearer",
        "email": email,
        "expires_at": expires_at.isoformat(),
        }
    )
    resp.set_cookie(
        key="audit_session",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=AUTH_SESSION_TTL_SECONDS,
    )
    return resp


@app.get("/auth/me")
def auth_me(user: str = Depends(verify)):
    return {"email": user}


@app.post("/auth/logout")
def auth_logout(user: str = Depends(verify)):
    to_remove = [token for token, row in AUTH_SESSIONS.items() if row.get("email") == user]
    for token in to_remove:
        AUTH_SESSIONS.pop(token, None)
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("audit_session")
    return resp


def _normalize_recipient_email(email: str) -> str:
    return _normalize_anderson_email(email)


def _collect_delivery_recipients(advisor_email: str, student_email: str) -> list[str]:
    recipients: list[str] = []
    for raw in (advisor_email, student_email):
        value = (raw or "").strip()
        if not value:
            continue
        normalized = _normalize_recipient_email(value)
        if normalized not in recipients:
            recipients.append(normalized)
    return recipients


def send_audit_email(
    to_addresses: list[str],
    student_name: str,
    major_label: str,
    pdf_path: str,
    filename: str,
    sender_email: str,
):
    if not to_addresses:
        return
    msg = EmailMessage()
    msg["Subject"] = f"Degree Audit — {student_name} — {major_label}"
    msg["From"] = sender_email
    # Keep delivery/auth identity explicit when SMTP account differs.
    if SMTP_FROM and SMTP_FROM != sender_email:
        msg["Sender"] = SMTP_FROM
        msg["Reply-To"] = sender_email
    msg["To"] = ", ".join(to_addresses)
    msg.set_content(
        f"{sender_email} sent you a copy of the degree completion audit for "
        f"{student_name} ({major_label}).\n\n"
        "Please verify all requirements with your academic advisor.\n\n"
        "— Anderson University Degree Audit"
    )
    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=filename)
    _smtp_send(msg)


# ── LOGGING ───────────────────────────────────────────────────────────────────
def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return {"pulls": [], "total": 0}


def save_log(log):
    LOG_FILE.parent.mkdir(exist_ok=True)
    LOG_FILE.write_text(json.dumps(log, indent=2))


def record_pull(user, student, major, catalog):
    log = load_log()
    log["pulls"].append(
        {
            "ts": datetime.datetime.utcnow().isoformat(),
            "user": user,
            "student": student,
            "major": major,
            "catalog": catalog,
        }
    )
    log["total"] = len(log["pulls"])
    save_log(log)
    return log["total"]


# ── ENGINE LOADER ─────────────────────────────────────────────────────────────
def load_engine(engine_name: str):
    engine_file = ENGINES_DIR / f"{engine_name}.py"
    if not engine_file.exists():
        raise HTTPException(status_code=400, detail=f"Engine not found: {engine_name}")
    spec = importlib.util.spec_from_file_location("engine", engine_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── SHARED HELPERS ────────────────────────────────────────────────────────────
SKIP_KEYS = {
    "name",
    "total_credits",
    "delivery",
    "notes",
    "note",
    "teaching_fields",
    "department",
    "concentration_note",
    "special_rules",
    "same_as",
    "optional_cma",
    "concentrations",
    "tracks",
    "total_major_credits",
    "lead_courses_credits",
    "la_credits",
    "elective_credits",
    "min_level",
    "choose_one",
    "accreditation",
    "prerequisites",
    "dummy_2022_23",
    "dummy_elective",
    "required_old",
    "dept_dummy",
    "upper_div_psyc",
}


def _norm_code(c):
    return c.strip().upper().replace(" ", "_").replace("-", "_")


def _safe_credits(val, fallback=3):
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    if isinstance(val, str):
        try:
            return int(val.split("-")[0])
        except ValueError:
            return fallback
    return fallback


def _download_name_from_student(student_name: str) -> str:
    """
    Build download filename stem as FirstName_LastInitial.
    Falls back gracefully when parts are missing.
    """
    cleaned = "".join(c if c.isalnum() or c in " -_" else " " for c in (student_name or "")).strip()
    parts = [p for p in cleaned.replace("_", " ").split() if p]
    if not parts:
        return "Student_A"
    first = parts[0]
    last_initial = parts[-1][0] if len(parts) > 1 and parts[-1] else "A"
    safe_first = "".join(c for c in first if c.isalnum()) or "Student"
    safe_last_initial = "".join(c for c in last_initial if c.isalnum()) or "A"
    return f"{safe_first}_{safe_last_initial.upper()}"


def _status_of_c(c):
    if c is None:
        return "Not Satisfied"
    if c["status"] == "grade posted" and c["grade"].upper() not in ("", "W", "DRP", "NC"):
        return "Satisfied"
    if c["status"] == "current":
        return "Current"
    if c["status"] == "scheduled":
        return "Scheduled"
    return "Not Satisfied"


def _build_major_rows(prog_reqs, raw_courses, sm_mod, concentration=""):
    """
    Dynamically build major requirement rows from a program definition dict.
    Handles: list keys (required courses), dict keys with 'credits' (electives/choose blocks).
    """
    sm_best = sm_mod.best
    sm_norm = sm_mod.norm

    def _find_course(code_list):
        normalized = [sm_norm(c.replace(" ", "_").replace("-", "_")) for c in code_list]
        return sm_best(raw_courses, normalized)

    course_name_lookup = {}
    for _c in raw_courses:
        key = _c["raw"].upper().replace("-", " ")
        if _c.get("name") and _c["name"].strip():
            course_name_lookup[key] = _c["name"].strip()

    def _course_label(course_id, found_course=None):
        code_clean = course_id.strip().upper().replace("-", " ")
        if found_course and found_course.get("name"):
            return f"{course_id} {found_course['name']}"
        name = course_name_lookup.get(code_clean, "")
        return f"{course_id} {name}" if name else course_id

    _skip_keys = {
        "name",
        "total_credits",
        "delivery",
        "notes",
        "teaching_fields",
        "department",
        "concentration_note",
        "special_rules",
        "same_as",
        "optional_cma",
        "concentrations",
        "tracks",
        "total_major_credits",
        "lead_courses_credits",
        "la_credits",
        "elective_credits",
        "min_level",
        "choose_one",
        "accreditation",
    }

    rows = []
    used_required_codes = set()  # track codes already used by required rows

    # Pass 1: list-type keys → individual required course rows
    for req_key, req_val in prog_reqs.items():
        if req_key in _skip_keys:
            continue
        if isinstance(req_val, list) and req_val:
            for course_id in req_val:
                if not isinstance(course_id, str):
                    continue
                if "xxx" in course_id.lower() or course_id.upper().count("X") >= 3:
                    continue
                c = _find_course([course_id])
                rows.append(
                    {
                        "id": _norm_code(course_id),
                        "label": _course_label(course_id, c),
                        "status": _status_of_c(c),
                        "course": c,
                        "dcr": 3,
                        "note": "",
                    }
                )

    # Pass 2: dict-type keys with 'credits' → elective/choose blocks
    for ekey, edef in prog_reqs.items():
        if ekey in _skip_keys:
            continue
        if not isinstance(edef, (dict, int, float)):
            continue
        if isinstance(edef, dict) and "credits" not in edef:
            continue

        if isinstance(edef, dict):
            credits = _safe_credits(edef.get("credits", 3))
            dept = edef.get("dept", "")
            course = edef.get("course", "")
            choose_from = edef.get("choose_from", edef.get("options", edef.get("courses", [])))
            label = edef.get("label", "")
            if not label:
                if course:
                    label = f"{course} ({credits} cr)"
                elif dept:
                    dept_str = "/".join(dept) if isinstance(dept, list) else dept
                    label = f"{dept_str} elective — {credits} hrs"
                elif choose_from:
                    preview = ", ".join(str(x) for x in choose_from[:3])
                    suffix = "..." if len(choose_from) > 3 else ""
                    label = f"Choose from: {preview}{suffix} ({credits} cr)"
                else:
                    label = f"{ekey.replace('_',' ').title()} ({credits} cr)"
            # Skip notes-only blocks with nothing matchable
            if not course and not dept and not choose_from:
                continue
            opts = [course] if course else (choose_from if isinstance(choose_from, list) else [])

            # For multi-course choose blocks (e.g. credits=6 = 2 x 3cr courses),
            # generate one row per required course so each shows separately
            course_size = 3  # most AU courses are 3 credits
            num_needed = max(1, round(credits / course_size)) if not course else 1

            if num_needed > 1 and opts:
                # Find up to num_needed distinct matching courses
                sm_norm = sm_mod.norm
                used_codes = set()
                for slot in range(num_needed):
                    remaining_opts = [
                        o
                        for o in opts
                        if sm_norm(o.replace(" ", "_").replace("-", "_")) not in used_codes
                    ]
                    c = _find_course(remaining_opts) if remaining_opts else None
                    if c:
                        used_codes.add(c["code"])
                    slot_label = f"{label} ({slot+1} of {num_needed})" if c or slot == 0 else label
                    rows.append(
                        {
                            "id": _norm_code(f"{ekey}_{slot+1}"),
                            "label": slot_label,
                            "status": _status_of_c(c),
                            "course": c,
                            "dcr": course_size,
                            "note": "",
                        }
                    )
            else:
                c = _find_course(opts) if opts else None
                if c is None and dept:
                    dept_list = [dept] if isinstance(dept, str) else dept
                    dept_prefixes = tuple(d.upper() for d in dept_list)
                    c = next(
                        (
                            x
                            for x in raw_courses
                            if x["raw"].upper().startswith(dept_prefixes)
                            and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")
                        ),
                        None,
                    )
                rows.append(
                    {
                        "id": _norm_code(ekey),
                        "label": label,
                        "status": _status_of_c(c),
                        "course": c,
                        "dcr": credits,
                        "note": "",
                    }
                )
                if c:
                    used_required_codes.add(c["code"])
        elif isinstance(edef, (int, float)):
            rows.append(
                {
                    "id": _norm_code(ekey),
                    "label": f"{ekey.replace('_',' ').title()} ({int(edef)} hrs)",
                    "status": "Not Satisfied",
                    "course": None,
                    "dcr": int(edef),
                    "note": "",
                }
            )

    # -- Pass 3: Distribution groups (e.g. Political Science American Politics / International) --
    # dist_groups is a list of dicts: {name, credits, min_courses, choose_from:[...]}
    # Previously these were silently ignored because they are a list-of-dicts,
    # which falls through both Pass 1 (list of strings) and Pass 2 (dict with 'credits').
    dist_groups = prog_reqs.get("dist_groups", [])
    for group in dist_groups:
        group_name = group.get("name", "Distribution Group")
        credits_needed = float(group.get("credits", 3))
        min_courses = int(group.get("min_courses", 1))
        choose_from = group.get("choose_from", [])
        earned_credits = 0.0
        ip_credits = 0.0
        first_earned_course = None
        first_ip_course = None
        courses_earned_count = 0
        courses_ip_count = 0
        sm_norm = sm_mod.norm
        for c_id in choose_from:
            c_norm = sm_norm(c_id.replace(" ", "_").replace("-", "_"))
            matched = next((x for x in raw_courses if x["code"] == c_norm), None)
            if matched:
                st = _status_of_c(matched)
                if st == "Satisfied":
                    earned_credits += matched.get("cr", 3)
                    courses_earned_count += 1
                    if first_earned_course is None:
                        first_earned_course = matched
                elif st in ("Current", "Scheduled"):
                    ip_credits += matched.get("cr", 3)
                    courses_ip_count += 1
                    if first_ip_course is None:
                        first_ip_course = matched
        if earned_credits >= credits_needed and courses_earned_count >= min_courses:
            grp_status = "Satisfied"
            display_course = first_earned_course
        elif (earned_credits + ip_credits) >= credits_needed or (courses_earned_count + courses_ip_count) >= min_courses:
            grp_status = "Current"
            display_course = first_ip_course or first_earned_course
        else:
            grp_status = "Not Satisfied"
            display_course = first_earned_course or first_ip_course
        preview = ", ".join(choose_from[:3]) + ("..." if len(choose_from) > 3 else "")
        rows.append(
            {
                "id": "DIST-" + str(sum(1 for r in rows if str(r.get("id","")).startswith("DIST-")) + 1).zfill(2),
                "label": (
                    group_name
                    + " -- "
                    + str(int(credits_needed))
                    + " cr (choose "
                    + str(min_courses)
                    + ": "
                    + preview
                    + ")"
                ),
                "status": grp_status,
                "course": display_course,
                "dcr": credits_needed,
                "note": (
                    str(int(earned_credits))
                    + "/"
                    + str(int(credits_needed))
                    + " cr earned"
                    + (", " + str(int(ip_credits)) + " cr in progress" if ip_credits else "")
                ),
            }
        )

    # -- Pass 4: choose_one groups (cross-listed / either-or courses) --
    # Each entry: {name: str, choose_from: [course_id, ...]}
    # Produces one row satisfied if ANY listed course is on the transcript.
    choose_one_groups = prog_reqs.get("choose_one", [])
    for group in choose_one_groups:
        group_name = group.get("name", "Choose one")
        choose_from = group.get("choose_from", [])
        if not choose_from:
            continue
        c = _find_course(choose_from)
        rows.append({
            "id": _norm_code(group_name),
            "label": " or ".join(choose_from) + " (" + group_name + ")",
            "status": _status_of_c(c),
            "course": c,
            "dcr": 3,
            "note": "",
        })

    # Apply concentration courses if one was selected
    if concentration and isinstance(prog_reqs.get("concentrations"), dict):
        conc_data = prog_reqs["concentrations"].get(concentration)
        if conc_data and isinstance(conc_data, dict):
            conc_rows = []

            def _process_conc_block(ckey, cval, prefix=""):
                """Recursively process a concentration block into audit rows."""
                label_prefix = (
                    f"[{concentration}]" if not prefix else f"[{concentration} — {prefix}]"
                )
                if isinstance(cval, list):
                    for course_id in cval:
                        if not isinstance(course_id, str):
                            continue
                        c = _find_course([course_id])
                        conc_rows.append(
                            {
                                "id": _norm_code(f"conc_{course_id}"),
                                "label": f"{label_prefix} {_course_label(course_id, c)}",
                                "status": _status_of_c(c),
                                "course": c,
                                "dcr": 3,
                                "note": "",
                            }
                        )
                elif isinstance(cval, dict):
                    # Has 'required' list and/or elective sub-blocks
                    if "required" in cval:
                        for course_id in cval["required"]:
                            if not isinstance(course_id, str):
                                continue
                            c = _find_course([course_id])
                            conc_rows.append(
                                {
                                    "id": _norm_code(f"conc_{course_id}"),
                                    "label": f"{label_prefix} {_course_label(course_id, c)}",
                                    "status": _status_of_c(c),
                                    "course": c,
                                    "dcr": 3,
                                    "note": "",
                                }
                            )
                    # Process elective/choose sub-blocks
                    for sub_key, sub_val in cval.items():
                        if sub_key in ("required", "notes", "name"):
                            continue
                        if not isinstance(sub_val, dict) or "credits" not in sub_val:
                            continue
                        credits = _safe_credits(sub_val.get("credits", 3))
                        dept = sub_val.get("dept", "")
                        course = sub_val.get("course", "")
                        choose_from = sub_val.get("choose_from", [])
                        note_txt = sub_val.get("notes", sub_key.replace("_", " ").title())
                        label = f"{label_prefix} {note_txt} ({credits} cr)"
                        if not course and not dept and not choose_from:
                            continue
                        opts = (
                            [course]
                            if course
                            else (choose_from if isinstance(choose_from, list) else [])
                        )
                        # For multi-course blocks find multiple matches
                        course_size = 3
                        num_needed = max(1, round(credits / course_size)) if not course else 1
                        if num_needed > 1 and opts:
                            sm_norm = sm_mod.norm
                            used = set()
                            for slot in range(num_needed):
                                remaining = [
                                    o
                                    for o in opts
                                    if sm_norm(o.replace(" ", "_").replace("-", "_")) not in used
                                ]
                                c = _find_course(remaining) if remaining else None
                                if c is None and dept:
                                    dept_list = [dept] if isinstance(dept, str) else dept
                                    dept_pfx = tuple(d.upper() for d in dept_list)
                                    c = next(
                                        (
                                            x
                                            for x in raw_courses
                                            if x["raw"].upper().startswith(dept_pfx)
                                            and x["code"] not in used
                                            and x["code"] not in used_required_codes
                                            and _status_of_c(x)
                                            in ("Satisfied", "Current", "Scheduled")
                                        ),
                                        None,
                                    )
                                if c:
                                    used.add(c["code"])
                                slot_lbl = (
                                    f"{label} ({slot+1} of {num_needed})"
                                    if num_needed > 1
                                    else label
                                )
                                conc_rows.append(
                                    {
                                        "id": _norm_code(f"conc_{sub_key}_{slot+1}"),
                                        "label": slot_lbl,
                                        "status": _status_of_c(c),
                                        "course": c,
                                        "dcr": course_size,
                                        "note": "",
                                    }
                                )
                        else:
                            c = _find_course(opts) if opts else None
                            if c is None and dept:
                                dept_list = [dept] if isinstance(dept, str) else dept
                                dept_pfx = tuple(d.upper() for d in dept_list)
                                c = next(
                                    (
                                        x
                                        for x in raw_courses
                                        if x["raw"].upper().startswith(dept_pfx)
                                        and x["code"] not in used_required_codes
                                        and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")
                                    ),
                                    None,
                                )
                            conc_rows.append(
                                {
                                    "id": _norm_code(f"conc_{sub_key}"),
                                    "label": label,
                                    "status": _status_of_c(c),
                                    "course": c,
                                    "dcr": credits,
                                    "note": "",
                                }
                            )

            for ckey, cval in conc_data.items():
                if ckey in SKIP_KEYS:
                    continue
                _process_conc_block(ckey, cval)

            rows.extend(conc_rows)

    # Apply MAP exceptions to major rows
    # MAP entries targeting a specific course code inject a satisfied clone
    for c in raw_courses:
        area = c.get("__map_area__")
        if not area:
            continue
        taken_code = c.get("__map_taken_code__", c["code"])
        # Check if any existing row has an id matching the area (normalized)
        area_norm = area.strip().upper().replace("-", "_").replace(" ", "_")
        matched = False
        for row in rows:
            if row["id"] == area_norm:
                # Override this row with the mapped course
                sm_norm = sm_mod.norm
                taken = next((x for x in raw_courses if x["code"] == sm_norm(taken_code)), None)
                if taken:
                    row["course"] = taken
                    row["status"] = _status_of_c(taken)
                matched = True
                break
        if not matched:
            # No existing row for this area — add a new one
            sm_norm = sm_mod.norm
            taken = next((x for x in raw_courses if x["code"] == sm_norm(taken_code)), None)
            if taken:
                rows.append(
                    {
                        "id": area_norm,
                        "label": f"{taken.get('name', taken_code)} (mapped to {area})",
                        "status": _status_of_c(taken),
                        "course": taken,
                        "dcr": taken.get("cr", 3),
                        "note": f"Advisor exception: mapped to {area}",
                    }
                )

    return rows


def _compute_gpa(raw_courses, major_codes_set):
    """Compute overall and major GPA from raw_courses."""
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
    op = oh = mp = mh = qp = 0.0
    earned = ip_hrs = 0
    seen = set()
    for c in raw_courses:
        g = c["grade"].upper()
        if g in ("W", "DRP") or c["status"] == "dropped":
            continue
        if c["status"] == "current":
            ip_hrs += c["cr"]
            continue
        if c["status"] != "grade posted":
            continue
        earned += c["cr"]
        if g in ("T", "CR", "NC", ""):
            continue
        gp = GP.get(g)
        if gp is None:
            continue
        cr = c["cr"]
        if c["code"] not in seen:
            op += gp * cr
            oh += cr
            qp += gp * cr
            seen.add(c["code"])
        if c["code"] in major_codes_set or c["raw"].upper().replace("-", "_") in major_codes_set:
            mp += gp * cr
            mh += cr
    return (
        round(op / oh, 2) if oh else 0.0,
        round(mp / mh, 2) if mh else 0.0,
        int(oh),
        earned,
        ip_hrs,
        round(qp, 1),
        earned + ip_hrs,
    )


# ── SINGLE UNIFIED GENERATE ENDPOINT ─────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return HTMLResponse(open("templates/index.html").read())


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(user=Depends(verify)):
    log = load_log()
    html = open("templates/dashboard.html").read()
    pulls_remaining = MAX_PULLS - log["total"]
    recent = log["pulls"][-10:][::-1]
    rows = "".join(
        f'<tr><td>{p["ts"][:16].replace("T"," ")}</td>'
        f'<td>{p.get("student","—")}</td>'
        f'<td>{p.get("major","—")}</td>'
        f'<td>{p.get("catalog","—")}</td></tr>'
        for p in recent
    )
    html = html.replace("{{TOTAL}}", str(log["total"]))
    html = html.replace("{{REMAINING}}", str(max(0, pulls_remaining)))
    html = html.replace("{{MAX}}", str(MAX_PULLS))
    html = html.replace("{{ROWS}}", rows or "<tr><td colspan='4'>No audits yet</td></tr>")
    pct = min(100, round(log["total"] / MAX_PULLS * 100))
    html = html.replace("{{PCT}}", str(pct))
    return HTMLResponse(html)


@app.post("/generate")
async def generate(
    student_name: str = Form(...),
    major: str = Form(...),
    catalog_year: str = Form(...),
    transcript: UploadFile = File(...),
    exceptions: str = Form(""),
    advisor_notes: str = Form(""),
    concentration: str = Form(""),
    concentration2: str = Form(""),
    concentration3: str = Form(""),
    minor1: str = Form(""),
    minor2: str = Form(""),
    minor3: str = Form(""),
    major2: str = Form(""),
    major3: str = Form(""),
    advisor_email: str = Form(""),
    student_email: str = Form(""),
    user: str = Depends(verify),
):
    if catalog_year not in CATALOG_YEARS:
        raise HTTPException(400, "Invalid catalog year")

    log = load_log()
    if log["total"] >= MAX_PULLS:
        raise HTTPException(429, "Annual pull limit reached. Contact Indy Collab to renew.")

    csv_bytes = await transcript.read()
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="wb") as tmp_in:
        tmp_in.write(csv_bytes)
        tmp_csv = tmp_in.name

    download_stem = _download_name_from_student(student_name)
    tmp_pdf = tempfile.mktemp(suffix=".pdf")

    try:
        sm_mod = load_engine("sport_marketing")
        raw_courses = sm_mod.parse_csv(tmp_csv)

        if exceptions.strip():
            raw_courses = sm_mod.apply_exceptions(raw_courses, exceptions)

        bucket = program_bucket(major, catalog_year)
        if bucket is None:
            raise HTTPException(400, f"Unknown or unavailable program for {catalog_year}: {major}")
        is_fsb = bucket == "FSB"

        if is_fsb:
            engine_name = FSB_ENGINE_MAP[major]
            mod = load_engine(engine_name)

            if hasattr(mod, "MAJOR_KEY"):
                mod.MAJOR_KEY = major
                mod.CATALOG_YEAR = catalog_year

            try:
                res = mod.audit(raw_courses, minor_key=minor1 or None)
            except TypeError:
                res = mod.audit(raw_courses)

            res["catalog_year"] = catalog_year
            res["advisor_notes"] = advisor_notes
            major_label = resolve_program_label(major, catalog_year)
            res["major_section_label"] = f"{major_label} Major — {catalog_year}"
            res["major_subsections"] = [(f"{major_label} Required Courses", res.get("mr", []))]
            res["eligible_to_walk"] = sm_mod.eligible_to_walk(res)

        else:
            from requirements.non_fsb_programs import (
                get_non_fsb_requirements,
                ALL_NON_FSB_PROGRAMS,
            )

            if major not in ALL_NON_FSB_PROGRAMS:
                raise HTTPException(400, f"Unknown major: {major}")

            prog_reqs = get_non_fsb_requirements(major, catalog_year) or {}
            prog_name = (
                prog_reqs.get("name", major.replace("_", " ").title())
                if isinstance(prog_reqs, dict)
                else major.replace("_", " ").title()
            )
            major_label = prog_name

            # Build major requirement rows
            mr_rows = _build_major_rows(
                prog_reqs,
                raw_courses,
                sm_mod,
                concentration=concentration,
            )

            # Build minor rows if provided
            minor_rows = None
            if minor1:
                minor_reqs = get_non_fsb_requirements(minor1, catalog_year) or {}
                if minor_reqs:
                    minor_rows = _build_major_rows(minor_reqs, raw_courses, sm_mod)

            # Major codes set for GPA calculation
            _skip_gpa = {
                "name",
                "total_credits",
                "delivery",
                "notes",
                "teaching_fields",
                "department",
                "same_as",
                "concentrations",
                "tracks",
                "accreditation",
                "total_major_credits",
                "la_credits",
                "elective_credits",
                "min_level",
            }
            major_codes_set = set()
            for _k, _v in prog_reqs.items():
                if _k in _skip_gpa:
                    continue
                if isinstance(_v, list):
                    for _cid in _v:
                        if isinstance(_cid, str) and "xxx" not in _cid.lower():
                            major_codes_set.add(_norm_code(_cid))

            gpa_o, gpa_m, gpa_hrs, earned, ip_hrs, qp, proj = _compute_gpa(
                raw_courses, major_codes_set
            )

            # LA rows
            la_rows = sm_mod.build_la_rows_for_non_fsb(raw_courses, catalog_year, major_key=major)

            # Additional non-FSB majors
            additional_major_sections = []
            for extra_key in [major2, major3]:
                if not extra_key:
                    continue

                # Could be FSB or non-FSB
                extra_bucket = program_bucket(extra_key, catalog_year)
                if extra_bucket == "FSB":
                    try:
                        extra_mod = load_engine(FSB_ENGINE_MAP[extra_key])
                        if hasattr(extra_mod, "MAJOR_KEY"):
                            extra_mod.MAJOR_KEY = extra_key
                            extra_mod.CATALOG_YEAR = catalog_year
                        try:
                            extra_res = extra_mod.audit(raw_courses, minor_key=None)
                        except TypeError:
                            extra_res = extra_mod.audit(raw_courses)
                        extra_rows = []
                        for r in extra_res.get("bc", []) + extra_res.get("mr", []):
                            r2 = dict(r)
                            r2.setdefault("note", "")
                            extra_rows.append(r2)
                        if extra_rows:
                            additional_major_sections.append(
                                (resolve_program_label(extra_key, catalog_year), extra_rows)
                            )
                    except Exception:
                        pass

                elif extra_bucket == "NON_FSB":
                    try:
                        extra_reqs = get_non_fsb_requirements(extra_key, catalog_year) or {}
                        extra_name = extra_reqs.get("name", extra_key.replace("_", " ").title())
                        extra_rows = _build_major_rows(extra_reqs, raw_courses, sm_mod)
                        if extra_rows:
                            additional_major_sections.append((extra_name, extra_rows))
                    except Exception:
                        pass

            res = {
                "catalog_year": catalog_year,
                "current_term_label": "2025-26",
                "gpa_o": gpa_o,
                "gpa_m": gpa_m,
                "earned": earned,
                "ip_hrs": ip_hrs,
                "proj": proj,
                "gpa_hrs": gpa_hrs,
                "qp": qp,
                "la": la_rows,
                "bc": [],
                "mr": mr_rows,
                "elecs": [],
                "elecs_ip": [],
                "ehrs": 0,
                "ehrs_ip": 0,
                "elec_required_hrs": 0,
                "courses": raw_courses,
                "minor_rows": minor_rows,
                "minor_key": minor1 or None,
                "major_section_label": f"{major_label} Major — {catalog_year}",
                "major_subsections": [(f"{major_label} Required Courses", mr_rows)],
                "notes_row_text": "",
                "elec_opts": [],
                "advisor_notes": advisor_notes,
                "additional_major_sections": additional_major_sections,
            }
            res["eligible_to_walk"] = sm_mod.eligible_to_walk(res)

        for extra_minor_key in [minor2, minor3]:
            if extra_minor_key:
                res.setdefault("extra_minor_keys", []).append(extra_minor_key)

        # ── Build combined label for multi-major PDFs ─────────────────────────
        def _label(key):
            return resolve_program_label(key, catalog_year)

        all_labels = [major_label] + [_label(k) for k in [major2, major3] if k]
        combined_label = " / ".join(all_labels)

        # ── Generate PDF ──────────────────────────────────────────────────────
        sm_mod.build(res, student_name, combined_label, tmp_pdf, exceptions=exceptions)

        total = record_pull(user, student_name, major_label, catalog_year)
        filename = f"{download_stem}_Audit.pdf"

        recipients = _collect_delivery_recipients(advisor_email, student_email)
        if recipients:
            try:
                send_audit_email(
                    recipients,
                    student_name,
                    major_label,
                    tmp_pdf,
                    filename,
                    sender_email=advisor_email or SMTP_FROM or "audit@anderson.edu",
                )
            except Exception as email_err:
                print(f"Email send failed: {email_err}")

        return FileResponse(
            tmp_pdf,
            media_type="application/pdf",
            filename=filename,
            headers={"X-Pulls-Used": str(total), "X-Pulls-Remaining": str(MAX_PULLS - total)},
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Audit generation failed: {str(e)}")
    finally:
        if os.path.exists(tmp_csv):
            os.unlink(tmp_csv)


# ── LEGACY REDIRECT: keep /generate/non-fsb working during transition ─────────
@app.post("/generate/non-fsb")
async def generate_non_fsb_legacy(
    student_name: str = Form(...),
    major: str = Form(...),
    catalog_year: str = Form(...),
    transcript: UploadFile = File(...),
    exceptions: str = Form(""),
    advisor_notes: str = Form(""),
    concentration: str = Form(""),
    concentration2: str = Form(""),
    concentration3: str = Form(""),
    minor1: str = Form(""),
    minor2: str = Form(""),
    minor3: str = Form(""),
    major2: str = Form(""),
    major3: str = Form(""),
    advisor_email: str = Form(""),
    student_email: str = Form(""),
    user: str = Depends(verify),
):
    """Legacy endpoint — redirects to unified /generate."""
    # Re-read the transcript since we already consumed it
    transcript_bytes = await transcript.read()

    # Create a fake UploadFile-like object
    from fastapi import UploadFile as FUF
    import io

    fake_file = FUF(filename=transcript.filename, file=io.BytesIO(transcript_bytes))

    return await generate(
        student_name=student_name,
        major=major,
        catalog_year=catalog_year,
        transcript=fake_file,
        exceptions=exceptions,
        advisor_notes=advisor_notes,
        minor1=minor1,
        minor2=minor2,
        minor3=minor3,
        major2=major2,
        major3=major3,
        advisor_email=advisor_email,
        student_email=student_email,
        user=user,
    )


# ── STATUS / UTILITY ENDPOINTS ────────────────────────────────────────────────
@app.get("/ping")
def ping():
    return {"ok": True}


@app.get("/status")
def status(user: str = Depends(verify)):
    log = load_log()
    all_majors = []
    for year in CATALOG_YEARS:
        all_majors.extend(get_fsb_program_labels_for_year(year).values())
        from requirements.non_fsb_programs import list_programs_by_year

        for key in list_programs_by_year(year):
            all_majors.append(resolve_program_label(key, year))
    # Keep status payload compact and deterministic.
    all_majors = sorted(set(all_majors))
    return {
        "total_pulls": log["total"],
        "remaining_pulls": max(0, MAX_PULLS - log["total"]),
        "max_pulls": MAX_PULLS,
        "majors_available": all_majors,
        "catalog_years": CATALOG_YEARS,
    }


@app.get("/catalog-years")
def catalog_years(user: str = Depends(verify)):
    return {"catalog_years": CATALOG_YEARS}


@app.get("/majors/{year}")
def majors_for_year(year: str, user: str = Depends(verify)):
    from requirements.non_fsb_programs import list_programs_by_year

    if year not in CATALOG_YEARS:
        raise HTTPException(400, "Invalid catalog year")

    fsb_labels = get_fsb_program_labels_for_year(year)
    fsb = [{"key": k, "label": label, "type": "FSB"} for k, label in fsb_labels.items()]

    non_fsb = []
    for k in list_programs_by_year(year):
        # Keep FSB/non-FSB partitions disjoint in UI payloads.
        if is_fsb_program_key(k, year):
            continue
        non_fsb.append({"key": k, "label": resolve_program_label(k, year), "type": "non-FSB"})
    return {"year": year, "majors": fsb + non_fsb}


@app.get("/programs/all/{year}")
def programs_all(year: str, user: str = Depends(verify)):
    from requirements.non_fsb_programs import list_programs_by_year

    if year not in CATALOG_YEARS:
        raise HTTPException(400, "Invalid catalog year")

    fsb_for_year = {label: key for key, label in get_fsb_program_labels_for_year(year).items()}
    non_fsb = {}
    for key in list_programs_by_year(year):
        # Keep FSB/non-FSB partitions disjoint in UI payloads.
        if is_fsb_program_key(key, year):
            continue
        non_fsb[key] = resolve_program_label(key, year)

    return {
        "catalog_year": year,
        "fsb_programs": {year: fsb_for_year},
        "non_fsb_programs": non_fsb,
        "total_programs": len(fsb_for_year) + len(non_fsb),
    }


# Keep API router endpoints protected and mounted after web routes so
# overlapping paths in this file take precedence.
app.include_router(router, dependencies=[Depends(verify)])
