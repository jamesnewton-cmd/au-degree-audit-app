import base64
import shutil
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import main


def _auth_headers(password: str = "ravens2025") -> dict[str, str]:
    token = base64.b64encode(f":{password}".encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {token}"}


def _sample_csv_bytes() -> bytes:
    return (
        "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
        "BSNS-2000,,grade posted,A,3,2024-08-20,Intro to Business\n"
    ).encode("utf-8")


class ProgramYearRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_log_file = main.LOG_FILE
        cls._tmp_dir = tempfile.mkdtemp(prefix="audit-regression-")
        main.LOG_FILE = Path(cls._tmp_dir) / "audit_log.json"
        cls.client = TestClient(main.app)
        cls.headers = _auth_headers()

    @classmethod
    def tearDownClass(cls):
        main.LOG_FILE = cls._orig_log_file
        shutil.rmtree(cls._tmp_dir, ignore_errors=True)

    def _post_generate(self, major: str, year: str):
        files = {"transcript": ("transcript.csv", _sample_csv_bytes(), "text/csv")}
        data = {"student_name": "Regression Student", "major": major, "catalog_year": year}
        return self.client.post("/generate", data=data, files=files, headers=self.headers)

    def test_status_requires_auth(self):
        self.assertEqual(self.client.get("/status").status_code, 401)
        self.assertEqual(self.client.get("/status", headers=self.headers).status_code, 200)

    def test_fsb_labels_are_year_aware(self):
        labels_2022 = main.get_fsb_program_labels_for_year("2022-23")
        labels_2025 = main.get_fsb_program_labels_for_year("2025-26")

        self.assertIn("global_business", labels_2022)
        self.assertIn("music_entertainment_business", labels_2022)
        self.assertNotIn("business_analytics", labels_2022)

        self.assertNotIn("global_business", labels_2025)
        self.assertNotIn("music_entertainment_business", labels_2025)
        self.assertEqual(labels_2025.get("sport_marketing"), "Sports Management")

    def test_bucket_resolution_prefers_fsb_for_overlap(self):
        self.assertEqual(main.program_bucket("engineering_management", "2022-23"), "FSB")
        self.assertEqual(main.program_bucket("engineering_management", "2025-26"), "FSB")
        self.assertEqual(main.program_bucket("biology_ba", "2025-26"), "NON_FSB")
        self.assertIsNone(main.program_bucket("global_business", "2025-26"))

    def test_programs_all_filters_overlap_from_non_fsb(self):
        payload = self.client.get("/programs/all/2025-26", headers=self.headers).json()
        fsb = payload["fsb_programs"]["2025-26"]
        non_fsb = payload["non_fsb_programs"]

        self.assertIn("engineering_management", fsb.values())
        self.assertNotIn("engineering_management", non_fsb)

    def test_generate_valid_and_invalid_program_year(self):
        valid_fsb = self._post_generate("management", "2022-23")
        self.assertEqual(valid_fsb.status_code, 200)
        self.assertEqual(valid_fsb.headers.get("content-type"), "application/pdf")

        valid_non_fsb = self._post_generate("biology_ba", "2025-26")
        self.assertEqual(valid_non_fsb.status_code, 200)
        self.assertEqual(valid_non_fsb.headers.get("content-type"), "application/pdf")

        invalid = self._post_generate("global_business", "2025-26")
        self.assertEqual(invalid.status_code, 400)
        self.assertIn("Unknown or unavailable program", invalid.text)

    def test_sport_marketing_has_no_elective_section_requirement(self):
        files = {"transcript": ("transcript.csv", _sample_csv_bytes(), "text/csv")}
        data = {
            "student_name": "Sport Marketing Regression Student",
            "major": "sport_marketing",
            "catalog_year": "2022-23",
        }
        response = self.client.post("/generate", data=data, files=files, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("content-type"), "application/pdf")
        content_disposition = response.headers.get("content-disposition", "")
        self.assertIn("Sport_S_Audit.pdf", content_disposition)


class CsvStatusNormalizationTests(unittest.TestCase):
    def test_scheduled_status_is_preserved(self):
        from engines.sport_marketing import parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-scheduled-status-"))
        try:
            csv_path = tmp_dir / "scheduled_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "BSNS-2310,,Scheduled,,3,2025-01-10,Business Analytics\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["code"], "BSNS_2310")
            self.assertEqual(rows[0]["status"], "scheduled")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_sport_marketing_w1_and_f7_accept_equivalents(self):
        from engines.sport_marketing import audit, parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-smkt-la-equivalents-"))
        try:
            csv_path = tmp_dir / "smkt_equivalent_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "RLGN-3010,,Grade Posted,A,3,2024-01-10,Faith in Context\n"
                    "NURS-1210,,Grade Posted,B+,2,2023-01-10,Nutrition for Hlthy Liv\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            res = audit(rows)
            la_by_area = {row["area"]: row for row in res["la"]}

            self.assertIn("W1", la_by_area)
            self.assertIn("F7", la_by_area)
            self.assertEqual(la_by_area["W1"]["status"], "Satisfied")
            self.assertEqual(la_by_area["F7"]["status"], "Satisfied")
            self.assertEqual(la_by_area["W1"]["course"]["code"], "RLGN_3010")
            self.assertEqual(la_by_area["F7"]["course"]["code"], "NURS_1210")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_status_exception_accepts_currently_enrolled_alias(self):
        from engines.sport_marketing import apply_exceptions, parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-status-alias-"))
        try:
            csv_path = tmp_dir / "status_alias_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "BSNS-4560,,Scheduled,,3,2025-01-10,Business of Game-Day Exper\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            updated = apply_exceptions(rows, "STATUS: BSNS-4560 = currently enrolled")
            match = next((r for r in updated if r["code"] == "BSNS_4560"), None)
            self.assertIsNotNone(match)
            self.assertEqual(match["status"], "current")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_map_exception_can_target_minor_requirement_row(self):
        from engines.sport_marketing import apply_exceptions, audit, parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-map-minor-row-"))
        try:
            csv_path = tmp_dir / "minor_map_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "PSYC-2510,,Grade Posted,A,3,2024-01-10,Developmental Psychology\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            rows = apply_exceptions(rows, "MAP: PSYC-2510 = BSNS_2710")
            res = audit(rows, minor_key="management_minor")
            minor_rows = res.get("minor_rows") or []
            mgmt_req = next((r for r in minor_rows if r.get("id") == "BSNS_2710"), None)
            self.assertIsNotNone(mgmt_req)
            self.assertEqual(mgmt_req.get("status"), "Satisfied")
            self.assertEqual(mgmt_req.get("course", {}).get("code"), "PSYC_2510")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


class FilenameFormattingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_log_file = main.LOG_FILE
        cls._tmp_dir = tempfile.mkdtemp(prefix="audit-filename-format-")
        main.LOG_FILE = Path(cls._tmp_dir) / "audit_log.json"
        cls.client = TestClient(main.app)
        cls.headers = _auth_headers()

    @classmethod
    def tearDownClass(cls):
        main.LOG_FILE = cls._orig_log_file
        shutil.rmtree(cls._tmp_dir, ignore_errors=True)

    def test_download_filename_uses_first_last_initial(self):
        files = {"transcript": ("transcript.csv", _sample_csv_bytes(), "text/csv")}
        data = {
            "student_name": "Tyler Houck",
            "major": "management",
            "catalog_year": "2022-23",
        }
        response = self.client.post("/generate", data=data, files=files, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        disposition = response.headers.get("content-disposition", "")
        self.assertIn('filename="Tyler_H_Audit.pdf"', disposition)


if __name__ == "__main__":
    unittest.main()
