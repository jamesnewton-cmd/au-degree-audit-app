import shutil
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import main


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _issue_auth_token(client: TestClient, email: str = "advisor@anderson.edu") -> str:
    req = client.post("/auth/request-code", json={"email": email})
    if req.status_code != 200:
        raise AssertionError(f"Unable to request auth code: {req.status_code} {req.text}")
    verify = client.post("/auth/verify-code", json={"email": email, "code": main.AUTH_STATIC_TEST_CODE})
    if verify.status_code != 200:
        raise AssertionError(f"Unable to verify auth code: {verify.status_code} {verify.text}")
    token = verify.json().get("access_token")
    if not token:
        raise AssertionError("Missing access token in auth response.")
    return token


def _sample_csv_bytes() -> bytes:
    return (
        "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
        "BSNS-2000,,grade posted,A,3,2024-08-20,Intro to Business\n"
    ).encode("utf-8")


class ProgramYearRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_log_file = main.LOG_FILE
        cls._orig_auth_static = main.AUTH_STATIC_TEST_CODE
        cls._tmp_dir = tempfile.mkdtemp(prefix="audit-regression-")
        main.LOG_FILE = Path(cls._tmp_dir) / "audit_log.json"
        main.AUTH_STATIC_TEST_CODE = "123456"
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()
        cls.client = TestClient(main.app)
        cls.headers = _auth_headers(_issue_auth_token(cls.client))

    @classmethod
    def tearDownClass(cls):
        main.LOG_FILE = cls._orig_log_file
        main.AUTH_STATIC_TEST_CODE = cls._orig_auth_static
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()
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

    def test_programs_all_includes_fsb_minors_like_social_media_minor(self):
        payload = self.client.get("/programs/all/2022-23", headers=self.headers).json()
        fsb = payload["fsb_programs"]["2022-23"]
        self.assertIn("Social Media Minor", fsb)
        self.assertEqual(fsb["Social Media Minor"], "social_media_minor")

    def test_programs_all_includes_all_year_valid_fsb_majors_and_minors(self):
        from requirements.fsb_majors import FSB_MAJORS
        from requirements.fsb_minors import FSB_MINORS, get_minor_requirements

        for year in main.CATALOG_YEARS:
            payload = self.client.get(f"/programs/all/{year}", headers=self.headers).json()
            fsb_keys = set(payload["fsb_programs"][year].values())

            expected_major_keys = {k for k, year_map in FSB_MAJORS.items() if isinstance(year_map.get(year), dict)}
            expected_minor_keys = {k for k in FSB_MINORS if get_minor_requirements(k, year)}
            expected_all = expected_major_keys | expected_minor_keys

            missing = expected_all - fsb_keys
            self.assertFalse(
                missing,
                f"Missing FSB programs in /programs/all/{year}: {sorted(missing)}",
            )

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

    def test_marketing_2022_uses_marketing_engine_notes_and_required_rows(self):
        files = {"transcript": ("transcript.csv", _sample_csv_bytes(), "text/csv")}
        data = {
            "student_name": "Marketing Regression Student",
            "major": "marketing",
            "catalog_year": "2022-23",
        }
        response = self.client.post("/generate", data=data, files=files, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("content-type"), "application/pdf")

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

    def test_marketing_pdf_build_uses_major_specific_w8_notes(self):
        files = {"transcript": ("transcript.csv", _sample_csv_bytes(), "text/csv")}
        data = {
            "student_name": "Marketing Build Regression Student",
            "major": "marketing",
            "catalog_year": "2022-23",
        }
        response = self.client.post("/generate", data=data, files=files, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Response headers must reflect major engine output, not sport marketing defaults.
        self.assertEqual(response.headers.get("content-type"), "application/pdf")
        content_disposition = response.headers.get("content-disposition", "")
        self.assertIn("Marketing_", content_disposition)
        self.assertIn("_Audit.pdf", content_disposition)


class CsvStatusNormalizationTests(unittest.TestCase):
    def test_scheduled_status_is_preserved(self):
        from engines.sport_marketing import parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-scheduled-status-"))
        try:
            csv_path = tmp_dir / "scheduled_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "BSNS-2310,,Scheduled,,3,2099-01-10,Business Analytics\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["code"], "BSNS_2310")
            self.assertEqual(rows[0]["status"], "scheduled")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_scheduled_with_started_term_is_promoted_to_current(self):
        from engines.sport_marketing import parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-scheduled-to-current-"))
        try:
            csv_path = tmp_dir / "scheduled_started_term.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "BSNS-4560,,Scheduled,,3,2025-01-10,Business of Game-Day Exper\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["status"], "current")
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

    def test_status_exception_normalizes_punctuation_and_case(self):
        from engines.sport_marketing import apply_exceptions, parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-status-normalize-"))
        try:
            csv_path = tmp_dir / "status_normalize_case.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "BSNS-4560,,Scheduled,,3,2025-01-10,Business of Game-Day Exper\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            updated = apply_exceptions(rows, "STATUS: BSNS-4560 = IN-PROGRESS")
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

    def test_exceptions_accept_mixed_case_commands_and_values(self):
        from engines.sport_marketing import apply_exceptions, parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-exception-case-"))
        try:
            csv_path = tmp_dir / "exception_case_mixed.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "PSYC-2510,,Grade Posted,A,3,2024-01-10,Developmental Psychology\n"
                    "BSNS-4560,,Scheduled,,3,2025-01-10,Business of Game-Day Exper\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            updated = apply_exceptions(
                rows,
                (
                    "sUb: bsns-2710 = psyc-2510\n"
                    "mAp: psyc-2510 = w5\n"
                    "wAiVe: comm-1000\n"
                    "stAtUs: bsns-4560 = CURRENTLY ENROLLED"
                ),
            )

            sub_match = next((r for r in updated if r.get("code") == "BSNS_2710"), None)
            self.assertIsNotNone(sub_match)
            self.assertEqual(sub_match.get("status"), "grade posted")

            map_match = next((r for r in updated if str(r.get("code", "")).startswith("__MAP__W5__")), None)
            self.assertIsNotNone(map_match)

            waive_match = next((r for r in updated if r.get("code") == "COMM_1000"), None)
            self.assertIsNotNone(waive_match)
            self.assertEqual(waive_match.get("grade"), "W/V")

            status_match = next((r for r in updated if r.get("code") == "BSNS_4560"), None)
            self.assertIsNotNone(status_match)
            self.assertEqual(status_match.get("status"), "current")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


class W8CrosslistCoverageTests(unittest.TestCase):
    def test_crosslist_loader_parses_expected_rows(self):
        from requirements.w8_crosslist import (
            get_fsb_w8_courses_by_major,
            get_non_fsb_w8_courses_by_major,
        )

        fsb = get_fsb_w8_courses_by_major()
        non_fsb = get_non_fsb_w8_courses_by_major()

        self.assertEqual(
            fsb.get("marketing"),
            ["BSNS_1050", "BSNS_2810", "BSNS_3130", "BSNS_3210", "BSNS_4110", "BSNS_4550", "BSNS_4800"],
        )
        self.assertEqual(
            non_fsb.get("public_relations_complementary"),
            ["COMM_4800"],
        )

    def test_fsb_w8_map_contains_crosslist_courses(self):
        from engines.fsb_engine import FSB_W8_BY_MAJOR

        self.assertEqual(
            FSB_W8_BY_MAJOR["marketing"],
            ["BSNS_1050", "BSNS_2810", "BSNS_3130", "BSNS_3210", "BSNS_4110", "BSNS_4550", "BSNS_4800"],
        )
        self.assertEqual(
            FSB_W8_BY_MAJOR["business_integrative_leadership"],
            ["LEAD_4990"],
        )
        self.assertEqual(
            FSB_W8_BY_MAJOR["music_entertainment_business"],
            ["MUBS_4800", "BSNS_4810"],
        )

    def test_non_fsb_w8_uses_aligned_program_keys(self):
        from engines.sport_marketing import build_la_rows_for_non_fsb

        # public_relations_complementary -> COMM 4800
        courses = [
            {
                "code": "COMM_4800",
                "raw": "COMM-4800",
                "name": "Communication Internship",
                "cr": 3,
                "status": "grade posted",
                "grade": "A",
                "reg_date": "2024-01-10",
            }
        ]
        la = build_la_rows_for_non_fsb(courses, "2022-23", major_key="public_relations_complementary")
        w8 = next((row for row in la if row.get("area") == "W8"), None)
        self.assertIsNotNone(w8)
        self.assertEqual(w8.get("status"), "Satisfied")
        self.assertEqual(w8.get("course", {}).get("code"), "COMM_4800")

        # data_science_complementary -> CPSC 4970
        courses = [
            {
                "code": "CPSC_4970",
                "raw": "CPSC-4970",
                "name": "Data Science Capstone",
                "cr": 3,
                "status": "grade posted",
                "grade": "A",
                "reg_date": "2024-01-10",
            }
        ]
        la = build_la_rows_for_non_fsb(courses, "2022-23", major_key="data_science_complementary")
        w8 = next((row for row in la if row.get("area") == "W8"), None)
        self.assertIsNotNone(w8)
        self.assertEqual(w8.get("status"), "Satisfied")
        self.assertEqual(w8.get("course", {}).get("code"), "CPSC_4970")


class ManagementW1RegressionTests(unittest.TestCase):
    def test_management_w1_accepts_rlgn_3010(self):
        from engines.management import audit

        courses = [
            {
                "code": "RLGN_3010",
                "raw": "RLGN-3010",
                "name": "Faith in Context",
                "cr": 3,
                "status": "grade posted",
                "grade": "C",
                "reg_date": "2024-04-24",
            }
        ]
        res = audit(courses)
        la_by_area = {row["area"]: row for row in res["la"]}
        self.assertIn("W1", la_by_area)
        self.assertEqual(la_by_area["W1"]["status"], "Satisfied")
        self.assertEqual(la_by_area["W1"]["course"]["code"], "RLGN_3010")


class AuthFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_auth_static = main.AUTH_STATIC_TEST_CODE
        main.AUTH_STATIC_TEST_CODE = "123456"
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()
        cls.client = TestClient(main.app)

    @classmethod
    def tearDownClass(cls):
        main.AUTH_STATIC_TEST_CODE = cls._orig_auth_static
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()

    def test_request_code_rejects_non_anderson_domain(self):
        response = self.client.post("/auth/request-code", json={"email": "user@gmail.com"})
        self.assertEqual(response.status_code, 403)

    def test_request_verify_and_me(self):
        req = self.client.post("/auth/request-code", json={"email": "advisor@anderson.edu"})
        self.assertEqual(req.status_code, 200)
        verify = self.client.post(
            "/auth/verify-code",
            json={"email": "advisor@anderson.edu", "code": "123456"},
        )
        self.assertEqual(verify.status_code, 200)
        token = verify.json().get("access_token")
        self.assertTrue(token)
        me = self.client.get("/auth/me", headers=_auth_headers(token))
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json().get("email"), "advisor@anderson.edu")

    def test_static_code_with_punctuation_still_verifies_digits(self):
        orig_static = main.AUTH_STATIC_TEST_CODE
        try:
            main.AUTH_CODES.clear()
            main.AUTH_SESSIONS.clear()
            main.AUTH_STATIC_TEST_CODE = "123456!"
            req = self.client.post("/auth/request-code", json={"email": "advisor@anderson.edu"})
            self.assertEqual(req.status_code, 200)
            verify = self.client.post(
                "/auth/verify-code",
                json={"email": "advisor@anderson.edu", "code": "123456"},
            )
            self.assertEqual(verify.status_code, 200)
            self.assertTrue(verify.json().get("access_token"))
        finally:
            main.AUTH_STATIC_TEST_CODE = orig_static


class FilenameFormattingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_log_file = main.LOG_FILE
        cls._orig_auth_static = main.AUTH_STATIC_TEST_CODE
        cls._tmp_dir = tempfile.mkdtemp(prefix="audit-filename-format-")
        main.LOG_FILE = Path(cls._tmp_dir) / "audit_log.json"
        main.AUTH_STATIC_TEST_CODE = "123456"
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()
        cls.client = TestClient(main.app)
        cls.headers = _auth_headers(_issue_auth_token(cls.client))

    @classmethod
    def tearDownClass(cls):
        main.LOG_FILE = cls._orig_log_file
        main.AUTH_STATIC_TEST_CODE = cls._orig_auth_static
        main.AUTH_CODES.clear()
        main.AUTH_SESSIONS.clear()
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
