#!/usr/bin/env python3
"""
Known-good QA runbook for AU Degree Audit.

Runs a repeatable set of /generate checks against a target base URL using
fixture transcripts committed under qa/fixtures/transcripts.
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURE_DIR = ROOT / "qa" / "fixtures" / "transcripts"
REPORT_DIR = ROOT / "qa" / "reports"
OUTPUT_DIR = ROOT / "qa" / "output"


CASES = [
    {
        "id": "fsb_management_2022_ok",
        "student_name": "QA FSB Management",
        "major": "management",
        "catalog_year": "2022-23",
        "fixture": "fsb_management_minimal.csv",
        "expect_status": 200,
    },
    {
        "id": "nonfsb_history_2022_ok",
        "student_name": "QA History",
        "major": "history",
        "catalog_year": "2022-23",
        "fixture": "nonfsb_history_minimal.csv",
        "expect_status": 200,
    },
    {
        "id": "nonfsb_biology_ba_2022_ok",
        "student_name": "QA Biology BA",
        "major": "biology_ba",
        "catalog_year": "2022-23",
        "fixture": "nonfsb_biology_ba_minimal.csv",
        "expect_status": 200,
    },
    {
        "id": "fsb_engineering_mgmt_2025_ok",
        "student_name": "QA Engineering Management",
        "major": "engineering_management",
        "catalog_year": "2025-26",
        "fixture": "fsb_engineering_management_minimal.csv",
        "expect_status": 200,
    },
    {
        "id": "fsb_global_business_2025_invalid",
        "student_name": "QA Global Business Invalid",
        "major": "global_business",
        "catalog_year": "2025-26",
        "fixture": "fsb_management_minimal.csv",
        "expect_status": 400,
        "expect_detail_contains": "Unknown or unavailable program",
    },
]


def _auth_header(password: str) -> str:
    token = base64.b64encode(f":{password}".encode()).decode()
    return f"Authorization: Basic {token}"


def run_case(base_url: str, password: str, case: dict) -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fixture_path = FIXTURE_DIR / case["fixture"]
    if not fixture_path.exists():
        return {
            "id": case["id"],
            "ok": False,
            "status": None,
            "error": f"Missing fixture: {fixture_path}",
        }

    body_file = OUTPUT_DIR / f"{case['id']}.body"
    cmd = [
        "curl",
        "-sS",
        "-o",
        str(body_file),
        "-w",
        "%{http_code}",
        "-H",
        _auth_header(password),
        "-F",
        f"student_name={case['student_name']}",
        "-F",
        f"major={case['major']}",
        "-F",
        f"catalog_year={case['catalog_year']}",
        "-F",
        f"transcript=@{fixture_path}",
        f"{base_url.rstrip('/')}/generate",
    ]

    try:
        status_txt = subprocess.check_output(cmd, text=True).strip()
        status = int(status_txt)
    except Exception as exc:
        return {
            "id": case["id"],
            "ok": False,
            "status": None,
            "error": f"curl failed: {exc}",
        }

    body = body_file.read_text(encoding="utf-8", errors="ignore")
    expected = case["expect_status"]
    ok = status == expected
    reason = f"expected {expected}, got {status}"

    if ok and status == 200:
        ok = body.startswith("%PDF-")
        reason = "200 response is PDF" if ok else "200 response did not look like a PDF"

    if ok and status >= 400 and case.get("expect_detail_contains"):
        needle = case["expect_detail_contains"]
        ok = needle in body
        reason = (
            f"error detail contains '{needle}'"
            if ok
            else f"error detail missing '{needle}'"
        )

    return {
        "id": case["id"],
        "ok": ok,
        "status": status,
        "expected_status": expected,
        "reason": reason,
    }


def run(base_url: str, password: str) -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = [run_case(base_url, password, case) for case in CASES]
    passed = sum(1 for r in results if r["ok"])
    total = len(results)

    print("\nAU Degree Audit — Known-Good QA Runbook")
    print("=" * 48)
    for r in results:
        icon = "PASS" if r["ok"] else "FAIL"
        print(f"[{icon}] {r['id']} — {r.get('reason', '')}")
    print("-" * 48)
    print(f"Summary: {passed}/{total} passed")

    report = {"base_url": base_url, "passed": passed, "total": total, "results": results}
    report_path = REPORT_DIR / "latest_qa_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report: {report_path}")

    return 0 if passed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run known-good QA audit fixtures")
    parser.add_argument("--base-url", required=True, help="Base URL, e.g. https://www.selah-au.com")
    parser.add_argument("--password", required=True, help="AUDIT_PASSWORD value")
    args = parser.parse_args()
    return run(args.base_url, args.password)


if __name__ == "__main__":
    sys.exit(main())
