"""
Anderson University — Liberal Arts Requirements
Covers all 4 catalog years: 2022-23, 2023-24, 2024-25, 2025-26

Old Framework (22-23 through 24-25): F1-F7 Foundational Skills + W1-W8 Ways of Knowing
New Framework (25-26): Raven Core (RC1-RC6) + AU Experience (AU1-AU6)
"""

# ─────────────────────────────────────────────
# OLD FRAMEWORK: 2022-23 through 2024-25
# ─────────────────────────────────────────────

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
        # Special rule: if F1 satisfied → W8 auto-satisfied (display BSNS 1050 in W8 row)
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
                "PHIL 2120", "RLGN 3120",  # LART 1100 changed to 3 hrs; COMM 3200 added
            ],
            "2024-25": [
                "LART 1100", "BSNS 3420", "COMM 2200", "COMM 3200",
                "PHIL 2120", "RLGN 3120",
                "POSC 2020",  # renamed "Introduction to World Politics"
                "ENGR 2060",  # now 2 hrs
            ],
        },
        "notes": {
            "2023-24": "LART 1100 changed from 2 to 3 hrs; COMM 3200 Communication Ethics added",
            "2024-25": "POSC 2020 renamed; ENGR 2060 now 2 hrs",
        }
    },

    "F3": {
        "label": "F3 Written Communication",
        "credits": 6,
        "required_courses": ["ENGL 1100", "ENGL 1110", "ENGL 1120"],
        "wi_courses_needed": 2,  # 2 WI-designated courses beyond ENGL 1120
        "wi_courses": {
            "2022-23": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
            "2023-24": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
            "2024-25": ["BSNS 3120", "BSNS 4910", "ENGL 1120"],
        },
        "notes": "ENGL 1100 and ENGL 1110 are interchangeable; ENGL 1120 required. 2 WI-flagged courses beyond ENGL 1120.",
    },

    "F4": {
        "label": "F4 Speaking and Listening",
        "credits": 3,
        "required_courses": ["COMM 1000"],
        "si_courses_needed": 1,  # 1 SI-designated course beyond COMM 1000
        "si_courses": {
            "2022-23": ["BSNS 3210", "BSNS 4480", "COMM 3310"],
            "2023-24": ["BSNS 3210", "BSNS 4480", "COMM 3310"],
            "2024-25": ["BSNS 3210", "BSNS 4480", "COMM 3310"],
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
                "CPSC 1100", "CPSC 1200", "CPSC 2020",  # CPSC 1400 replaced by 2020
                "MATH 1100", "MATH 1220", "MATH 1250", "MATH 1300", "MATH 1400",
                "MATH 2010", "MATH 2120", "PSYC 2440",
            ],
            "2024-25": [
                "CPSC 2020",  # CPSC 1100/1200 removed; MATH 1400 removed
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
            "2023-24": ["BIBL 3410", "RLGN 3010", "HNRS 3325"],
            "2024-25": ["BIBL 3410", "RLGN 3010", "HNRS 3325"],
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
                "CPSC 2040",  # added
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
                "AP_plus_AX": True,  # Can satisfy with AP + AX courses
            },
            "2023-24": {
                "integrative": ["ARTH 3040", "HNRS 3000"],  # ARTH 2000 replaced by ARTH 3040
                "AP_plus_AX": True,
            },
            "2024-25": {
                "integrative": ["ARTH 3040", "HNRS 3000"],
                "AP_plus_AX": True,
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
            "2022-23": ["FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020", "SPAN 1010", "SPAN 1020", "MLAN 2000"],
            "2023-24": ["FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020", "SPAN 1010", "SPAN 1020", "MLAN 2000"],
            "2024-25": ["FREN 1010", "FREN 1020", "GERM 1010", "GERM 1020", "SPAN 1010", "SPAN 1020", "MLAN 2000"],
        },
        "notes": "Part of the 7-hr Global/Intercultural block with W7. Students may fulfill with prior language credit.",
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
            ],
        },
        "notes": "BSNS 3120 counts as both W7 AND a course in the Business Core cross-listing",
    },

    "W8": {
        "label": "W8 Experiential Ways of Knowing",
        "credits": 0,  # auto-satisfied if F1 is satisfied
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
# NEW FRAMEWORK: 2025-26
# Raven Core (RC1-RC6) + AU Experience (AU1-AU6)
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
        # Return per-year slices from the old framework
        result = {}
        for section, data in LA_OLD_FRAMEWORK.items():
            if section == "years":
                continue
            entry = dict(data)
            # Resolve per-year course lists
            for field in ["courses", "credits"]:
                if field in entry and isinstance(entry[field], dict):
                    entry[field] = entry[field].get(catalog_year, entry[field])
            if "si_courses" in entry and isinstance(entry["si_courses"], dict):
                entry["si_courses"] = entry["si_courses"].get(catalog_year, [])
            if "wi_courses" in entry and isinstance(entry["wi_courses"], dict):
                entry["wi_courses"] = entry["wi_courses"].get(catalog_year, [])
            result[section] = entry
        return result
    else:
        return LA_RAVEN_CORE_2526


def course_satisfies_la(course_code: str, catalog_year: str) -> list:
    """
    Given a course code and catalog year, return a list of LA categories it satisfies.
    E.g. 'BSNS 3420' in 2022-23 returns ['F2', 'W5']
    """
    satisfied = []
    fw = get_la_framework(catalog_year)

    if fw == "OLD_FRAMEWORK":
        reqs = get_la_requirements(catalog_year)
        for section, data in reqs.items():
            courses = data.get("courses", [])
            if isinstance(courses, dict):
                courses = courses.get(catalog_year, [])
            if course_code in courses:
                satisfied.append(section)
            # Also check si_courses and wi_courses
            for extra in ["si_courses", "wi_courses"]:
                extra_list = data.get(extra, [])
                if isinstance(extra_list, dict):
                    extra_list = extra_list.get(catalog_year, [])
                if course_code in extra_list:
                    tag = f"{section}_WI" if extra == "wi_courses" else f"{section}_SI"
                    if tag not in satisfied:
                        satisfied.append(tag)
    else:
        # Raven Core / AU Experience
        data = LA_RAVEN_CORE_2526
        for rc_key, rc_data in data["RAVEN_CORE"].items():
            if rc_key == "label" or rc_key == "total_credits" or rc_key == "note":
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
# CROSS-LISTING MAP (quick lookup)
# ─────────────────────────────────────────────

CROSS_LISTED_COURSES = {
    # course: {year: [categories_it_satisfies]}
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
        "2025-26": [],  # Removed from Sport Marketing/Sports Management in 25-26
    },
    "BSNS 4910": {
        "2022-23": ["WI", "Business Core"],
        "2023-24": ["WI", "Business Core"],
        "2024-25": ["WI", "Business Core"],
        "2025-26": ["Business Core"],  # No longer explicitly WI
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
}
