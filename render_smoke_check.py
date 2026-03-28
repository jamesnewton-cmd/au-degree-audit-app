#!/usr/bin/env python3
"""
Render smoke checks for AU Degree Audit.

Usage examples:
  python3 render_smoke_check.py --base-url https://your-app.onrender.com --password "secret"
  python3 render_smoke_check.py --base-url https://your-app.onrender.com --password "secret" --include-generate
"""

from __future__ import annotations

import argparse
import base64
import json
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


EXPECTED_YEARS = {"2022-23", "2023-24", "2024-25", "2025-26"}


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def _auth_header(password: str) -> str:
    token = base64.b64encode(f":{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def _request_json(
    method: str,
    url: str,
    *,
    auth: str | None = None,
    body: bytes | None = None,
    content_type: str | None = None,
    timeout: float = 30.0,
):
    headers = {}
    if auth:
        headers["Authorization"] = auth
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, method=method, headers=headers, data=body)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def _build_multipart(fields: dict[str, str], file_field: str, file_path: Path):
    boundary = "----au-audit-smoke-boundary"
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode("utf-8")
        )

    file_bytes = file_path.read_bytes()
    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'
            "Content-Type: text/csv\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_bytes)
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))

    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def run_checks(base_url: str, password: str, include_generate: bool, timeout: float) -> list[CheckResult]:
    base_url = base_url.rstrip("/")
    auth = _auth_header(password)
    results: list[CheckResult] = []

    status_url = f"{base_url}/status"
    years_url = f"{base_url}/catalog-years"
    programs_2526_url = f"{base_url}/programs/all/2025-26"

    # 1) Unauthenticated should be blocked.
    code, body, _ = _request_json("GET", status_url, timeout=timeout)
    results.append(
        CheckResult(
            name="unauth /status is blocked",
            ok=code == 401,
            detail=f"expected 401, got {code}",
        )
    )

    # 2) Authenticated status returns expected keys.
    code, body, _ = _request_json("GET", status_url, auth=auth, timeout=timeout)
    ok = code == 200
    detail = f"expected 200, got {code}"
    if ok:
        try:
            payload = json.loads(body.decode("utf-8"))
            required = {"total_pulls", "remaining_pulls", "max_pulls", "catalog_years"}
            missing = sorted(required - set(payload.keys()))
            ok = not missing
            detail = "status payload keys ok" if ok else f"missing keys: {missing}"
        except Exception as e:
            ok = False
            detail = f"invalid JSON payload: {e}"
    results.append(CheckResult(name="auth /status payload", ok=ok, detail=detail))

    # 3) Catalog years endpoint.
    code, body, _ = _request_json("GET", years_url, auth=auth, timeout=timeout)
    ok = code == 200
    detail = f"expected 200, got {code}"
    if ok:
        try:
            payload = json.loads(body.decode("utf-8"))
            years = set(payload.get("catalog_years", []))
            ok = EXPECTED_YEARS.issubset(years)
            detail = (
                "catalog years include expected set"
                if ok
                else f"missing years: {sorted(EXPECTED_YEARS - years)}"
            )
        except Exception as e:
            ok = False
            detail = f"invalid JSON payload: {e}"
    results.append(CheckResult(name="auth /catalog-years content", ok=ok, detail=detail))

    # 4) Program matrix for 2025-26.
    code, body, _ = _request_json("GET", programs_2526_url, auth=auth, timeout=timeout)
    ok = code == 200
    detail = f"expected 200, got {code}"
    if ok:
        try:
            payload = json.loads(body.decode("utf-8"))
            fsb = (payload.get("fsb_programs") or {}).get("2025-26", {})
            non_fsb = payload.get("non_fsb_programs", {})
            has_sports_mgmt = "Sports Management" in fsb
            has_global_business = "Global Business" in fsb
            overlap_ok = "engineering_management" not in non_fsb
            ok = has_sports_mgmt and (not has_global_business) and overlap_ok
            detail = (
                "FSB/non-FSB year mapping looks correct"
                if ok
                else (
                    f"has_sports_management={has_sports_mgmt}, "
                    f"has_global_business={has_global_business}, "
                    f"engineering_management_in_nonfsb={not overlap_ok}"
                )
            )
        except Exception as e:
            ok = False
            detail = f"invalid JSON payload: {e}"
    results.append(CheckResult(name="auth /programs/all/2025-26 mapping", ok=ok, detail=detail))

    # Optional generate checks (consumes at least one pull).
    if include_generate:
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write(
                "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
            )
            tmp.write("BSNS-2000,,grade posted,A,3,2024-08-20,Intro to Business\n")
            csv_path = Path(tmp.name)

        try:
            valid_fields = {
                "student_name": "Render Smoke Test",
                "major": "management",
                "catalog_year": "2022-23",
            }
            body_bytes, content_type = _build_multipart(valid_fields, "transcript", csv_path)
            code, body, headers = _request_json(
                "POST",
                f"{base_url}/generate",
                auth=auth,
                body=body_bytes,
                content_type=content_type,
                timeout=timeout,
            )
            content_type_header = str(headers.get("Content-Type", "")).lower()
            ok = code == 200 and "application/pdf" in content_type_header
            detail = (
                "valid generate returned PDF"
                if ok
                else f"expected 200/pdf, got {code} and Content-Type={content_type_header}"
            )
            results.append(CheckResult(name="auth POST /generate valid", ok=ok, detail=detail))

            invalid_fields = {
                "student_name": "Render Smoke Invalid Combo",
                "major": "global_business",
                "catalog_year": "2025-26",
            }
            body_bytes, content_type = _build_multipart(invalid_fields, "transcript", csv_path)
            code, body, _ = _request_json(
                "POST",
                f"{base_url}/generate",
                auth=auth,
                body=body_bytes,
                content_type=content_type,
                timeout=timeout,
            )
            ok = code == 400
            detail = f"expected 400, got {code}"
            results.append(CheckResult(name="auth POST /generate invalid combo", ok=ok, detail=detail))
        finally:
            csv_path.unlink(missing_ok=True)

    return results


def main():
    parser = argparse.ArgumentParser(description="Run Render smoke checks for AU Degree Audit.")
    parser.add_argument("--base-url", required=True, help="Render base URL, e.g. https://app.onrender.com")
    parser.add_argument("--password", required=True, help="AUDIT_PASSWORD value for Basic auth")
    parser.add_argument(
        "--include-generate",
        action="store_true",
        help="Also test /generate (uses at least one pull on target system).",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    args = parser.parse_args()

    results = run_checks(args.base_url, args.password, args.include_generate, args.timeout)
    all_ok = all(r.ok for r in results)

    print("\nAU Degree Audit — Render Smoke Check")
    print("=" * 44)
    for r in results:
        marker = "PASS" if r.ok else "FAIL"
        print(f"[{marker}] {r.name} — {r.detail}")

    print("-" * 44)
    print("GO" if all_ok else "NO-GO")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
