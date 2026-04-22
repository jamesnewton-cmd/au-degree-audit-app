"""
Anderson University — Graduation Audit Web Application
FastAPI backend with file upload, audit generation, and PDF download.

Endpoints:
  GET  /           → Upload form (HTML)
  POST /generate   → Run audit, return PDF
  GET  /health     → Health check for Render

Environment variables:
  AUDIT_PASSWORD   → HTTP Basic Auth password (default: "audit2024")
  SECRET_KEY       → Session secret (optional)
"""

import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

import sys
sys.path.insert(0, os.path.dirname(__file__))

from engines.csv_parser import parse_csv, get_student_info
from engines.audit_engine import run_audit
from engines.pdf_generator import generate_pdf

# ─────────────────────────────────────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Anderson University Graduation Audit",
    description="Registrar audit engine — generates PDF graduation audits from student CSV exports",
    version="3.0.0",
)




# ─────────────────────────────────────────────────────────────────────────────
# MAJOR KEY MAP — normalize form input to internal major key
# ─────────────────────────────────────────────────────────────────────────────

MAJOR_KEY_MAP = {
    # Political Science variants
    "political science": "political_science",
    "political_science": "political_science",
    "polsci": "political_science",
    "posc": "political_science",
    "polj": "political_science",
    # Accounting variants
    "accounting": "accounting",
    "accj": "accounting",
    "acct": "accounting",
    # Visual Communication variants
    "visual communication": "visual_communication",
    "visual communications": "visual_communication",
    "visual_communication": "visual_communication",
    "visual_communications": "visual_communication",
    "vcdj": "visual_communication",
    # History
    "history": "history",
    "hist": "history",
    # Communication
    "communication": "communication",
    "comm": "communication",
    # Psychology
    "psychology": "psychology",
    "psyc": "psychology",
    # Biology
    "biology": "biology",
    "biol": "biology",
    # Chemistry
    "chemistry": "chemistry",
    "chem": "chemistry",
    # Nursing
    "nursing": "nursing",
    "nurs": "nursing",
    # Education
    "education": "education",
    "elementary education": "elementary_education",
    "elementary_education": "elementary_education",
    "educ": "education",
    # Math
    "math": "math",
    "mathematics": "math",
    # Computer Science
    "computer science": "computer_science",
    "computer_science": "computer_science",
    "cpsc": "computer_science",
    # Criminal Justice
    "criminal justice": "criminal_justice",
    "criminal_justice": "criminal_justice",
    "crim": "criminal_justice",
    # Social Work
    "social work": "social_work",
    "social_work": "social_work",
    "sowk": "social_work",
    # Exercise Science
    "exercise science": "exercise_science",
    "exercise_science": "exercise_science",
    "exsc": "exercise_science",
    # Music
    "music": "music",
    "musc": "music",
    # Theatre
    "theatre": "theatre",
    "theater": "theatre",
    "thea": "theatre",
    # Spanish
    "spanish": "spanish",
    "span": "spanish",
    # Engineering
    "engineering": "engineering",
    "engr": "engineering",
    # Business
    "management": "management",
    "marketing": "marketing",
    "finance": "finance",
    "sport marketing": "sport_marketing",
    "sport_marketing": "sport_marketing",
    "bsns": "management",
}


def normalize_major(raw: str) -> str:
    key = raw.strip().lower()
    return MAJOR_KEY_MAP.get(key, key.replace(" ", "_"))


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "version": "3.0.0"}


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=_upload_form_html(), status_code=200)


@app.post("/generate")
async def generate(
    csv_file: UploadFile = File(...),
    student_name: str = Form(""),
    student_id: str = Form(""),
    major: str = Form(...),
    catalog_year: str = Form("2022-23"),
):
    """
    Run a graduation audit and return a PDF.

    Form fields:
      - csv_file: Student transcript CSV export
      - student_name: Full name (optional — parsed from filename if blank)
      - student_id: Student ID (optional)
      - major: Major name or code
      - catalog_year: "2022-23", "2023-24", or "2024-25"
    """
    # Save uploaded CSV to temp file
    suffix = Path(csv_file.filename).suffix or ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await csv_file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Parse CSV
        course_map = parse_csv(tmp_path)

        # Auto-detect student info from filename if not provided
        if not student_name or not major:
            info = get_student_info(tmp_path if not csv_file.filename else
                                    _temp_with_name(tmp_path, csv_file.filename))
            if not student_name:
                student_name = info.get("name", "Unknown Student")
            if not major:
                major = info.get("major", "undeclared")
            if catalog_year == "2022-23" and info.get("catalog_year"):
                catalog_year = info["catalog_year"]

        major_key = normalize_major(major)

        # Run audit
        result = run_audit(
            course_map=course_map,
            student_name=student_name,
            student_id=student_id,
            major_key=major_key,
            catalog_year=catalog_year,
        )

        # Generate PDF
        pdf_path = tmp_path.replace(suffix, ".pdf")
        generate_pdf(result, pdf_path)

        # Return PDF
        safe_name = f"{student_name.replace(' ', '_')}_{major_key}_audit.pdf"
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=safe_name,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit generation failed: {str(e)}")
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def _temp_with_name(tmp_path: str, original_name: str) -> str:
    """Create a symlink or copy with the original filename for info parsing."""
    import shutil
    dir_ = os.path.dirname(tmp_path)
    named = os.path.join(dir_, original_name)
    shutil.copy2(tmp_path, named)
    return named


# ─────────────────────────────────────────────────────────────────────────────
# HTML UPLOAD FORM
# ─────────────────────────────────────────────────────────────────────────────

def _upload_form_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anderson University — Graduation Audit</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f4f4; color: #333; }
  header {
    background: #7B1C1C; color: white; padding: 18px 32px;
    display: flex; align-items: center; gap: 16px;
  }
  header h1 { font-size: 1.3rem; font-weight: 700; }
  header p { font-size: 0.85rem; opacity: 0.85; }
  .container { max-width: 680px; margin: 40px auto; padding: 0 16px; }
  .card {
    background: white; border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 32px;
  }
  h2 { font-size: 1.1rem; color: #7B1C1C; margin-bottom: 20px; border-bottom: 2px solid #B8962E; padding-bottom: 8px; }
  .form-group { margin-bottom: 18px; }
  label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: #555; }
  input[type=text], input[type=file], select {
    width: 100%; padding: 9px 12px; border: 1px solid #ccc;
    border-radius: 5px; font-size: 0.9rem;
  }
  input[type=file] { padding: 6px; background: #fafafa; }
  .required { color: #C62828; }
  .hint { font-size: 0.78rem; color: #888; margin-top: 3px; }
  .btn {
    background: #7B1C1C; color: white; border: none;
    padding: 12px 28px; border-radius: 5px; font-size: 1rem;
    font-weight: 600; cursor: pointer; width: 100%; margin-top: 8px;
    transition: background 0.2s;
  }
  .btn:hover { background: #5a1414; }
  .note {
    background: #FFF8E1; border-left: 4px solid #B8962E;
    padding: 10px 14px; border-radius: 4px; font-size: 0.82rem;
    margin-top: 20px; color: #555;
  }
  footer { text-align: center; font-size: 0.78rem; color: #aaa; margin: 30px 0 20px; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Anderson University — Graduation Audit Engine</h1>
    <p>Registrar Office · Audit Engine v3</p>
  </div>
</header>
<div class="container">
  <div class="card">
    <h2>Generate Student Graduation Audit</h2>
    <form method="post" action="/generate" enctype="multipart/form-data">
      <div class="form-group">
        <label>Student CSV Export <span class="required">*</span></label>
        <input type="file" name="csv_file" accept=".csv" required>
        <p class="hint">Export from the SIS as CSV. Filename format: FirstnameLastname-Major22-23.csv</p>
      </div>
      <div class="form-group">
        <label>Student Full Name</label>
        <input type="text" name="student_name" placeholder="e.g. Jennifer Eisinger">
        <p class="hint">Leave blank to auto-detect from filename.</p>
      </div>
      <div class="form-group">
        <label>Student ID</label>
        <input type="text" name="student_id" placeholder="e.g. 1234567">
      </div>
      <div class="form-group">
        <label>Major <span class="required">*</span></label>
        <input type="text" name="major" placeholder="e.g. Political Science, Accounting, Visual Communication" required>
        <p class="hint">Enter the major name exactly as it appears on the advising sheet.</p>
      </div>
      <div class="form-group">
        <label>Catalog Year <span class="required">*</span></label>
        <select name="catalog_year">
          <option value="2022-23">2022-23</option>
          <option value="2023-24">2023-24</option>
          <option value="2024-25">2024-25</option>
        </select>
      </div>
      <button type="submit" class="btn">Generate Audit PDF</button>
    </form>
    <div class="note">
      <strong>Note:</strong> The audit PDF will download automatically. It includes the Liberal Arts evaluation,
      major requirements, course history, and action plan. All logic is deterministic — no AI inference at runtime.
    </div>
  </div>
</div>
<footer>Anderson University Registrar · Audit Engine v3 · Confidential</footer>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
