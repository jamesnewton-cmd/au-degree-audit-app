# Anderson University Degree Audit System
**Powered by Indy Collab, LLC**

---

## Overview
A web application that accepts a student transcript CSV and returns a graduation audit PDF. Built for Anderson University Falls School of Business.

- **Majors supported:** Management, Sport Marketing
- **Catalog years:** 2022-23 through 2025-26
- **Pull limit:** 1,000 audits/year (tracked automatically)
- **Auth:** Password-protected (HTTP Basic Auth)

---

## Project Structure
```
audit_app/
├── main.py                  # FastAPI backend
├── requirements.txt         # Python dependencies
├── render.yaml              # Render.com deployment config
├── templates/
│   ├── index.html           # Upload form UI
│   └── dashboard.html       # Usage dashboard
├── engines/
│   ├── management.py        # Management major audit engine
│   └── sport_marketing.py   # Sport Marketing audit engine
└── logs/
    └── audit_log.json       # Auto-created, tracks all pulls
```

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload

# Open in browser
http://localhost:8000
```

Default password for local dev: `ravens2025`
**Change this before deploying.**

---

## Deployment on Render.com (Recommended — Free Tier)

1. **Create a Render account** at render.com
2. **Push this folder to a GitHub repo** (private recommended)
3. In Render dashboard → **New Web Service** → connect your repo
4. Render auto-detects `render.yaml` and configures everything
5. In Render **Environment Variables**, set:
   - `AUDIT_PASSWORD` → your chosen password (share with AU staff)
   - `MAX_PULLS` → `1000`
6. Deploy — Render gives you a URL like `au-degree-audit.onrender.com`
7. Point `audits.indycollab.com` to that URL via a CNAME in your DNS settings

**Cost:** Free tier on Render is sufficient for 1,000 pulls/year.
Note: Free tier spins down after 15 min of inactivity (first request takes ~30s to wake).
Upgrade to Starter ($7/mo) for always-on if AU prefers instant response.

---

## Adding a New Major

1. Copy `engines/management.py` as a starting point
2. Rename and update the requirement lists, elective options, and LA rows
3. Save as `engines/your_major_name.py`
4. Add entry to `MAJORS` dict in `main.py`:
   ```python
   "your_major_key": {"label": "Your Major Label", "engine": "your_major_name"},
   ```
5. Add `<option>` to the major dropdown in `templates/index.html`
6. Redeploy

---

## Adding a New Catalog Year

1. Update `CATALOG_YEARS` list in `main.py`
2. Add `<option>` to the catalog year dropdown in `templates/index.html`
3. Redeploy

---

## Monitoring Usage

- Visit `/dashboard` (password-protected) to see pull count and recent audits
- `audit_log.json` in the `/logs` directory stores full history
- At 1,000 pulls the system blocks new requests with a clear error message

---

## Annual Renewal (per MOA)

When the university renews at $3,000/year:
1. Reset the log: delete or archive `logs/audit_log.json`
2. The counter resets to 0 automatically

---

## Security Notes

- Never commit `AUDIT_PASSWORD` to git — set it only in Render environment variables
- The `/logs` disk is persistent on Render (survives redeploys)
- All audit generation happens server-side; no student data is stored beyond the log entry (name, major, catalog year, timestamp)

---

## Support
James Newton — Indy Collab, LLC
