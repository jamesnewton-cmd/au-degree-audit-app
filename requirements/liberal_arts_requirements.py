"""
Anderson University — Liberal Arts Requirements
Source of truth: Official AU LA Program Requirements PDFs
  - 22-23: Rev 08/2022
  - 23-24: Rev 10/2023
  - 24-25: Rev 10/2024
  - 25-26: Raven Core / AU Experience (new framework)

Courses may appear in multiple areas (double-dip by design).
The audit engine is responsible for enforcing that a single course
is only used to satisfy one requirement at a time.

OR rules (course satisfies ONE but not both):
  HNRS 2110 → F3 OR W3
  MLAN 2000 → W6 OR W7
  SOCI 2450 → F2 OR W7  (22-23 through 24-25)
"""

# ─────────────────────────────────────────────────────────────────────
# OLD FRAMEWORK: 2022-23, 2023-24, 2024-25
# ─────────────────────────────────────────────────────────────────────

LA_OLD_FRAMEWORK = {
    "years": ["2022-23", "2023-24", "2024-25"],

    # ── F1 ────────────────────────────────────────────────────────────
    "F1": {
        "label": "F1 Understanding College",
        "credits": 1,
        "courses": {
            "2022-23": ["LART 1050"],
            "2023-24": ["LART 1050"],
            "2024-25": ["LART 1050"],
        },
        "special_rule": "F1_SATISFIES_W8",
    },

    # ── F2 ────────────────────────────────────────────────────────────
    # Source: All three LA PDFs — same list 22-23 through 24-25 with minor delta
    # COMM 3200 added in 23-24; ENGR 2060 hrs changed 22-23→24-25 but still counts
    # SOCI 2450 is F2 OR W7 (OR rule)
    "F2": {
        "label": "F2 Civil Discourse & Critical Reasoning",
        "credits": {"2022-23": "2-4", "2023-24": "2-4", "2024-25": "2-4"},
        "courses": {
            "2022-23": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "ENGL 3190", "ENGL 3580",
                "ENGR 2060",
                "HIST 2300",
                "HNRS 2125",
                "LART 1100",
                "MUED 1000",
                "PHIL 2000", "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",
                "RLGN 3120",
                "SOCI 2450",   # OR rule: F2 OR W7
                "SPED 2400",
            ],
            "2023-24": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "COMM 3200",
                "ENGL 3190", "ENGL 3580",
                "ENGR 2060",
                "HIST 2300",
                "HNRS 2125",
                "LART 1100",
                "MUED 1000",
                "PHIL 2000", "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",
                "RLGN 3120",
                "SOCI 2450",   # OR rule: F2 OR W7
                "SPED 2400",
            ],
            "2024-25": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "COMM 3200",
                "ENGL 3190", "ENGL 3580",
                "ENGR 2060",
                "HIST 2300",
                "HNRS 2125",
                "LART 1100",
                "MUED 1000",
                "PHIL 2000", "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",
                "RLGN 3120",
                "SOCI 2450",   # OR rule: F2 OR W7
                "SPED 2400",
            ],
        },
    },

    # ── F3 ────────────────────────────────────────────────────────────
    # HNRS 2110 satisfies F3 OR W3 (OR rule — not both)
    # 22-23/23-24: HNRS 2110 = 5 hrs (Honors Literature and History)
    # 24-25: HNRS 2110 = 3 hrs (renamed Honors Literature & Writing)
    "F3": {
        "label": "F3 Written Communication",
        "credits": 6,
        "courses": {
            "2022-23": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "2023-24": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "2024-25": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
        },
        "notes": (
            "ENGL 1100 / ENGL 1110 are placement-based alternatives. "
            "ENGL 1120 required. 2 WI courses beyond ENGL 1120 also required. "
            "HNRS 2110 satisfies F3 OR W3 (not both)."
        ),
    },

    # ── F4 ────────────────────────────────────────────────────────────
    # COMM 1000 required; plus one SI-designated course
    "F4": {
        "label": "F4 Speaking and Listening",
        "credits": 3,
        "required_courses": ["COMM 1000"],
        "si_courses_needed": 1,
        "notes": "COMM 1000 required. One SI-designated course also required. See SI list.",
    },

    # ── F5 ────────────────────────────────────────────────────────────
    # 22-23: includes CPSC 1100, 1200, 1400; MATH 1220 not listed
    # 23-24: adds MATH 1220; drops CPSC 1400
    # 24-25: drops CPSC 1100, 1200 (keeps CPSC 2020); adds MATH 1220
    "F5": {
        "label": "F5 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2022-23": [
                "CPSC 1100", "CPSC 1200", "CPSC 1400", "CPSC 2020",
                "LEAD 3100",
                "MATH 1100", "MATH 1250", "MATH 1300", "MATH 1400",
                "MATH 2010", "MATH 2120",
                "PSYC 2440",
            ],
            "2023-24": [
                "CPSC 1100", "CPSC 1200", "CPSC 2020",
                "LEAD 3100",
                "MATH 1100", "MATH 1220", "MATH 1250", "MATH 1300", "MATH 1400",
                "MATH 2010", "MATH 2120",
                "PSYC 2440",
            ],
            "2024-25": [
                "CPSC 2020",
                "LEAD 3100",
                "MATH 1100", "MATH 1220", "MATH 1250", "MATH 1300",
                "MATH 2010", "MATH 2120",
                "PSYC 2440",
            ],
        },
    },

    # ── F6 ────────────────────────────────────────────────────────────
    "F6": {
        "label": "F6 Biblical Literacy",
        "credits": 3,
        "courses": {
            "2022-23": ["BIBL 2000"],
            "2023-24": ["BIBL 2000"],
            "2024-25": ["BIBL 2000"],
        },
    },

    # ── F7 ────────────────────────────────────────────────────────────
    "F7": {
        "label": "F7 Personal Wellness",
        "credits": 2,
        "courses": {
            "2022-23": ["DANC 3060", "NURS 1210", "PEHS 1000"],
            "2023-24": ["DANC 3060", "NURS 1210", "PEHS 1000"],
            "2024-25": ["DANC 3060", "NURS 1210", "PEHS 1000"],
        },
        "notes": "PEHS 1000 test-out available for prior practical experience.",
    },

    # ── W1 ────────────────────────────────────────────────────────────
    # BIBL/RLGN 3000 is also WI
    # HNRS 3325 Honors only
    "W1": {
        "label": "W1 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BIBL 3000", "RLGN 3000",   # cross-listed, also WI
                "BIBL 3410",
                "HNRS 3325",
                "PHIL 3250", "RLGN 3250",   # cross-listed
                "RLGN 3010", "RLGN 3020", "RLGN 3100",
            ],
            "2023-24": [
                "BIBL 3000", "RLGN 3000",
                "BIBL 3410",
                "HNRS 3325",
                "PHIL 3250", "RLGN 3250",
                "RLGN 3010", "RLGN 3020", "RLGN 3100",
            ],
            "2024-25": [
                "BIBL 3000", "RLGN 3000",
                "BIBL 3410",
                "HNRS 3325",
                "PHIL 3250", "RLGN 3250",
                "RLGN 3010", "RLGN 3020", "RLGN 3100",
            ],
        },
    },

    # ── W2 ────────────────────────────────────────────────────────────
    # 22-23: includes PHYS 1140 (Musical Acoustics); 24-25 drops PHYS 1140 and PHYS 1240
    # CPSC 2040 added in 23-24
    "W2": {
        "label": "W2 Scientific Ways of Knowing",
        "credits": 4,
        "courses": {
            "2022-23": [
                "BIOL 1000", "BIOL 2070", "BIOL 2080", "BIOL 2210",
                "CHEM 1000", "CHEM 2110",
                "EXSC 2140",
                "HNRS 2210",
                "PHYS 1000", "PHYS 1020", "PHYS 1140", "PHYS 1240",
                "PHYS 2140", "PHYS 2240",
                "PSYC 3210",
            ],
            "2023-24": [
                "BIOL 1000", "BIOL 2070", "BIOL 2080", "BIOL 2210",
                "CHEM 1000", "CHEM 2110",
                "CPSC 2040",
                "EXSC 2140",
                "HNRS 2210",
                "PHYS 1000", "PHYS 1020", "PHYS 1240",
                "PHYS 2140", "PHYS 2240",
                "PSYC 3210",
            ],
            "2024-25": [
                "BIOL 1000", "BIOL 2070", "BIOL 2080", "BIOL 2210",
                "CHEM 1000", "CHEM 2110",
                "CPSC 2040",
                "EXSC 2140",
                "HNRS 2210",
                "PHYS 1000", "PHYS 1020", "PHYS 1240",
                "PHYS 2140", "PHYS 2240",
                "PSYC 3210",
            ],
        },
    },

    # ── W3 ────────────────────────────────────────────────────────────
    # HNRS 2110 satisfies W3 OR F3 (OR rule)
    # 24-25: HNRS 2300 (Honors History) replaces HNRS 2110 in W3 list
    "W3": {
        "label": "W3 Civic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "HIST 2000", "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR rule: W3 OR F3
                "POSC 2100",
            ],
            "2023-24": [
                "HIST 2000", "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR rule: W3 OR F3
                "POSC 2100",
            ],
            "2024-25": [
                "HIST 2000", "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR rule: W3 OR F3
                "HNRS 2300",   # new in 24-25 (Honors History)
                "POSC 2100",
            ],
        },
    },

    # ── W4 ────────────────────────────────────────────────────────────
    # Three paths:
    #   AE  = one 3-hr integrative course (satisfies W4 alone)
    #   AP + AX = one Appreciation course + one Experiential course
    # ENGL 2500 is AP and also WI-designated
    # COMM 2550 is AE and also SI-designated (22-23 only — not in 23-24 AE list)
    # ARTH 2000 (22-23) → ARTH 3040 (23-24+)
    # 24-25 adds ENGL 3592 and ARTS 1210 in AP section (at 2 hrs)
    "W4": {
        "label": "W4 Aesthetic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": {
                "AE_integrative": [
                    "ARTH 2000",
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "COMM 2550",   # also SI
                    "ENGL 3590",
                    "MUSC 2210",
                ],
                "AP_appreciation": [
                    "DANC 3510",
                    "ENGL 2500",   # also WI
                    "MUED 2110",
                    "MUSC 2110", "MUSC 2220",
                    "THEA 2350",
                ],
                "AX_experiential": [
                    "DANC 1120", "DANC 2120", "DANC 3120",
                    "DANC 1220", "DANC 2220", "DANC 3220", "DANC 4220",
                    "DANC 1320", "DANC 2320", "DANC 3320", "DANC 4320",
                    "DANC 1420", "DANC 2420", "DANC 3420", "DANC 4420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090",
                    "MUPF 1110", "MUPF 1220",
                    "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 4890",
                ],
            },
            "2023-24": {
                "AE_integrative": [
                    "ARTH 3040",
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "ENGL 3590",
                    "HNRS 3000",   # Honors only
                    "MUSC 2210",
                ],
                "AP_appreciation": [
                    "DANC 3510",
                    "ENGL 2500",   # also WI
                    "MUED 2110",
                    "MUSC 2110", "MUSC 2220",
                    "THEA 2350",
                ],
                "AX_experiential": [
                    "DANC 1120", "DANC 2120", "DANC 3120",
                    "DANC 1220", "DANC 2220", "DANC 3220", "DANC 4220",
                    "DANC 1320", "DANC 2320", "DANC 3320", "DANC 4320",
                    "DANC 1420", "DANC 2420", "DANC 3420", "DANC 4420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090",
                    "MUPF 1110", "MUPF 1220",
                    "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 4890",
                ],
            },
            "2024-25": {
                "AE_integrative": [
                    "ARTH 3040",
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "ENGL 3590", "ENGL 3592",
                    "HNRS 3000",   # Honors only
                ],
                "AP_appreciation": [
                    "ARTS 1210",   # listed at 2 hrs in AP section (double-listed)
                    "DANC 3510",
                    "ENGL 2500",   # also WI
                    "MUSC 2110", "MUSC 2220",
                    "THEA 2350",
                ],
                "AX_experiential": [
                    "DANC X120", "DANC X220", "DANC X320", "DANC X420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090",
                    "MUPF 1110", "MUPF 1220",
                    "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 4890",
                ],
            },
        },
    },

    # ── W5 ────────────────────────────────────────────────────────────
    # Official W5 list from PDFs — does NOT include BSNS 3420 or POSC courses
    # HNRS 3311 (22-23 only, Honors Social Science)
    "W5": {
        "label": "W5 Social & Behavioral Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "ECON 2010",
                "EDUC 2110", "PSYC 2110",
                "HNRS 3311",   # Honors only
                "LEAD 2300",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
            "2023-24": [
                "ECON 2010",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
            "2024-25": [
                "ECON 2010",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
        },
    },

    # ── W6 ────────────────────────────────────────────────────────────
    # Modern + Ancient languages
    # MLAN 2000 is W6 OR W7 (OR rule)
    # SPAN 3010 is W6 and also WI
    "W6": {
        "label": "W6 Modern Languages",
        "credits": 4,
        "courses": {
            "2022-23": [
                "FREN 1010", "FREN 1020", "FREN 2010", "FREN 2020",
                "GERM 1010", "GERM 1020", "GERM 2010",
                "MLAN 2000",   # OR rule: W6 OR W7
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010",   # also WI
                # Ancient languages
                "BIBL 2110", "BIBL 2120",
                "BIBL 2210", "BIBL 2220",
            ],
            "2023-24": [
                "FREN 1010", "FREN 1020", "FREN 2010", "FREN 2020",
                "GERM 1010", "GERM 1020", "GERM 2010",
                "MLAN 2000",   # OR rule: W6 OR W7
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010",   # also WI
                "BIBL 2110", "BIBL 2120",
                "BIBL 2210", "BIBL 2220",
            ],
            "2024-25": [
                "FREN 1010", "FREN 1020", "FREN 2010", "FREN 2020",
                "GERM 1010", "GERM 1020", "GERM 2010",
                "MLAN 2000",   # OR rule: W6 OR W7
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010",   # also WI
                "BIBL 2110", "BIBL 2120",
                "BIBL 2210", "BIBL 2220",
            ],
        },
        "notes": (
            "One language course (4 hrs) based on placement required, "
            "plus one additional global/intercultural or language course (W7). "
            "MLAN 2000 may satisfy W6 OR W7 — not both."
        ),
    },

    # ── W7 ────────────────────────────────────────────────────────────
    # MLAN 2000 is W6 OR W7 (OR rule)
    # SOCI 2450 is F2 OR W7 (OR rule)
    # Several courses are also WI: HIST 3260, 3300, 3425; POSC 3320, 3450; ENGR 2090
    # HNRS 3221 is Honors only and WI
    # LEAD 4550 is Adults only
    "W7": {
        "label": "W7 Global/Intercultural Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BIBL 3310",
                "BSNS 3120",   # also WI
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGL 2220",
                "ENGR 2080",
                "ENGR 2090",   # also WI
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260",   # also WI
                "HIST 3280",
                "HIST 3300",   # also WI
                "HIST 3320", "RLGN 3320",   # cross-listed HIST/RLGN 3320
                "HIST 3360", "HIST 3370",
                "HIST 3425",   # also WI
                "HNRS 3221",   # Honors only, also WI
                "LEAD 4550",   # Adults only
                "MLAN 2000",   # OR rule: W6 OR W7
                "MLAN 3400",
                "MUSC 2330",
                "POSC 3320",   # also WI
                "POSC 3450",   # also WI
                "SOCI 2450",   # OR rule: F2 OR W7
                "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
            ],
            "2023-24": [
                "BIBL 3310",
                "BSNS 3120",
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGL 2220",
                "ENGR 2080",
                "ENGR 2090",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260",
                "HIST 3280",
                "HIST 3300",
                "HIST 3320", "RLGN 3320",
                "HIST 3360", "HIST 3370",
                "HIST 3425",
                "HNRS 3221",
                "LEAD 4550",
                "MLAN 2000",
                "MLAN 3400",
                "MUSC 2330",
                "POSC 3320",
                "POSC 3450",
                "SOCI 2450",
                "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
            ],
            "2024-25": [
                "BIBL 3310",
                "BSNS 3120",
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGL 2220",
                "ENGR 2080",
                "ENGR 2090",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260",
                "HIST 3280",
                "HIST 3300",
                "HIST 3320",   # 24-25 PDF lists as HIST 3320 (no RLGN cross-list)
                "HIST 3360", "HIST 3370",
                "HIST 3425",
                "HNRS 3221",
                "LEAD 4550",
                "MLAN 2000",
                "MLAN 3400",
                "MUSC 2330",
                "POSC 3320",
                "POSC 3450",
                "SOCI 2450",
                "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
            ],
        },
    },

    # ── W8 ────────────────────────────────────────────────────────────
    # Auto-satisfied when F1 (LART 1050) is completed
    # Per-major course list is in W8_BY_MAJOR below
    "W8": {
        "label": "W8 Experiential Ways of Knowing",
        "credits": 0,
        "auto_satisfy_if": "F1",
        "auto_display_course": "BSNS 1050",
        "notes": (
            "Fulfilled by a course, internship, practicum, capstone, "
            "clinical, or approved academic department activity. "
            "Auto-satisfied when F1 (LART 1050) is completed for FSB students."
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────
# WI — Writing Intensive courses (all years)
# Source: Advanced Writing Competency lists in LA PDFs
# ─────────────────────────────────────────────────────────────────────

WI_COURSES = {
    "2022-23": [
        # From F3 / WI designation
        "ENGL 1120",
        # From W1
        "BIBL 3000", "RLGN 3000",
        # From W4
        "ENGL 2500",
        # From W6
        "SPAN 3010",
        # From W7
        "BSNS 3120",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "HNRS 3221",
        "POSC 3320", "POSC 3450",
        # From Advanced Writing Competency list (22-23 PDF pages 3-4)
        "ACCT 4900",
        "ARTH 3030",
        "ATRG 3440", "ATRG 4550",
        "BIOL 4050",
        "BSNS 3330", "BSNS 4910",
        "CHEM 3100",
        "CMIN 4250",
        "COMM 2130", "COMM 2160", "COMM 3130", "COMM 3220", "COMM 3230", "COMM 3340",
        "CPSC 4950",
        "CRIM 2510", "SOCI 2510",
        "DANC 3010",
        "EDUC 3120", "EDUC 4120", "EDUC 4710",
        "ENGL 3050", "ENGL 3110", "ENGL 3120", "ENGL 3140", "ENGL 3160",
        "ENGL 3180", "ENGL 3190", "ENGL 3500", "ENGL 3551", "ENGL 3580",
        "ENGL 4550", "ENGL 4700", "ENGL 4910",
        "ENGR 2090", "ENGR 4950", "ENGR 4960",
        "EXSC 3480", "EXSC 4910",
        "HIST 3440", "HIST 3451", "HIST 3452", "HIST 3470", "HIST 3510",
        "LEAD 4990",
        "MLAN 4900",
        "MUBS 3350", "MUBS 3500",
        "MUSC 3110", "MUSC 3120", "MUSC 3130", "MUSC 3170", "MUSC 3180",
        "NURS 3391", "NURS 4470",
        "PEHS 3340",
        "PETE 2250", "PETE 4300",
        "PHYS 3100",
        "POSC 2400", "POSC 3211", "POSC 3310",
        "PSYC 2010",
        "PSYC 4510",
        "PUBH 3010", "PSYC 3010", "SOCI 3010",
        "PUBH 3700", "SOCI 3700",
        "RLGN 3300",
        "SPAN 3010",
        "SPED 3120",
    ],
    "2023-24": [
        "ENGL 1120",
        "BIBL 3000", "RLGN 3000",
        "ENGL 2500",
        "SPAN 3010",
        "BSNS 3120",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "HNRS 3221",
        "POSC 3320", "POSC 3450",
        "ACCT 4900",
        "BIOL 4050",
        "BSNS 3330", "BSNS 4910",
        "CHEM 3100",
        "CMIN 4250",
        "COMM 2130", "COMM 2160", "COMM 3130", "COMM 3220", "COMM 3230", "COMM 3340",
        "CPSC 4960",
        "CRIM 2510", "SOCI 2510",
        "DANC 3010",
        "EDUC 3120", "EDUC 4120", "EDUC 4710",
        "ENGL 3050", "ENGL 3110", "ENGL 3120", "ENGL 3140", "ENGL 3160",
        "ENGL 3180", "ENGL 3190", "ENGL 3580", "ENGL 4700", "ENGL 4910",
        "ENGR 4950", "ENGR 4960",
        "EXSC 3480", "EXSC 4910",
        "HIST 3440", "HIST 3451", "HIST 3452", "HIST 3470", "HIST 3510",
        "LEAD 4990",
        "MLAN 4900",
        "MUBS 3350", "MUBS 3500",
        "MUSC 3110", "MUSC 3120", "MUSC 3130", "MUSC 3170", "MUSC 3180",
        "NURS 3391", "NURS 4470",
        "PEHS 3340",
        "PETE 2250", "PETE 4300",
        "POSC 2400", "POSC 3211", "POSC 3310",
        "PSYC 2010",
        "PSYC 4510",
        "PUBH 3010", "PSYC 3010", "SOCI 3010",
        "PUBH 3700", "SOCI 3700",
        "RLGN 3300",
        "SPED 3120",
    ],
    "2024-25": [
        "ENGL 1120",
        "BIBL 3000", "RLGN 3000",
        "ENGL 2500",
        "SPAN 3010",
        "BSNS 3120",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "HNRS 3221",
        "POSC 3320", "POSC 3450",
        "ACCT 4900",
        "BIOL 4050",
        "BSNS 3330", "BSNS 4910",
        "CHEM 3100",
        "CMIN 4250",
        "COMM 2130", "COMM 2160", "COMM 3130", "COMM 3220", "COMM 3230", "COMM 3340",
        "CPSC 4960",
        "CRIM 2510", "SOCI 2510",
        "DANC 3010",
        "EDUC 3120", "EDUC 4120", "EDUC 4710",
        "ENGL 3050", "ENGL 3110", "ENGL 3120", "ENGL 3140", "ENGL 3160",
        "ENGL 3180", "ENGL 3190", "ENGL 3580", "ENGL 4700", "ENGL 4910",
        "ENGR 4950", "ENGR 4960",
        "EXSC 3480", "EXSC 4910",
        "HIST 3440", "HIST 3470", "HIST 3510",
        "LEAD 4990",
        "MLAN 4900",
        "MUBS 3350", "MUBS 3500",
        "MUSC 3110", "MUSC 3120", "MUSC 3130", "MUSC 3170", "MUSC 3180",
        "NURS 3391", "NURS 4470",
        "PEHS 3340",
        "PETE 2250", "PETE 4300",
        "POSC 2400", "POSC 3211", "POSC 3310",
        "PSYC 2010",
        "PSYC 4510",
        "PUBH 3010", "PSYC 3010", "SOCI 3010",
        "PUBH 3700", "SOCI 3700",
        "RLGN 3300",
        "SPED 3120",
    ],
}


# ─────────────────────────────────────────────────────────────────────
# SI — Speaking Intensive courses (all years)
# Source: Speaking Intensive lists in LA PDFs (COMM 1000 prerequisite)
# ─────────────────────────────────────────────────────────────────────

SI_COURSES = {
    "2022-23": [
        # From 22-23 PDF speaking intensive list
        "ARTS 4950",
        "ATRG 4910",
        "BSNS 3210", "BSNS 4480",
        "CHEM 4910", "BIOL 4910", "PHYS 4910",
        "CHEM 4920", "BIOL 4920", "PHYS 4920",
        "CMIN 3910",
        "COMM 2550", "COMM 3420",
        "CPSC 4960",
        "CRIM 4900",
        "DANC 3050",
        "EDUC 4120", "EDUC 4710",
        "ENGL 2220", "ENGL 3050",
        "ENGR 4960",
        "EXSC 4920",
        "HIST 2300", "HIST 2350", "HIST 4930",
        "HNRS 2125",
        "LART 4500",
        "LEAD 4990",
        "MATH 4000",
        "MLAN 4900",
        "MUBS 3350", "BSNS 3330",
        "MUED 3110", "MUED 3350",
        "MUSC 4955",
        "MUTR 3210", "THEA 3210",
        "NURS 4960",
        "PETE 4900",
        "POSC 3211", "POSC 3212", "POSC 3370",
        "PSYC 3200", "PSYC 4110", "PSYC 4210", "PSYC 4520",
        "SOCI 4200", "SOCI 4950",
        "SOWK 4850",
        "SPAN 3020",
        "THEA 3210",
    ],
    "2023-24": [
        "ARTH 3040",
        "ARTG 4910",
        "BSNS 3210", "BSNS 4480",
        "CHEM 4910", "BIOL 4910", "PHYS 4910",
        "CHEM 4920", "BIOL 4920", "PHYS 4920",
        "CMIN 3050", "CMIN 3910",
        "COMM 2550", "COMM 3420",
        "CPSC 4950",
        "CRIM 4900",
        "DANC 3050",
        "EDUC 4120", "EDUC 4710",
        "ENGL 2220", "ENGL 3050",
        "EXSC 4920",
        "HIST 2300", "HIST 2350", "HIST 4930",
        "HNRS 2125",
        "LART 4500",
        "LEAD 4990",
        "MATH 4000",
        "MLAN 4900",
        "MUBS 3350", "BSNS 3330",
        "MUED 3110", "MUED 3350",
        "MUSC 4955",
        "MUTR 3210", "THEA 3210",
        "NURS 4960",
        "PETE 4960",
        "POSC 3211", "POSC 3212", "POSC 3370",
        "PSYC 3200", "PSYC 4110", "PSYC 4210", "PSYC 4520",
        "SOCI 4200", "SOCI 4950",
        "SOWK 4850",
        "SPAN 3020",
    ],
    "2024-25": [
        "ARTH 3040",
        "ARTG 4910",
        "BSNS 3210", "BSNS 4480",
        "CHEM 4910", "BIOL 4910", "PHYS 4910",
        "CHEM 4920", "BIOL 4920", "PHYS 4920",
        "CMIN 3050", "CMIN 3910",
        "COMM 2550", "COMM 3420",
        "CPSC 4950",
        "CRIM 4900",
        "DANC 3050",
        "EDUC 4120", "EDUC 4710",
        "ENGL 2220", "ENGL 3050",
        "EXSC 4920",
        "HIST 2300", "HIST 2350", "HIST 4930",
        "HNRS 2125",
        "LART 4500",
        "LEAD 4990",
        "MATH 4000",
        "MLAN 4900",
        "MUBS 3350", "BSNS 3330",
        "MUED 3110", "MUED 3350",
        "MUSC 4955",
        "MUTR 3210", "THEA 3210",
        "NURS 4960",
        "PETE 4960",
        "POSC 3211", "POSC 3212", "POSC 3370",
        "PSYC 3200", "PSYC 4110", "PSYC 4210", "PSYC 4520",
        "SOCI 4200", "SOCI 4950",
        "SOWK 4850",
        "SPAN 3020",
    ],
}


# ─────────────────────────────────────────────────────────────────────
# OR Cross-Listings
# A course satisfying one of these areas does NOT also satisfy the other
# ─────────────────────────────────────────────────────────────────────

OR_CROSS_LISTINGS = {
    "HNRS 2110": ["F3", "W3"],
    "MLAN 2000": ["W6", "W7"],
    "SOCI 2450": ["F2", "W7"],
}


# ─────────────────────────────────────────────────────────────────────
# NEW FRAMEWORK: 2025-26 — Raven Core + AU Experience
# ─────────────────────────────────────────────────────────────────────

LA_RAVEN_CORE_2526 = {
    "year": "2025-26",
    "icc_exemption": (
        "Students completing Indiana College Core (ICC) are EXEMPT from RC1-RC6 "
        "but must complete AU Experience (AU1-AU6)."
    ),

    "RAVEN_CORE": {
        "label": "Raven Core",
        "total_credits": 30,
        "note": "At least one course in each RC category required. ICC-exempt students skip RC entirely.",

        "RC1": {
            "label": "RC1 Written Communication",
            "max_credits": 6,
            "courses": ["ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "grade_required": {"ENGL 1110": "C-", "ENGL 1120": "C-", "HNRS 2110": "C-"},
        },
        "RC2": {
            "label": "RC2 Speaking and Listening",
            "max_credits": 6,
            "courses": ["COMM 1000", "COMM 3310", "PSYC 2100"],
        },
        "RC3": {
            "label": "RC3 Quantitative Reasoning",
            "max_credits": 8,
            "courses": [
                "CPSC 2020",
                "LEAD 3100",
                "MATH 1100", "MATH 1250", "MATH 1300",
                "MATH 2010", "MATH 2120",
                "PSYC 2440",
            ],
        },
        "RC4": {
            "label": "RC4 Scientific Ways of Knowing",
            "max_credits": 8,
            "courses": [
                "BIOL 1000", "BIOL 2210", "BIOL 2230",
                "CHEM 1000", "CHEM 2110",
                "EXSC 2140",
                "HNRS 2210",
                "PHYS 1020", "PHYS 2140", "PHYS 2240",
            ],
        },
        "RC5": {
            "label": "RC5 Social & Behavioral Ways of Knowing",
            "max_credits": 12,
            "courses": [
                "BSNS 3420",
                "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020",
            ],
        },
        "RC6": {
            "label": "RC6 Humanistic & Artistic Ways of Knowing",
            "max_credits": 12,
            "courses": [
                "ENGL 2500", "ENGL 3590",
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "HNRS 2300", "HNRS 3100",
                "MUSC 2110", "MUSC 3120", "MUSC 3130",
                "SPAN 1010", "SPAN 1020",
            ],
        },
    },

    "AU_EXPERIENCE": {
        "label": "AU Experience",
        "total_credits_range": (14, 17),
        "note": "Complete one course in each AU category.",

        "AU1": {
            "label": "AU1 Understanding College",
            "credits": 1,
            "courses": ["LART 1050"],
        },
        "AU2": {
            "label": "AU2 Biblical Literacy",
            "credits": 3,
            "courses": ["BIBL 2000"],
        },
        "AU3": {
            "label": "AU3 Christian Ways of Knowing",
            "credits": 3,
            "courses": ["BIBL 3410", "HNRS 3325", "RLGN 3010"],
        },
        "AU4": {
            "label": "AU4 Personal Wellness",
            "credits_range": (2, 3),
            "courses": [
                "EXSC 2440",
                "NURS 1210",
                "PEHS 1000",
                "PSYC 3500", "SOCI 3500",
                "RLGN 1100",
            ],
        },
        "AU5": {
            "label": "AU5 Civil Discourse & Conflict Transformation",
            "credits_range": (2, 3),
            "courses": [
                "BIOL 3510",
                "COMM 3200",
                "HIST 2300",
                "HNRS 2125",
                "LART 2000",
                "PACT 2100",
                "PHIL 2120",
                "PSYC 3200",
                "RLGN 3120",
                "RLGN 3250", "PHIL 3250",
                "SOCI 2450",
                "SPED 2400",
            ],
        },
        "AU6": {
            "label": "AU6 Global Ways of Knowing",
            "credits_range": (3, 4),
            "courses": [
                "BIBL 3310",
                "BSNS 3120",
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGL 2220",
                "ENGR 2080", "ENGR 2090",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260", "HIST 3280", "HIST 3300", "HIST 3320",
                "HIST 3360", "HIST 3370", "HIST 3425",
                "HNRS 3221",
                "LEAD 4550",
                "MLAN 2000", "MLAN 3400",
                "MUSC 2330",
                "POSC 3320", "POSC 3450",
                "SOCI 2450", "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
            ],
        },
    },
}


# ─────────────────────────────────────────────────────────────────────
# Helper: framework lookup
# ─────────────────────────────────────────────────────────────────────

def get_la_framework(catalog_year: str) -> str:
    if catalog_year in ["2022-23", "2023-24", "2024-25"]:
        return "OLD_FRAMEWORK"
    elif catalog_year == "2025-26":
        return "RAVEN_CORE"
    raise ValueError(f"Unknown catalog year: {catalog_year}")


def get_la_requirements(catalog_year: str) -> dict:
    fw = get_la_framework(catalog_year)
    if fw == "OLD_FRAMEWORK":
        result = {}
        for section, data in LA_OLD_FRAMEWORK.items():
            if section == "years":
                continue
            entry = dict(data)
            for field in ["courses", "credits"]:
                if field in entry and isinstance(entry[field], dict):
                    entry[field] = entry[field].get(catalog_year, entry[field])
            if "si_courses" in entry and isinstance(entry["si_courses"], dict):
                entry["si_courses"] = entry["si_courses"].get(catalog_year, [])
            if "wi_courses" in entry and isinstance(entry["wi_courses"], dict):
                entry["wi_courses"] = entry["wi_courses"].get(catalog_year, [])
            result[section] = entry
        result["_WI_COURSES"] = WI_COURSES.get(catalog_year, [])
        result["_SI_COURSES"] = SI_COURSES.get(catalog_year, [])
        result["_OR_CROSS_LISTINGS"] = OR_CROSS_LISTINGS
        return result
    else:
        return LA_RAVEN_CORE_2526


def is_wi_course(course_code: str, catalog_year: str) -> bool:
    return course_code in WI_COURSES.get(catalog_year, [])


def is_si_course(course_code: str, catalog_year: str) -> bool:
    return course_code in SI_COURSES.get(catalog_year, [])


def get_or_cross_listing(course_code: str) -> list:
    return OR_CROSS_LISTINGS.get(course_code, [])


def course_satisfies_la(course_code: str, catalog_year: str) -> list:
    """Return list of LA requirement areas this course satisfies for the given year."""
    satisfied = []
    fw = get_la_framework(catalog_year)

    if fw == "OLD_FRAMEWORK":
        reqs = get_la_requirements(catalog_year)
        for section, data in reqs.items():
            if section.startswith("_"):
                continue
            courses = data.get("courses", [])
            # W4 uses a nested dict structure
            if isinstance(courses, dict):
                all_courses = []
                for v in courses.values():
                    if isinstance(v, list):
                        all_courses.extend(v)
                courses = all_courses
            if course_code in courses:
                satisfied.append(section)
        if is_wi_course(course_code, catalog_year) and "WI" not in satisfied:
            satisfied.append("WI")
        if is_si_course(course_code, catalog_year) and "SI" not in satisfied:
            satisfied.append("SI")
    else:
        data = LA_RAVEN_CORE_2526
        for rc_key, rc_data in data["RAVEN_CORE"].items():
            if rc_key in ("label", "total_credits", "note"):
                continue
            if isinstance(rc_data, dict) and course_code in rc_data.get("courses", []):
                satisfied.append(rc_key)
        for au_key, au_data in data["AU_EXPERIENCE"].items():
            if au_key in ("label", "total_credits_range", "note"):
                continue
            if isinstance(au_data, dict) and course_code in au_data.get("courses", []):
                satisfied.append(au_key)

    return satisfied


# ─────────────────────────────────────────────────────────────────────
# W8 Experiential — Per-Major Course Lookup
# Source: W8 Experiential Ways of Knowing sheet (updated 11/14/2023)
# ─────────────────────────────────────────────────────────────────────

W8_BY_MAJOR = {
    # FSB majors
    "accounting": {
        "courses": ["ACCT 2020", "ACCT 3500", "ACCT 3860", "ACCT 4020", "ACCT 4800", "BSNS 1050", "BSNS 4800"],
        "required_in_major": [],
    },
    "business_analytics": {
        "courses": ["BSNS 1050"],
        "required_in_major": [],
    },
    "finance": {
        "courses": ["BSNS 1050", "BSNS 4150", "BSNS 4800"],
        "required_in_major": [],
    },
    "global_business": {
        "courses": ["BSNS 1050", "BSNS 3850", "BSNS 4800"],
        "required_in_major": [],
    },
    "management": {
        "courses": ["BSNS 1050", "BSNS 2550", "BSNS 4240", "BSNS 4310", "BSNS 4500", "BSNS 4800"],
        "required_in_major": [],
    },
    "engineering_management": {
        "courses": ["BSNS 1050"],
        "required_in_major": [],
    },
    "marketing": {
        "courses": ["BSNS 1050", "BSNS 2810", "BSNS 3130", "BSNS 3210", "BSNS 4110", "BSNS 4550", "BSNS 4800"],
        "required_in_major": [],
    },
    "sport_marketing": {
        "courses": ["BSNS 1050", "BSNS 4110", "BSNS 4330", "BSNS 4560", "BSNS 4800"],
        "required_in_major": ["BSNS 4800"],
    },
    "business_integrative_leadership": {
        "courses": ["LEAD 4990"],
        "required_in_major": ["LEAD 4990"],
    },
    # Non-FSB majors
    "psychology": {
        "courses": ["PSYC 2850", "PSYC 3450", "PSYC 4100", "PSYC 4210", "PSYC 4520"],
        "no_required_experiential": True,
    },
    "cinema_media_arts": {
        "courses": ["COMM 4800"],
        "required_in_major": ["COMM 4800"],
    },
    "public_relations": {
        "courses": ["COMM 4800"],
        "required_in_major": ["COMM 4800"],
    },
    "journalism_multimedia": {
        "courses": ["COMM 4800"],
        "required_in_major": ["COMM 4800"],
    },
    "communication_studies": {
        "courses": ["COMM 4800"],
        "required_in_major": ["COMM 4800"],
    },
    "education_elementary": {
        "courses": ["EDUC 4800"],
        "required_in_major": ["EDUC 4800"],
    },
    "education_secondary": {
        "courses": ["EDUC 4800"],
        "required_in_major": ["EDUC 4800"],
    },
    "csf_complementary": {
        "courses": ["RLGN 4960"],
        "required_in_major": ["RLGN 4960"],
    },
    "math_ba": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "math_bs": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "math_economics_ba": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "math_finance_ba": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "math_teaching_ba": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "math_decision_science_ba": {"courses": ["MATH 4000"], "required_in_major": ["MATH 4000"]},
    "exercise_science": {
        "courses": ["EXSC 4160", "EXSC 4800"],
        "required_in_major": [],
    },
    "sport_recreational_leadership": {
        "courses": ["SPRL 4850"],
        "required_in_major": ["SPRL 4850"],
    },
    "nursing_bsn": {
        "courses": ["NURS 4560", "NURS 4950", "NURS 4960", "NURS 4970"],
        "required_in_major": [],
    },
    "history": {
        "courses": [
            "HIST 2300", "HIST 3260", "HIST 4700", "HIST 4800", "HIST 4915", "HIST 4930",
            "POSC 2810", "POSC 4800", "POSC 4810", "POSC 4820", "POSC 4860", "POSC 4915",
            "EDUC 4010",
        ],
        "also": "POSC 2840 Model UN (2 semesters), study-abroad courses",
    },
    "political_science": {
        "courses": ["POSC 2810", "POSC 4800", "POSC 4810", "POSC 4820", "POSC 4860", "POSC 4915"],
        "also": "POSC 2840 Model UN (2 semesters), study-abroad courses",
    },
    "polsci_philosophy_economics": {
        "courses": ["POSC 2810", "POSC 4800", "POSC 4810", "POSC 4820", "POSC 4860", "POSC 4915"],
        "also": "POSC 2840 Model UN (2 semesters), study-abroad courses",
    },
    "international_relations": {
        "courses": [
            "HIST 2300", "HIST 3260", "HIST 4700", "HIST 4800", "HIST 4915", "HIST 4930",
            "POSC 2810", "POSC 4800", "POSC 4810", "POSC 4820", "POSC 4860", "POSC 4915",
            "EDUC 4010",
        ],
        "no_required_experiential": True,
        "also": "POSC 2840 Model UN (2 semesters), study-abroad courses",
    },
    "national_security": {
        "courses": ["POSC 4800", "POSC 4810", "POSC 4820", "POSC 4860", "POSC 4915", "POSC 4930"],
        "also": "POSC 2840 Model UN (2 semesters)",
    },
    "criminal_justice": {
        "courses": ["CRIM 4810"],
        "required_in_major": ["CRIM 4810"],
    },
    "criminal_justice_online": {
        "courses": ["CRIM 4810"],
        "required_in_major": ["CRIM 4810"],
    },
    "social_work": {
        "courses": ["SOWK 4850"],
        "required_in_major": ["SOWK 4850"],
    },
    "spanish": {
        "courses": ["FLAN 3500"],
        "required_in_major": [],
    },
    "voice_performance_bmus": {
        "courses": ["MUPF 4540", "MUPF 4550", "MUPF 4560", "MUPF 4570", "MUPF 4580", "MUPF 4590"],
        "required_in_major": [],
    },
    "instrumental_performance_bmus": {
        "courses": ["MUPF 4540", "MUPF 4550", "MUPF 4560", "MUPF 4570", "MUPF 4580", "MUPF 4590"],
        "required_in_major": [],
    },
    "musical_theatre_bmus": {
        "courses": ["MUTR 4500", "MUPF 4540"],
        "required_in_major": ["MUTR 4500", "MUPF 4540"],
    },
    "worship_arts_ba": {
        "courses": ["MUSC 3800"],
        "required_in_major": ["MUSC 3800"],
    },
    "musical_theatre_ba": {
        "courses": ["MUPF 1170", "MUPF 4910"],
        "required_in_major": [],
    },
    "music_ba": {
        "courses": ["MUSC 4950", "MUSC 4955"],
        "required_in_major": [],
    },
    "music_business": {
        "courses": ["MUBS 4800", "BSNS 4810"],
        "required_in_major": [],
    },
    "songwriting": {
        "courses": ["MUBS 4500"],
        "required_in_major": [],
    },
    "dance": {
        "courses": ["DANC 4800", "DANC 4910"],
        "required_in_major": [],
    },
    "theatre": {
        "courses": ["THEA 4800"],
        "required_in_major": ["THEA 4800"],
    },
    "cs_ba": {
        "courses": ["CPSC 2800", "CPSC 3800", "CPSC 4800", "CPSC 4960"],
        "no_required_experiential": True,
    },
    "cs_bs": {
        "courses": ["CPSC 2800", "CPSC 3800", "CPSC 4800", "CPSC 4960"],
        "no_required_experiential": True,
    },
    "data_science_ba": {
        "courses": ["CPSC 4970"],
        "required_in_major": [],
    },
    "data_science_bs": {
        "courses": ["CPSC 4970"],
        "required_in_major": [],
    },
    "professional_development_ba": {
        "courses": ["LART 4500"],
        "required_in_major": ["LART 4500"],
    },
    "biochemistry_ba": {
        "courses": ["CHEM 4920"],
        "required_in_major": [],
    },
    "biochemistry_bs": {
        "courses": ["CHEM 4920"],
        "required_in_major": [],
    },
    "electrical_engineering_bs": {
        "courses": ["ENGR 4960"],
        "required_in_major": ["ENGR 4960"],
    },
    "mechanical_engineering_bs": {
        "courses": ["ENGR 4960"],
        "required_in_major": ["ENGR 4960"],
    },
    "mechatronics_engineering_bs": {
        "courses": ["ENGR 4960"],
        "required_in_major": ["ENGR 4960"],
    },
    "civil_engineering_bs": {
        "courses": ["ENGR 4960"],
        "required_in_major": ["ENGR 4960"],
    },
    "computer_engineering_bs": {
        "courses": ["CPSC 2800", "CPSC 3800", "CPSC 4800", "CPSC 4960", "ENGR 4960"],
        "required_in_major": [],
    },
    "public_history": {
        "courses": ["HIST 4800"],
        "required_in_major": ["HIST 4800"],
    },
    "public_health_ba": {
        "courses": ["PUBH 4950", "NURS 4950", "PUBH 4810", "SOCI 4810"],
        "required_in_major": [],
    },
    "public_health_bs": {
        "courses": ["PUBH 4950", "NURS 4950", "PUBH 4810", "SOCI 4810"],
        "required_in_major": [],
    },
    "cybersecurity_major": {
        "courses": ["CPSC 4480", "CPSC 4820", "CPSC 4970"],
        "required_in_major": [],
    },
    "biology_ba":  {"courses": ["LAWK 18EC"], "no_required_experiential": True},
    "biology_bs":  {"courses": ["LAWK 18EC"], "no_required_experiential": True},
}


def get_w8_courses_for_major(major_key: str) -> dict:
    return W8_BY_MAJOR.get(major_key, {
        "courses": ["LAWK 18EC"],
        "no_required_experiential": True,
        "notes": "No W8 course defined for this major — exception process applies",
    })


def course_satisfies_w8(course_code: str, major_key: str) -> bool:
    w8_data = get_w8_courses_for_major(major_key)
    return course_code in w8_data.get("courses", [])
