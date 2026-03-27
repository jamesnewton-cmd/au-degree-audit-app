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
            "2022-23": ["LART_1050", "HNRS_2110"],   # Honors students exempt via HNRS-2110
            "2023-24": ["LART_1050", "HNRS_2110"],
            "2024-25": ["LART_1050", "HNRS_2110"],
        },
        "special_rule": "F1_SATISFIES_W8_FSB_ONLY",
        "honors_note": "Honors students exempt from LART-1050; HNRS-2110 satisfies F1",
    },

    # ── F2 Civil Discourse & Critical Reasoning ─────────────────────────────
    "F2": {
        "label": "F2 Civil Discourse & Critical Reasoning",
        "credits": {"2022-23": 2, "2023-24": 3, "2024-25": 3},
        "courses": {
            "2022-23": [
                "BIOL_3510", "PUBH_3510",
                "BSNS_3420",
                "CMIN_2270",
                "ENGL_3190",   # also WI
                "ENGL_3580",   # also WI
                "ENGR_2060",
                "HIST_2300",   # also SI
                "HNRS_2125",   # also SI
                "LART_1100",
                "MUED_1000",
                "PHIL_2000",
                "PHIL_2120",
                "POSC_2020",
                "PSYC_3200",   # also SI
                "RLGN_3120",
                "SOCI_2450",   # OR W7
                "SPED_2400",
            ],
            "2023-24": [
                "BIOL_3510", "PUBH_3510",
                "BSNS_3420",
                "CMIN_2270",
                "COMM_3200",
                "ENGL_3190",   # also WI
                "ENGL_3580",   # also WI
                "ENGR_2060",
                "HIST_2300",   # also SI
                "HNRS_2125",   # also SI
                "LART_1100",
                "MUED_1000",
                "PHIL_2000",
                "PHIL_2120",
                "POSC_2020",
                "PSYC_3200",   # also SI
                "RLGN_3120",
                "SOCI_2450",   # OR W7
                "SPED_2400",
            ],
            "2024-25": [
                "BIOL_3510", "PUBH_3510",
                "BSNS_3420",
                "CMIN_2270",
                "COMM_3200",
                "ENGL_3190",   # also WI
                "ENGL_3580",   # also WI
                "ENGR_2060",
                "HIST_2300",   # also SI
                "HNRS_2125",   # also SI
                "LART_1100",
                "MUED_1000",
                "PHIL_2000",
                "PHIL_2120",
                "POSC_2020",
                "PSYC_3200",   # also SI
                "RLGN_3120",
                "SOCI_2450",   # OR W7
                "SPED_2400",
            ],
        },
    },

    # ── F3 Written Communication ────────────────────────────────────────────
    # HNRS 2110 can satisfy F3 OR W3 (not both) — engine enforces single-use
    "F3": {
        "label": "F3 Written Communication",
        "credits": 6,
        "required_courses": ["ENGL_1100", "ENGL_1110", "ENGL_1120", "HNRS_2110"],
        "notes": "ENGL 1100/1110 interchangeable by placement. HNRS 2110 satisfies F3 OR W3.",
    },

    # ── F4 Speaking and Listening ────────────────────────────────────────────
    "F4": {
        "label": "F4 Speaking and Listening",
        "credits": 3,
        "required_courses": ["COMM_1000"],
        "requires_si": True,
        "notes": "Plus one SI-designated course."
    },

    # ── F5 Quantitative Reasoning ────────────────────────────────────────────
    "F5": {
        "label": "F5 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2022-23": [
                "CPSC_1100", "CPSC_1200", "CPSC_1400",
                "LEAD_3100",
                "MATH_1100", "MATH_1250", "MATH_1300", "MATH_1400",
                "MATH_2010", "MATH_2120",
                "PSYC_2440",
            ],
            "2023-24": [
                "CPSC_1100", "CPSC_1200", "CPSC_2020",
                "LEAD_3100",
                "MATH_1100", "MATH_1220", "MATH_1250", "MATH_1300", "MATH_1400",
                "MATH_2010", "MATH_2120",
                "PSYC_2440",
            ],
            "2024-25": [
                "CPSC_2020",
                "LEAD_3100",
                "MATH_1100", "MATH_1220", "MATH_1250", "MATH_1300",
                "MATH_2010", "MATH_2120",
                "PSYC_2440",
            ],
        },
    },

    # ── F6 Biblical Literacy ─────────────────────────────────────────────────
    "F6": {
        "label": "F6 Biblical Literacy",
        "credits": 3,
        "courses": {
            "2022-23": ["BIBL_2000"],
            "2023-24": ["BIBL_2000"],
            "2024-25": ["BIBL_2000"],
        },
    },

    # ── F7 Personal Wellness ─────────────────────────────────────────────────
    "F7": {
        "label": "F7 Personal Wellness",
        "credits": 2,
        "courses": {
            "2022-23": ["PEHS_1000", "DANC_3060", "NURS_1210"],
            "2023-24": ["PEHS_1000", "DANC_3060", "NURS_1210"],
            "2024-25": ["PEHS_1000", "DANC_3060", "NURS_1210"],
        },
    },

    # ── W1 Christian Ways of Knowing ─────────────────────────────────────────
    "W1": {
        "label": "W1 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BIBL_3000", "RLGN_3000",   # cross-listed, also WI
                "BIBL_3410",
                "HNRS_3325",                 # Honors only
                "PHIL_3250", "RLGN_3250",
                "RLGN_3010",
                "RLGN_3020",
                "RLGN_3100",
            ],
            "2023-24": [
                "BIBL_3000", "RLGN_3000",
                "BIBL_3410",
                "HNRS_3325",
                "PHIL_3250", "RLGN_3250",
                "RLGN_3010",
                "RLGN_3020",
                "RLGN_3100",
            ],
            "2024-25": [
                "BIBL_3000", "RLGN_3000",
                "BIBL_3410",
                "HNRS_3325",
                "PHIL_3250", "RLGN_3250",
                "RLGN_3010",
                "RLGN_3020",
                "RLGN_3100",
            ],
        },
    },

    # ── W2 Scientific Ways of Knowing ────────────────────────────────────────
    "W2": {
        "label": "W2 Scientific Ways of Knowing",
        "credits": 4,
        "courses": {
            "2022-23": [
                "BIOL_1000", "BIOL_2070", "BIOL_2080", "BIOL_2210",
                "CHEM_1000", "CHEM_2110",
                "EXSC_2140",
                "HNRS_2210",
                "PHYS_1000", "PHYS_1020", "PHYS_1140", "PHYS_1240",
                "PHYS_2140", "PHYS_2240",
                "PSYC_3210",
            ],
            "2023-24": [
                "BIOL_1000", "BIOL_2070", "BIOL_2080", "BIOL_2210",
                "CHEM_1000", "CHEM_2110",
                "CPSC_2040",
                "EXSC_2140",
                "HNRS_2210",
                "PHYS_1000", "PHYS_1020", "PHYS_1240",
                "PHYS_2140", "PHYS_2240",
                "PSYC_3210",
            ],
            "2024-25": [
                "BIOL_1000", "BIOL_2070", "BIOL_2080", "BIOL_2210",
                "CHEM_1000", "CHEM_2110",
                "CPSC_2040",
                "EXSC_2140",
                "HNRS_2210",
                "PHYS_1000", "PHYS_1020", "PHYS_1240",
                "PHYS_2140", "PHYS_2240",
                "PSYC_3210",
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
                "HIST_2000",
                "HIST_2030", "HIST_2040",
                "HIST_2110", "HIST_2120",
                "HNRS_2110",   # OR F3
                "POSC_2100",
            ],
            "2023-24": [
                "HIST_2000",
                "HIST_2030", "HIST_2040",
                "HIST_2110", "HIST_2120",
                "HNRS_2110",   # OR F3
                "POSC_2100",
            ],
            "2024-25": [
                "HIST_2000",
                "HIST_2030", "HIST_2040",
                "HIST_2110", "HIST_2120",
                "HNRS_2110",   # OR F3
                "HNRS_2300",   # Honors only, added 24-25
                "POSC_2100",
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
                    "ARTS_1210", "ARTS_1230", "ARTS_1250",
                    "ARTH_2000",
                    "COMM_2550",   # AE + SI, 22-23 only
                    "ENGL_3590",
                    "HNRS_3000",   # Honors only
                    "MUSC_2210",
                ],
                "AP": [
                    "DANC_3510", "ENGL_2500", "MUED_2110",
                    "MUSC_2110", "MUSC_2220", "THEA_2350",
                ],
                "AX": [
                    "DANC_1120", "DANC_2120", "DANC_3120",
                    "DANC_1220", "DANC_2220", "DANC_3220", "DANC_4220",
                    "DANC_1320", "DANC_2320", "DANC_3320", "DANC_4320",
                    "DANC_1420", "DANC_2420", "DANC_3420", "DANC_4420",
                    "ENGL_2510",
                    "MUPF_1010", "MUPF_1030",
                    "MUPF_1070", "MUPF_1080", "MUPF_1090", "MUPF_1100",
                    "MUPF_1110", "MUPF_1220", "MUPF_1410", "MUPF_1420",
                    "MUPF_1700", "MUPF_1800", "MUPF_1900",
                    "MUPF_2000", "MUPF_2100", "MUPF_2200", "MUPF_2300",
                    "MUPF_2400", "MUPF_2500", "MUPF_2600", "MUPF_2700",
                    "MUPF_2800", "MUPF_2900", "MUPF_3000", "MUPF_3100",
                    "MUPF_3200", "MUPF_3300", "MUPF_3400", "MUPF_3500",
                    "MUPF_3600", "MUPF_3700", "MUPF_3800", "MUPF_3900",
                    "MUPF_4100", "MUPF_4200", "MUPF_4300", "MUPF_4400",
                    "MUPF_4500", "MUPF_4600", "MUPF_4700", "MUPF_4800",
                    "MUPF_4890",
                ],
            },
            "2023-24": {
                "integrative": [
                    "ARTH_3040",   # also SI
                    "ARTS_1210", "ARTS_1230", "ARTS_1250",
                    "COMM_2550",   # also SI
                    "ENGL_3590",
                    "HNRS_3000",   # Honors only
                    "MUSC_2210",
                ],
                "AP": [
                    "DANC_3510", "ENGL_2500", "MUED_2110",
                    "MUSC_2110", "MUSC_2220", "THEA_2350",
                ],
                "AX": [
                    "DANC_1120", "DANC_2120", "DANC_3120",
                    "DANC_1220", "DANC_2220", "DANC_3220", "DANC_4220",
                    "DANC_1320", "DANC_2320", "DANC_3320", "DANC_4320",
                    "DANC_1420", "DANC_2420", "DANC_3420", "DANC_4420",
                    "ENGL_2510",
                    "MUPF_1010", "MUPF_1030",
                    "MUPF_1070", "MUPF_1080", "MUPF_1090", "MUPF_1100",
                    "MUPF_1110", "MUPF_1220", "MUPF_1410", "MUPF_1420",
                    "MUPF_1700", "MUPF_4890",
                ],
            },
            "2024-25": {
                "integrative": [
                    "ARTH_3040",   # also SI
                    "ARTS_1210", "ARTS_1230", "ARTS_1250",
                    "COMM_2550",   # also SI
                    "ENGL_3590", "ENGL_3592",
                    "HNRS_3000",   # Honors only
                    "MUSC_2210",
                ],
                "AP": [
                    "ARTS_1210",   # listed at 2 hrs in 24-25 AP section
                    "DANC_3510", "ENGL_2500", "MUED_2110",
                    "MUSC_2110", "MUSC_2220", "THEA_2350",
                ],
                "AX": [
                    "DANC_1120", "DANC_2120", "DANC_3120",
                    "DANC_1220", "DANC_2220", "DANC_3220", "DANC_4220",
                    "DANC_1320", "DANC_2320", "DANC_3320", "DANC_4320",
                    "DANC_1420", "DANC_2420", "DANC_3420", "DANC_4420",
                    "ENGL_2510",
                    "MUPF_1010", "MUPF_1030",
                    "MUPF_1070", "MUPF_1080", "MUPF_1090", "MUPF_1100",
                    "MUPF_1110", "MUPF_1220", "MUPF_1410", "MUPF_1420",
                    "MUPF_1700", "MUPF_4890",
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
                "BSNS_3420",
                "ECON_2010", "ECON_2020",
                "EDUC_2110", "PSYC_2110",
                "HNRS_3311",   # Honors only
                "LEAD_2300",
                "POSC_2020", "POSC_2100",
                "PSYC_2000",
                "SOCI_2010", "SOCI_2020", "SOCI_2100",
            ],
            "2023-24": [
                "BSNS_3420",
                "ECON_2010", "ECON_2020",
                "EDUC_2110", "PSYC_2110",
                "HNRS_3311",
                "LEAD_2300",
                "POSC_2020", "POSC_2100",
                "PSYC_2000",
                "SOCI_2010", "SOCI_2020", "SOCI_2100",
            ],
            "2024-25": [
                "BSNS_3420",
                "ECON_2010", "ECON_2020",
                "EDUC_2110", "PSYC_2110",
                "HNRS_3311",
                "LEAD_2300",
                "POSC_2020", "POSC_2100",
                "PSYC_2000",
                "SOCI_2010", "SOCI_2020", "SOCI_2100",
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
                "FREN_1010", "FREN_1020",
                "GERM_1010", "GERM_1020",
                "MLAN_2000",   # OR W7
                "SPAN_1010", "SPAN_1020",
                "SPAN_3010",   # also WI
            ],
            "2023-24": [
                "BIBL_2110", "BIBL_2120",   # Beginning Hebrew I/II
                "BIBL_2210", "BIBL_2220",   # Beginning Greek I/II
                "FREN_1010", "FREN_1020", "FREN_2010", "FREN_2020",
                "GERM_1010", "GERM_1020", "GERM_2010",
                "MLAN_2000",   # OR W7
                "SPAN_1010", "SPAN_1020", "SPAN_2010", "SPAN_2020",
                "SPAN_3010",   # also WI
            ],
            "2024-25": [
                "BIBL_2110", "BIBL_2120",
                "BIBL_2210", "BIBL_2220",
                "FREN_1010", "FREN_1020", "FREN_2010", "FREN_2020",
                "GERM_1010", "GERM_1020", "GERM_2010",
                "MLAN_2000",   # OR W7
                "SPAN_1010", "SPAN_1020", "SPAN_2010", "SPAN_2020",
                "SPAN_3010",   # also WI
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
                "BSNS_3120",   # also WI
                "COMM_3050",
                "DANC_3000",
                "EDUC_3550",
                "ENGR_2080",
                "ENGR_2090",   # also WI
                "ENGL_2220",   # also SI
                "HIST_3100", "HIST_3190",
                "HIST_3240", "HIST_3250", "HIST_3260",   # 3260 also WI
                "HIST_3280",
                "HIST_3300",   # also WI
                "HIST_3320", "RLGN_3320",   # World Religions (HIST/RLGN cross-listed)
                "HIST_3360", "HIST_3370",
                "HIST_3425",   # also WI
                "HNRS_3221",
                "LEAD_4550",
                "MLAN_2000",   # OR W6
                "MLAN_3400",
                "MUSC_2330",
                "POSC_3320",   # also WI
                "POSC_3450",   # also WI
                "SOCI_2450",   # OR F2
                "SOCI_3470",
                "SPAN_2101", "SPAN_2102", "SPAN_2103", "SPAN_2104",
                "SPAN_3020",   # also SI
            ],
            "2023-24": [
                "BIBL_3310",
                "BSNS_3120",
                "COMM_3050",
                "DANC_3000",
                "EDUC_3550",
                "ENGR_2080",
                "ENGR_2090",
                "ENGL_2220",
                "HIST_3100", "HIST_3190",
                "HIST_3240", "HIST_3250", "HIST_3260",
                "HIST_3280",
                "HIST_3300",
                "HIST_3320", "RLGN_3320",   # World Religions (HIST/RLGN cross-listed)
                "HIST_3360", "HIST_3370",
                "HIST_3425",
                "HNRS_3221",
                "LEAD_4550",
                "MLAN_2000",
                "MLAN_3400",
                "MUSC_2330",
                "POSC_3320",
                "POSC_3450",
                "SOCI_2450",
                "SOCI_3470",
                "SPAN_2101", "SPAN_2102", "SPAN_2103", "SPAN_2104",
                "SPAN_3020",
            ],
            "2024-25": [
                "BIBL_3310",
                "BSNS_3120",
                "COMM_3050",
                "DANC_3000",
                "EDUC_3550",
                "ENGR_2080",
                "ENGR_2090",
                "ENGL_2220",
                "HIST_3100", "HIST_3190",
                "HIST_3240", "HIST_3250", "HIST_3260",
                "HIST_3280",
                "HIST_3300",
                "HIST_3320", "RLGN_3320",   # World Religions (HIST/RLGN cross-listed)
                "HIST_3360", "HIST_3370",
                "HIST_3425",
                "HNRS_3221",
                "LEAD_4550",
                "MLAN_2000",
                "MLAN_3400",
                "MUSC_2330",
                "POSC_3320",
                "POSC_3450",
                "SOCI_2450",
                "SOCI_3470",
                "SPAN_2101", "SPAN_2102", "SPAN_2103", "SPAN_2104",
                "SPAN_3020",
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
            "2022-23": ["BSNS_1050", "BSNS_4110", "BSNS_4330", "BSNS_4560", "BSNS_4800"],
            "2023-24": ["BSNS_1050", "BSNS_4110", "BSNS_4330", "BSNS_4560", "BSNS_4800"],
            "2024-25": ["BSNS_1050", "BSNS_4110", "BSNS_4330", "BSNS_4560", "BSNS_4800"],
        },
    },

    # ── WI Writing Intensive ──────────────────────────────────────────────────
    # Two WI courses required beyond ENGL 1120; at least one upper-division (3000+)
    # Complete list from AU Advanced Writing Competency document (Rev 08/2022)
    # Same list applies 2022-23 through 2024-25
    "WI": {
        "label": "WI Writing Intensive",
        "credits": 3,
        "courses": {
            "2022-23": [
                "ACCT_4900",
                "ARTH_3030",
                "ATRG_3440",
                "ATRG_4550",
                "BIBL_3000",
                "RLGN_3000",
                "BIOL_4050",
                "BIOL_4910",
                "CHEM_4910",
                "PHYS_4910",
                "BIOL_4920",
                "CHEM_4920",
                "PHYS_4920",
                "BSNS_3120",
                "BSNS_3330",
                "BSNS_4910",
                "CHEM_3100",
                "CMIN_4250",
                "COMM_2130",
                "COMM_2160",
                "COMM_3130",
                "COMM_3220",
                "COMM_3230",
                "COMM_3340",
                "CPSC_4950",
                "CRIM_2510",
                "SOCI_2510",
                "DANC_3010",
                "EDUC_3120",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_2500",
                "ENGL_3050",
                "ENGL_3110",
                "ENGL_3120",
                "ENGL_3140",
                "ENGL_3160",
                "ENGL_3180",
                "ENGL_3190",
                "ENGL_3500",
                "ENGL_3551",
                "ENGL_3580",
                "ENGL_4550",
                "ENGL_4700",
                "ENGL_4910",
                "ENGR_2090",
                "ENGR_4950",
                "ENGR_4960",
                "EXSC_4910",
                "HIST_3260",
                "HIST_3300",
                "HIST_3320",
                "RLGN_3320",
                "HIST_3425",
                "HIST_3440",
                "HIST_3451",
                "HIST_3452",
                "HIST_3470",
                "HIST_3510",
                "HNRS_3221",
                "LEAD_4990",
                "MLAN_4900",
                "MUBS_3350",
                "MUBS_3500",
                "MUSC_3110",
                "MUSC_3120",
                "MUSC_3130",
                "MUSC_3170",
                "MUSC_3180",
                "NURS_3391",
                "NURS_4470",
                "PEHS_3340",
                "PETE_2250",
                "PETE_4300",
                "PHYS_3100",
                "POSC_2400",
                "POSC_3211",
                "POSC_3310",
                "POSC_3320",
                "POSC_3450",
                "PSYC_2010",
                "PSYC_3010",
                "PUBH_3010",
                "SOCI_3010",
                "PSYC_4510",
                "PUBH_3700",
                "SOCI_3700",
                "RLGN_3300",
                "SPAN_3010",
                "SPED_3120",
            ],
            "2023-24": [
                "ACCT_4900",
                "ARTH_3030",
                "ATRG_3440",
                "ATRG_4550",
                "BIBL_3000",
                "RLGN_3000",
                "BIOL_4050",
                "BIOL_4910",
                "CHEM_4910",
                "PHYS_4910",
                "BIOL_4920",
                "CHEM_4920",
                "PHYS_4920",
                "BSNS_3120",
                "BSNS_3330",
                "BSNS_4910",
                "CHEM_3100",
                "CMIN_4250",
                "COMM_2130",
                "COMM_2160",
                "COMM_3130",
                "COMM_3220",
                "COMM_3230",
                "COMM_3340",
                "CPSC_4950",
                "CRIM_2510",
                "SOCI_2510",
                "DANC_3010",
                "EDUC_3120",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_2500",
                "ENGL_3050",
                "ENGL_3110",
                "ENGL_3120",
                "ENGL_3140",
                "ENGL_3160",
                "ENGL_3180",
                "ENGL_3190",
                "ENGL_3500",
                "ENGL_3551",
                "ENGL_3580",
                "ENGL_4550",
                "ENGL_4700",
                "ENGL_4910",
                "ENGR_2090",
                "ENGR_4950",
                "ENGR_4960",
                "EXSC_4910",
                "HIST_3260",
                "HIST_3300",
                "HIST_3320",
                "RLGN_3320",
                "HIST_3425",
                "HIST_3440",
                "HIST_3451",
                "HIST_3452",
                "HIST_3470",
                "HIST_3510",
                "HNRS_3221",
                "LEAD_4990",
                "MLAN_4900",
                "MUBS_3350",
                "MUBS_3500",
                "MUSC_3110",
                "MUSC_3120",
                "MUSC_3130",
                "MUSC_3170",
                "MUSC_3180",
                "NURS_3391",
                "NURS_4470",
                "PEHS_3340",
                "PETE_2250",
                "PETE_4300",
                "PHYS_3100",
                "POSC_2400",
                "POSC_3211",
                "POSC_3310",
                "POSC_3320",
                "POSC_3450",
                "PSYC_2010",
                "PSYC_3010",
                "PUBH_3010",
                "SOCI_3010",
                "PSYC_4510",
                "PUBH_3700",
                "SOCI_3700",
                "RLGN_3300",
                "SPAN_3010",
                "SPED_3120",
            ],
            "2024-25": [
                "ACCT_4900",
                "ARTH_3030",
                "ATRG_3440",
                "ATRG_4550",
                "BIBL_3000",
                "RLGN_3000",
                "BIOL_4050",
                "BIOL_4910",
                "CHEM_4910",
                "PHYS_4910",
                "BIOL_4920",
                "CHEM_4920",
                "PHYS_4920",
                "BSNS_3120",
                "BSNS_3330",
                "BSNS_4910",
                "CHEM_3100",
                "CMIN_4250",
                "COMM_2130",
                "COMM_2160",
                "COMM_3130",
                "COMM_3220",
                "COMM_3230",
                "COMM_3340",
                "CPSC_4950",
                "CRIM_2510",
                "SOCI_2510",
                "DANC_3010",
                "EDUC_3120",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_2500",
                "ENGL_3050",
                "ENGL_3110",
                "ENGL_3120",
                "ENGL_3140",
                "ENGL_3160",
                "ENGL_3180",
                "ENGL_3190",
                "ENGL_3500",
                "ENGL_3551",
                "ENGL_3580",
                "ENGL_4550",
                "ENGL_4700",
                "ENGL_4910",
                "ENGR_2090",
                "ENGR_4950",
                "ENGR_4960",
                "EXSC_4910",
                "HIST_3260",
                "HIST_3300",
                "HIST_3320",
                "RLGN_3320",
                "HIST_3425",
                "HIST_3440",
                "HIST_3451",
                "HIST_3452",
                "HIST_3470",
                "HIST_3510",
                "HNRS_3221",
                "LEAD_4990",
                "MLAN_4900",
                "MUBS_3350",
                "MUBS_3500",
                "MUSC_3110",
                "MUSC_3120",
                "MUSC_3130",
                "MUSC_3170",
                "MUSC_3180",
                "NURS_3391",
                "NURS_4470",
                "PEHS_3340",
                "PETE_2250",
                "PETE_4300",
                "PHYS_3100",
                "POSC_2400",
                "POSC_3211",
                "POSC_3310",
                "POSC_3320",
                "POSC_3450",
                "PSYC_2010",
                "PSYC_3010",
                "PUBH_3010",
                "SOCI_3010",
                "PSYC_4510",
                "PUBH_3700",
                "SOCI_3700",
                "RLGN_3300",
                "SPAN_3010",
                "SPED_3120",
            ],
        },
    },

    # ── SI Speaking Intensive ─────────────────────────────────────────────────
    # One SI course required; must be upper-division (beyond COMM 1000)
    # Complete list from AU Advanced Competency document (Rev 08/2022)
    "SI": {
        "label": "SI Speaking Intensive",
        "credits": 3,
        "courses": {
            "2022-23": [
                "ARTS_4950",
                "ATRG_4910",
                "BSNS_3210",
                "BSNS_4480",
                "CHEM_4910",
                "BIOL_4910",
                "PHYS_4910",
                "CMIN_3910",
                "COMM_2550",
                "COMM_3420",
                "CRIM_4900",
                "CPSC_4960",
                "DANC_3050",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_3050",
                "ENGL_2220",
                "ENGR_4960",
                "EXSC_4920",
                "MLAN_4900",
                "HIST_2300",
                "HIST_2350",
                "HIST_4930",
                "HNRS_2125",
                "LART_4500",
                "LEAD_4990",
                "MATH_4000",
                "MUBS_3350",
                "MUED_3110",
                "MUED_3350",
                "MUSC_4955",
                "MUTR_3210",
                "NURS_4960",
                "PETE_4900",
                "POSC_3211",
                "POSC_3212",
                "POSC_3370",
                "PSYC_3200",
                "PSYC_4110",
                "PSYC_4210",
                "PSYC_4520",
                "SOCI_4200",
                "SOCI_4950",
                "SOWK_4850",
                "SPAN_3020",
                "THEA_3210",
                "ARTH_3040",
                "COMM_1000",
                "COMM_2000",
                "COMM_2130",
                "COMM_2140",
            ],
            "2023-24": [
                "ARTS_4950",
                "ATRG_4910",
                "BSNS_3210",
                "BSNS_4480",
                "CHEM_4910",
                "BIOL_4910",
                "PHYS_4910",
                "CMIN_3910",
                "COMM_2550",
                "COMM_3420",
                "CRIM_4900",
                "CPSC_4960",
                "DANC_3050",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_3050",
                "ENGL_2220",
                "ENGR_4960",
                "EXSC_4920",
                "MLAN_4900",
                "HIST_2300",
                "HIST_2350",
                "HIST_4930",
                "HNRS_2125",
                "LART_4500",
                "LEAD_4990",
                "MATH_4000",
                "MUBS_3350",
                "MUED_3110",
                "MUED_3350",
                "MUSC_4955",
                "MUTR_3210",
                "NURS_4960",
                "PETE_4900",
                "POSC_3211",
                "POSC_3212",
                "POSC_3370",
                "PSYC_3200",
                "PSYC_4110",
                "PSYC_4210",
                "PSYC_4520",
                "SOCI_4200",
                "SOCI_4950",
                "SOWK_4850",
                "SPAN_3020",
                "THEA_3210",
                "ARTH_3040",
                "COMM_1000",
                "COMM_2000",
                "COMM_2130",
                "COMM_2140",
            ],
            "2024-25": [
                "ARTS_4950",
                "ATRG_4910",
                "BSNS_3210",
                "BSNS_4480",
                "CHEM_4910",
                "BIOL_4910",
                "PHYS_4910",
                "CMIN_3910",
                "COMM_2550",
                "COMM_3420",
                "CRIM_4900",
                "CPSC_4960",
                "DANC_3050",
                "EDUC_4120",
                "EDUC_4710",
                "ENGL_3050",
                "ENGL_2220",
                "ENGR_4960",
                "EXSC_4920",
                "MLAN_4900",
                "HIST_2300",
                "HIST_2350",
                "HIST_4930",
                "HNRS_2125",
                "LART_4500",
                "LEAD_4990",
                "MATH_4000",
                "MUBS_3350",
                "MUED_3110",
                "MUED_3350",
                "MUSC_4955",
                "MUTR_3210",
                "NURS_4960",
                "PETE_4900",
                "POSC_3211",
                "POSC_3212",
                "POSC_3370",
                "PSYC_3200",
                "PSYC_4110",
                "PSYC_4210",
                "PSYC_4520",
                "SOCI_4200",
                "SOCI_4950",
                "SOWK_4850",
                "SPAN_3020",
                "THEA_3210",
                "ARTH_3040",
                "COMM_1000",
                "COMM_2000",
                "COMM_2130",
                "COMM_2140",
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
            "2025-26": ["ENGL_1110", "ENGL_1120", "HNRS_2110"],
        },
    },
    "RC2": {
        "label": "RC2 Speaking and Listening",
        "credits": 3,
        "courses": {
            "2025-26": ["COMM_1000", "COMM_3310", "PSYC_2100"],
        },
    },
    "RC3": {
        "label": "RC3 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2025-26": [
                "CPSC_2020", "LEAD_3100",
                "MATH_1100", "MATH_1250", "MATH_1300",
                "MATH_2010", "MATH_2120",
                "PSYC_2440",
            ],
        },
    },
    "RC4": {
        "label": "RC4 Scientific Ways of Knowing",
        "credits": 4,
        "courses": {
            "2025-26": [
                "BIOL_1000", "BIOL_2210", "BIOL_2230",
                "CHEM_1000", "CHEM_2110",
                "EXSC_2140",
                "HNRS_2210",
                "PHYS_1020", "PHYS_2140", "PHYS_2240",
            ],
        },
    },
    "RC5": {
        "label": "RC5 Social and Behavioral Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BSNS_3420",
                "ECON_2010", "ECON_2020",
                "EDUC_2110", "PSYC_2110",
                "LEAD_2300",
                "POSC_2020", "POSC_2100",
                "PSYC_2000",
                "SOCI_2010", "SOCI_2020",
            ],
        },
    },
    "RC6": {
        "label": "RC6 Humanistic and Artistic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "ENGL_2500", "ENGL_3590",
                "HIST_2030", "HIST_2040", "HIST_2110", "HIST_2120",
                "HNRS_2300", "HNRS_3100",
                "MUSC_2110", "MUSC_3120", "MUSC_3130",
                "SPAN_1010", "SPAN_1020",
            ],
        },
    },

    # AU Experience — complete one course in each category
    "AU1": {
        "label": "AU1 Understanding College",
        "credits": 1,
        "courses": {"2025-26": ["LART_1050"]},
    },
    "AU2": {
        "label": "AU2 Biblical Literacy",
        "credits": 3,
        "courses": {"2025-26": ["BIBL_2000"]},
    },
    "AU3": {
        "label": "AU3 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": ["BIBL_3410", "HNRS_3325", "RLGN_3010"],
        },
    },
    "AU4": {
        "label": "AU4 Personal Wellness",
        "credits": 2,
        "courses": {
            "2025-26": [
                "EXSC_2440", "NURS_1210", "PEHS_1000",
                "PSYC_3500", "SOCI_3500",
                "RLGN_1100",
            ],
        },
    },
    "AU5": {
        "label": "AU5 Civil Discourse and Conflict Transformation",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BIOL_3510",
                "COMM_3200",
                "HIST_2300",
                "HNRS_2125",
                "LART_2000",
                "PACT_2100",
                "PHIL_2120",
                "PSYC_3200",
                "RLGN_3120", "RLGN_3250", "PHIL_3250",
                "SOCI_2450",
                "SPED_2400",
            ],
        },
    },
    "AU6": {
        "label": "AU6 Global Ways of Knowing",
        "credits": 3,
        "courses": {
            "2025-26": [
                "BIBL_3310",
                "BSNS_3120",
                "COMM_3050",
                "DANC_3000",
                "EDUC_3550",
                "ENGL_2220",
                "ENGR_2080", "ENGR_2090",
                "HIST_3100", "HIST_3190",
                "HIST_3240", "HIST_3250", "HIST_3260",
                "HIST_3280", "HIST_3300", "HIST_3320", "RLGN_3320",   # World Religions (HIST/RLGN cross-listed)
                "HIST_3360", "HIST_3370", "HIST_3425",
                "HNRS_3221",
                "LEAD_4550",
                "MLAN_2000", "MLAN_3400",
                "MUSC_2330",
                "POSC_3320", "POSC_3450",
                "SOCI_2450", "SOCI_3470",
                "SPAN_2101", "SPAN_2102", "SPAN_2103", "SPAN_2104",
                "SPAN_3020",
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
    "ARTH_3040":      (["W4", "SI"],   "AND"),
    "BIBL_3000":      (["W1", "WI"],   "AND"),
    "RLGN_3000":      (["W1", "WI"],   "AND"),
    "BSNS_3120":      (["W7", "WI"],   "AND"),
    "COMM_2550":      (["W4", "SI"],   "AND"),   # 22-23 only
    "ENGL_2220":      (["W7", "SI"],   "AND"),
    "ENGL_2500":      (["W4", "WI"],   "AND"),
    "ENGL_3190":      (["F2", "WI"],   "AND"),
    "ENGL_3580":      (["F2", "WI"],   "AND"),
    "ENGR_2090":      (["W7", "WI"],   "AND"),
    "HIST_2300":      (["F2", "SI"],   "AND"),
    "HIST_3260":      (["W7", "WI"],   "AND"),
    "HIST_3300":      (["W7", "WI"],   "AND"),
    "HIST_3425":      (["W7", "WI"],   "AND"),
    "HNRS_2110":      (["F3", "W3"],   "OR"),
    "HNRS_2125":      (["F2", "SI"],   "AND"),
    "MLAN_2000":      (["W6", "W7"],   "OR"),
    "POSC_3320":      (["W7", "WI"],   "AND"),
    "POSC_3450":      (["W7", "WI"],   "AND"),
    "PSYC_3200":      (["F2", "SI"],   "AND"),
    "SOCI_2450":      (["F2", "W7"],   "OR"),
    "SPAN_3010":      (["W6", "WI"],   "AND"),
    "SPAN_3020":      (["W7", "SI"],   "AND"),
}

# W8 major-specific course list is in engines/sport_marketing.py (W8_BY_MAJOR dict)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS (required by audit_engine.py)
# ─────────────────────────────────────────────

def get_la_framework(catalog_year: str) -> str:
    """Return which LA framework a catalog year uses."""
    if catalog_year in ["2022-23", "2023-24", "2024-25"]:
        return "OLD_FRAMEWORK"
    elif catalog_year == "2025-26":
        return "RAVEN_CORE"
    raise ValueError(f"Unknown catalog year: {catalog_year}")


def get_la_requirements(catalog_year: str) -> dict:
    """Return the full LA requirements dict for a given catalog year."""
    fw = get_la_framework(catalog_year)
    if fw == "OLD_FRAMEWORK":
        result = {}
        for section, data in LA_OLD_FRAMEWORK.items():
            if section == "years":
                continue
            entry = dict(data)
            for field in ["courses", "credits"]:
                if field in entry and isinstance(entry[field], dict):
                    entry[field] = entry[field].get(catalog_year)
            result[section] = entry
        return result
    else:
        return dict(LA_RAVEN_CORE_2526)
