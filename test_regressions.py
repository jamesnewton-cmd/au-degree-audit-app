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
        # The generated filename should not include any extra elective-specific error behavior.
        self.assertIn("Sport_Marketing", response.headers.get("content-disposition", ""))


class CsvStatusNormalizationTests(unittest.TestCase):
    def test_scheduled_is_normalized_to_current(self):
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
            self.assertEqual(rows[0]["status"], "current")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
