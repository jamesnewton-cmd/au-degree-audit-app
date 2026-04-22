"""
Standalone scheduling web app.

This app is intentionally separate from the graduation audit system.
It provides advisor/professor scheduling from Excel uploads only.
"""

from __future__ import annotations

import datetime
import os
import secrets
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from engines.scheduling import (
    build_schedule_workbook,
    generate_student_schedules,
    parse_class_sections_workbook,
    parse_student_requests_workbook,
)

ALLOWED_EMAIL_DOMAIN = os.environ.get("ALLOWED_EMAIL_DOMAIN", "anderson.edu").lower().strip()
AUTH_CODE_TTL_SECONDS = int(os.environ.get("AUTH_CODE_TTL_SECONDS", "600"))
AUTH_SESSION_TTL_SECONDS = int(os.environ.get("AUTH_SESSION_TTL_SECONDS", "43200"))
AUTH_CODE_RESEND_SECONDS = int(os.environ.get("AUTH_CODE_RESEND_SECONDS", "45"))
AUTH_CODE_MAX_ATTEMPTS = int(os.environ.get("AUTH_CODE_MAX_ATTEMPTS", "6"))
AUTH_STATIC_TEST_CODE = os.environ.get("AUTH_STATIC_TEST_CODE", "").strip()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER") or os.environ.get("GMAIL_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS") or os.environ.get("GMAIL_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)

app = FastAPI(title="AU Advisor Scheduling", docs_url="/docs", redoc_url=None)
bearer_security = HTTPBearer(auto_error=False)

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
    msg["Subject"] = "Anderson Advisor Scheduling Login Verification Code"
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = to_email
    msg.set_content(
        "Your advisor scheduling login verification code is:\n\n"
        f"{code}\n\n"
        f"This code expires in {AUTH_CODE_TTL_SECONDS // 60} minutes.\n"
        "If you did not request this code, you can ignore this message."
    )
    _smtp_send(msg)


def verify(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
):
    _cleanup_auth_state()
    token = ""
    if credentials and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    if not token:
        token = request.cookies.get("scheduling_session", "")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session = AUTH_SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if session["expires_at"] <= _now_utc():
        AUTH_SESSIONS.pop(token, None)
        raise HTTPException(status_code=401, detail="Session expired")
    return session["email"]


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
        key="scheduling_session",
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
    resp.delete_cookie("scheduling_session")
    return resp


@app.get("/", response_class=HTMLResponse)
def scheduling_page(user=Depends(verify)):
    return HTMLResponse(Path("templates/scheduling.html").read_text())


@app.post("/generate")
async def scheduling_generate(
    class_listings: UploadFile = File(...),
    student_requests: UploadFile = File(...),
    max_courses_per_student: int = Form(5),
    user: str = Depends(verify),
):
    del user
    if max_courses_per_student < 1:
        raise HTTPException(400, "Max courses per student must be at least 1.")

    class_bytes = await class_listings.read()
    student_bytes = await student_requests.read()
    if not class_bytes:
        raise HTTPException(400, "Class listing workbook is empty.")
    if not student_bytes:
        raise HTTPException(400, "Student request workbook is empty.")

    try:
        sections, class_warnings = parse_class_sections_workbook(class_bytes)
        students, request_warnings = parse_student_requests_workbook(student_bytes)
        result = generate_student_schedules(
            sections,
            students,
            max_courses_per_student=max_courses_per_student,
        )
        workbook_bytes = build_schedule_workbook(
            result,
            warnings=class_warnings + request_warnings,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Scheduling generation failed: {str(e)}")

    return Response(
        content=workbook_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="student_schedules.xlsx"',
            "X-Scheduling-Students": str(result["summary"]["students"]),
            "X-Scheduling-Assignments": str(result["summary"]["assignments"]),
            "X-Scheduling-Unscheduled": str(result["summary"]["unscheduled"]),
        },
    )


@app.get("/ping")
def ping():
    return {"ok": True, "app": "scheduling"}
