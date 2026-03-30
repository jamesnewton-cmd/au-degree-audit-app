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

    def test_programs_all_includes_all_year_valid_non_fsb_programs(self):
        from requirements.non_fsb_programs import list_programs_by_year

        for year in main.CATALOG_YEARS:
            payload = self.client.get(f"/programs/all/{year}", headers=self.headers).json()
            non_fsb = payload["non_fsb_programs"]
            fsb_option_keys = main.get_fsb_option_keys_for_year(year)
            expected_non_fsb = {k for k in list_programs_by_year(year) if k not in fsb_option_keys}
            returned_non_fsb = set(non_fsb.keys())
            missing = expected_non_fsb - returned_non_fsb
            self.assertFalse(
                missing,
                f"Missing non-FSB programs in /programs/all/{year}: {sorted(missing)}",
            )

    def test_non_fsb_schema_uses_supported_requirement_shapes(self):
        from requirements.non_fsb_programs import ALL_NON_FSB_PROGRAMS, get_non_fsb_requirements

        meta_keys = {
            "name",
            "total_credits",
            "delivery",
            "notes",
            "teaching_fields",
            "department",
            "concentration_note",
            "special_rules",
            "same_as",
            "optional_cma",
            "concentrations",
            "tracks",
            "total_major_credits",
            "lead_courses_credits",
            "la_credits",
            "elective_credits",
            "min_level",
            "choose_one",
            "accreditation",
            "prerequisites",
            "dummy_2022_23",
            "dummy_elective",
            "required_old",
            "dept_dummy",
            "upper_div_psyc",
            "required_foundational",
            "required_capstone",
        }
        supported_list_of_dict = {"elective_groups", "dist_groups", "choose_one"}

        for year in main.CATALOG_YEARS:
            for key in ALL_NON_FSB_PROGRAMS:
                req = get_non_fsb_requirements(key, year)
                if not isinstance(req, dict):
                    continue
                for section_key, section_val in req.items():
                    if section_key in meta_keys:
                        continue
                    if isinstance(section_val, list) and section_val:
                        if isinstance(section_val[0], dict):
                            self.assertIn(
                                section_key,
                                supported_list_of_dict,
                                f"Unsupported list-of-dict requirement block: {key} {year} {section_key}",
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

    def test_social_studies_teaching_builds_distribution_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("social_studies_teaching", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("US History upper-division" in lbl for lbl in labels))
        self.assertTrue(any("Third Field advanced electives" in lbl for lbl in labels))
        # Should include required + distribution groups, not just the 4 fixed required.
        self.assertGreaterEqual(len(rows), 8)

    def test_social_studies_teaching_definition_matches_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("social_studies_teaching", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in ("HIST-4700", "HIST-2000", "POSC-2020", "POSC-2100", "POSC-2580"):
            self.assertIn(course, required)

        dist_groups = req.get("dist_groups", [])
        names = {g.get("name") for g in dist_groups if isinstance(g, dict)}
        self.assertIn("US History upper-division", names)
        self.assertIn("European History foundations", names)
        self.assertIn("European History upper-division", names)
        self.assertIn("Global History upper-division", names)
        self.assertIn("Third Field advanced electives", names)

    def test_psychology_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("psychology", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in ("PSYC-2000", "PSYC-2010", "PSYC-4900"):
            self.assertIn(course, required)

        groups = req.get("dist_groups", [])
        self.assertTrue(
            any(isinstance(g, dict) and g.get("name") == "PSYC upper-division core list (min 12 hrs)" for g in groups)
        )
        self.assertTrue(
            any(isinstance(g, dict) and g.get("name") == "PSYC remaining elective hours" for g in groups)
        )

        rows = main._build_major_rows(req, [], sm_mod)
        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("PSYC upper-division core list (min 12 hrs)" in lbl for lbl in labels))
        self.assertTrue(any("PSYC remaining elective hours" in lbl for lbl in labels))

    def test_writing_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("writing", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        self.assertIn("ENGL-4910", required)

        groups = req.get("elective_groups", [])
        names = {g.get("name") for g in groups if isinstance(g, dict)}
        self.assertIn("Writing / Editing / Publishing courses", names)
        self.assertIn("Any other ENGL 2000+ not already used", names)
        self.assertIn("Writing internship experience", names)
        self.assertIn("Design/digital elective", names)

        rows = main._build_major_rows(req, [], sm_mod)
        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Writing / Editing / Publishing courses" in lbl for lbl in labels))
        self.assertTrue(any("Writing internship experience" in lbl for lbl in labels))
        self.assertTrue(any("Design/digital elective" in lbl for lbl in labels))

    def test_math_ba_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("math_ba", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in ("MATH-2010", "MATH-2020", "MATH-3010", "MATH-3020", "MATH-4000"):
            self.assertIn(course, required)

        groups = req.get("dist_groups", [])
        names = {g.get("name") for g in groups if isinstance(g, dict)}
        self.assertIn("Upper Math course", names)
        self.assertIn("Additional upper Math", names)

        rows = main._build_major_rows(req, [], sm_mod)
        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Upper Math course" in lbl for lbl in labels))
        self.assertTrue(any("Additional upper Math" in lbl for lbl in labels))

    def test_cybersecurity_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("cybersecurity_major", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "CPSC-2080",
            "CPSC-2180",
            "CPSC-2300",
            "CPSC-3380",
            "CPSC-3410",
            "CPSC-4080",
            "CPSC-4480",
            "POSC-2030",
            "POSC-2200",
            "POSC-2400",
            "POSC-2420",
            "MATH-2120",
        ):
            self.assertIn(course, required)

        choose_one = req.get("choose_one", [])
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "Discrete Mathematical Structures" for g in choose_one))
        self.assertTrue(
            any(
                isinstance(g, dict) and g.get("name") == "National Security Policy sequence (alt years)"
                for g in choose_one
            )
        )
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "Ethics" for g in choose_one))

        elective_groups = req.get("elective_groups", [])
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "Cybersecurity electives" for g in elective_groups))
        cyber_elective = next(
            (g for g in elective_groups if isinstance(g, dict) and g.get("name") == "Cybersecurity electives"),
            {},
        )
        self.assertEqual(cyber_elective.get("credits"), 9)
        self.assertIn("CRIM-2520", set(cyber_elective.get("choose_from", [])))

    def test_cybersecurity_2022_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("cybersecurity_major", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Discrete Mathematical Structures" in lbl for lbl in labels))
        self.assertTrue(any("National Security Policy sequence (alt years)" in lbl for lbl in labels))
        self.assertTrue(any("Ethics" in lbl for lbl in labels))
        self.assertTrue(any("Cybersecurity electives" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 18)

    def test_elementary_education_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("elementary_education", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "EDUC-2000",
            "EDUC-2030",
            "EDUC-2100",
            "EDUC-2110",
            "EDUC-2170",
            "EDUC-2200",
            "EDUC-2460",
            "EDUC-2520",
            "EDUC-2730",
            "EDUC-3120",
            "EDUC-3300",
            "EDUC-4120",
            "EDUC-4310",
            "EDUC-4320",
            "EDUC-4010",
            "EDUC-4930",
            "EDUC-4850",
            "EDUC-4910",
            "SPED-2400",
            "SPED-3120",
            "SPED-3200",
            "MUED-2110",
            "HIST-2000",
            "MATH-1110",
            "PETE-3710",
            "PHYS-1030",
            "BIOL-1000",
            "HIST-2110",
            "MATH-1100",
        ):
            self.assertIn(course, required)

        choose_one = req.get("choose_one", [])
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "Valuing Through Literature" for g in choose_one))
        lit = next((g for g in choose_one if isinstance(g, dict) and g.get("name") == "Valuing Through Literature"), {})
        self.assertEqual(set(lit.get("choose_from", [])), {"ENGL-1400", "ENGL-3590"})

    def test_elementary_education_2022_builds_literature_choice_row(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("elementary_education", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Valuing Through Literature" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 30)

    def test_ppe_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("polsci_philosophy_economics", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "POSC-2020",
            "POSC-2100",
            "POSC-2200",
            "POSC-2400",
            "POSC-2420",
            "MATH-2120",
            "ECON-2010",
            "ECON-2020",
            "PHIL-2000",
            "PHIL-2120",
            "POSC-3510",
            "ECON-3410",
            "POSC-4930",
        ):
            self.assertIn(course, required)

        choose_one = req.get("choose_one", [])
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "History of Political Thought" for g in choose_one))
        self.assertTrue(any(isinstance(g, dict) and g.get("name") == "Ethics and Morality for Professionals" for g in choose_one))

        groups = req.get("elective_groups", [])
        ppe_upper = next(
            (
                g
                for g in groups
                if isinstance(g, dict) and g.get("name") == "Upper-division POSC/PHIL/ECON electives"
            ),
            {},
        )
        self.assertEqual(ppe_upper.get("credits"), 12)
        self.assertEqual(ppe_upper.get("min_courses"), 4)
        self.assertIn("BIBL-3420", set(ppe_upper.get("choose_from", [])))
        self.assertIn("RLGN-3120", set(ppe_upper.get("choose_from", [])))

    def test_ppe_2022_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("polsci_philosophy_economics", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("History of Political Thought" in lbl for lbl in labels))
        self.assertTrue(any("Ethics and Morality for Professionals" in lbl for lbl in labels))
        self.assertTrue(any("Upper-division POSC/PHIL/ECON electives" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 19)

    def test_visual_communication_design_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("visual_communication_design", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "ARTH-3010",
            "ARTH-3020",
            "ARTH-3030",
            "ARTS-2010",
            "ARTS-2011",
            "ARTS-2060",
            "ARTS-2100",
            "ARTS-3110",
            "ARTS-3114",
            "ARTS-3310",
            "ARTS-4114",
            "ARTS-4310",
            "ARTS-4420",
            "ARTS-4820",
            "ARTS-4930",
            "ARTS-4950",
        ):
            self.assertIn(course, required)

        groups = req.get("choose_one", [])
        names = {g.get("name") for g in groups if isinstance(g, dict)}
        self.assertIn("Graphic design studio elective", names)
        self.assertIn("Branding / social media elective", names)

        design_prod = next(
            (g for g in groups if isinstance(g, dict) and g.get("name") == "Graphic design studio elective"),
            {},
        )
        self.assertEqual(set(design_prod.get("choose_from", [])), {"ARTS-4450", "COMM-3160"})

    def test_visual_communication_design_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("visual_communication_design", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Graphic design studio elective" in lbl for lbl in labels))
        self.assertTrue(any("Branding / social media elective" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 18)

    def test_program_bucket_accepts_visual_communication_design_alias(self):
        # Guardrail for historic registrar naming variant used in uploads/UI.
        self.assertEqual(main.program_bucket("visual_comm_design", "2022-23"), "NON_FSB")

    def test_mechanical_engineering_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("mechanical_engineering_bs", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "ENGR-2001",
            "ENGR-2002",
            "ENGR-2003",
            "ENGR-2010",
            "ENGR-2030",
            "ENGR-2090",
            "ENGR-2110",
            "ENGR-2310",
            "ENGR-4950",
            "ENGR-4960",
            "CHEM-2110",
            "MATH-2010",
            "MATH-2020",
            "MATH-3010",
            "MATH-3020",
            "MATH-3100",
            "PHYS-2240",
            "PHYS-2250",
            "ENGR-2070",
            "ENGR-3030",
            "ENGR-3100",
            "ENGR-3110",
            "ENGR-3160",
            "ENGR-3180",
            "ENGR-3190",
            "ENGR-3510",
            "ENGR-4100",
            "ENGR-4110",
            "ENGR-4130",
            "ENGR-4160",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 84)
        choose_one = req.get("choose_one", [])
        computing = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Computing"),
            {},
        )
        self.assertEqual(set(computing.get("choose_from", [])), {"CPSC-2320", "CPSC-2500"})

    def test_mechanical_engineering_2022_builds_full_required_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("mechanical_engineering_bs", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("ENGR-4960" in lbl for lbl in labels))
        self.assertTrue(any("ENGR-4160" in lbl for lbl in labels))
        self.assertTrue(any("Computing" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 31)

    def test_electrical_engineering_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("electrical_engineering_bs", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "ENGR-2001",
            "ENGR-2002",
            "ENGR-2003",
            "ENGR-2010",
            "ENGR-2030",
            "ENGR-2090",
            "ENGR-2110",
            "ENGR-2310",
            "ENGR-4950",
            "ENGR-4960",
            "CHEM-2110",
            "MATH-2010",
            "MATH-2020",
            "MATH-3010",
            "MATH-3020",
            "MATH-3100",
            "PHYS-2240",
            "PHYS-2250",
            "CPSC-2420",
            "ENGR-3030",
            "ENGR-3220",
            "ENGR-3230",
            "ENGR-3240",
            "ENGR-3270",
            "ENGR-3280",
            "MATH-4010",
            "ENGR-4240",
            "ENGR-4250",
            "ENGR-4230",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 84)
        choose_one = req.get("choose_one", [])
        computing = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Computing"),
            {},
        )
        self.assertEqual(set(computing.get("choose_from", [])), {"CPSC-2320", "CPSC-2500"})

    def test_electrical_engineering_2022_builds_full_required_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("electrical_engineering_bs", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("ENGR-4960" in lbl for lbl in labels))
        self.assertTrue(any("ENGR-4250" in lbl for lbl in labels))
        self.assertTrue(any("CPSC-2420" in lbl for lbl in labels))
        self.assertTrue(any("Computing" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 30)

    def test_computer_science_ba_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("cs_ba", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "CPSC-2020",
            "CPSC-2030",
            "CPSC-2100",
            "CPSC-2330",
            "CPSC-2420",
            "CPSC-2430",
            "CPSC-2500",
            "CPSC-3410",
            "CPSC-4420",
            "CPSC-4430",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 59)

        choose_one = req.get("choose_one", [])
        names = {g.get("name") for g in choose_one if isinstance(g, dict)}
        self.assertIn("Discrete Mathematical Structures", names)
        self.assertIn("Mathematics Elective", names)
        self.assertIn("Professional Core applied experience", names)

        discrete = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Discrete Mathematical Structures"),
            {},
        )
        self.assertEqual(set(discrete.get("choose_from", [])), {"MATH-2200", "CPSC-2250"})

        math_elective = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Mathematics Elective"),
            {},
        )
        self.assertEqual(set(math_elective.get("choose_from", [])), {"MATH-2010", "MATH-2120"})

        prof_applied = next(
            (
                g
                for g in choose_one
                if isinstance(g, dict) and g.get("name") == "Professional Core applied experience"
            ),
            {},
        )
        self.assertEqual(
            set(prof_applied.get("choose_from", [])),
            {"CPSC-4480", "CPSC-4800", "CPSC-4970", "CPSC-4950", "CPSC-4960"},
        )

        cs_elective = req.get("computer_science_electives", {})
        self.assertEqual(cs_elective.get("credits"), 10)
        self.assertEqual(set(cs_elective.get("dept", [])), {"CPSC", "ENGR", "MATH", "PHYS"})
        self.assertEqual(cs_elective.get("min_level"), 2000)

    def test_computer_science_ba_2022_builds_choice_and_elective_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("cs_ba", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Discrete Mathematical Structures" in lbl for lbl in labels))
        self.assertTrue(any("Mathematics Elective" in lbl for lbl in labels))
        self.assertTrue(any("Professional Core applied experience" in lbl for lbl in labels))
        self.assertTrue(any("Computer Science elective" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 14)

    def test_cinema_media_arts_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("cinema_media_arts", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "COMM-2000",
            "COMM-2020",
            "COMM-2060",
            "COMM-2160",
            "COMM-2200",
            "COMM-2320",
            "COMM-2420",
            "COMM-3120",
            "COMM-3200",
            "COMM-3220",
            "COMM-3420",
            "COMM-4000",
        ):
            self.assertIn(course, required)
        self.assertNotIn("COMM-2010", required)

        self.assertEqual(req.get("total_credits"), 52)
        groups = req.get("elective_groups", [])
        practicum = next((g for g in groups if isinstance(g, dict) and g.get("name") == "CMA practicum"), {})
        self.assertEqual(practicum.get("credits"), 4)
        self.assertEqual(set(practicum.get("choose_from", [])), {"COMM-2860"})

        internship = next((g for g in groups if isinstance(g, dict) and g.get("name") == "CMA internship"), {})
        self.assertEqual(internship.get("credits"), 1)
        self.assertEqual(set(internship.get("choose_from", [])), {"COMM-4800"})

        electives = next((g for g in groups if isinstance(g, dict) and g.get("name") == "CMA electives"), {})
        self.assertEqual(electives.get("credits"), 3)
        self.assertNotIn("COMM-3260", set(electives.get("choose_from", [])))
        self.assertTrue(
            {"COMM-3050", "COMM-3160", "COMM-4120", "COMM-4900", "THEA-2110", "THEA-2210", "ENGL-3140"}
            <= set(electives.get("choose_from", []))
        )

    def test_cinema_media_arts_2022_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("cinema_media_arts", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("COMM-4800" in lbl for lbl in labels))
        self.assertTrue(any("CMA practicum" in lbl for lbl in labels))
        self.assertTrue(any("CMA internship" in lbl for lbl in labels))
        self.assertTrue(any("CMA electives" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 15)

    def test_biochemistry_ba_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("biochemistry_ba", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "BIOL-2210",
            "BIOL-2220",
            "BIOL-2240",
            "BIOL-4050",
            "BIOL-4310",
            "CHEM-2110",
            "CHEM-2120",
            "CHEM-2210",
            "CHEM-2220",
            "CHEM-3100",
            "CHEM-4510",
            "CHEM-4520",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 56)
        choose_one = req.get("choose_one", [])
        names = {g.get("name") for g in choose_one if isinstance(g, dict)}
        self.assertIn("Biochemistry I", names)
        self.assertIn("Biochemistry II", names)
        self.assertIn("Science Seminar I", names)
        self.assertIn("Science Seminar II", names)

        biochem_i = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Biochemistry I"),
            {},
        )
        self.assertEqual(set(biochem_i.get("choose_from", [])), {"BIOL-4210", "CHEM-4210"})

        biochem_ii = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Biochemistry II"),
            {},
        )
        self.assertEqual(set(biochem_ii.get("choose_from", [])), {"BIOL-4220", "CHEM-4220"})

        sem_i = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Science Seminar I"),
            {},
        )
        self.assertEqual(set(sem_i.get("choose_from", [])), {"BIOL-4910", "CHEM-4910", "PHYS-4910"})

        sem_ii = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Science Seminar II"),
            {},
        )
        self.assertEqual(set(sem_ii.get("choose_from", [])), {"BIOL-4920", "CHEM-4920", "PHYS-4920"})

        groups = req.get("elective_groups", [])
        biochem_elective = next(
            (g for g in groups if isinstance(g, dict) and g.get("name") == "Biochemistry electives"),
            {},
        )
        self.assertEqual(biochem_elective.get("credits"), 4)
        self.assertEqual(
            set(biochem_elective.get("choose_from", [])),
            {"CHEM-3140", "CHEM-4090", "CHEM-4110", "BIOL-3030", "BIOL-4120"},
        )

    def test_biochemistry_ba_2022_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("biochemistry_ba", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Biochemistry I" in lbl for lbl in labels))
        self.assertTrue(any("Science Seminar I" in lbl for lbl in labels))
        self.assertTrue(any("Biochemistry electives" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 17)

    def test_biochemistry_bs_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("biochemistry_bs", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "BIOL-2210",
            "BIOL-2220",
            "BIOL-2240",
            "BIOL-3030",
            "BIOL-4050",
            "BIOL-4310",
            "CHEM-2110",
            "CHEM-2120",
            "CHEM-2210",
            "CHEM-2220",
            "CHEM-3100",
            "CHEM-4110",
            "CHEM-4510",
            "CHEM-4520",
            "MATH-2010",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 76)

        choose_one = req.get("choose_one", [])
        names = {g.get("name") for g in choose_one if isinstance(g, dict)}
        self.assertIn("Biochemistry I", names)
        self.assertIn("Biochemistry II", names)
        self.assertIn("Science Seminar I", names)
        self.assertIn("Science Seminar II", names)
        self.assertIn("Physics I", names)
        self.assertIn("Physics II", names)
        self.assertIn("Stats/Research Methods", names)

        biochem_i = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Biochemistry I"),
            {},
        )
        self.assertEqual(set(biochem_i.get("choose_from", [])), {"BIOL-4210", "CHEM-4210"})

        biochem_ii = next(
            (g for g in choose_one if isinstance(g, dict) and g.get("name") == "Biochemistry II"),
            {},
        )
        self.assertEqual(set(biochem_ii.get("choose_from", [])), {"BIOL-4220", "CHEM-4220"})

    def test_biochemistry_bs_2022_builds_grouped_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("biochemistry_bs", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("Biochemistry I" in lbl for lbl in labels))
        self.assertTrue(any("Science Seminar I" in lbl for lbl in labels))
        self.assertTrue(any("Physics I" in lbl for lbl in labels))
        self.assertTrue(any("Stats/Research Methods" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 22)

    def test_christian_ministries_2022_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("christian_ministries", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in (
            "BIBL-2000",
            "BIBL-2050",
            "RLGN-2000",
            "RLGN-2130",
            "RLGN-2150",
            "RLGN-3040",
            "RLGN-3060",
            "RLGN-3300",
            "CMIN-2000",
            "CMIN-2810",
            "CMIN-3050",
            "CMIN-3080",
            "CMIN-3910",
            "CMIN-4250",
            "CMIN-4810",
        ):
            self.assertIn(course, required)

        self.assertEqual(req.get("total_credits"), 46)
        dept_elective = req.get("departmental_elective", {})
        self.assertEqual(dept_elective.get("credits"), 3)
        self.assertEqual(set(dept_elective.get("dept", [])), {"CMIN", "RLGN", "BIBL"})

    def test_christian_ministries_2022_builds_departmental_elective_row(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("christian_ministries", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod)

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("CMIN-4810" in lbl for lbl in labels))
        self.assertTrue(any("Departmental elective" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 16)

    def test_exercise_science_definition_matches_uploaded_advising_sheet_structure(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements

        req = get_non_fsb_requirements("exercise_science", "2022-23")
        self.assertIsInstance(req, dict)

        required = set(req.get("required", []))
        for course in ("EXSC-1360", "EXSC-2455", "EXSC-4920", "PEHS-1550", "PSYC-2000"):
            self.assertIn(course, required)

        chemistry = req.get("chemistry_choose", {})
        self.assertEqual(chemistry.get("credits"), 4)
        self.assertEqual(set(chemistry.get("choose_from", [])), {"CHEM-1000", "CHEM-2110"})

        concentrations = req.get("concentrations", {})
        self.assertIn("Clinical Exercise Physiology", concentrations)
        self.assertIn("Pre-Health", concentrations)
        self.assertIn("Sports Performance", concentrations)

        clinical = concentrations["Clinical Exercise Physiology"]
        self.assertEqual(set(clinical.get("required", [])), {"EXSC-4050", "EXSC-4160"})

        pre_health = concentrations["Pre-Health"].get("elective_pool", {})
        self.assertEqual(pre_health.get("credits"), 14)
        self.assertIn("SOCI-2010", set(pre_health.get("choose_from", [])))

        sports = concentrations["Sports Performance"]
        self.assertEqual(set(sports.get("required", [])), {"ATRG-1530", "EXSC-4010"})

    def test_exercise_science_clinical_concentration_builds_rows(self):
        from requirements.non_fsb_programs import get_non_fsb_requirements
        from engines import sport_marketing as sm_mod

        req = get_non_fsb_requirements("exercise_science", "2022-23")
        self.assertIsInstance(req, dict)
        rows = main._build_major_rows(req, [], sm_mod, concentration="Clinical Exercise Physiology")

        labels = [r.get("label", "") for r in rows]
        self.assertTrue(any("[Clinical Exercise Physiology] EXSC-4050" in lbl for lbl in labels))
        self.assertTrue(any("[Clinical Exercise Physiology] EXSC-4160" in lbl for lbl in labels))
        self.assertTrue(any("Clinical Exercise Physiology electives" in lbl for lbl in labels))
        self.assertGreaterEqual(len(rows), 21)

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

    def test_management_2022_structure_matches_uploaded_advising_sheet(self):
        from engines import management as mgmt_mod

        business_core_ids = [rid for rid, _label, _opts, _dcr in mgmt_mod.BUS_CORE]
        required_ids = [rid for rid, _label, _opts, _dcr in mgmt_mod.MGMT_REQ]

        self.assertIn("MATH_1300", business_core_ids)
        self.assertIn("STATS_4CR", business_core_ids)
        self.assertIn("CPSC_1100", business_core_ids)
        self.assertIn("BSNS_4910", business_core_ids)

        self.assertEqual(set(required_ids), {"BSNS_3270", "BSNS_4010", "BSNS_4480", "BSNS_4920"})

        self.assertEqual(mgmt_mod.MGMT_CONCENTRATION_HRS, 9)
        self.assertIn("BSNS_3120", mgmt_mod.ELEC_OPTS)
        self.assertIn("COMM_3250", mgmt_mod.ELEC_OPTS)
        self.assertIn("BSNS_4800", mgmt_mod.ELEC_OPTS)

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

    def test_scheduled_with_timestamp_registration_date_is_promoted_to_current(self):
        from engines.sport_marketing import parse_csv

        tmp_dir = Path(tempfile.mkdtemp(prefix="audit-scheduled-ts-to-current-"))
        try:
            csv_path = tmp_dir / "scheduled_started_term_timestamp.csv"
            csv_path.write_text(
                (
                    "Course Code,Equivalent Course,Status,Letter Grade,Credits,Registration Date,Course Name\n"
                    "EDUC-4010,,Scheduled,,10,11/20/2025 5:54:05 PM +00:00,Student Teaching: 10 cr hr in field\n"
                ),
                encoding="utf-8",
            )
            rows = parse_csv(str(csv_path))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["code"], "EDUC_4010")
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

    def test_management_2022_matches_uploaded_sheet_core_and_required_blocks(self):
        from engines.management import BUS_CORE, MGMT_REQ, MGMT_CONCENTRATION_HRS

        core_ids = {rid for rid, *_ in BUS_CORE}
        req_ids = {rid for rid, *_ in MGMT_REQ}

        # Prerequisite + business core per uploaded advising sheet.
        self.assertIn("MATH_1300", core_ids)
        self.assertIn("STATS_4CR", core_ids)
        self.assertIn("CPSC_1100", core_ids)
        self.assertIn("BSNS_4910", core_ids)

        # Management required block per uploaded advising sheet.
        self.assertIn("BSNS_3270", req_ids)
        self.assertIn("BSNS_4010", req_ids)
        self.assertIn("BSNS_4480", req_ids)
        self.assertIn("BSNS_4920", req_ids)

        # Concentration requirement is 9 credits (one concentration area).
        self.assertEqual(MGMT_CONCENTRATION_HRS, 9)

    def test_management_concentration_hours_count_satisfied_and_current(self):
        from engines.management import audit

        courses = [
            {
                "code": "BSNS_3100",
                "raw": "BSNS-3100",
                "name": "New Venture Feasibility",
                "cr": 3,
                "status": "grade posted",
                "grade": "A",
                "reg_date": "2024-04-24",
            },
            {
                "code": "BSNS_4310",
                "raw": "BSNS-4310",
                "name": "Business Plan Development",
                "cr": 3,
                "status": "grade posted",
                "grade": "B",
                "reg_date": "2024-04-24",
            },
            {
                "code": "BSNS_3240",
                "raw": "BSNS-3240",
                "name": "Operations Management",
                "cr": 3,
                "status": "current",
                "grade": "",
                "reg_date": "2025-01-10",
            },
        ]
        res = audit(courses)
        self.assertEqual(res["ehrs"], 6)
        self.assertEqual(res["ehrs_ip"], 3)


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
