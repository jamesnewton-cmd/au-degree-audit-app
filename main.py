"""
Anderson University — Degree Audit Web App
Indy Collab, LLC
"""

import os, io, csv, json, hashlib, datetime, tempfile, importlib.util, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# ── CONFIG ────────────────────────────────────────────────────────────────────
APP_PASSWORD = os.environ.get("AUDIT_PASSWORD", "ravens2025")   # change in prod
LOG_FILE     = Path("logs/audit_log.json")
ENGINES_DIR  = Path("engines")
MAX_PULLS    = int(os.environ.get("MAX_PULLS", 1000))
GMAIL_USER   = os.environ.get("GMAIL_USER", "")
GMAIL_PASS   = os.environ.get("GMAIL_PASS", "")  # App password

MAJORS = {
    "management":     {"label": "Management",     "engine": "management"},
    "sport_marketing": {"label": "Sport Marketing", "engine": "sport_marketing"},
}

CATALOG_YEARS = ["2022-23", "2023-24", "2024-25", "2025-26"]

# ── APP ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="AU Degree Audit", docs_url="/docs", redoc_url=None)
security = HTTPBasic()

# ── ROUTER (all majors, minors, liberal arts) ─────────────────────────────────
from engines.audit_routes import router
app.include_router(router)

# ── AUTH ──────────────────────────────────────────────────────────────────────
def verify(credentials: HTTPBasicCredentials = Depends(security)):
    ok = secrets.compare_digest(credentials.password.encode(), APP_PASSWORD.encode())
    if not ok:
        raise HTTPException(status_code=401, detail="Unauthorized",
                            headers={"WWW-Authenticate": "Basic"})
    return credentials.username

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
    log["pulls"].append({
        "ts":      datetime.datetime.utcnow().isoformat(),
        "user":    user,
        "student": student,
        "major":   major,
        "catalog": catalog,
    })
    log["total"] = len(log["pulls"])
    save_log(log)
    return log["total"]

# ── ENGINE LOADER ─────────────────────────────────────────────────────────────
def load_engine(major_key: str):
    engine_file = ENGINES_DIR / f"{MAJORS[major_key]['engine']}.py"
    if not engine_file.exists():
        raise HTTPException(status_code=400, detail=f"Engine not found for {major_key}")
    spec = importlib.util.spec_from_file_location("engine", engine_file)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return HTMLResponse(open("templates/index.html").read())

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(user=Depends(verify)):
    log  = load_log()
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
    student_name:   str = Form(...),
    major:          str = Form(...),
    catalog_year:   str = Form(...),
    transcript:     UploadFile = File(...),
    advisor_notes:  str = Form(""),
    waiver_notes:   str = Form(""),
):
    if major not in MAJORS:
        raise HTTPException(400, "Invalid major")
    if catalog_year not in CATALOG_YEARS:
        raise HTTPException(400, "Invalid catalog year")

    log = load_log()
    if log["total"] >= MAX_PULLS:
        raise HTTPException(429, "Annual pull limit reached. Contact Indy Collab to renew.")

    csv_bytes = await transcript.read()
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="wb") as tmp_in:
        tmp_in.write(csv_bytes)
        tmp_csv = tmp_in.name

    safe_name = "".join(c if c.isalnum() or c in "_ " else "_" for c in student_name).strip()
    tmp_pdf = tempfile.mktemp(suffix=".pdf")

    try:
        mod = load_engine(major)
        courses = mod.parse_csv(tmp_csv)
        res     = mod.audit(courses)
        major_label = MAJORS[major]["label"]

        # Calculate progress - handle both AuditResult object and dict
        if hasattr(res, 'liberal_arts'):
            all_reqs = res.liberal_arts + res.business_core + res.major_requirements + res.minor_requirements
        elif isinstance(res, dict):
            all_reqs = res.get('liberal_arts', []) + res.get('business_core', []) + res.get('major_requirements', []) + res.get('minor_requirements', [])
        else:
            all_reqs = []
        total_reqs = len(all_reqs)
        satisfied_reqs = sum(1 for r in all_reqs if (r.status if hasattr(r, 'status') else r.get('status','')) == "Satisfied")
        pct = round(satisfied_reqs / total_reqs * 100) if total_reqs else 0

        mod.build(res, student_name, major_label, tmp_pdf)

        if hasattr(mod, 'set_catalog_year'):
            mod.set_catalog_year(catalog_year)
            mod.build(res, student_name, major_label, tmp_pdf)

        total = record_pull("advisor", student_name, MAJORS[major]["label"], catalog_year)

        filename = f"{safe_name}_{major_label.replace(' ','_')}_Audit.pdf"
        return FileResponse(
            tmp_pdf,
            media_type="application/pdf",
            filename=filename,
            headers={
                "X-Pulls-Used": str(total),
                "X-Pulls-Remaining": str(MAX_PULLS - total),
                "X-Progress-Pct": str(pct),
                "X-Progress-Satisfied": str(satisfied_reqs),
                "X-Progress-Total": str(total_reqs),
                "X-Pdf-Path": tmp_pdf,
                "Access-Control-Expose-Headers": "X-Pulls-Used,X-Pulls-Remaining,X-Progress-Pct,X-Progress-Satisfied,X-Progress-Total,X-Pdf-Path,Content-Disposition",
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Audit generation failed: {str(e)}")
    finally:
        os.unlink(tmp_csv)

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/history/{student_name}")
def get_history(student_name: str):
    log = load_log()
    student_lower = student_name.lower()
    history = [p for p in log["pulls"] if p.get("student","").lower() == student_lower]
    return {"history": history[-20:]}

@app.post("/email-audit")
async def email_audit(
    student_email: str = Form(...),
    student_name:  str = Form(...),
    pdf_path:      str = Form(...),
):
    if not GMAIL_USER or not GMAIL_PASS:
        raise HTTPException(500, "Email not configured on server.")
    if not os.path.exists(pdf_path):
        raise HTTPException(404, "PDF not found. Generate audit first.")
    try:
        msg = MIMEMultipart()
        msg["From"]    = GMAIL_USER
        msg["To"]      = student_email
        msg["Subject"] = f"Your Degree Completion Audit — {student_name}"
        body = f"""Dear {student_name},\n\nPlease find your Degree Completion Audit attached.\n\nIf you have questions, please contact your academic advisor.\n\nSelah Academic Solutions | Anderson University"""
        msg.attach(MIMEText(body, "plain"))
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{student_name}_Audit.pdf"')
        msg.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        return {"ok": True, "message": f"Audit sent to {student_email}"}
    except Exception as e:
        raise HTTPException(500, f"Email failed: {str(e)}")

@app.get("/status")
def status():
    log = load_log()
    return {
        "total_pulls":     log["total"],
        "remaining_pulls": max(0, MAX_PULLS - log["total"]),
        "max_pulls":       MAX_PULLS,
        "majors_available": [v["label"] for v in MAJORS.values()],
        "catalog_years":   CATALOG_YEARS,
    }
