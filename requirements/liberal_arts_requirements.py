"""
Anderson University — Liberal Arts Requirements
All 4 catalog years: 2022-23, 2023-24, 2024-25, 2025-26
Built from official AU Academic Advising LA Program Requirements PDFs.

Old Framework (22-23 through 24-25): F1-F7 Foundational Skills + W1-W8 Ways of Knowing
New Framework (25-26): Raven Core (RC1-RC6) + AU Experience (AU1-AU6)

HONORS NOTES:
- HNRS 2110 satisfies F3 OR W3 (22-23 through 24-25) — counts for only one
- HNRS 2110 satisfies RC1 in 25-26
- HNRS 2125 satisfies F2 (and SI cross-listing)
- HNRS 2210 satisfies W2
- HNRS 2300 satisfies W3 (24-25 only)
- HNRS 3000 satisfies W4 AE (23-24, 24-25)
- HNRS 3221 satisfies W7 (24-25)
- HNRS 3311 satisfies W5 (all old-framework years)
- HNRS 3325 satisfies W1 (all old-framework years)

CROSS-LISTING RULES (from LA Requirement Application PDF, 23-24):
AND = satisfies both; OR = satisfies only one (engine enforces single-use for OR)
- ARTH 3040:   W4 AND SI
- BIBL/RLGN 3000: W1 AND WI
- BSNS 3120:   W7 AND WI
- COMM 2550:   W4 (AE) AND SI  [22-23 only]
- ENGL 2220:   W7 AND SI
- ENGL 2500:   W4 (AP) AND WI
- ENGL 3190:   F2 AND WI
- ENGL 3580:   F2 AND WI
- ENGR 2090:   W7 AND WI
- HIST 2300:   F2 AND SI
- HIST 3260:   W7 AND WI
- HIST 3300:   W7 AND WI
- HIST 3425:   W7 AND WI
- HNRS 2110:   F3 OR W3
- HNRS 2125:   F2 AND SI
- MLAN 2000:   W6 OR W7
- POSC 3320:   W7 AND WI
- POSC 3450:   W7 AND WI
- PSYC 3200:   F2 AND SI
- SOCI 2450:   F2 OR W7
- SPAN 3010:   W6 AND WI
- SPAN 3020:   W7 AND SI
"""

# ─────────────────────────────────────────────
# OLD FRAMEWORK: 2022-23 through 2024-25
# ─────────────────────────────────────────────

LA_OLD_FRAMEWORK = {
    "years": ["2022-23", "2023-24", "2024-25"],

    # ── F1 Understanding College ────────────────────────────────────────────
    "F1": {
        "label": "F1 Understanding College",
        "credits": 1,
        "courses": {
            "2022-23": ["LART 1050"],
            "2023-24": ["LART 1050"],
            "2024-25": ["LART 1050"],
        },
        "special_rule": "F1_SATISFIES_W8_FSB_ONLY",
    },

    # ── F2 Civil Discourse & Critical Reasoning ─────────────────────────────
    "F2": {
        "label": "F2 Civil Discourse & Critical Reasoning",
        "credits": {"2022-23": 2, "2023-24": 3, "2024-25": 3},
        "courses": {
            "2022-23": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "ENGL 3190",   # also WI
                "ENGL 3580",   # also WI
                "ENGR 2060",
                "HIST 2300",   # also SI
                "HNRS 2125",   # also SI
                "LART 1100",
                "MUED 1000",
                "PHIL 2000",
                "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",   # also SI
                "RLGN 3120",
                "SOCI 2450",   # OR W7
                "SPED 2400",
            ],
            "2023-24": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "COMM 3200",
                "ENGL 3190",   # also WI
                "ENGL 3580",   # also WI
                "ENGR 2060",
                "HIST 2300",   # also SI
                "HNRS 2125",   # also SI
                "LART 1100",
                "MUED 1000",
                "PHIL 2000",
                "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",   # also SI
                "RLGN 3120",
                "SOCI 2450",   # OR W7
                "SPED 2400",
            ],
            "2024-25": [
                "BIOL 3510", "PUBH 3510",
                "BSNS 3420",
                "CMIN 2270",
                "COMM 3200",
                "ENGL 3190",   # also WI
                "ENGL 3580",   # also WI
                "ENGR 2060",
                "HIST 2300",   # also SI
                "HNRS 2125",   # also SI
                "LART 1100",
                "MUED 1000",
                "PHIL 2000",
                "PHIL 2120",
                "POSC 2020",
                "PSYC 3200",   # also SI
                "RLGN 3120",
                "SOCI 2450",   # OR W7
                "SPED 2400",
            ],
        },
    },

    # ── F3 Written Communication ────────────────────────────────────────────
    # HNRS 2110 can satisfy F3 OR W3 (not both) — engine enforces single-use
    "F3": {
        "label": "F3 Written Communication",
        "credits": 6,
        "required_courses": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
        "notes": "ENGL 1100/1110 interchangeable by placement. HNRS 2110 satisfies F3 OR W3.",
    },

    # ── F4 Speaking and Listening ────────────────────────────────────────────
    "F4": {
        "label": "F4 Speaking and Listening",
        "credits": 3,
        "required_courses": ["COMM 1000"],
        "notes": "Plus one SI-designated course.",
    },

    # ── F5 Quantitative Reasoning ────────────────────────────────────────────
    "F5": {
        "label": "F5 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2022-23": [
                "CPSC 1100", "CPSC 1200", "CPSC 1400",
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

    # ── F6 Biblical Literacy ─────────────────────────────────────────────────
    "F6": {
        "label": "F6 Biblical Literacy",
        "credits": 3,
        "courses": {
            "2022-23": ["BIBL 2000"],
            "2023-24": ["BIBL 2000"],
            "2024-25": ["BIBL 2000"],
        },
    },

    # ── F7 Personal Wellness ─────────────────────────────────────────────────
    "F7": {
        "label": "F7 Personal Wellness",
        "credits": 2,
        "courses": {
            "2022-23": ["PEHS 1000", "DANC 3060", "NURS 1210"],
            "2023-24": ["PEHS 1000", "DANC 3060", "NURS 1210"],
            "2024-25": ["PEHS 1000", "DANC 3060", "NURS 1210"],
        },
    },

    # ── W1 Christian Ways of Knowing ─────────────────────────────────────────
    "W1": {
        "label": "W1 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BIBL 3000", "RLGN 3000",   # cross-listed, also WI
                "BIBL 3410",
                "HNRS 3325",                 # Honors only
                "PHIL 3250", "RLGN 3250",
                "RLGN 3010",
                "RLGN 3020",
                "RLGN 3100",
            ],
            "2023-24": [
                "BIBL 3000", "RLGN 3000",
                "BIBL 3410",
                "HNRS 3325",
                "PHIL 3250", "RLGN 3250",
                "RLGN 3010",
                "RLGN 3020",
                "RLGN 3100",
            ],
            "2024-25": [
                "BIBL 3000", "RLGN 3000",
                "BIBL 3410",
                "HNRS 3325",
                "PHIL 3250", "RLGN 3250",
                "RLGN 3010",
                "RLGN 3020",
                "RLGN 3100",
            ],
        },
    },

    # ── W2 Scientific Ways of Knowing ────────────────────────────────────────
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

    # ── W3 Civic Ways of Knowing ──────────────────────────────────────────────
    # HNRS 2110 satisfies F3 OR W3 (not both) — engine enforces single-use
    # HNRS 2300 added 24-25 only
    "W3": {
        "label": "W3 Civic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "HIST 2000",
                "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR F3
                "POSC 2100",
            ],
            "2023-24": [
                "HIST 2000",
                "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR F3
                "POSC 2100",
            ],
            "2024-25": [
                "HIST 2000",
                "HIST 2030", "HIST 2040",
                "HIST 2110", "HIST 2120",
                "HNRS 2110",   # OR F3
                "HNRS 2300",   # Honors only, added 24-25
                "POSC 2100",
            ],
        },
    },

    # ── W4 Aesthetic Ways of Knowing ─────────────────────────────────────────
    # AE = Integrative (3 hr, satisfies alone)
    # AP + AX = two smaller courses together (Appreciation + Experiential)
    # ARTH 3040 also satisfies SI (cross-listed)
    # COMM 2550 satisfies W4 AE in 22-23 only (also SI)
    # ENGL 2500 satisfies W4 AP and WI
    "W4": {
        "label": "W4 Aesthetic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": {
                "integrative": [
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "ARTH 2000",
                    "COMM 2550",   # AE + SI, 22-23 only
                    "ENGL 3590",
                    "MUSC 2210",
                ],
                "AP": [
                    "DANC 3510", "ENGL 2500", "MUED 2110",
                    "MUSC 2110", "MUSC 2220", "THEA 2350",
                ],
                "AX": [
                    "DANC 1120", "DANC 2120", "DANC 3120",
                    "DANC 1220", "DANC 2220", "DANC 3220", "DANC 4220",
                    "DANC 1320", "DANC 2320", "DANC 3320", "DANC 4320",
                    "DANC 1420", "DANC 2420", "DANC 3420", "DANC 4420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090", "MUPF 1100",
                    "MUPF 1110", "MUPF 1220", "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 1800", "MUPF 1900",
                    "MUPF 2000", "MUPF 2100", "MUPF 2200", "MUPF 2300",
                    "MUPF 2400", "MUPF 2500", "MUPF 2600", "MUPF 2700",
                    "MUPF 2800", "MUPF 2900", "MUPF 3000", "MUPF 3100",
                    "MUPF 3200", "MUPF 3300", "MUPF 3400", "MUPF 3500",
                    "MUPF 3600", "MUPF 3700", "MUPF 3800", "MUPF 3900",
                    "MUPF 4100", "MUPF 4200", "MUPF 4300", "MUPF 4400",
                    "MUPF 4500", "MUPF 4600", "MUPF 4700", "MUPF 4800",
                    "MUPF 4890",
                ],
            },
            "2023-24": {
                "integrative": [
                    "ARTH 3040",   # also SI
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "ENGL 3590",
                    "HNRS 3000",   # Honors only
                    "MUSC 2210",
                ],
                "AP": [
                    "DANC 3510", "ENGL 2500", "MUED 2110",
                    "MUSC 2110", "MUSC 2220", "THEA 2350",
                ],
                "AX": [
                    "DANC 1120", "DANC 2120", "DANC 3120",
                    "DANC 1220", "DANC 2220", "DANC 3220", "DANC 4220",
                    "DANC 1320", "DANC 2320", "DANC 3320", "DANC 4320",
                    "DANC 1420", "DANC 2420", "DANC 3420", "DANC 4420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090", "MUPF 1100",
                    "MUPF 1110", "MUPF 1220", "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 4890",
                ],
            },
            "2024-25": {
                "integrative": [
                    "ARTH 3040",   # also SI
                    "ARTS 1210", "ARTS 1230", "ARTS 1250",
                    "ENGL 3590", "ENGL 3592",
                    "HNRS 3000",   # Honors only
                    "MUSC 2210",
                ],
                "AP": [
                    "ARTS 1210",   # listed at 2 hrs in 24-25 AP section
                    "DANC 3510", "ENGL 2500", "MUED 2110",
                    "MUSC 2110", "MUSC 2220", "THEA 2350",
                ],
                "AX": [
                    "DANC 1120", "DANC 2120", "DANC 3120",
                    "DANC 1220", "DANC 2220", "DANC 3220", "DANC 4220",
                    "DANC 1320", "DANC 2320", "DANC 3320", "DANC 4320",
                    "DANC 1420", "DANC 2420", "DANC 3420", "DANC 4420",
                    "ENGL 2510",
                    "MUPF 1010", "MUPF 1030",
                    "MUPF 1070", "MUPF 1080", "MUPF 1090", "MUPF 1100",
                    "MUPF 1110", "MUPF 1220", "MUPF 1410", "MUPF 1420",
                    "MUPF 1700", "MUPF 4890",
                ],
            },
        },
    },

    # ── W5 Social and Behavioral Ways of Knowing ──────────────────────────────
    "W5": {
        "label": "W5 Social & Behavioral Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BSNS 3420",
                "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "HNRS 3311",   # Honors only
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
            "2023-24": [
                "BSNS 3420",
                "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "HNRS 3311",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
            "2024-25": [
                "BSNS 3420",
                "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "HNRS 3311",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020", "SOCI 2100",
            ],
        },
    },

    # ── W6 Modern Languages ───────────────────────────────────────────────────
    # MLAN 2000 satisfies W6 OR W7 (not both)
    # SPAN 3010 satisfies W6 AND WI
    "W6": {
        "label": "W6 Modern Languages",
        "credits": 4,
        "courses": {
            "2022-23": [
                "FREN 1010", "FREN 1020",
                "GERM 1010", "GERM 1020",
                "MLAN 2000",   # OR W7
                "SPAN 1010", "SPAN 1020",
                "SPAN 3010",   # also WI
            ],
            "2023-24": [
                "BIBL 2110", "BIBL 2120",   # Beginning Hebrew I/II
                "BIBL 2210", "BIBL 2220",   # Beginning Greek I/II
                "FREN 1010", "FREN 1020", "FREN 2010", "FREN 2020",
                "GERM 1010", "GERM 1020", "GERM 2010",
                "MLAN 2000",   # OR W7
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010",   # also WI
            ],
            "2024-25": [
                "BIBL 2110", "BIBL 2120",
                "BIBL 2210", "BIBL 2220",
                "FREN 1010", "FREN 1020", "FREN 2010", "FREN 2020",
                "GERM 1010", "GERM 1020", "GERM 2010",
                "MLAN 2000",   # OR W7
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010",   # also WI
            ],
        },
    },

    # ── W7 Global/Intercultural Ways of Knowing ───────────────────────────────
    # MLAN 2000 satisfies W6 OR W7 (not both)
    # SOCI 2450 satisfies F2 OR W7
    "W7": {
        "label": "W7 Global/Intercultural Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BSNS 3120",   # also WI
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGR 2080",
                "ENGR 2090",   # also WI
                "ENGL 2220",   # also SI
                "HIST 3100", "HIST 3190",
                "HIST 3240", "HIST 3250", "HIST 3260",   # 3260 also WI
                "HIST 3280",
                "HIST 3300",   # also WI
                "HIST 3320",
                "HIST 3360", "HIST 3370",
                "HIST 3425",   # also WI
                "HNRS 3221",
                "LEAD 4550",
                "MLAN 2000",   # OR W6
                "MLAN 3400",
                "MUSC 2330",
                "POSC 3320",   # also WI
                "POSC 3450",   # also WI
                "SOCI 2450",   # OR F2
                "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",   # also SI
            ],
            "2023-24": [
                "BIBL 3310",
                "BSNS 3120",
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGR 2080",
                "ENGR 2090",
                "ENGL 2220",
                "HIST 3100", "HIST 3190",
                "HIST 3240", "HIST 3250", "HIST 3260",
                "HIST 3280",
                "HIST 3300",
                "HIST 3320",
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
                "ENGR 2080",
                "ENGR 2090",
                "ENGL 2220",
                "HIST 3100", "HIST 3190",
                "HIST 3240", "HIST 3250", "HIST 3260",
                "HIST 3280",
                "HIST 3300",
                "HIST 3320",
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

    # ── W8 Experiential Ways of Knowing ───────────────────────────────────────
    # FSB ONLY: auto-satisfied when F1 (LART 1050) is completed
    # Non-FSB: use W8_BY_MAJOR dict in sport_marketing.py (from W8 spreadsheet)
    "W8": {
        "label": "W8 Experiential Ways of Knowing",
        "credits": 2,
        "auto_satisfy_if_F1": "FSB_ONLY",
        "courses": {
            "2022-23": ["BSNS 1050", "BSNS 4110", "BSNS 4330", "BSNS 4560", "BSNS 4800"],
            "2023-24": ["BSNS 1050", "BSNS 4110", "BSNS 4330", "BSNS 4560", "BSNS 4800"],
            "2024-25": ["BSNS 1050", "BSNS 4110", "BSNS 4330", "BSNS 4560", "BSNS 4800"],
        },
    },

    # ── WI Writing Intensive ──────────────────────────────────────────────────
    # Two WI courses required beyond ENGL 1120; at least one upper-division (3000+)
    # Cross-listed WI courses: BIBL/RLGN 3000, BSNS 3120, ENGL 3190, ENGL 3580,
    # ENGR 2090, HIST 3260, HIST 3300, HIST 3425, POSC 3320, POSC 3450, SPAN 3010
    "WI": {
        "label": "WI Writing Intensive",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BIBL 3000", "RLGN 3000",
                "BSNS 3120", "BSNS 4910",
                "COMM 3130",
                "ENGL 2500",
                "ENGL 3110", "ENGL 3190", "ENGL 3580",
                "ENGR 2090",
                "HIST 3260", "HIST 3300", "HIST 3425",
                "POSC 3320", "POSC 3450",
                "SPAN 3010",
            ],
            "2023-24": [
                "BIBL 3000", "RLGN 3000",
                "BSNS 3120", "BSNS 4910",
                "COMM 3130",
                "ENGL 2500",
                "ENGL 3110", "ENGL 3190", "ENGL 3580",
                "ENGR 2090",
                "HIST 3260", "HIST 3300", "HIST 3425",
                "POSC 3320", "POSC 3450",
                "SPAN 3010",
            ],
            "2024-25": [
                "BIBL 3000", "RLGN 3000",
                "BSNS 3120", "BSNS 4910",
                "COMM 3130",
                "ENGL 2500",
                "ENGL 3110", "ENGL 3190", "ENGL 3580",
                "ENGR 2090",
                "HIST 3260", "HIST 3300", "HIST 3425",
                "POSC 3320", "POSC 3450",
                "SPAN 3010",
            ],
        },
    },

    # ── SI Speaking Intensive ─────────────────────────────────────────────────
    # Cross-listed: ARTH 3040, COMM 2550 (22-23), ENGL 2220, HIST 2300,
    #               HNRS 2125, PSYC 3200, SPAN 3020
    "SI": {
        "label": "SI Speaking Intensive",
        "credits": 3,
        "courses": {
            "2022-23": [
                "ARTH 3040",
                "BSNS 3210", "BSNS 4480",
                "COMM 2000", "COMM 2130", "COMM 2140", "COMM 2550",
                "ENGL 2220",
                "HIST 2300",
                "HNRS 2125",
                "PSYC 3200",
                "SPAN 3020",
            ],
            "2023-24": [
                "ARTH 3040",
                "BSNS 3210", "BSNS 4480",
                "COMM 2000", "COMM 2130", "COMM 2140",
                "ENGL 2220",
                "HIST 2300",
                "HNRS 2125",
                "PSYC 3200",
                "SPAN 3020",
            ],
            "2024-25": [
                "ARTH 3040",
                "BSNS 3210", "BSNS 4480",
                "COMM 2000", "COMM 2130", "COMM 2140",
                "ENGL 2220",
                "HIST 2300",
                "HNRS 2125",
                "PSYC 3200",
                "SPAN 3020",
            ],
        },
    },
}


# ─────────────────────────────────────────────
# NEW FRAMEWORK: 2025-26
# Raven Core (RC1-RC6) + AU Experience (AU1-AU6)
# ─────────────────────────────────────────────

LA_RAVEN_CORE_2526 = {
    "year": "2025-26",
    "note": "ICC-exempt students skip RC1-RC6 entirely.",

    # Raven Core — 30 hrs, at least one course per category
    "RC1": {
        "label": "RC1 Written Communication",
        "credits": 6,
        "courses": {
            "2025-26": ["ENGL 1110", "ENGL 1120", "HNRS 2110"],
        },
    },
    "RC2": {
        "label": "RC2 Speaking and Listening",
        "credits": 3,
        "courses": {
            "2025-26": ["COMM 1000", "COMM 3310", "PSYC 2100"],
        },
    },
    "RC3": {
        "label": "RC3 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2025-26": [
                "CPSC 2020", "LEAD 3100",
                "MATH 1100", "MATH 1250", "MATH 1300",
                "MATH 2010", "MATH 2120",
                "PSYC 2440",
            ],
        },
    },
    "RC4": {
        "label": "RC4 Scientific Ways of Knowing",
        "credits": 4,
        "courses": {
            "2025-26": [
                "BIOL 1000", "BIOL 2210", "BIOL 2230",
                "CHEM 1000", "CHEM 2110",
                "EXSC 2140",
                "HNRS 2210",
                "PHYS 1020", "PHYS 2140", "PHYS 2240",
            ],
        },
    },
    "RC5": {
        "label": "RC5 Social and Behavioral Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BSNS 3420",
                "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020",
            ],
        },
    },
    "RC6": {
        "label": "RC6 Humanistic and Artistic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "ENGL 2500", "ENGL 3590",
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "HNRS 2300", "HNRS 3100",
                "MUSC 2110", "MUSC 3120", "MUSC 3130",
                "SPAN 1010", "SPAN 1020",
            ],
        },
    },

    # AU Experience — complete one course in each category
    "AU1": {
        "label": "AU1 Understanding College",
        "credits": 1,
        "courses": {"2025-26": ["LART 1050"]},
    },
    "AU2": {
        "label": "AU2 Biblical Literacy",
        "credits": 3,
        "courses": {"2025-26": ["BIBL 2000"]},
    },
    "AU3": {
        "label": "AU3 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": ["BIBL 3410", "HNRS 3325", "RLGN 3010"],
        },
    },
    "AU4": {
        "label": "AU4 Personal Wellness",
        "credits": 2,
        "courses": {
            "2025-26": [
                "EXSC 2440", "NURS 1210", "PEHS 1000",
                "PSYC 3500", "SOCI 3500",
                "RLGN 1100",
            ],
        },
    },
    "AU5": {
        "label": "AU5 Civil Discourse and Conflict Transformation",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BIOL 3510",
                "COMM 3200",
                "HIST 2300",
                "HNRS 2125",
                "LART 2000",
                "PACT 2100",
                "PHIL 2120",
                "PSYC 3200",
                "RLGN 3120", "RLGN 3250", "PHIL 3250",
                "SOCI 2450",
                "SPED 2400",
            ],
        },
    },
    "AU6": {
        "label": "AU6 Global Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BIBL 3310",
                "BSNS 3120",
                "COMM 3050",
                "DANC 3000",
                "EDUC 3550",
                "ENGL 2220",
                "ENGR 2080", "ENGR 2090",
                "HIST 3100", "HIST 3190",
                "HIST 3240", "HIST 3250", "HIST 3260",
                "HIST 3280", "HIST 3300", "HIST 3320",
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


# ─────────────────────────────────────────────
# CROSS-LISTING RULES
# Preserved here for reference; engine enforces these.
# ─────────────────────────────────────────────

LA_CROSS_LISTINGS = {
    # course: (areas_it_satisfies, rule)
    # rule = 'AND' means satisfies both; 'OR' means satisfies only one
    "ARTH 3040":      (["W4", "SI"],   "AND"),
    "BIBL 3000":      (["W1", "WI"],   "AND"),
    "RLGN 3000":      (["W1", "WI"],   "AND"),
    "BSNS 3120":      (["W7", "WI"],   "AND"),
    "COMM 2550":      (["W4", "SI"],   "AND"),   # 22-23 only
    "ENGL 2220":      (["W7", "SI"],   "AND"),
    "ENGL 2500":      (["W4", "WI"],   "AND"),
    "ENGL 3190":      (["F2", "WI"],   "AND"),
    "ENGL 3580":      (["F2", "WI"],   "AND"),
    "ENGR 2090":      (["W7", "WI"],   "AND"),
    "HIST 2300":      (["F2", "SI"],   "AND"),
    "HIST 3260":      (["W7", "WI"],   "AND"),
    "HIST 3300":      (["W7", "WI"],   "AND"),
    "HIST 3425":      (["W7", "WI"],   "AND"),
    "HNRS 2110":      (["F3", "W3"],   "OR"),
    "HNRS 2125":      (["F2", "SI"],   "AND"),
    "MLAN 2000":      (["W6", "W7"],   "OR"),
    "POSC 3320":      (["W7", "WI"],   "AND"),
    "POSC 3450":      (["W7", "WI"],   "AND"),
    "PSYC 3200":      (["F2", "SI"],   "AND"),
    "SOCI 2450":      (["F2", "W7"],   "OR"),
    "SPAN 3010":      (["W6", "WI"],   "AND"),
    "SPAN 3020":      (["W7", "SI"],   "AND"),
}

# W8 major-specific course list is in engines/sport_marketing.py (W8_BY_MAJOR dict)
