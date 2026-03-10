"""
Anderson University — Liberal Arts Requirements
Covers all 4 catalog years: 2022-23, 2023-24, 2024-25, 2025-26
"""

LA_OLD_FRAMEWORK = {
    "years": ["2022-23", "2023-24", "2024-25"],

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

    "F2": {
        "label": "F2 Civil Discourse & Critical Reasoning",
        "credits": {"2022-23": 2, "2023-24": 3, "2024-25": 3},
        "courses": {
            "2022-23": [
                "LART 1100", "BSNS 3420", "COMM 2200", "COMM 3200",
                "PHIL 2120", "RLGN 3120",
            ],
            "2023-24": [
                "LART 1100", "BSNS 3420", "COMM 2200", "COMM 3200",
                "PHIL 2120", "RLGN 3120",
                # Added from cross-listing PDF (2023-24)
                "ENGL 3190", "ENGL 3580",
                "HIST 2300",
                "HNRS 2125",
                "PSYC 3200",
            ],
            "2024-25": [
                "LART 1100", "BSNS 3420", "COMM 2200", "COMM 3200",
                "PHIL 2120", "RLGN 3120",
                "POSC 2020",
                "ENGR 2060",
                # Added from cross-listing PDF
                "ENGL 3190", "ENGL 3580",
                "HIST 2300",
                "HNRS 2125",
                "PSYC 3200",
            ],
        },
        "notes": {
            "2023-24": "Added cross-listed courses: ENGL 3190, ENGL 3580 (WI), HIST 2300 (SI), HNRS 2125 (SI), PSYC 3200 (SI)",
            "2024-25": "POSC 2020 renamed; ENGR 2060 now 2 hrs; cross-listed courses added",
        }
    },

    "F3": {
        "label": "F3 Written Communication",
        "credits": 6,
        "required_courses": ["ENGL 1100", "ENGL 1110", "ENGL 1120"],
        "wi_courses_needed": 2,
        # HNRS 2110 satisfies F3 OR W3 (OR rule — not both)
        "courses": {
            "2022-23": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "2023-24": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "2024-25": ["ENGL 1100", "ENGL 1110", "ENGL 1120", "HNRS 2110"],
        },
        "wi_courses": {
            "2022-23": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
            "2023-24": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
            "2024-25": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
        },
        "notes": "ENGL 1100 and ENGL 1110 are interchangeable; ENGL 1120 required. 2 WI-flagged courses beyond ENGL 1120. HNRS 2110 satisfies F3 OR W3 (not both).",
    },

    "F4": {
        "label": "F4 Speaking and Listening",
        "credits": 3,
        "required_courses": ["COMM 1000"],
        "si_courses_needed": 1,
        "si_courses": {
            "2022-23": ["BSNS 3210", "BSNS 4480", "COMM 3310"],
            "2023-24": [
                "BSNS 3210", "BSNS 4480", "COMM 3310",
                # Added from cross-listing PDF (SI-designated)
                "ARTH 3040", "ENGL 2220", "HIST 2300", "HNRS 2125",
                "PSYC 3200", "SPAN 3020",
            ],
            "2024-25": [
                "BSNS 3210", "BSNS 4480", "COMM 3310",
                "ARTH 3040", "ENGL 2220", "HIST 2300", "HNRS 2125",
                "PSYC 3200", "SPAN 3020",
            ],
        },
    },

    "F5": {
        "label": "F5 Quantitative Reasoning",
        "credits": 3,
        "courses": {
            "2022-23": [
                "CPSC 1100", "CPSC 1200", "CPSC 1400", "CPSC 2020",
                "MATH 1100", "MATH 1250", "MATH 1300", "MATH 1400",
                "MATH 2010", "MATH 2120", "PSYC 2440",
            ],
            "2023-24": [
                "CPSC 1100", "CPSC 1200", "CPSC 2020",
                "MATH 1100", "MATH 1220", "MATH 1250", "MATH 1300", "MATH 1400",
                "MATH 2010", "MATH 2120", "PSYC 2440",
            ],
            "2024-25": [
                "CPSC 2020",
                "MATH 1100", "MATH 1220", "MATH 1250", "MATH 1300",
                "MATH 2010", "MATH 2120", "PSYC 2440",
            ],
        },
    },

    "F6": {
        "label": "F6 Biblical Literacy",
        "credits": 3,
        "courses": {
            "2022-23": ["BIBL 2000"],
            "2023-24": ["BIBL 2000"],
            "2024-25": ["BIBL 2000"],
        },
    },

    "F7": {
        "label": "F7 Personal Wellness",
        "credits": 2,
        "courses": {
            "2022-23": ["PEHS 1000"],
            "2023-24": ["PEHS 1000"],
            "2024-25": ["PEHS 1000"],
        },
        "notes": "PEHS 1000 test-out available all years",
    },

    "W1": {
        "label": "W1 Christian Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": ["BIBL 3410", "RLGN 3010", "HNRS 3325"],
            "2023-24": [
                "BIBL 3410", "RLGN 3010", "HNRS 3325",
                # Added from cross-listing PDF — BIBL/RLGN 3000 satisfy W1 and WI
                "BIBL 3000", "RLGN 3000",
            ],
            "2024-25": [
                "BIBL 3410", "RLGN 3010", "HNRS 3325",
                "BIBL 3000", "RLGN 3000",
            ],
        },
    },

    "W2": {
        "label": "W2 Scientific Ways of Knowing",
        "credits": 4,
        "courses": {
            "2022-23": [
                "BIOL 1000", "BIOL 2080", "BIOL 2210", "BIOL 2230",
                "CHEM 1000", "CHEM 2110",
                "EXSC 2140", "HNRS 2210",
                "PHYS 1020", "PHYS 1140", "PHYS 2140", "PHYS 2240",
            ],
            "2023-24": [
                "BIOL 1000", "BIOL 2080", "BIOL 2210", "BIOL 2230",
                "CHEM 1000", "CHEM 2110",
                "CPSC 2040",
                "EXSC 2140", "HNRS 2210",
                "PHYS 1020", "PHYS 1140", "PHYS 2140", "PHYS 2240",
            ],
            "2024-25": [
                "BIOL 1000", "BIOL 2080", "BIOL 2210", "BIOL 2230",
                "CHEM 1000", "CHEM 2110",
                "CPSC 2040",
                "EXSC 2140", "HNRS 2210",
                "PHYS 1020", "PHYS 1140", "PHYS 2140", "PHYS 2240",
            ],
        },
    },

    "W3": {
        "label": "W3 Civic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "POSC 2100",
            ],
            "2023-24": [
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "POSC 2100",
            ],
            "2024-25": [
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "POSC 2100",
            ],
        },
    },

    "W4": {
        "label": "W4 Aesthetic Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": {
                "integrative": ["ARTH 2000", "HNRS 3000"],
                "AP_plus_AX": True,
                # ENGL 2500 satisfies W4 (AP) and WI
                "ap_courses": ["ENGL 2500"],
            },
            "2023-24": {
                "integrative": ["ARTH 3040", "HNRS 3000"],
                "AP_plus_AX": True,
                # ENGL 2500 satisfies W4 (AP) and WI
                "ap_courses": ["ENGL 2500"],
            },
            "2024-25": {
                "integrative": ["ARTH 3040", "HNRS 3000"],
                "AP_plus_AX": True,
                "ap_courses": ["ENGL 2500"],
                "notes": "ARTS 1210 listed at 2 hrs in AP section",
            },
        },
    },

    "W5": {
        "label": "W5 Social & Behavioral Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BSNS 3420", "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020",
            ],
            "2023-24": [
                "BSNS 3420", "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020",
            ],
            "2024-25": [
                "BSNS 3420", "ECON 2010", "ECON 2020",
                "EDUC 2110", "PSYC 2110",
                "LEAD 2300",
                "POSC 2020", "POSC 2100",
                "PSYC 2000",
                "SOCI 2010", "SOCI 2020",
            ],
        },
    },

    "W6": {
        "label": "W6 Modern Languages",
        "credits": 4,
        "courses": {
            "2022-23": [
                "FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020",
                "SPAN 1010", "SPAN 1020", "MLAN 2000",
                # SPAN 3010 satisfies W6 and WI
                "SPAN 3010",
            ],
            "2023-24": [
                "FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020",
                "SPAN 1010", "SPAN 1020", "MLAN 2000",
                "SPAN 3010",
            ],
            "2024-25": [
                "FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020",
                "SPAN 1010", "SPAN 1020", "MLAN 2000",
                "SPAN 3010",
            ],
        },
        "notes": "Part of the 7-hr Global/Intercultural block with W7. MLAN 2000 may count W6 OR W7 (not both). SPAN 3010 satisfies W6 and WI.",
    },

    "W7": {
        "label": "W7 Global/Intercultural Ways of Knowing",
        "credits": 3,
        "courses": {
            "2022-23": [
                "BSNS 3120", "COMM 3050", "EDUC 3550",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260", "HIST 3280", "HIST 3300", "HIST 3320",
                "HIST 3360", "HIST 3370", "HIST 3425",
                "MLAN 3400",
                "POSC 3320", "POSC 3450",
                "SOCI 2450", "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
            ],
            "2023-24": [
                "BSNS 3120", "COMM 3050", "EDUC 3550",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260", "HIST 3280", "HIST 3300", "HIST 3320",
                "HIST 3360", "HIST 3370", "HIST 3425",
                "MLAN 3400",
                "POSC 3320", "POSC 3450",
                "SOCI 2450", "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
                # Added from cross-listing PDF
                "ENGL 2220",   # W7 and SI
                "ENGR 2090",   # W7 and WI
                "MLAN 2000",   # W6 OR W7 — included here; engine must enforce OR logic
            ],
            "2024-25": [
                "BSNS 3120", "COMM 3050", "EDUC 3550",
                "HIST 3100", "HIST 3190", "HIST 3240", "HIST 3250",
                "HIST 3260", "HIST 3280", "HIST 3300", "HIST 3320",
                "HIST 3360", "HIST 3370", "HIST 3425",
                "MLAN 3400",
                "POSC 3320", "POSC 3450",
                "SOCI 2450", "SOCI 3470",
                "SPAN 2101", "SPAN 2102", "SPAN 2103", "SPAN 2104",
                "SPAN 3020",
                "ENGL 2220", "ENGR 2090", "MLAN 2000",
            ],
        },
        "notes": "BSNS 3120 counts as both W7 AND WI. MLAN 2000 counts W6 OR W7 (not both).",
    },

    "W8": {
        "label": "W8 Experiential Ways of Knowing",
        "credits": 0,
        "auto_satisfy_if": "F1",
        "auto_display_course": "BSNS 1050",
        "courses": {
            "2022-23": ["BSNS 4800", "BSNS 4810"],
            "2023-24": ["BSNS 4800", "BSNS 4810"],
            "2024-25": ["BSNS 4800", "BSNS 4810"],
        },
        "notes": "Auto-satisfied when F1 (LART 1050) is completed. Displays BSNS 1050 in the W8 row.",
    },
}


# ─────────────────────────────────────────────
# WI courses by year (Writing Intensive)
# ─────────────────────────────────────────────
WI_COURSES = {
    "2022-23": [
        "BSNS 3120", "BSNS 4910", "ENGL 1120",
        "BIBL 3000", "RLGN 3000",
        "ENGL 3190", "ENGL 3580",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "POSC 3320", "POSC 3450",
        "SPAN 3010",
        "ENGL 2500",
    ],
    "2023-24": [
        "BSNS 3120", "BSNS 4910", "ENGL 1120",
        "BIBL 3000", "RLGN 3000",
        "ENGL 3190", "ENGL 3580",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "POSC 3320", "POSC 3450",
        "SPAN 3010",
        "ENGL 2500",
    ],
    "2024-25": [
        "BSNS 3120", "BSNS 4910", "ENGL 1120",
        "BIBL 3000", "RLGN 3000",
        "ENGL 3190", "ENGL 3580",
        "ENGR 2090",
        "HIST 3260", "HIST 3300", "HIST 3425",
        "POSC 3320", "POSC 3450",
        "SPAN 3010",
        "ENGL 2500",
    ],
}

# ─────────────────────────────────────────────
# SI courses by year (Speaking Intensive)
# ─────────────────────────────────────────────
SI_COURSES = {
    "2022-23": [
        "BSNS 3210", "BSNS 4480", "COMM 3310",
    ],
    "2023-24": [
        "BSNS 3210", "BSNS 4480", "COMM 3310",
        "ARTH 3040", "ENGL 2220",
        "HIST 2300", "HNRS 2125",
        "PSYC 3200", "SPAN 3020",
    ],
    "2024-25": [
        "BSNS 3210", "BSNS 4480", "COMM 3310",
        "ARTH 3040", "ENGL 2220",
        "HIST 2300", "HNRS 2125",
        "PSYC 3200", "SPAN 3020",
    ],
}

# ─────────────────────────────────────────────
# OR-only cross-listings (course may satisfy ONE but not both)
# ─────────────────────────────────────────────
OR_CROSS_LISTINGS = {
    # course: [option_a, option_b]  — student gets credit for whichever is more beneficial
    "HNRS 2110": ["F3", "W3"],
    "MLAN 2000": ["W6", "W7"],
    "SOCI 2450": ["F2", "W7"],
}


# ─────────────────────────────────────────────
# NEW FRAMEWORK: 2025-26
# ─────────────────────────────────────────────

LA_RAVEN_CORE_2526 = {
    "year": "2025-26",
    "icc_exemption": "Students completing Indiana College Core (ICC) are EXEMPT from RC1-RC6 but must complete AU Experience (AU1-AU6)",

    "RAVEN_CORE": {
        "label": "Raven Core",
        "total_credits": 30,
        "note": "At least one course in each RC category required",

        "RC1": {
            "label": "RC1 Written Communication",
            "max_credits": 6,
            "courses": ["ENGL 1110", "ENGL 1120", "HNRS 2110"],
            "grade_required": {"ENGL 1110": "C-", "ENGL 1120": "C-"},
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
                "CPSC 2020", "LEAD 3100",
                "MATH 1100", "MATH 1250", "MATH 1300", "MATH 2010", "MATH 2120",
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
            "courses": ["EXSC 2440", "NURS 1210", "PEHS 1000", "PSYC 3500", "SOCI 3500", "RLGN 1100"],
        },
        "AU5": {
            "label": "AU5 Civil Discourse & Conflict Transformation",
            "credits_range": (2, 3),
            "courses": [
                "BIOL 3510", "COMM 3200",
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
        "AU6": {
            "label": "AU6 Global Ways of Knowing",
            "credits_range": (3, 4),
            "courses": [
                "BIBL 3310", "BSNS 3120", "COMM 3050",
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

    "EMBEDDED_COMPETENCIES": {
        "note": "In 25-26, WI, SI, and Experiential competencies are embedded in the major definition, not tracked separately as LA requirements.",
        "WI": "Writing Intensive — satisfied by designated courses within the major",
        "SI": "Speaking Intensive — BSNS 2550 in the Business Core satisfies this",
        "W8_equiv": "Experiential — BSNS 4800 in the Business Core satisfies this",
    },
}


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
        # Inject WI and SI course lists for the year
        result["_WI_COURSES"] = WI_COURSES.get(catalog_year, [])
        result["_SI_COURSES"] = SI_COURSES.get(catalog_year, [])
        result["_OR_CROSS_LISTINGS"] = OR_CROSS_LISTINGS
        return result
    else:
        return LA_RAVEN_CORE_2526


def is_wi_course(course_code: str, catalog_year: str) -> bool:
    """Return True if a course is Writing Intensive for the given catalog year."""
    return course_code in WI_COURSES.get(catalog_year, [])


def is_si_course(course_code: str, catalog_year: str) -> bool:
    """Return True if a course is Speaking Intensive for the given catalog year."""
    return course_code in SI_COURSES.get(catalog_year, [])


def get_or_cross_listing(course_code: str) -> list:
    """If a course has an OR cross-listing, return the two options. Else return []."""
    return OR_CROSS_LISTINGS.get(course_code, [])


def course_satisfies_la(course_code: str, catalog_year: str) -> list:
    satisfied = []
    fw = get_la_framework(catalog_year)

    if fw == "OLD_FRAMEWORK":
        reqs = get_la_requirements(catalog_year)
        for section, data in reqs.items():
            if section.startswith("_"):
                continue
            courses = data.get("courses", [])
            if isinstance(courses, dict):
                # W4 has nested structure
                all_courses = []
                for v in courses.values():
                    if isinstance(v, list):
                        all_courses.extend(v)
                courses = all_courses
            if course_code in courses:
                satisfied.append(section)
            for extra in ["si_courses", "wi_courses"]:
                extra_list = data.get(extra, [])
                if isinstance(extra_list, dict):
                    extra_list = extra_list.get(catalog_year, [])
                if course_code in extra_list:
                    tag = f"{section}_WI" if extra == "wi_courses" else f"{section}_SI"
                    if tag not in satisfied:
                        satisfied.append(tag)
        # Also tag WI/SI globally
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
            if au_key in ("label", "total_credits_range"):
                continue
            if isinstance(au_data, dict) and course_code in au_data.get("courses", []):
                satisfied.append(au_key)

    return satisfied


# ─────────────────────────────────────────────
# CROSS-LISTING MAP (quick reference)
# ─────────────────────────────────────────────

CROSS_LISTED_COURSES = {
    "BSNS 3420": {
        "2022-23": ["F2", "W5", "Business Core"],
        "2023-24": ["F2", "W5", "Business Core"],
        "2024-25": ["F2", "W5", "Business Core"],
        "2025-26": ["RC5", "Business Core"],
    },
    "BSNS 3120": {
        "2022-23": ["W7", "WI", "Business Core (not required)"],
        "2023-24": ["W7", "WI", "Business Core (not required)"],
        "2024-25": ["W7", "WI"],
        "2025-26": ["AU6", "Business Core"],
    },
    "BSNS 3210": {
        "2022-23": ["F4 SI", "Major (Sport Marketing / Marketing)"],
        "2023-24": ["F4 SI", "Major (Sport Marketing / Marketing)"],
        "2024-25": ["F4 SI", "Major (Sport Marketing / Marketing)"],
        "2025-26": [],
    },
    "BSNS 4910": {
        "2022-23": ["WI", "Business Core"],
        "2023-24": ["WI", "Business Core"],
        "2024-25": ["WI", "Business Core"],
        "2025-26": ["Business Core"],
    },
    "BSNS 4800": {
        "2022-23": ["W8", "Major elective"],
        "2023-24": ["W8", "Major elective"],
        "2024-25": ["W8", "Major elective"],
        "2025-26": ["Business Core", "Experiential"],
    },
    "LART 1050": {
        "2022-23": ["F1", "→ auto-satisfies W8"],
        "2023-24": ["F1", "→ auto-satisfies W8"],
        "2024-25": ["F1", "→ auto-satisfies W8"],
        "2025-26": ["AU1"],
    },
    # Added from PDF cross-listing table
    "ARTH 3040":  {"2023-24": ["W4", "SI"], "2024-25": ["W4", "SI"]},
    "BIBL 3000":  {"2023-24": ["W1", "WI"], "2024-25": ["W1", "WI"]},
    "RLGN 3000":  {"2023-24": ["W1", "WI"], "2024-25": ["W1", "WI"]},
    "ENGL 2220":  {"2023-24": ["W7", "SI"], "2024-25": ["W7", "SI"]},
    "ENGL 2500":  {"2023-24": ["W4", "WI"], "2024-25": ["W4", "WI"]},
    "ENGL 3190":  {"2023-24": ["F2", "WI"], "2024-25": ["F2", "WI"]},
    "ENGL 3580":  {"2023-24": ["F2", "WI"], "2024-25": ["F2", "WI"]},
    "ENGR 2090":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "HIST 2300":  {"2023-24": ["F2", "SI"], "2024-25": ["F2", "SI"]},
    "HIST 3260":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "HIST 3300":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "HIST 3425":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "HNRS 2110":  {"2023-24": ["F3 OR W3"], "2024-25": ["F3 OR W3"]},  # OR rule
    "HNRS 2125":  {"2023-24": ["F2", "SI"], "2024-25": ["F2", "SI"]},
    "MLAN 2000":  {"2023-24": ["W6 OR W7"], "2024-25": ["W6 OR W7"]},  # OR rule
    "POSC 3320":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "POSC 3450":  {"2023-24": ["W7", "WI"], "2024-25": ["W7", "WI"]},
    "PSYC 3200":  {"2023-24": ["F2", "SI"], "2024-25": ["F2", "SI"]},
    "SOCI 2450":  {"2023-24": ["F2 OR W7"], "2024-25": ["F2 OR W7"]},  # OR rule
    "SPAN 3010":  {"2023-24": ["W6", "WI"], "2024-25": ["W6", "WI"]},
    "SPAN 3020":  {"2023-24": ["W7", "SI"], "2024-25": ["W7", "SI"]},
}


# ─────────────────────────────────────────────
# W8 EXPERIENTIAL — Per-Major Course Lookup
# Source: W8 Experiential Ways of Knowing sheet (updated 11/14/2023)
# "and" = course is REQUIRED for the major (bold in original)
# "*"   = no required experiential courses; listed courses are optional
# ─────────────────────────────────────────────

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
        "required_in_major": ["BSNS 4800"],  # required in major
    },
    "business_integrative_leadership": {
        "courses": ["LEAD 4990"],
        "required_in_major": ["LEAD 4990"],
    },
    # Non-FSB majors
    "psychology": {
        "courses": ["PSYC 2850", "PSYC 3450", "PSYC 4100", "PSYC 4210", "PSYC 4520"],
        "no_required_experiential": True,  # asterisk in original
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
    "visual_communication_design": {
        "courses": ["ARTH 4800"],
        "required_in_major": ["ARTH 4800"],
    },
    "literary_studies": {
        "courses": ["ENGL 4910"],
        "required_in_major": [],
    },
    "writing": {
        "courses": ["ENGL 4910"],
        "required_in_major": [],
    },
    "language_arts_teaching": {
        "courses": ["ENGL 4910"],
        "required_in_major": [],
    },
    "elementary_education": {
        "courses": ["EDUC 4010"],
        "required_in_major": ["EDUC 4010"],
    },
    "christian_ministries": {
        "courses": ["CMIN 3340", "CMIN 4810", "CMIN 4850", "THFE 7810"],
        "required_in_major": [],
    },
    "youth_ministries": {
        "courses": ["CMIN 3340", "CMIN 4810", "CMIN 4850", "THFE 7810"],
        "required_in_major": [],
    },
    "ministry_studies_online": {
        "courses": ["CMIN 4810"],
        "required_in_major": [],
    },
    "csf_complementary": {
        "courses": ["RLGN 4960"],
        "required_in_major": ["RLGN 4960"],
    },
    "math_ba": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
    "math_bs": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
    "math_economics_ba": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
    "math_finance_ba": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
    "math_teaching_ba": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
    "math_decision_science_ba": {
        "courses": ["MATH 4000"],
        "required_in_major": ["MATH 4000"],
    },
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
        "no_required_experiential": True,  # asterisk
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
        "no_required_experiential": True,  # asterisk
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
    # Majors with no required experiential (use LAWK 18EC as fallback)
    "biology_ba":   {"courses": ["LAWK 18EC"], "no_required_experiential": True},
    "biology_bs":   {"courses": ["LAWK 18EC"], "no_required_experiential": True},
}


def get_w8_courses_for_major(major_key: str) -> dict:
    """
    Return W8-eligible courses for a given major key.
    Returns dict with 'courses' list and metadata.
    Falls back to LAWK 18EC (exception process) if major not found.
    """
    return W8_BY_MAJOR.get(major_key, {
        "courses": ["LAWK 18EC"],
        "no_required_experiential": True,
        "notes": "No W8 course defined for this major — exception process applies",
    })


def course_satisfies_w8(course_code: str, major_key: str) -> bool:
    """Return True if a course satisfies W8 for the given major."""
    w8_data = get_w8_courses_for_major(major_key)
    return course_code in w8_data.get("courses", [])
