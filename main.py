"""
Anderson University — Degree Audit Web App
Indy Collab, LLC
"""

import os, io, csv, json, hashlib, datetime, tempfile, importlib.util
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

MAJORS = {
    "management":     {"label": "Management",     "engine": "management"},
    "sport_marketing": {"label": "Sport Marketing", "engine": "sport_marketing"},
}

CATALOG_YEARS = ["2022-23", "2023-24", "2024-25", "2025-26"]

# ── APP ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="AU Degree Audit", docs_url=None, redoc_url=None)
security = HTTPBasic()

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
    user=Depends(verify),
    student_name: str = Form(...),
    major:        str = Form(...),
    catalog_year: str = Form(...),
    transcript:   UploadFile = File(...),
):
    # Validate inputs
    if major not in MAJORS:
        raise HTTPException(400, "Invalid major")
    if catalog_year not in CATALOG_YEARS:
        raise HTTPException(400, "Invalid catalog year")

    # Check pull limit
    log = load_log()
    if log["total"] >= MAX_PULLS:
        raise HTTPException(429, "Annual pull limit reached. Contact Indy Collab to renew.")

    # Save uploaded CSV to temp file
    csv_bytes = await transcript.read()
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="wb") as tmp_in:
        tmp_in.write(csv_bytes)
        tmp_csv = tmp_in.name

    # Output PDF path
    safe_name = "".join(c if c.isalnum() or c in "_ " else "_" for c in student_name).strip()
    tmp_pdf = tempfile.mktemp(suffix=".pdf")

    try:
        mod = load_engine(major)

        # Patch catalog year into engine before running
        # Engines expose: parse_csv(path), audit(courses), build(res, name, label, out)
        courses = mod.parse_csv(tmp_csv)
        res     = mod.audit(courses)

        major_label = MAJORS[major]["label"]
        mod.build(res, student_name, major_label, tmp_pdf)

        # Patch catalog year text in PDF is handled inside engine via catalog_year param
        # For now we pass it via a module-level override if the engine supports it
        if hasattr(mod, 'set_catalog_year'):
            mod.set_catalog_year(catalog_year)
            mod.build(res, student_name, major_label, tmp_pdf)

        # Record pull
        total = record_pull(user, student_name, MAJORS[major]["label"], catalog_year)

        filename = f"{safe_name}_{major_label.replace(' ','_')}_Audit.pdf"
        return FileResponse(
            tmp_pdf,
            media_type="application/pdf",
            filename=filename,
            headers={"X-Pulls-Used": str(total), "X-Pulls-Remaining": str(MAX_PULLS - total)}
        )
    except Exception as e:
        raise HTTPException(500, f"Audit generation failed: {str(e)}")
    finally:
        os.unlink(tmp_csv)

@app.get("/status")
def status(user=Depends(verify)):
    log = load_log()
    return {
        "total_pulls":     log["total"],
        "remaining_pulls": max(0, MAX_PULLS - log["total"]),
        "max_pulls":       MAX_PULLS,
        "majors_available": [v["label"] for v in MAJORS.values()],
        "catalog_years":   CATALOG_YEARS,
    }
