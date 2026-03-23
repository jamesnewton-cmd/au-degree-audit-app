"""
Anderson University — Non-FSB Department Requirements
All majors, minors, and complementary majors across all 4 catalog years.

Departments:
  Biology / Natural Sciences
  Chemistry
  Physics & Engineering Physics
  Computer Science & Mathematics
  Cybersecurity / Security Studies
  Data Science
  Communication & Design Arts / Humanities
  English
  History & Political Science
  Modern Languages
  Music, Theatre & Dance / School of Music & Performing Arts
  Christian Ministry
  Kinesiology / Exercise Science
  Nursing
  Psychology
  Public Health
  Social Work, Criminal Justice & Family Science
  Teacher Education
  Peace & Conflict Transformation
  Women's Studies
  Statistics
  Interdisciplinary / Honors
  Engineering (Physical Sciences)
"""

# ─────────────────────────────────────────────
# BIOLOGY / NATURAL SCIENCES
# ─────────────────────────────────────────────

BIOLOGY = {
    "biology_ba": {
        "2022-23": {
            "name": "Biology (BA)",
            "total_credits": 48,
            "required": [
                "BIOL 2210", "BIOL 2220", "BIOL 2240", "BIOL 3030",
                # 3510 OR 3920
                "BIOL 4050", "BIOL 4070", "BIOL 4910", "BIOL 4920",
                "CHEM 2110", "CHEM 2120", "CHEM 2210",
            ],
            "choose_one": ["BIOL 3510", "BIOL 3920"],
            "elective_upper_div": {"credits": 8, "dept": "BIOL", "min_level": 3000},
            "notes": "BIOL 2230, 3800, 4700 do not apply toward major",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Biology (BA)",
            "total_credits": 49,
            "department": "Natural Sciences",
            "required": [
                "BIOL 2210", "BIOL 2220", "BIOL 2240", "BIOL 3030",
                "BIOL 4050", "BIOL 4070", "BIOL 4910", "BIOL 4920",
                "CHEM 2110", "CHEM 2120", "CHEM 2210",
            ],
            "choose_one": ["BIOL 3510", "BIOL 3920"],
            "elective_upper_div": {"credits": 8, "dept": "BIOL", "min_level": 3000},
            "notes": "Dept. reorganized under Natural Sciences in 25-26",
        },
    },
    "biology_bs": {
        "2022-23": {
            "name": "Biology (BS)",
            "total_credits": 72,
            "required": [
                "BIOL 2210", "BIOL 2220", "BIOL 2240", "BIOL 3030",
                "BIOL 4050", "BIOL 4070", "BIOL 4910", "BIOL 4920",
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 2220",
            ],
            "choose_one_phys": ["PHYS 2140", "PHYS 2240"],
            "choose_one_phys2": ["PHYS 2150", "PHYS 2250"],
            "choose_one_stats": ["MATH 2120", "PSYC 2440"],
            "elective_upper_div": {"credits": 12, "dept": "BIOL", "min_level": 3000},
            "additional_hours": 4,
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23", "department": "Natural Sciences"},
    },
    "biochemistry_ba": {
        "2022-23": {
            "name": "Biochemistry (BA)",
            "total_credits": 56,
            "required": [
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 2220",
                "BIOL 2210", "BIOL 2220", "BIOL 2240", "BIOL 3030",
                "BIOL 4050",
                "BIOL 4210", "BIOL 4220",   # same as CHEM 4210, 4220
                "BIOL 4310",
                "BIOL 4910", "BIOL 4920",   # same as CHEM/PHYS 4910, 4920
            ],
            "choose_one_phys": ["PHYS 2140", "PHYS 2240"],
            "choose_one_stats": ["MATH 2120", "PSYC 2440"],
            "notes": "BIOL/CHEM cross-listed courses: 4210, 4220, 4910, 4920",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23", "department": "Natural Sciences"},
    },
    "biochemistry_bs": {
        "2022-23": {
            "name": "Biochemistry (BS)",
            "total_credits": 76,
            "required": [
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 2220",
                "CHEM 3100", "CHEM 4110", "CHEM 4510", "CHEM 4520",
                "BIOL 2210", "BIOL 2220", "BIOL 2240", "BIOL 3030",
                "BIOL 4050", "BIOL 4310",
                "BIOL 4210",  # BIOL/CHEM 4210
                "BIOL 4220",  # BIOL/CHEM 4220
                "BIOL 4910", "BIOL 4920",  # BIOL/CHEM/PHYS 4910/4920
                "MATH 2010",
            ],
            "choose_one_phys": ["PHYS 2140", "PHYS 2240"],
            "choose_one_phys2": ["PHYS 2150", "PHYS 2250"],
            "choose_one_stats": ["MATH 2120", "PSYC 2440"],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23", "department": "Natural Sciences"},
    },
    "biology_minor": {
        "all_years": {
            "name": "Biology Minor",
            "total_credits": 16,
            "notes": "Select from BIOL courses; at least 8 hrs upper-division",
        },
    },
}

# ─────────────────────────────────────────────
# CHEMISTRY (22-23 through 24-25 only)
# ─────────────────────────────────────────────

CHEMISTRY = {
    "chemistry_ba": {
        "2022-23": {
            "name": "Chemistry (BA)",
            "total_credits": 52,
            "required": [
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 2220",
                "CHEM 3100", "CHEM 4110",
                "BIOL 2210",
                "MATH 2010", "MATH 2020",
                "PHYS 2140",  # or 2240
                "PHYS 2150",  # or 2250
            ],
            "elective_chem": {"credits": 8, "dept": "CHEM"},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": None,  # Absorbed into Natural Sciences; standalone listing removed
    },
    "chemistry_bs": {
        "2022-23": {
            "name": "Chemistry (BS)",
            "total_credits": 60,
            "required": [
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 2220",
                "CHEM 3100", "CHEM 4110", "CHEM 4510", "CHEM 4520",
                "MATH 2010", "MATH 2020", "MATH 3010",
                "PHYS 2140", "PHYS 2150",  # or 2240/2250
            ],
            "elective_chem": {"credits": 6, "dept": "CHEM"},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": None,
    },
    "chemistry_minor": {
        "all_years": {
            "name": "Chemistry Minor",
            "total_credits": 16,
            "required": ["CHEM 2110", "CHEM 2120"],
            "elective_upper": {"credits": 8, "dept": "CHEM"},
        },
    },
}

# ─────────────────────────────────────────────
# PHYSICS (22-23 only for BA/BS; minor persists)
# ─────────────────────────────────────────────

PHYSICS = {
    "physics_ba": {
        "2022-23": {
            "name": "Physics (BA)",
            "total_credits": 63,
            "required": [
                "PHYS 1000", "PHYS 1020", "PHYS 1240",
                "PHYS 2140", "PHYS 2150", "PHYS 2240", "PHYS 2250",
                "PHYS 3130", "PHYS 4510", "PHYS 4520", "PHYS 4910", "PHYS 4920",
                "MATH 2010", "MATH 2020", "MATH 3010",
                "CHEM 2110", "CHEM 2120",
            ],
        },
        "2023-24": None,  # Removed
        "2024-25": None,
        "2025-26": None,
    },
    "engineering_physics_bs": {
        "2022-23": {
            "name": "Engineering Physics (BS)",
            "total_credits": 76,
            "required": [
                "PHYS 2140", "PHYS 2150", "PHYS 2240", "PHYS 2250",
                "PHYS 3130", "PHYS 4510", "PHYS 4520", "PHYS 4910", "PHYS 4920",
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3100",
                "CHEM 2110", "CHEM 2120",
                "ENGR 2001", "ENGR 2002", "ENGR 2003", "ENGR 2010", "ENGR 2090",
                "ENGR 2130",
            ],
        },
        "2023-24": None,
        "2024-25": None,
        "2025-26": None,
    },
    "physical_science_ba": {
        "2022-23": {
            "name": "Physical Science (BA) — Teaching Track",
            "total_credits": 50,
            "required": [
                "PHYS 1000", "PHYS 1020", "PHYS 1240",
                "PHYS 2240", "PHYS 2250", "PHYS 3130", "PHYS 4510", "PHYS 4520",
                "PHYS 4910", "PHYS 4920",
                "CHEM 2110", "CHEM 2120", "CHEM 2210", "CHEM 3100",
                "MATH 2010", "MATH 2020",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": None,
    },
    "physics_minor": {
        "2022-23": {
            "name": "Physics Minor",
            "total_credits": 16,
            "required": ["PHYS 2140", "PHYS 2240"],
            "elective": {"credits": 8, "dept": "PHYS"},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────
# COMPUTER SCIENCE
# ─────────────────────────────────────────────

COMPUTER_SCIENCE = {
    "cs_ba": {
        "2022-23": {
            "name": "Computer Science (BA)",
            "total_credits": 59,
            "required": [
                "CPSC 1400", "CPSC 1500", "CPSC 2100", "CPSC 2330",
                "CPSC 2420", "CPSC 2430", "CPSC 2500",
                "ENGR 2200",
                "CPSC 2250",   # MATH 2200/CPSC 2250
                "CPSC 3380", "CPSC 3410", "CPSC 4420", "CPSC 4430",
                "CPSC 4950", "CPSC 4960",
            ],
            "elective_upper": {"credits": 6, "min_level": 2000, "dept": ["CPSC", "ENGR"]},
            "math": {"credits": "3-4", "choose_from": ["MATH 1300 and above"]},
        },
        "2023-24": {
            "name": "Computer Science (BA)",
            "total_credits": 59,
            "required": [
                "CPSC 2020", "CPSC 1500", "CPSC 2100", "CPSC 2330",  # CPSC 1400 → 2020
                "CPSC 2420", "CPSC 2430", "CPSC 2500",
                "ENGR 2200", "CPSC 2250",
                "CPSC 3380", "CPSC 3410", "CPSC 4420", "CPSC 4430",
                "CPSC 4950", "CPSC 4960",
            ],
            "elective_upper": {"credits": 6, "dept": ["CPSC","ENGR","MATH"]},
            "math": {"credits": "3-4", "dept": "MATH"},
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": None,  # Only BS in 25-26 catalog listing
    },
    "cs_bs": {
        "2022-23": {
            "name": "Computer Science (BS)",
            "total_credits": 82,
            "required": [
                "CPSC 1400", "CPSC 1500", "CPSC 2100", "CPSC 2330",
                "CPSC 2420", "CPSC 2430", "CPSC 2500",
                "ENGR 2200", "CPSC 2250",
                "CPSC 3380", "CPSC 3410", "CPSC 4420", "CPSC 4430",
                "CPSC 4950", "CPSC 4960",
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 3010",
            ],
        },
        "2023-24": {
            "name": "Computer Science (BS)",
            "total_credits": 71,
            "required": [
                "CPSC 2020", "CPSC 1500", "CPSC 2100", "CPSC 2330",
                "CPSC 2420", "CPSC 2430", "CPSC 2500",
                "ENGR 2200", "CPSC 2250",
                "CPSC 3380", "CPSC 3410", "CPSC 4420", "CPSC 4430",
                "CPSC 4950", "CPSC 4960",
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 3010",
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Computer Science (BS)",
            "total_credits": 72,
            "required": [
                "CPSC 2020", "CPSC 2030", "CPSC 2100", "CPSC 2330",
                "CPSC 2420", "CPSC 2430", "CPSC 2500",
                "CPSC 2150", "CPSC 3410", "CPSC 4420", "CPSC 4430",
                "MATH 2200",   # MATH 2200/CPSC 2250
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 3010",
                "POSC 2420",
            ],
            "choose_one": ["CPSC 4480", "CPSC 4800"],
            "elective_upper": {"credits": 10, "dept": ["CPSC", "ENGR", "MATH", "PHYS"]},
            "notes": "New courses 25-26: CPSC 2030, 2150; CPSC 4840 added to catalog",
        },
    },
    "cs_complementary": {
        "all_years": {
            "name": "Computer Science Complementary Major",
            "total_credits": 32,
            "required": ["CPSC 2020", "CPSC 2030", "CPSC 2100", "CPSC 2500"],
            "elective": {"credits": 16, "min_level": 2000, "dept": ["CPSC", "MATH", "ENGR"]},
        },
    },
    "cs_minor": {
        "all_years": {
            "name": "Computer Science Minor",
            "total_credits": 16,
            "required": ["CPSC 2020", "CPSC 2100"],
            "elective_upper": {"credits": 10, "dept": ["CPSC","ENGR"]},
        },
    },
    "cybersecurity_major": {
        "2022-23": {
            "name": "Cybersecurity",
            "total_credits": 56,
            "dept": "Security Studies",
            "foundation": ["CPSC 2080", "CPSC 2180", "CPSC 2300", "MATH 2120", "CPSC 2250",
                           "POSC 2030", "POSC 2200", "POSC 2400", "POSC 2420"],
            "professional_core": ["CPSC 3380", "CPSC 3410", "CPSC 4080", "CPSC 4480"],
            "national_security": ["POSC 3350", "POSC 3370"],   # POSC/CRIM 3350
            "ethics": ["PHIL 3250"],   # PHIL/RLGN 3250
            "elective": {"credits": "8-9", "choose_from": ["CPSC 2000+", "CRIM 2520", "POSC 3310", "POSC 3250"]},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Cybersecurity",
            "total_credits": 64,
            "dept": "Computer Science & Mathematics",  # Moved dept
            "foundation": ["CPSC 2080", "CPSC 2180", "CPSC 2300", "MATH 2120", "CPSC 2250",
                           "POSC 2030", "POSC 2200", "POSC 2400", "POSC 2420"],
            "professional_core": [
                "CPSC 2150", "CPSC 3380", "CPSC 3410", "CPSC 3480",  # NEW: 2150, 3480
                "CPSC 4060", "CPSC 4070", "CPSC 4080",               # NEW: 4060, 4070
            ],
            "national_security": ["POSC 3350", "POSC 3370"],
            "ethics": ["PHIL 3250"],
            "elective": {"credits": "8-9"},
        },
    },
    "cybersecurity_minor": {
        "all_years": {
            "name": "Cybersecurity Minor",
            "total_credits": 16,
            "core": ["CPSC 2080", "POSC 2030", "CPSC 2180"],
            "elective": {"credits": 7, "choose_from": ["CPSC 2300", "CPSC 3380", "CPSC 3410", "CPSC 4080", "CPSC 4480"]},
        },
    },
    "data_science_ba": {
        "2022-23": {
            "name": "Data Science (BA)",
            "total_credits": 57,
            "required": [
                "MATH 2010", "MATH 2120", "POSC 2420",
                "CPSC 1400", "CPSC 1500", "CPSC 2040", "CPSC 2080",
                "CPSC 2100", "CPSC 2330", "CPSC 2500",
                "CPSC 3520", "CPSC 4100", "CPSC 4430",
                "CPSC 4950", "CPSC 4960", "PHIL 3250",
            ],
            "comm_elective": {"credits": 3, "dept": ["COMM","ENGL"]},
            "domain_elective": {"credits": 3, "dept": ["PSYC","SOCI","BSNS","BIOL","POSC"]},
        },
        "dummy_2022_23": None,  # replaced above
        "2023-24": {
            "name": "Data Science (BA)",
            "total_credits": 55,
            "required": [
                "CPSC 2020", "CPSC 2040", "CPSC 2100", "CPSC 2330",
                "MATH 2120", "MATH 2200",
                "CPSC 4390",
            ],
            "domain_elective": {"credits": 3, "notes": "One 3000+ course in approved domain area"},
            "elective": {"credits": 12},
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Data Science (BA)",
            "total_credits": 55,
            "notes": "Follows ACM curriculum guidelines for data science",
        },
    },
    "data_science_bs": {
        "2022-23": {
            "name": "Data Science (BS)",
            "total_credits": 72,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 4010",
                "POSC 2420",
                "CPSC 1400", "CPSC 1500", "CPSC 2040", "CPSC 2080",
                "CPSC 2100", "CPSC 2330", "CPSC 2500",
                "CPSC 3520", "CPSC 4100", "CPSC 4430",
                "CPSC 4950", "CPSC 4960", "PHIL 3250",
            ],
            "comm_elective": {"credits": 4, "dept": ["COMM","ENGL"]},
            "domain_elective": {"credits": 4, "dept": ["PSYC","SOCI","BSNS","BIOL","POSC"]},
        },
        "2023-24": {
            "name": "Data Science (BS)",
            "total_credits": 65,
            "required": [
                "CPSC 2020", "CPSC 2040", "CPSC 2100", "CPSC 2330",
                "MATH 2010", "MATH 2120", "MATH 2200", "MATH 3010",
                "CPSC 4390",
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
        "2022-23": None,
    },
    "data_science_minor": {
        "all_years": {
            "name": "Data Science Minor",
            "total_credits": 16,
            "required": ["CPSC 2020", "CPSC 2040", "CPSC 2100", "MATH 2120"],
        },
    },
    "information_systems_minor": {
        "all_years": {
            "name": "Information Systems Minor",
            "total_credits": 15,
            "required": ["CPSC 2020", "CPSC 2100"],
            "elective": {"credits": 9, "dept": ["CPSC","BSNS"]},
        },
    },
}

# ─────────────────────────────────────────────
# MATHEMATICS
# ─────────────────────────────────────────────

MATHEMATICS = {
    "math_ba": {
        "all_years": {
            "name": "Mathematics (BA)",
            "total_credits": 30,
            "required": ["MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 4000"],
            "elective_upper": {"credits": 12, "dept": "MATH", "min_level": 3000},
        },
    },
    "actuarial_science_ba": {
        "2022-23": {"same_as": "2025-26"},
        "2023-24": {"same_as": "2025-26"},
        "2024-25": {"same_as": "2025-26"},
        "2025-26": {
            "name": "Actuarial Science (BA)",
            "total_credits": 66,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 3010", "MATH 3020",
                "MATH 3200", "MATH 3400", "MATH 4000", "MATH 4010", "MATH 4020",
                "ACCT 2010", "ACCT 2020",
                "BSNS 2510", "BSNS 3390", "BSNS 4150", "BSNS 4390",
                "CPSC 2020",
                "ECON 2010", "ECON 2020", "ECON 3410",
                "POSC 2420",
            ],
        },
    },
        "math_bs": {
        "all_years": {
            "name": "Mathematics (BS)",
            "total_credits": 47,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 2200",
                "MATH 3010", "MATH 3020", "MATH 4000",
            ],
            "choose_one": ["MATH 3100", "MATH 3200", "MATH 3300"],
            "elective_upper": {"credits": 16, "dept": "MATH", "min_level": 3000},
        },
    },
    "math_economics_ba": {
        "all_years": {
            "name": "Mathematics-Economics (BA)",
            "total_credits": 38,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 4000", "MATH 4010",
                "ECON 2010", "ECON 2020", "ECON 3020", "ECON 3410",
            ],
            "elective_upper": {"credits": 4, "dept": ["MATH", "ECON"], "min_level": 3000},
        },
    },
    "math_finance_ba": {
        "all_years": {
            "name": "Mathematics-Finance (BA)",
            "total_credits": 53,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2120", "MATH 3010", "MATH 3020",
                "MATH 3400", "MATH 4000", "MATH 4010",
                "ACCT 2010", "BSNS 2510", "BSNS 3350", "BSNS 4150",
                "ECON 2010", "ECON 2020", "ECON 3410",
            ],
            "choose_one": ["MATH 3100", "MATH 3200", "MATH 3300"],
        },
    },
    "math_teaching_ba": {
        "2022-23": {
            "name": "Mathematics Teaching (BA)",
            "total_credits": 40,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2200", "MATH 2300",
                "MATH 3010", "MATH 3020", "MATH 4000", "MATH 4100", "MATH 4200",
                "MATH 4700",
            ],
            "choose_one_calc": ["MATH 2120", "MATH 4010"],
            "choose_one_elective": ["MATH 3100", "MATH 3200", "MATH 3300", "MATH 3400"],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Mathematics Teaching (BA)",
            "total_credits": 44,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2200", "MATH 2300",
                "MATH 3010", "MATH 3020", "MATH 3200", "MATH 4000", "MATH 4010", "MATH 4200",
                "CPSC 2020",
                "MATH 4700",
            ],
            "choose_one": ["MATH 2120", "MATH 4020"],
        },
    },
    "math_minor": {
        "all_years": {
            "name": "Mathematics Minor",
            "total_credits": 16,
            "required": ["MATH 2010", "MATH 2020"],
            "elective_upper": {"credits": 8, "dept": "MATH", "min_level": 2120},
        },
    },
    "statistics_minor": {
        "all_years": {
            "name": "Statistics Minor",
            "total_credits": 16,
            "choose_one_intro": ["MATH 2120", "PSYC 2440"],
            "required": ["MATH 4010"],
            "elective": {
                "credits": 9,
                "choose_from": ["PSYC 3240", "PSYC 4650", "POSC 2420", "POSC 3140"],
                "or_approved_math": True,
            },
        },
    },
}

# ─────────────────────────────────────────────
# COMMUNICATION & DESIGN ARTS / HUMANITIES
# ─────────────────────────────────────────────

COMMUNICATION = {
    "cinema_media_arts": {
        "all_years": {
            "name": "Cinema and Media Arts",
            "total_credits": 52,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2020", "COMM 2060", "COMM 2160",
                "COMM 2200", "COMM 2320", "COMM 2420", "COMM 2860",
                "COMM 3120", "COMM 3200", "COMM 3220", "COMM 3420",
                "COMM 4000", "COMM 4800",
            ],
            "elective": {
                "credits": 9,
                "choose_from": ["COMM 3050", "COMM 3160", "COMM 3260", "COMM 4120", "COMM 4900",
                                "ENGL 3140", "THEA 2110", "THEA 2210"],
            },
        },
    },
    "journalism_multimedia": {
        "2022-23": {
            "name": "Journalism",
            "total_credits": 42,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130", "COMM 2140", "COMM 2200",
                "COMM 2850", "COMM 3130", "COMM 3200", "COMM 3230",
                "COMM 4000", "COMM 4800",
            ],
            "elective": {
                "credits": 7,
                "choose_from": ["COMM 3050", "COMM 3330", "COMM 3370", "CPSC 1200",
                                "ECON 2010", "ENGL 3140", "ENGL 3160", "PHIL 2000",
                                "POSC 2100", "POSC 3010", "RLGN 2000", "SOCI 2010", "SOCI 2450"],
            },
        },
        "2023-24": {
            "name": "Multimedia Journalism",
            "total_credits": 42,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130", "COMM 2140", "COMM 2200",
                "COMM 2850", "COMM 3130", "COMM 3200", "COMM 3230",
                "COMM 4000", "COMM 4800",
            ],
            "elective": {"credits": 7, "dept": "PSYC"},
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24", "dept": "Humanities"},
    },
    "public_relations": {
        "all_years": {
            "name": "Public Relations",
            "total_credits": 52,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130", "COMM 2200", "COMM 2240",
                "COMM 2840", "COMM 3050", "COMM 3200", "COMM 3240", "COMM 3250",
                "COMM 3330", "COMM 3340", "COMM 3370", "COMM 3440",
                "COMM 4000", "COMM 4800",
            ],
            "concentrations": {
                "Standard PR": {},
                "Event Planning and Management": {
                    "required": ["COMM 3860", "COMM 4340"],
                    "elective": {"credits": 3, "choose_from": ["BSNS 3150","COMM 3230","ENGL 3140"]},
                },
                "Social Media": {
                    "required": ["BSNS 4400"],
                    "elective": {"credits": 3, "choose_from": ["BSNS 3550","COMM 3230","CPSC 1200","ENGL 3140"]},
                },
            },
        },
    },
    "visual_communication_design": {
        "all_years": {
            "name": "Visual Communication Design",
            "total_credits": 53,
            "required": [
                "ARTH 2000",  # or 3040 in 23-24+
                "ARTS 1210", "ARTS 2010", "ARTS 2011", "ARTS 2100",
                "ARTS 3110", "ARTS 3114", "ARTS 3310", "ARTS 4110", "ARTS 4114",
                "ARTS 4310", "ARTS 4420",
            ],
        },
        "2023-24": {
            "name": "Visual Communication Design",
            "total_credits": 53,
            "notes": "ARTH 2000 replaced by ARTH 3040 in 23-24",
            "required": [
                "ARTH 3040",  # changed from 2000
                "ARTS 1210", "ARTS 2010", "ARTS 2011", "ARTS 2100",
                "ARTS 3110", "ARTS 3114", "ARTS 3310", "ARTS 4110", "ARTS 4114",
                "ARTS 4310", "ARTS 4420",
            ],
        },
    },
    "comm_minors": {
        "cinema_media_arts_minor": {
            "all_years": {
                "name": "Cinema and Media Arts Minor",
                "total_credits": 18,
                "required": ["COMM 2020", "COMM 2060", "COMM 2160", "COMM 2200", "COMM 2860"],
                "choose_one": ["COMM 2320", "COMM 2420"],
            },
        },
        "communication_minor": {
            "all_years": {
                "name": "Communication Minor",
                "total_credits": 18,
                "notes": "Any COMM-captioned course except 4750 and 4800",
            },
        },
        "event_planning_minor": {
            "all_years": {
                "name": "Event Planning and Management Minor",
                "total_credits": "15-16",
                "required": ["BSNS 2810", "COMM 2240", "COMM 3250", "COMM 3370", "COMM 4340"],
                "choose_one": ["COMM 3860"],  # 1-2 hrs
            },
        },
        "journalism_minor": {
            "all_years": {
                "name": "Journalism/Multimedia Journalism Minor",
                "total_credits": 18,
                "required": ["COMM 2000", "COMM 2010", "COMM 2130", "COMM 2850", "COMM 3230"],
                "choose_one": ["COMM 3200", "COMM 4000"],
            },
        },
        "public_relations_minor": {
            "2025-26": {
                "name": "Public Relations Minor",
                "total_credits": 18,
                "required": ["COMM 2000", "COMM 2010", "COMM 2130", "COMM 2240"],
                "choose_one": ["COMM 3250", "COMM 3440"],
                "elective": {"credits": 9, "choose_from": ["COMM 3050", "COMM 3240", "COMM 3340", "COMM 3370"]},
            },
        },
    },
}

# ─────────────────────────────────────────────
# ENGLISH
# ─────────────────────────────────────────────

ENGLISH = {
    "literary_studies": {
        "all_years": {
            "name": "Literary Studies",
            "total_credits": 35,
            "required": ["ENGL 2500", "ENGL 2510", "ENGL 4700"],
            "elective_lit": {
                "credits": 18,
                "choose_from": ["ENGL 2220", "ENGL 2400", "ENGL 3320", "ENGL 3540",
                                "ENGL 3560", "ENGL 3570", "ENGL 3580", "ENGL 3590"],
            },
            "elective_writing": {"credits": 9, "choose_from": ["ENGL 3110", "ENGL 3120", "ENGL 3140"]},
        },
    },
    "writing": {
        "2022-23": {
            "name": "Writing",
            "total_credits": 35,
            "required": ["ENGL 4800", "ENGL 4700"],
            "elective": {
                "credits": 18,
                "choose_from": ["ENGL 2500", "ENGL 2510", "ENGL 2580", "ENGL 3000",
                                "ENGL 3110", "ENGL 3120", "ENGL 3140", "ENGL 3160",
                                "ENGL 3180", "ENGL 3190", "ENGL 3870", "ENGL 3880"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Writing",
            "total_credits": 35,
            "required_writing": {
                "credits": "18-25",
                "choose_from": ["ENGL 2500", "ENGL 2510", "ENGL 2580", "ENGL 3000",
                                "ENGL 3110", "ENGL 3120", "ENGL 3140", "ENGL 3160",
                                "ENGL 3180", "ENGL 3190", "ENGL 3870", "ENGL 3880",
                                "COMM 3220", "COMM 3260"],
            },
            "additional": {"credits": "3-8", "notes": "Other ENGL 2000+ courses not listed above"},
            "required": ["ENGL 4800"],  # 1-3 hrs internship
        },
    },
    "language_arts_teaching": {
        "2022-23": {
            "name": "Language Arts Teaching (English Language Arts)",
            "total_credits": 44,
            "required": [
                "ENGL 2500", "ENGL 2510", "ENGL 3140", "ENGL 3160", "ENGL 3570",
                "ENGL 3590", "ENGL 4700",
                "COMM 1000",
            ],
            "elective": {"credits": 18, "dept": "ENGL"},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "songwriting": {
        "all_years": {
            "name": "Songwriting",
            "total_credits": 44,
            "required": [
                "MUSC 1010", "MUSC 1030", "MUSC 2110",
                "MUPF 1050",
                "MUBS 2010", "MUBS 2020", "MUBS 2070", "MUBS 4500",
                "ENGL 2400", "ENGL 2500", "ENGL 3120",
            ],
            "mupf_study": {"credits": 2, "course": "MUPF 2900"},
            "applied_music": {"credits": 2, "dept": ["MUPF"]},
            "mubs_elective": {
                "credits": 6,
                "choose_from": ["MUBS 3100","MUBS 3210","MUBS 3220",
                                "MUBS 3310","MUBS 4800","MUBS 4900",
                                "BSNS 3330","BSNS 3360"],
            },
            "engl_elective": {
                "credits": 6,
                "choose_from": ["ENGL 2580","ENGL 3320","ENGL 3540",
                                "ENGL 3560","ENGL 3570"],
            },
            "dept_dummy": "old code follows below",
            "required_old": [
                "MUSC 1010", "MUSC 1030",
                "MUSC 2310",  # or equiv
                "ENGL 2500", "ENGL 3160", "ENGL 3870", "ENGL 3880",
                "MUBS 2010", "MUBS 2020",
                "COMM 2140",
            ],
            "applied_music": {"credits": 4},
            "elective": {"credits": 9, "dept": ["PSYC","SOCI","CMIN","EDUC"]},
        },
    },
    "english_minors": {
        "literary_studies_minor": {
            "all_years": {
                "name": "Literary Studies Minor",
                "total_credits": 15,
                "required": ["ENGL 2500"],
                "elective": {"credits": 12, "dept": "ENGL", "min_level": 2000},
            },
        },
        "writing_minor": {
            "all_years": {
                "name": "Writing Minor",
                "total_credits": 15,
                "required": ["ENGL 2500", "ENGL 4800"],
                "elective": {"credits": 9, "dept": "ENGL"},
            },
        },
        "english_studies_minor": {
            "all_years": {
                "name": "English Studies Minor",
                "total_credits": 15,
                "notes": "Flexible; any ENGL 2000+ combination. ENGL 1100, 1110, 1120, 4700 do not apply.",
            },
        },
    },
}

# ─────────────────────────────────────────────
# HISTORY & POLITICAL SCIENCE
# ─────────────────────────────────────────────

HISTORY_POLSCI = {
    "history": {
        "2022-23": {
            "name": "History",
            "total_credits": 36,
            "required_foundational": ["HIST 2000", "HIST 2300", "HIST 2350"],
            "foundational_west_choose": {"credits": 3, "choose_from": ["HIST 2030","HIST 2040"]},
            "foundational_us_choose": {"credits": 3, "choose_from": ["HIST 2110","HIST 2120"]},
            "required_capstone": ["HIST 4930", "HIST 4800"],
            "american_hist_choose": {
                "credits": 6,
                "choose_from": ["HIST 3420","HIST 3425","HIST 3440","HIST 3451",
                                "HIST 3452","HIST 3470","HIST 3510","HIST 3520",
                                "HIST 3540","HIST 3560","HIST 4030"],
            },
            "european_hist_choose": {
                "credits": 6,
                "choose_from": ["HIST 3100","HIST 3135","HIST 3150",
                                "HIST 3190","HIST 3220","HIST 3280"],
            },
            "world_hist_choose": {
                "credits": 6,
                "choose_from": ["HIST 3240","HIST 3250","HIST 3260",
                                "HIST 3300","HIST 3360","HIST 3370"],
            },
            "notes": "HIST 4700 does not apply toward the major",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "History",
            "total_credits": 36,
            "required": [
                "HIST 2000", "HIST 2300", "HIST 2350",  # New foundational courses
                "HIST 4930",   # New capstone
            ],
            "elective_upper": {"credits": 21, "dept": "HIST"},
            "notes": "25-26: New foundational required courses; HIST 4930 replaces 4700",
        },
    },
    "public_history": {
        "all_years": {
            "name": "Public History",
            "total_credits": "59-60",
            "required": [
                "HIST 2030",  # or similar survey
                "HIST 3600", "HIST 3610", "HIST 4700", "HIST 4810",
                "POSC 2200",
                "COMM 2130",
            ],
            "elective": {"credits": 24, "dept": ["HIST", "POSC", "SOCI", "COMM"]},
            "internship": {"credits": 3, "course": "HIST 4810"},
        },
    },
    "social_studies_teaching": {
        "all_years": {
            "name": "Social Studies Teaching",
            "total_credits": 51,
            "teaching_fields": ["Historical Perspectives", "Government & Citizenship"],
            "required_hist": [
                "HIST 2030", "HIST 2040", "HIST 2110", "HIST 2120",
                "HIST 3xxx",  # upper div
            ],
            "required_gov": [
                "POSC 2020", "POSC 2100", "POSC 2200", "POSC 3xxx",
            ],
            "notes": "See Teacher Education requirements for full licensure requirements",
        },
    },
    "political_science": {
        "all_years": {
            "name": "Political Science",
            "total_credits": 36,
            "required": ["POSC 2020", "POSC 2100", "POSC 4930"],
            "advanced": {"credits": 12, "dept": "POSC", "min_level": 3000},
            "experiential": {"credits": "4-5", "choose_from": ["POSC 2840", "POSC 4820"]},
            "elective": {"credits": 8, "dept": "POSC", "min_level": 2000},
        },
    },
    "polsci_philosophy_economics": {
        "2022-23": {
            "name": "Political Science, Philosophy, and Economics (PPE)",
            "total_credits": 54,
            "required": [
                "POSC 2020", "POSC 2100", "POSC 2200", "POSC 2400", "POSC 2420",
                "MATH 2120",
                "ECON 2010", "ECON 2020",
                "PHIL 2000", "PHIL 2120",
                "POSC 3510",
                "POSC 4930",
            ],
            "advanced": {
                "credits": 12,
                "required": ["POSC 3510"],
                "choose_from": ["ECON 3110","ECON 3210","PHIL 3010","POSC 3010",
                                  "HIST 3010","PHIL 3250","RLGN 3250"],
            },
            "elective": {"credits": 12, "dept": ["POSC","PHIL","ECON"]},
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "international_relations": {
        "all_years": {
            "name": "International Relations",
            "total_credits": "42-43",
            "foundational": [
                "POSC 2020", "POSC 2200", "POSC 2400", "POSC 2580", "MATH 2120",
            ],
            "advanced": ["POSC 3300", "POSC 3400", "POSC 3510"],
            "choose_one_advanced": ["POSC 3310", "POSC 3320", "POSC 3330", "POSC 3360", "POSC 3450"],
            "experiential": ["POSC 2840", "POSC 4820"],
            "capstone": ["POSC 4930"],
            "elective": {
                "credits": 9,
                "choose_from": ["ECON 3210", "HIST 3xxx", "SPAN 2010+"],
            },
        },
    },
    "national_security": {
        "all_years": {
            "name": "National Security",
            "total_credits": 44,
            "required": [
                "POSC 2020", "POSC 2030", "POSC 2200", "POSC 2400", "POSC 2420",
                "POSC 3350", "POSC 3370", "POSC 3400", "POSC 3510",
                "PHIL 3250",
                "POSC 4930",
            ],
            "elective": {"credits": 9, "choose_from": ["POSC 3xxx", "CRIM 2520", "CPSC 2080"]},
        },
    },
    "history_minors": {
        "history_minor": {
            "all_years": {
                "name": "History Minor",
                "total_credits": 15,
                "notes": "Selected from HIST courses; at least 2 upper-div courses. HIST 4700 does not apply.",
            },
        },
        "public_history_minor": {
            "all_years": {
                "name": "Public History Minor",
                "total_credits": 18,
                "required": ["HIST 3600", "HIST 3610"],
                "elective": {"credits": 9, "dept": ["PSYC","SOCI","CMIN","EDUC"]},
            },
        },
        "polsci_minor": {
            "all_years": {
                "name": "Political Science Minor",
                "total_credits": 15,
                "required": ["POSC 2020", "POSC 2100"],
                "elective_upper": {"credits": 9, "dept": "POSC"},
            },
        },
        "international_relations_minor": {
            "all_years": {
                "name": "International Relations Minor",
                "total_credits": 15,
                "required": ["POSC 2020", "POSC 2200", "POSC 2400"],
                "elective": {"credits": 6, "dept": "POSC"},
            },
        },
        "legal_studies_minor": {
            "2022-23": {
                "name": "Legal Studies Minor",
                "total_credits": 15,
                "required": ["POSC 2210", "POSC 4810", "ENGL 3190"],
                "choose_one": ["BSNS 3420", "CRIM 3110", "COMM 4000", "POSC 3250"],
                "choose_one_b": ["BIBL 3420", "POSC 3010", "PHIL 2120", "PHIL 3250", "RLGN 3120", "RLGN 3250"],
            },
            "2023-24": {"same_as": "2022-23"},
            "2024-25": {"same_as": "2022-23"},
            "2025-26": {"same_as": "2022-23"},
        },
    },
}

# ─────────────────────────────────────────────
# MODERN LANGUAGES
# ─────────────────────────────────────────────

MODERN_LANGUAGES = {
    "spanish": {
        "all_years": {
            "name": "Spanish",
            "total_credits": "43-45",
            "required": [
                "SPAN 1010", "SPAN 1020", "SPAN 2010", "SPAN 2020",
                "SPAN 3010", "SPAN 3020", "SPAN 3140",
                "SPAN 4xxx",  # upper-level lit
                "MLAN 3500", "MLAN 4900",
            ],
            "choose_one": ["SPAN 3400", "SPAN 3440"],
            "study_abroad_or_internship": {"credits": 6, "dept": "SPAN"},
        },
    },
    "spanish_complementary": {
        "all_years": {
            "name": "Spanish Complementary Major",
            "total_credits": 30,
            "required": ["MLAN 3500", "MLAN 4900"],
            "span_courses": {"credits": 26, "dept": "SPAN"},
        },
    },
    "spanish_education": {
        "2022-23": {
            "name": "Spanish Education (P-12)",
            "total_credits": "91-93",
            "notes": "Spanish BA + Education licensure requirements",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "minors": {
        "french_studies_minor": {
            "all_years": {
                "name": "French Studies Minor",
                "total_credits": "15-16",
                "required_lang": {"credits": 8, "dept": "FREN"},
                "required_hist": {"credits": 3, "notes": "History course on France"},
                "required_culture": {"credits": 4, "notes": "Language culture course"},
            },
        },
        "german_studies_minor": {
            "all_years": {
                "name": "German Studies Minor",
                "total_credits": "15-16",
                "required_lang": {"credits": 8, "dept": "GERM"},
                "required_hist": {"credits": 3},
                "required_culture": {"credits": 4},
            },
        },
        "spanish_minor": {
            "2022-23": {
                "name": "Spanish Minor",
                "total_credits": 18,
                "required": ["SPAN 1010", "SPAN 1020", "SPAN 2010"],
                "elective": {"credits": 9, "dept": "SPAN", "min_level": 2020},
            },
            "2023-24": {
                "name": "Spanish Studies Minor",
                "total_credits": 15,
                "required": ["SPAN 1010", "SPAN 1020"],
                "elective": {"credits": 9, "dept": "SPAN"},
            },
            "2024-25": {"same_as": "2023-24"},
            "2025-26": {"same_as": "2023-24"},
        },
    },
}

# ─────────────────────────────────────────────
# MUSIC, THEATRE & DANCE
# ─────────────────────────────────────────────

MUSIC_THEATRE_DANCE = {
    "voice_performance_bmus": {
        "all_years": {
            "name": "Voice Performance (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUSC 2010", "MUSC 2020", "MUSC 2030", "MUSC 2040",
                "MUSC 2110", "MUSC 2330", "MUSC 3120", "MUSC 3130",
                "MUED 2470",
                "MUBS 3470",
            ],
            "applied_primary": {"credits": 22, "dept": ["MUPF"], "notes": "Private study in primary area; half + full recital"},
            "major_ensemble": {"credits": 7, "dept": ["MUPF"]},
            "elective": {"credits": 4, "choose_from": ["MUSC 3030", "MUSC 3100", "MUSC 4900", "MUBS 2050"]},
        },
    },
    "instrumental_performance_bmus": {
        "all_years": {
            "name": "Instrumental Performance (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUSC 2010", "MUSC 2020", "MUSC 2030", "MUSC 2040",
                "MUSC 2110", "MUSC 2330", "MUSC 3040", "MUSC 3120", "MUSC 3130",
                "MUED 2470", "MUED 3480",
                "MUBS 3470",
            ],
            "applied": {"credits": 22, "dept": ["MUPF"]},
            "major_ensemble": {"credits": 7, "dept": ["MUPF"]},
        },
    },
    "music_education_bmus": {
        "all_years": {
            "name": "Music Education K-12/P-12 (BMus)",
            "total_credits": 101,
            "required_theory": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUSC 2010", "MUSC 2020", "MUSC 2030", "MUSC 2040",
                "MUSC 2110", "MUSC 2330", "MUSC 3030", "MUSC 3040",
            ],
            "musc_history_choose": {
                "credits": 6,
                "choose_from": ["MUSC 3110", "MUSC 3120", "MUSC 3130"],
                "notes": "6 hrs from Music History (2 of 3)",
            },
            "required_keyboard": ["MUPF 1050", "MUPF 1060"],
            "keyboard_choose": {
                "credits": 2,
                "choose_from": ["MUPF 1710", "MUPF 2030", "MUPF 2040"],
            },
            "required_mued": [
                "MUED 1000", "MUED 1100", "MUED 1200", "MUED 1300", "MUED 1400",
                "MUED 2470",
                "MUED 3100", "MUED 3110", "MUED 3120", "MUED 3130",
                "MUED 3470", "MUED 3480", "MUED 4700",
            ],
            "mued_pedagogy_choose": {
                "credits": 2,
                "choose_from": ["MUED 3330", "MUED 3350", "MUED 3370"],
            },
            "mued_diction_choose": {
                "credits": 2,
                "choose_from": ["MUED 2510", "MUED 2520", "MUED 3460"],
            },
            "applied_music": {"credits": 8, "dept": ["MUPF"],
                             "notes": "8 hrs applied music incl. half recital"},
            "required_education": [
                "EDUC 2100", "EDUC 2110", "EDUC 3120", "EDUC 4010", "SPED 2400",
            ],
            "educ_methods_choose": {
                "credits": 3,
                "choose_from": ["EDUC 4120", "EDUC 4710"],
            },
        },
    },
    "musical_theatre_bmus": {
        "2022-23": {
            "name": "Musical Theatre (BMus)",
            "total_credits": 80,
            "notes": "Distinct from BA Musical Theatre — uses BMus Theory + Theatre",
        },
        "2025-26": {
            "name": "Musical Theatre (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUSC 2010", "MUSC 2030", "MUSC 2110", "MUSC 2330", "MUSC 3180",
                "MUED 2510",
                "MUTR 2410", "MUTR 2420", "MUTR 3210", "MUTR 3220",
                "MUTR 3410", "MUTR 4500", "MUTR 4910",
                "THEA 2110", "THEA 2120", "THEA 2210", "THEA 2220",
                "THEA 3110", "THEA 3120",
            ],
            "applied_voice": {"credits": 10, "includes": "MUPF 4540 (2 hrs)"},
            "mupf_1170": {"credits": 6, "semesters": 6},
            "major_ensemble": {"semesters": 8},
            "dance": {"credits": 6},
        },
    },
    "worship_arts_ba": {
        "all_years": {
            "name": "Worship Arts (BA)",
            "total_credits": 53,
            "required": [
                "MUSC 1010", "MUSC 1030", "MUSC 3150", "MUSC 3160", "MUSC 3800",
                "MUED 2470",
                "MUPF 1050", "MUPF 1410",
                "MUBS 2020", "MUBS 3450",
                "THEA 2350",
                "DANC 1580", "DANC 1590",
                "COMM 2140", "COMM 2200",
            ],
            "applied_music": {"credits": 4, "dept": ["MUPF"]},
            "ensembles": {"credits": 4, "dept": ["MUPF"]},
            "ministry_elective": {
                "credits": 12,
                "choose_from": ["CMIN 2000","CMIN 2270","CMIN 3050",
                                "RLGN 2060","RLGN 3040","RLGN 3420",
                                "HIST 2060","HIST 3420"],
            },
        },
    },
    "musical_theatre_ba": {
        "all_years": {
            "name": "Musical Theatre (BA)",
            "total_credits": 45,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUTR 2410", "MUTR 2420", "MUTR 3210", "MUTR 3220",
                "MUPF 4910",
                "THEA 2110", "THEA 2120", "THEA 2210", "THEA 3110",
            ],
            "voice_study": {"credits": 6, "choose_from": ["MUPF 2700", "MUPF 4700"]},
            "piano_study": {"credits": 2, "choose_from": ["MUPF 1050","MUPF 1060","MUPF 1710","MUPF 1720","MUPF 2030"]},
            "mupf_1170": {"credits": 2, "course": "MUPF 1170"},
        },
    },
    "music_ba": {
        "all_years": {
            "name": "Music (BA)",
            "total_credits": 50,
            "core_required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUSC 2110", "MUSC 2330",
                "MUED 2470",
            ],
            "tracks": {
                "Theory and History": {
                    "required": ["MUSC 2020", "MUSC 2030", "MUSC 2040", "MUSC 3110"],
                    "elective": {"credits": 7, "dept": "PSYC"},
                },
                "Composition": {
                    "required": ["MUSC 2020", "MUSC 3040"],
                    "applied": {"credits": 4},
                    "elective": {"credits": 6, "dept": "DANC"},
                },
            },
        },
    },
    "music_business": {
        "2022-23": {
            "name": "Music Business (BA)",
            "total_credits": 53,
            "core": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040", "MUSC 2210",
                "MUBS 2010", "MUBS 2020", "MUBS 4900",
                "MUPF 1050", "MUPF 1060",
                "BSNS 3320", "BSNS 3330",
            ],
            "applied": {"credits": 4},
            "ensembles": {"credits": 4},
            "tracks": {
                "Management": ["BSNS 4480", "BSNS 2810", "MUBS 3220", "MUBS 3450", "MUBS 3470"],
                "Marketing": ["BSNS 2710", "BSNS 4110", "MUBS 2030", "MUBS 3370", "MUBS 3380"],
                "Production": ["MUSC 3040", "MUBS 2060", "MUBS 2070", "MUBS 3100"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Music Business (BA)",
            "total_credits": 53,
            "core": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040",
                "MUBS 2010", "MUBS 2020",
                "MUPF 1050", "MUPF 1060",
            ],
            "applied": {"credits": 4},
            "ensembles": {"credits": 4},
            "elective_music_biz": {
                "credits": 12,
                "choose_from": [
                    "MUBS 2070", "MUBS 2450", "MUBS 3100", "MUBS 3210", "MUBS 3220",
                    "MUBS 3370", "MUBS 3380", "MUBS 3450", "MUBS 3470", "MUBS 4500",
                    "MUBS 4850", "MUBS 4870", "MUBS 4950",
                    "MUPF 2905", "MUPF 4905",
                    "BSNS 4400", "CRIM 2520",
                ],
            },
            "notes": "Tracks restructured in 25-26",
        },
    },
    "theatre": {
        "all_years": {
            "name": "Theatre (BA)",
            "total_credits": 42,
            "required": [
                "THEA 2110", "THEA 2210", "THEA 2220", "THEA 2410",
                "THEA 3010", "THEA 3020", "THEA 3400", "THEA 3500", "THEA 3550",
                "THEA 4800",
                "THEA 2890",  # 8 hrs
            ],
            "elective": {
                "credits": 8,
                "choose_from": ["THEA 2120", "THEA 2420", "THEA 3110", "THEA 3120",
                                "MUPF 1070-1390", "MUPF 2700", "MUPF 4910",
                                "DANC 1420"],
            },
        },
    },
    "dance": {
        "all_years": {
            "name": "Dance (BA)",
            "total_credits": 54,
            "core": [
                "DANC 1580", "DANC 1590", "DANC 3000", "DANC 3020", "DANC 4500",
            ],
            "modern_tech": {"credits": 3, "from": "DANC 1220-4220"},
            "ballet_tech": {"credits": 3, "from": "DANC 2420-4420"},
            "jazz_tech": {"credits": 2, "from": ["DANC 2330", "DANC 3320"]},
            "tracks": {
                "Performance": {
                    "required": ["DANC 3050", "DANC 3055"],
                    "tech_additional": {"credits": 6},
                    "elective": {"credits": 8},
                },
                "Choreography": {
                    "required": ["DANC 3010", "DANC 3020", "DANC 3050"],
                    "elective": {"credits": 8},
                },
                "Pedagogy": {
                    "required": [
                        "DANC 1150", "DANC 1160", "DANC 2580", "DANC 2590",
                        "DANC 3010", "DANC 3050", "DANC 3055", "DANC 3590", "DANC 4590",
                        "EDUC 2110",
                    ],
                },
                "Science": {
                    "required": [
                        "DANC 3060", "DANC 4060",
                        "CHEM 1000", "MATH 2120", "PHYS 2140", "PSYC 2000", "SOCI 2010",
                    ],
                },
            },
        },
    },
    "complementary_music": {
        "all_years": {
            "name": "Complementary Music Major",
            "total_credits": 33,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030", "MUSC 1040", "MUSC 2110", "MUSC 2330",
                "MUBS 3470",
                "MUPF 1050", "MUPF 1060",
            ],
            "applied": {"credits": 4, "dept": ["MUPF"]},
            "ensembles": {"credits": 4, "dept": ["MUPF"]},
            "elective": {"credits": 6, "dept": ["MUSC","MUPF","MUED"]},
        },
    },
    "complementary_dance": {
        "all_years": {
            "name": "Complementary Dance Major",
            "total_credits": 33,
            "required": ["DANC 1150", "DANC 1580", "DANC 1590", "DANC 3000"],
            "technique": {"credits": 9, "dept": "DANC"},
            "elective": {"credits": 12, "dept": "DANC"},
        },
    },
    "minors": {
        "music_minor": {
            "all_years": {
                "name": "Music Minor",
                "total_credits": 18,
                "required": ["MUSC 1010", "MUSC 1030"],
                "applied": {"credits": 2},
                "ensembles": {"credits": 2},
                "elective": {"credits": 10},
            },
        },
        "music_performance_minor": {
            "all_years": {
                "name": "Music Performance Minor",
                "total_credits": "15-18",
                "admission": "By audition",
                "tracks": {
                    "For music majors": {"credits": "15-16"},
                    "For non-music majors": {"credits": "18"},
                },
            },
        },
        "theatre_minor": {
            "all_years": {
                "name": "Theatre Minor",
                "total_credits": 17,
                "required": ["THEA 2110", "THEA 2210", "THEA 3400"],
                "choose_one": ["THEA 3010", "THEA 3020", "THEA 4900"],
                "choose_one_b": ["THEA 3500", "THEA 3550"],
                "thea_2890": {"credits": 2},
            },
        },
        "dance_minor": {
            "all_years": {
                "name": "Dance Minor",
                "total_credits": 18,
                "required": ["DANC 1580", "DANC 1590", "DANC 3000"],
                "technique": {"credits": 6, "dept": "DANC"},
                "elective": {"credits": 6, "dept": "DANC"},
            },
        },
    },
}

# ─────────────────────────────────────────────
# CHRISTIAN MINISTRY
# ─────────────────────────────────────────────

CHRISTIAN_MINISTRY = {
    "christian_ministries": {
        "2022-23": {
            "name": "Christian Ministries",
            "total_credits": 46,
            "dept_core": [
                "BIBL 2000", "BIBL 2050",
                "RLGN 2000", "RLGN 2130", "RLGN 2150",
                "RLGN 3040", "RLGN 3060", "RLGN 3300",
            ],
            "ministry_core": [
                "CMIN 2000", "CMIN 2810",
                "CMIN 3050", "CMIN 3080", "CMIN 3910",
                "CMIN 4250", "CMIN 4810",
            ],
            "dept_elective": {
                "credits": 3, "dept": ["BIBL","RLGN","CMIN"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Christian Ministries",
            "total_credits": 46,
            "core": [
                "BIBL 2000", "BIBL 2050", "RLGN 2000", "RLGN 2150",
                "CMIN 2000", "CMIN 2810", "CMIN 4250", "CMIN 4810",
            ],
            "choose_one_each_category": {
                "Biblical Studies": ["BIBL 2050", "BIBL 2150", "BIBL xxxx", "RLGN 2150"],
                "Church History": ["HIST 3060", "HIST 3420", "RLGN 3300"],
                "Christian Ethics": ["RLGN 2130", "RLGN 3120"],
                "Educational Ministry": ["CMIN 2260", "CMIN 3260", "CMIN 3910"],
                "Practices of Ministry": ["CMIN 2270", "CMIN 3050", "CMIN 3080"],
            },
            "notes": "Restructured in 25-26 — categories more explicit",
        },
    },
    "youth_ministries": {
        "all_years": {
            "name": "Youth Ministries",
            "total_credits": 49,
            "dept_core": [
                "BIBL 2000", "BIBL 2050",
                "RLGN 2000", "RLGN 2130", "RLGN 2150", "RLGN 3040", "RLGN 3060", "RLGN 3300",
            ],
            "ministry_core": ["CMIN 2000", "CMIN 2810", "CMIN 4250", "CMIN 4810"],
            "ministry_elective_choose": {
                "credits": 3,
                "choose_from": ["CMIN 3050","CMIN 3080","CMIN 3910"],
            },
            "youth_courses": ["CMIN 2260", "CMIN 3260"],
            "family_choose": {
                "credits": 3,
                "choose_from": ["CMIN 3230","HIST 4030","SOCI 2100"],
            },
            "dept_elective": {"credits": 3, "dept": ["BIBL","RLGN","CMIN"]},
        },
    },
    "ministry_studies_online": {
        "all_years": {
            "name": "Ministry Studies (Online Major)",
            "total_credits": 34,
            "required": [
                "BIBL 2000", "BIBL 2050",
                "RLGN 2000", "RLGN 2130", "RLGN 2150",
                "CMIN 2000",
            ],
            "choose_one_each": {
                "Church History": ["HIST 3060", "RLGN 3300"],
                "Elective Ministry": ["CMIN 3050", "CMIN 3080", "CMIN 3910"],
                "Ethics": ["RLGN 3120"],
                "Educational Ministry": ["CMIN 2260", "CMIN 3260"],
                "Practices": ["CMIN 2270", "CMIN 3050", "CMIN 3080"],
            },
        },
    },
    "christian_spiritual_formation_minor": {
        "all_years": {
            "name": "Christian Spiritual Formation Minor",
            "total_credits": 15,
            "required": ["RLGN 1100", "RLGN 4960"],
            "rlgn_choose": {
                "credits": 3, "choose_from": ["RLGN 2410", "RLGN 2430"],
            },
            "category_choose": {
                "credits": 6,
                "choose_from": [
                    "BIBL 3000", "RLGN 3000", "BIBL 2150",
                    "HIST 3060", "RLGN 3060", "HIST 3540", "RLGN 2270",
                    "RLGN 3250", "PHIL 3250", "PHIL 2000", "RLGN 3120",
                    "RLGN 2310", "RLGN 3100", "RLGN 3530",
                ],
                "notes": "6 hrs from two categories: Scripture, Tradition, Reason, Experience",
            },
        },
    },
    "christian_spiritual_formation_complementary": {
        "all_years": {
            "name": "Christian Spiritual Formation Complementary Major",
            "total_credits": "28-30",
            "core": ["RLGN 1100", "RLGN 4960"],
            "choose_one": ["RLGN 2410", "RLGN 2430"],
            "categories": {
                "Scripture": ["BIBL 3000", "BIBL 2150"],
                "Tradition": ["HIST 3060", "HIST 3540", "RLGN 2270"],
                "Reason": ["RLGN 3250", "PHIL 2000", "RLGN 3120"],
                "Experience": ["RLGN 2310", "RLGN 3100", "RLGN 3530"],
            },
        },
    },
    "minors": {
        "biblical_studies_minor": {
            "2022-23": {
                "name": "Biblical Studies Minor",
                "total_credits": 15,
                "required": ["BIBL 2050", "RLGN 2150"],
                "elective": {"credits": 6, "dept": "BIBL"},
            },
            "2025-26": {
                "name": "Biblical Studies Minor",
                "total_credits": 15,
                "required": ["BIBL 2000", "BIBL 2050", "RLGN 2150"],
                "elective": {"credits": 6, "dept": "BIBL"},
            },
        },
        "christian_ministries_minor": {
            "all_years": {
                "name": "Christian Ministries Minor",
                "total_credits": 16,
                "required": ["CMIN 2000", "CMIN 2810"],
                "upper_div": {"credits": 3, "dept": "dept offerings"},
                "additional_cmin": {"credits": 9},
            },
        },
        "csf_minor": {
            "all_years": {
                "name": "Christian Spiritual Formation Minor",
                "total_credits": 15,
                "required": ["RLGN 1100", "RLGN 4960"],
                "choose_one": ["RLGN 2410", "RLGN 2430"],
                "categories": {"credits": 6, "two_categories": True},
            },
        },
        "ethics_minor": {
            "all_years": {
                "name": "Ethics Minor",
                "total_credits": 15,
                "required": ["RLGN 2130", "PHIL 2120", "RLGN/PHIL 3250"],
                "elective": {"credits": 6},
            },
        },
        "history_of_christianity_minor": {
            "all_years": {
                "name": "History of Christianity Minor",
                "total_credits": 15,
                "required": ["HIST 3060", "RLGN 3300"],
                "elective": {"credits": 9, "dept": ["HIST", "RLGN"]},
            },
        },
        "philosophy_minor": {
            "all_years": {
                "name": "Philosophy Minor",
                "total_credits": 15,
                "required": ["PHIL 2000", "PHIL 2120"],
                "elective": {"credits": 9, "dept": "PHIL"},
            },
        },
        "religion_minor": {
            "2022-23": None,
            "2023-24": {
                "name": "Religion Minor",
                "total_credits": 15,
                "required": ["RLGN 2000", "RLGN 3060", "RLGN 3320"],
                "elective": {"credits": 6, "dept": "RLGN"},
            },
            "2024-25": {"same_as": "2023-24"},
            "2025-26": {"same_as": "2023-24"},
        },
    },
}

# ─────────────────────────────────────────────
# KINESIOLOGY
# ─────────────────────────────────────────────

KINESIOLOGY = {
    "exercise_science": {
        "2022-23": {
            "name": "Exercise Science",
            "total_credits": 70,
            "required_core": [
                "BIOL 2410", "BIOL 2420",
                "EXSC 1360", "EXSC 2455", "EXSC 2580",
                "EXSC 3470", "EXSC 3480", "EXSC 3520", "EXSC 3530",
                "EXSC 4150", "EXSC 4800", "EXSC 4910", "EXSC 4920",
                "PEHS 1550", "PSYC 2000",
            ],
            "chem_choose": {
                "credits": 4,
                "choose_from": ["CHEM 1000","CHEM 2110"],
            },
            "concentrations": {
                "Clinical Exercise Physiology": {
                    "required": ["EXSC 4050", "EXSC 4160"],
                    "elective": {
                        "credits": 10,
                        "choose_from": ["BIOL 2010","EXSC 4010","EXSC 2440",
                                        "PSYC 3450","EXSC 2550","EXSC 3300"],
                    },
                },
                "Pre-Health": {
                    "elective": {
                        "credits": 14,
                        "choose_from": ["BIOL 2010","BIOL 2210","BIOL 2220",
                                        "CHEM 2120","MATH 2120","PHYS 2140",
                                        "PHYS 2150","PSYC 2510","PSYC 3120",
                                        "PSYC 3450","SOCI 2010"],
                    },
                },
                "Sports Performance": {
                    "elective": {
                        "credits": 14,
                        "dept": ["EXSC","PEHS","PETE","ATRG"],
                        "notes": "14 hrs from approved sports performance courses",
                    },
                },
            },
            "required_science": [
                "BIOL 2410", "BIOL 2420",   # A&P I and II
                "BIOL 2230",                 # Microbiology
                "CHEM 1000",
                "PSYC 2000",
            ],
            "required_exsc": [
                "EXSC 2140", "EXSC 2200", "EXSC 3100", "EXSC 3200",
                "EXSC 4110", "EXSC 4120", "EXSC 4910",
            ],
            "concentrations": {
                "Clinical Exercise Physiology": [
                    "EXSC 4050", "EXSC 4160",
                ],
                "Pre-Health": {
                    "credits": 12,
                    "choose_from": [
                        "BIOL 2010", "BIOL 2210", "BIOL 2220", "CHEM 2120",
                        "MATH 2120", "PSYC 2510",
                    ],
                },
                "Sports Performance": ["ATRG 1530", "EXSC 4010"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Exercise Science",
            "total_credits": 70,
            "notes": "ATRG 1530 renamed EXSC 1530",
            "core": [
                "PETE 1300", "PETE 2250", "PETE 3720", "PETE 4900",
                "PEHS 1450", "PEHS 3340", "PEHS 3410",
                "EXSC 1530",   # renamed from ATRG 1530
                "EXSC 2580",
                "ACCT 2010",
                "BSNS 2710", "BSNS 2810",
            ],
        },
        "2025-26": {
            "name": "Exercise Science",
            "total_credits": 70,
            "core": [
                "PETE 1300", "PETE 2250", "PETE 3720", "PETE 4900",
                "PEHS 1450", "PEHS 3340", "PEHS 3410",
                "EXSC 1530", "EXSC 2580",
                "ACCT 2010", "BSNS 2710", "BSNS 2810",
            ],
            "concentrations": {
                "Clinical Exercise Physiology": [
                    "EXSC 4050", "EXSC 4160",
                ],
                "Pre-Health": {
                    "credits": 12,
                    "choose_from": [
                        "BIOL 2010", "BIOL 2210", "BIOL 2220", "CHEM 2120",
                        "MATH 2120", "PSYC 2510",
                    ],
                },
                "Sports Performance": ["EXSC 1530", "EXSC 4010"],
            },
        },
    },
    "sport_recreational_leadership": {
        "all_years": {
            "name": "Sport and Recreational Leadership",
            "total_credits": 52,
            "required": [
                "SPRL 1350", "SPRL 2450", "SPRL 2550", "SPRL 3150",
                "SPRL 3250", "SPRL 3300", "SPRL 4850",
                "PETE 1300", "PETE 2250", "PETE 3720", "PETE 4900",
                "PEHS 1450", "PEHS 3340", "PEHS 3410",
                "EXSC 1530", "EXSC 2580",
                "ACCT 2010",
                "BSNS 2710", "BSNS 2810",
            ],
        },
    },
    "minors": {
        "athletic_coaching_minor": {
            "all_years": {
                "name": "Athletic Coaching Minor",
                "total_credits": 15,
                "required": [
                    "PETE 1300", "PETE 2250", "PEHS 1450",
                    "EXSC 1530",  # was ATRG 1530 pre-24-25
                    "SPRL 3250",
                ],
            },
        },
        "nutrition_minor": {
            "all_years": {
                "name": "Nutrition Minor",
                "total_credits": 16,
                "notes": "See department for current course list",
            },
        },
        "sport_rec_leadership_minor": {
            "all_years": {
                "name": "Sport and Recreational Leadership Minor",
                "total_credits": "16-17",
                "required": [
                    "PETE 1300", "PEHS 1450",
                    "SPRL 1350", "SPRL 2450", "SPRL 2550", "SPRL 3150",
                ],
                "choose_one": ["PETE 3720", "PETE 4900", "SPRL 3300", "SPRL 4850"],
            },
        },
    },
}

# ─────────────────────────────────────────────
# NURSING
# ─────────────────────────────────────────────

NURSING = {
    "bsn": {
        "all_years": {
            "name": "Nursing (BSN)",
            "total_credits": 120,
            "notes": "Competitive admission program; progression requirements apply",
            "prerequisites_for_admission": [
                "BIOL 2410", "BIOL 2420",
                "PSYC 2000", "PSYC 2510",
                "CHEM 1000",
                "BIOL 2230",
            ],
            "freshman_required": [
                "NURS 1100",   # or equivalent
                "BIOL 2410", "BIOL 2420",
                "PSYC 2000",
            ],
            "progression_requirements": {
                "sophomore_admission": "GPA 3.2+; C or above in prerequisites",
            },
            "nursing_core_sequence": [
                "NURS 2140", "NURS 2241", "NURS 2340",
                "NURS 3351", "NURS 3352",
                "NURS 4xxx",   # upper-division clinical courses
            ],
            "supporting_courses": [
                "BIBL 2000", "ENGL 1110", "ENGL 1120",
                "COMM 1000", "MATH 2010", "PSYC 2510",
            ],
        },
    },
    "rn_bsn": {
        "all_years": {
            "name": "RN-BSN (Completion Track)",
            "notes": "For licensed RNs completing BSN; accelerated online format",
        },
    },
    "accelerated_bsn": {
        "all_years": {
            "name": "Accelerated BSN",
            "notes": "For students with prior bachelor's degree; GPA 2.75+ required",
            "prerequisites": [
                "BIOL 2410", "BIOL 2420", "PSYC 2000", "PSYC 2510",
                "CHEM 1000", "BIOL 2230",
            ],
        },
    },
}

# ─────────────────────────────────────────────
# PSYCHOLOGY
# ─────────────────────────────────────────────

PSYCHOLOGY = {
    "psychology_major": {
        "all_years": {
            "name": "Psychology",
            "total_credits": 30,
            "required": ["PSYC 2000", "PSYC 2010"],
            "capstone": {"credits": 1, "course": "PSYC 4900"},
            "upper_div_choose": {
                "credits": 15,
                "choose_from": ["PSYC 3010","PSYC 3030","PSYC 3040","PSYC 3060",
                                "PSYC 3100","PSYC 3120","PSYC 3200","PSYC 3210",
                                "PSYC 3240","PSYC 3330","PSYC 3400","PSYC 3450",
                                "PSYC 4030","PSYC 4100","PSYC 4110","PSYC 4140",
                                "PSYC 4150","PSYC 4510","PSYC 4520","PSYC 4650"],
                "notes": "15 hrs from 3000/4000-level PSYC; PSYC 4900 excluded",
            },
            "choose_one_soci": ["SOCI 3050", "SOCI 3140", "SOCI 3150"],
        },
    },
    "psychology_complementary": {
        "all_years": {
            "name": "Psychology Complementary Major",
            "total_credits": 26,
            "required": [
                "PSYC 2000", "PSYC 2010",
            ],
            "upper_div_elective": {"credits": 12, "dept": "PSYC"},
            "dummy_elective": {"credits": 9},
        },
    },
    "youth_leadership_development": {
        "all_years": {
            "name": "Youth Leadership Development / Youth Leadership Complementary",
            "total_credits": 28,
            "required": [
                "PSYC 2000", "PSYC 2510", "PSYC 4210",
                "SOCI 3100", "SOCI 3210",
                "EDUC 2110",
                "CMIN 2000",
            ],
            "elective": {"credits": 9, "dept": ["PSYC","SOCI","CMIN","EDUC"]},
        },
    },
    "psychology_minor": {
        "all_years": {
            "name": "Psychology Minor",
            "total_credits": 16,
            "required": ["PSYC 2000"],
            "upper_div_psyc": {"credits": 6, "dept": "PSYC", "min_level": 3000},
            "elective": {"credits": 7, "dept": "PSYC"},
        },
    },
}

# ─────────────────────────────────────────────
# PUBLIC HEALTH
# ─────────────────────────────────────────────

PUBLIC_HEALTH = {
    "public_health_ba": {
        "2022-23": {
            "name": "Public Health (BA)",
            "total_credits": 48,
            "core": [
                "PUBH 2010",   # if exists — see notes
                "PUBH 3000", "PUBH 3100", "PUBH 3200", "PUBH 3300", "PUBH 3400",
                "PUBH 4500", "PUBH 4810",
            ],
            "social_sciences": {
                "credits": 9,
                "choose_from": ["SOCI 2010", "SOCI 2020", "PSYC 2000", "POSC 2100", "ECON 2010"],
            },
            "natural_sciences_ba": {
                "credits": 6,
                "choose_from": ["BIOL 2040", "BIOL 2010", "CHEM 1000"],
            },
            "elective": {"credits": "2-4"},
        },
        "2023-24": {
            "name": "Public Health (BA)",
            "total_credits": 48,
            "notes": "PUBH 2010 added as new intro course in 23-24",
            "required": ["PUBH 2010"],
            "core": [
                "PUBH 3000", "PUBH 3100", "PUBH 3200", "PUBH 3300", "PUBH 3400",
                "PUBH 4500", "PUBH 4810",
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "public_health_bs": {
        "2022-23": None,
        "2023-24": None,
        "2024-25": {
            "name": "Public Health (BS)",
            "total_credits": 53,
            "required_core": [
                "PUBH 2010", "PUBH 3000", "PUBH 3100", "PUBH 3200",
                "PUBH 3300", "PUBH 3400", "PUBH 4500", "PUBH 4810",
            ],
            "natural_sciences_bs": {
                "credits": 12,
                "required": ["BIOL 2410", "BIOL 2420", "BIOL 2230"],
            },
            "elective": {"credits": "2-4"},
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "public_health_minor": {
        "all_years": {
            "name": "Public Health Minor",
            "total_credits": "15-17",
            "required": ["PUBH 2010", "PUBH 3100"],
            "elective": {"credits": 9, "dept": "PUBH"},
        },
    },
}

# ─────────────────────────────────────────────
# SOCIAL WORK & CRIMINAL JUSTICE
# ─────────────────────────────────────────────

SOCIAL_WORK_CRIMINAL_JUSTICE = {
    "social_work": {
        "all_years": {
            "name": "Social Work (BSW)",
            "total_credits": 64,
            "accreditation": "CSWE accredited",
            "prerequisites_for_admission": [
                "SOCI 2010", "SOCI 2020", "SOWK 2000", "SOWK 2100",
            ],
            "foundation": [
                "BIOL 2040", "POSC 2100", "PSYC 2000", "PSYC 2440",
                "SOCI 3100", "SOCI 3400",
            ],
            "core": [
                "SOWK 2200", "SOWK 3100", "SOWK 4350", "SOWK 4710",
                "SOWK 4720", "SOWK 4730", "SOWK 4850",
                "SOCI 3700",
            ],
            "practicum": {"credits": 12, "course": "SOWK 4850", "hours": 442},
            "notes": "Admission to Social Work Program required for upper-division courses",
        },
        "2025-26": {
            "name": "Social Work (BSW)",
            "total_credits": 64,
            "core": [
                "SOWK 2200", "SOWK 3100", "SOWK 4350", "SOWK 4710",
                "SOWK 4720", "SOWK 4730", "SOWK 4850",
                "SOCI 3700",
            ],
        },
    },
    "criminal_justice": {
        "all_years": {
            "name": "Criminal Justice (BA)",
            "total_credits": 34,
            "required": ["CRIM 2510", "CRIM 2520", "CRIM 3110", "SOCI 3700"],
            "internship": {"credits": 4, "course": "CRIM 4810"},
            "capstone": {"credits": 3, "course": "CRIM 4900"},
            "soci_choose": {"credits": 3, "choose_from": ["SOCI 2010","SOCI 2020"]},
            "crim_elective": {"credits": 9, "dept": "CRIM"},
            "internship": {"credits": 4, "course": "CRIM 4810"},
        },
    },
    "criminal_justice_online": {
        "all_years": {
            "name": "Criminal Justice Online (BA)",
            "required": [
                "CRIM 2510", "CRIM 2520", "CRIM 3110", "CRIM 4900",
                "SOCI 2010",  # or 2020
                "SOCI 3700",
            ],
            "crim_elective": {"credits": 9, "dept": "CRIM"},
            "experience": {"credits": 4, "from": "CRIM 4810"},
        },
    },
    "criminal_justice_associate": {
        "all_years": {
            "name": "Criminal Justice Associate of Arts (AA)",
            "total_credits": 60,
            "required": [
                "BIBL 2000", "SOCI 2450",
                "CRIM 2510", "CRIM 2520", "CRIM 3110",
            ],
            "choose_one_soci": ["SOCI 2010", "SOCI 2020"],
            "additional_crim": {"credits": 9, "dept": "CRIM"},
            "la": {"credits": 12, "dept": ["HIST","POSC","PSYC","SOCI","ENGL","BIBL","COMM"], "notes": "From liberal arts program"},
            "other": {"credits": "varies"},
        },
    },
    "family_science_major": {
        "2022-23": {
            "name": "Family Science",
            "total_credits": 48,
            "required": [
                "SOCI 2100", "SOCI 3100", "SOCI 3140", "SOCI 3210",
                "SOCI 3700", "SOCI 3850", "SOCI 4350", "SOCI 4820",
                "SOCI 4910", "SOCI 4950",
                "BSNS 3150",
                "PSYC 2000", "PSYC 2100", "PSYC 2510",
                "SOWK 3200",
            ],
        },
        "2023-24": None,  # REMOVED
        "2024-25": None,
        "2025-26": None,
    },
    "minors": {
        "criminal_justice_minor": {
            "all_years": {
                "name": "Criminal Justice Minor",
                "total_credits": 17,
                "required": ["CRIM 2510", "CRIM 2520", "CRIM 3110", "CRIM 4900"],
                "elective": {"credits": 3, "dept": "CRIM"},
            },
        },
        "social_work_minor": {
            "all_years": {
                "name": "Social Work Minor",
                "total_credits": 17,
                "required": ["SOWK 2000", "SOWK 2100", "SOWK 3100"],
                "elective": {"credits": 8},
            },
        },
        "sociology_minor": {
            "all_years": {
                "name": "Sociology Minor",
                "total_credits": 15,
                "required": ["SOCI 2010"],  # or 2020
                "elective_upper": {"credits": 9, "dept": "SOCI", "min_level": 3000},
                "elective": {"credits": 3},
            },
        },
        "family_science_minor": {
            "2022-23": {
                "name": "Family Science Minor",
                "total_credits": 15,
                "required": ["SOCI 2100", "SOCI 3100", "SOCI 3140", "SOCI 3210"],
                "elective": {
                    "credits": 3,
                    "choose_from": ["BSNS 3150", "PSYC 2000", "PSYC 2510",
                                    "SOCI 2200", "SOCI 2450", "SOWK 3200"],
                },
            },
            "2023-24": None,  # Removed
            "2024-25": None,
            "2025-26": None,
        },
    },
}

# ─────────────────────────────────────────────
# TEACHER EDUCATION
# ─────────────────────────────────────────────

TEACHER_EDUCATION = {
    "elementary_education": {
        "2022-23": {
            "name": "Elementary Education K-6",
            "total_credits": 83,
            "required": [
                "EDUC 2000", "EDUC 2030", "EDUC 2100", "EDUC 2110",
                "EDUC 2170", "EDUC 2200", "EDUC 2460", "EDUC 2520",
                "EDUC 2730", "EDUC 3120", "EDUC 3300", "EDUC 4120",
                "EDUC 4125", "EDUC 4310", "EDUC 4320", "EDUC 4850",
                "EDUC 4910",
                "SPED 2400",
                "MUED 2110",
                "EDUC 4010",  # student teaching
                "EDUC 4930",
            ],
            "la_licensure": {
                "credits": 21,
                "note": "Specific LA courses that also satisfy state licensure",
                "courses": ["MATH 1100", "BIOL 1000", "PHYS 1020",
                            "ENGL 3590", "HIST 2030 or 2040", "HIST 2110 or 2120"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Elementary Education K-6",
            "total_credits": 102,
            "notes": "SPED embedded into program — now includes full SPED coursework",
            "required": [
                "EDUC 2000", "EDUC 2030", "EDUC 2100", "EDUC 2110",
                "EDUC 2170", "EDUC 2200", "EDUC 2460", "EDUC 2520",
                "EDUC 2730", "EDUC 3120", "EDUC 3300", "EDUC 4120",
                "EDUC 4125", "EDUC 4310", "EDUC 4320", "EDUC 4850",
                "EDUC 4910",
                "SPED 2400", "SPED 2500", "SPED 2550", "SPED 3120", "SPED 3200",
                "MUED 2110",
                "EDUC 4010", "EDUC 4930",
            ],
        },
        "2025-26": {
            "name": "Elementary Education K-6",
            "total_credits": 102,
            "notes": "Same structure as 24-25; Raven Core integration for licensing",
            "la_raven_core_licensure": {
                "note": "Students must complete specific Raven Core courses for state licensure",
                "courses": ["MATH 1100", "BIOL 1000", "PHYS 1020",
                            "ENGL 3590", "HIST 2030 or 2040", "HIST 2110 or 2120"],
                "icc_note": "ICC-exempt students still must fulfill these licensure requirements",
            },
        },
    },
    "education_non_license": {
        "all_years": {
            "name": "Education (Non-License) BA",
            "total_credits": 30,
            "required": [
                "EDUC 2000", "EDUC 2030", "EDUC 2100", "EDUC 2110",
                "EDUC 2170", "EDUC 2200", "EDUC 2460",
                "PETE 3710", "SPED 2400",
            ],
            "internship": {"credits": 3, "course": "EDUC 4810"},
            "notes": "Non-license; does not satisfy Indiana teaching licensure",
        },
    },
    "education_minor": {
        "all_years": {
            "name": "Education Minor (Non-License)",
            "total_credits": 16,
            "required": [
                "EDUC 2000", "EDUC 2100", "EDUC 2110",
                "EDUC 2460", "SPED 2400",
            ],
            "internship": {"credits": 3, "course": "EDUC 4810"},
            "elective_educ": {
                "credits": 2,
                "dept": ["EDUC", "SPED"],
                "notes": "Remaining hrs from approved Teacher Ed courses",
            },
        },
    },
    "minors": {
        "education_minor": {
            "all_years": {
                "name": "Education Minor",
                "total_credits": 16,
                "required": ["EDUC 2000", "EDUC 2110"],
                "elective": {"credits": 10, "dept": "EDUC"},
            },
        },
        "special_education_minor": {
            "all_years": {
                "name": "Special Education / Mild Intervention Minor",
                "total_credits": 15,
                "required": ["SPED 2400", "SPED 2500", "SPED 2550", "SPED 3120", "SPED 3200"],
            },
        },
    },
}

# ─────────────────────────────────────────────
# INTERDISCIPLINARY PROGRAMS
# ─────────────────────────────────────────────

INTERDISCIPLINARY = {
    "peace_conflict_transformation_minor": {
        "2022-23": {
            "name": "Peace and Conflict Transformation (PACT) Minor",
            "total_credits": 18,
            "required": ["PACT 2100", "PACT 2200", "PACT 2300", "PACT 2400"],
            "service_learning": {"credits": 1, "notes": "Cross-cultural, service-learning, or internship"},
            "elective": {
                "credits": 9,
                "choose_from": [
                    "BSNS 3230", "BSNS 3300", "CMIN 3340", "CRIM 3010",
                    "DANC 3000", "ECON 2010", "ENGL 3190", "ENGL 3580",
                    "MLAN 2000", "HIST 3190", "PHIL 3210",
                    "POSC 3300", "POSC 3310", "POSC 3320", "POSC 3360",
                    "PSYC 2100", "RLGN 3020", "RLGN 3120",
                ],
            },
        },
        "2023-24": {
            "name": "Peace and Conflict Transformation (PACT) Minor",
            "total_credits": 16,
            "foundation": ["PACT 2100", "PACT 2200", "PACT 2400"],  # Restructured; PACT 2300 removed from required
            "elective": {"credits": "10-11"},
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Peace & Conflict Transformation Minor",
            "total_credits": "16-17",
            "foundation": {
                "credits": 6,
                "required": ["PACT 2100", "PACT 2200", "PACT 2400"],
            },
            "interpersonal": {
                "credits": "3-4",
                "choose_from": ["CMIN 3340", "PSYC 2100"],
            },
            "global": {
                "credits": 3,
                "notes": "Global conflict course",
            },
            "elective": {"credits": "4-5"},
        },
    },
    "womens_studies_minor": {
        "all_years": {
            "name": "Women's Studies Minor",
            "total_credits": 15,
            "host_dept": "History and Political Science",
            "required": [
                "HIST 3260",
                "HIST 4650",  # or POSC 4650, ENGL 4650, SOCI 4650 with approval
            ],
            "elective": {
                "credits": 9,
                "choose_from": [
                    "HIST 4030", "SOCI 2120", "SOCI 3100",
                    "PSYC 2000", "POSC 3xxx",
                ],
            },
        },
    },
    "honors_program": {
        "all_years": {
            "name": "Honors Program",
            "notes": "Not a standalone major — HNRS courses count toward LA requirements",
            "courses_count_toward": {
                "F2": ["HNRS 2125"],
                "F3 WI": ["HNRS 2110"],
                "W1": ["HNRS 3325"],
                "W2": ["HNRS 2210"],
                "W3/RC6": ["HNRS 2300", "HNRS 3100"],
                "RC6": ["HNRS 2300", "HNRS 3100"],
                "AU3": ["HNRS 3325"],
                "AU6": ["HNRS 3221"],
            },
        },
    },
}

# ─────────────────────────────────────────────
# ENGINEERING (Physical Sciences / Engineering Dept)
# ─────────────────────────────────────────────

ENGINEERING = {
    "electrical_engineering_bs": {
        "all_years": {
            "name": "Electrical Engineering (BS)",
            "total_credits": 84,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 3100",
                "PHYS 2140", "PHYS 2150", "PHYS 2240", "PHYS 2250",
                "CHEM 2110",
                "ENGR 2001", "ENGR 2002", "ENGR 2003", "ENGR 2010", "ENGR 2020",
                "ENGR 2030", "ENGR 2070", "ENGR 2090", "ENGR 2200", "ENGR 2310",
                "ENGR 3020", "ENGR 3040", "ENGR 3050", "ENGR 3060", "ENGR 3070",
                "ENGR 4000", "ENGR 4010", "ENGR 4020", "ENGR 4950", "ENGR 4960",
                "CPSC 2500",
            ],
        },
    },
    "computer_engineering_bs": {
        "all_years": {
            "name": "Computer Engineering (BS)",
            "total_credits": 82,
            "accreditation": "ABET accredited",
            "required": [
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 3100",
                "PHYS 2140", "PHYS 2150",
                "CHEM 2110",
                "ENGR 2001", "ENGR 2002", "ENGR 2003", "ENGR 2010", "ENGR 2020",
                "ENGR 2030", "ENGR 2090", "ENGR 2200", "ENGR 2310",
                "ENGR 3020", "ENGR 3040", "ENGR 3060", "ENGR 4000", "ENGR 4010",
                "ENGR 4950", "ENGR 4960",
                "CPSC 1500", "CPSC 2500", "CPSC 2330",
            ],
        },
    },
    "mechanical_engineering_bs": {
        "all_years": {
            "name": "Mechanical Engineering (BS)",
            "total_credits": 83,
            "accreditation": "ABET accredited",
            "required": [
                "CPSC 2320",   # or CPSC 2500
                "CHEM 2110",
                "PHYS 2240", "PHYS 2250",
                "MATH 2010", "MATH 2020", "MATH 3010", "MATH 3020", "MATH 3100",
                "ENGR 2001", "ENGR 2002", "ENGR 2003", "ENGR 2010", "ENGR 2030",
                "ENGR 2070", "ENGR 2090", "ENGR 2110", "ENGR 2310",
                "ENGR 3030", "ENGR 3100", "ENGR 3110", "ENGR 3160", "ENGR 3180",
                "ENGR 3190", "ENGR 3510", "ENGR 4100", "ENGR 4110", "ENGR 4130",
                "ENGR 4160", "ENGR 4950", "ENGR 4960",
            ],
        },
    },
    "civil_engineering_bs": {
        "2022-23": None,
        "2023-24": {
            "name": "Civil Engineering (BS)",
            "total_credits": 130,
            "notes": "Added in 23-24",
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "mechatronics_engineering_bs": {
        "2022-23": None,
        "2023-24": {
            "name": "Mechatronics Engineering (BS)",
            "notes": "Multidisciplinary: mechanical + electrical + computer engineering",
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "humanitarian_engineering_complementary": {
        "all_years": {
            "name": "Humanitarian Engineering Complementary Major",
            "total_credits": 47,
            "required": [
                "PHYS 2240",
                "MATH 2010", "MATH 2020",
                "ENGR 2001", "ENGR 2002", "ENGR 2003", "ENGR 2010", "ENGR 2030",
                "ENGR 2060", "ENGR 2080", "ENGR 2090", "ENGR 2110", "ENGR 2310",
                "ENGR 3080", "ENGR 4950", "ENGR 4960",
            ],
            "human_context": {
                "credits": 7,
                "choose_from": [
                    "BSNS 2710", "BSNS 3120", "BSNS 4480",
                    "CMIN 2000", "CMIN 3910",
                    "RLGN 2130", "RLGN 3040", "RLGN 3120",
                    "PSYC 2000", "PSYC 2100", "PSYC 3200",
                    "SOCI 2020", "SOCI 2100", "SOCI 4350",
                    "SPAN 2010",
                ],
            },
        },
    },
    "humanitarian_engineering_minor": {
        "all_years": {
            "name": "Humanitarian Engineering Minor",
            "total_credits": "15-18",
            "required": ["ENGR 2060", "ENGR 2080", "ENGR 2090", "ENGR 3080"],
            "elective": {"credits": "4-7", "choose_from": "see complementary major list"},
        },
    },
}


# ─────────────────────────────────────────────
# MISSING PROGRAMS — added after gap analysis
# ─────────────────────────────────────────────

# ── Christian Ministry minors / major ─────────
CHRISTIAN_MINISTRY_EXTRA = {
    "bible_religion": {
        "all_years": {
            "name": "Bible and Religion Major",
            "total_credits": 36,
            "required": [
                "BIBL 2000", "BIBL 2050",
                "RLGN 2000", "RLGN 2130", "RLGN 2150",
                "RLGN 3040", "RLGN 3060", "RLGN 3300", "RLGN 3320",
            ],
            "elective_upper": {
                "credits": 3,
                "dept": ["BIBL", "RLGN"],
                "min_level": 3000,
                "notes": "3 upper-division hrs from BIBL or RLGN",
            },
            "choose_one_exegesis_ot": {
                "options": ["BIBL 3XXX"],  # Hebrew Bible exegetical course 3 hrs
                "credits": 3,
            },
            "choose_one_exegesis_nt": {
                "options": ["BIBL 4XXX"],  # New Testament exegetical course 3 hrs
                "credits": 3,
            },
        },
    },
    "biblical_studies_minor": {
        "all_years": {
            "name": "Biblical Studies Minor",
            "total_credits": 15,
            "required": ["BIBL 2050", "RLGN 2150"],
            "elective_upper": {
                "credits": 6, "dept": "BIBL",
                "notes": "6 hrs from BIBL courses (2110,2120,2210,2220 eligible)",
            },
        },
    },
    "christian_ministries_minor": {
        "all_years": {
            "name": "Christian Ministries Minor",
            "total_credits": 16,
            "required": ["CMIN 2000", "CMIN 2810"],
            "elective_upper": {
                "credits": 9, "dept": "CMIN",
                "notes": "9 additional hrs from CMIN courses",
            },
            "elective_upper_div": {
                "credits": 3, "dept": ["CMIN", "RLGN", "BIBL"],
                "min_level": 3000,
                "notes": "3 upper-division hrs from dept courses",
            },
        },
    },
    "christian_ministries_complementary": {
        "all_years": {
            "name": "Christian Ministries Complementary Major",
            "total_credits": 28,
            "required": [
                "BIBL 2000",
                "RLGN 2130", "RLGN 2150", "RLGN 3040", "RLGN 3060",
                "CMIN 2000",
            ],
            "choose_one_cmin": ["CMIN 3050", "CMIN 3080", "CMIN 3910"],
            "elective_upper": {
                "credits": 1, "dept": ["CMIN"],
                "notes": "At least 1 hr from CMIN 2810, 4810, or 3340",
            },
            "elective_upper_div": {
                "credits": 6, "dept": ["CMIN", "RLGN", "BIBL"],
                "notes": "3 additional CMIN hrs + 3 upper-div dept hrs",
            },
        },
    },
    "ethics_minor": {
        "all_years": {
            "name": "Ethics Minor",
            "total_credits": 15,
            "required": ["PHIL 2120"],
            "elective_upper": {
                "credits": 12,
                "choose_from": [
                    "BIBL 3420", "PHIL 3210", "RLGN 2130",
                    "RLGN 3120", "PHIL 3250",
                ],
                "notes": "4 courses from approved ethics list",
            },
        },
    },
    "history_of_christianity_minor": {
        "all_years": {
            "name": "History of Christianity Minor",
            "total_credits": 15,
            "required": ["RLGN 3060", "RLGN 3300"],
            "elective_upper": {
                "credits": 9,
                "dept": ["RLGN", "BIBL", "HIST"],
                "min_level": 3000,
                "notes": "Additional upper-div RLGN/HIST courses",
            },
        },
    },
    "philosophy_minor": {
        "all_years": {
            "name": "Philosophy Minor",
            "total_credits": 15,
            "required": ["PHIL 2120"],
            "elective_upper": {
                "credits": 12,
                "dept": "PHIL",
                "notes": "12 additional hrs from PHIL courses",
            },
        },
    },
    "religion_minor": {
        "all_years": {
            "name": "Religion Minor",
            "total_credits": 15,
            "required": ["RLGN 2000", "RLGN 3060", "RLGN 3320"],
            "elective_upper": {
                "credits": 6, "dept": "RLGN",
                "notes": "Remaining hrs from RLGN-captioned courses not applied to LA",
            },
        },
    },
}

# ── Communication minors / complementaries ─────
COMMUNICATION_EXTRA = {
    "cinema_media_arts_minor": {
        "all_years": {
            "name": "Cinema and Media Arts Minor",
            "total_credits": 18,
            "required": [
                "COMM 2020", "COMM 2060", "COMM 2160",
                "COMM 2200", "COMM 2860",
            ],
            "choose_one_comm": ["COMM 2320", "COMM 2420"],
        },
    },
    "communication_minor": {
        "all_years": {
            "name": "Communication Minor",
            "total_credits": 18,
            "elective_upper": {
                "credits": 18, "dept": "COMM",
                "notes": "Any COMM-captioned course except 4750 and 4800",
            },
        },
    },
    "event_planning_minor": {
        "all_years": {
            "name": "Event Planning and Management Minor",
            "total_credits": 15,
            "required": [
                "BSNS 2810", "COMM 2240", "COMM 3250",
                "COMM 3370", "COMM 4340",
            ],
            "elective_upper": {
                "credits": 1,
                "choose_from": ["COMM 3860"],
                "notes": "COMM 3860 (1-2 hrs)",
            },
        },
    },
    "journalism_minor": {
        "all_years": {
            "name": "Journalism Minor",
            "total_credits": 18,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130",
                "COMM 3130", "COMM 3230",
            ],
            "choose_one_comm": ["COMM 3200", "COMM 4000"],
            "elective_upper": {
                "credits": 2,
                "choose_from": ["COMM 2850"],
                "notes": "2 hrs from COMM 2850",
            },
        },
    },
    "journalism_complementary": {
        "all_years": {
            "name": "Journalism Complementary Major",
            "total_credits": 30,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130",
                "COMM 2200", "COMM 3130", "COMM 3200",
                "COMM 3230", "COMM 4000",
            ],
            "elective_upper": {
                "credits": 5,
                "choose_from": [
                    "COMM 2850", "COMM 4800",
                    "COMM 2140", "COMM 3330", "COMM 3370",
                ],
            },
        },
    },
    "public_relations_minor": {
        "all_years": {
            "name": "Public Relations Minor",
            "total_credits": 18,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130", "COMM 2240",
            ],
            "choose_one_comm": ["COMM 3250", "COMM 3440"],
            "elective_upper": {
                "credits": 6,
                "choose_from": [
                    "COMM 3050", "COMM 3240", "COMM 3340", "COMM 3370",
                ],
            },
        },
    },
    "public_relations_complementary": {
        "all_years": {
            "name": "Public Relations Complementary Major",
            "total_credits": 30,
            "required": [
                "COMM 2000", "COMM 2010", "COMM 2130",
                "COMM 2200", "COMM 2240", "COMM 3050",
                "COMM 3200", "COMM 3250", "COMM 3330",
                "COMM 3340", "COMM 3370", "COMM 3440", "COMM 4000",
            ],
        },
    },
    "visual_communication_design_minor": {
        "all_years": {
            "name": "Visual Communication Design Minor",
            "total_credits": 18,
            "required": ["ARTS 2011", "ARTS 3110", "ARTS 3310"],
            "choose_one_arth": ["ARTH 2000", "ARTH 3030"],
            "choose_one_arts_a": ["ARTS 1210", "ARTS 2010"],
            "choose_one_arts_b": ["ARTS 1250", "ARTS 2100"],
        },
    },
}

# ── English minors ────────────────────────────
ENGLISH_EXTRA = {
    "english_studies_minor": {
        "all_years": {
            "name": "English Studies Minor",
            "total_credits": 15,
            "elective_upper": {
                "credits": 15,
                "dept": "ENGL",
                "min_level": 2000,
                "notes": "Any combination of ENGL 2000+ (excl. 1100,1110,1120,4700)",
            },
        },
    },
    "literary_studies_minor": {
        "all_years": {
            "name": "Literary Studies Minor",
            "total_credits": 15,
            "required": ["ENGL 2400"],
            "elective_upper": {
                "credits": 12,
                "dept": "ENGL",
                "min_level": 2000,
                "notes": "Courses from British, American, and World lit groups",
            },
        },
    },
    "writing_minor": {
        "all_years": {
            "name": "Writing Minor",
            "total_credits": 15,
            "elective_upper": {
                "credits": 15,
                "choose_from": [
                    "ENGL 2500", "ENGL 2510", "ENGL 2580",
                    "ENGL 3000", "ENGL 3110", "ENGL 3120",
                    "ENGL 3140", "ENGL 3160", "ENGL 3180",
                    "ENGL 3190", "ENGL 3870", "ENGL 3880",
                    "COMM 3220", "COMM 3260",
                ],
                "notes": "15 hrs from writing courses",
            },
        },
    },
}

# ── History / PolSci minors ───────────────────
HISTORY_POLSCI_EXTRA = {
    "history_minor": {
        "all_years": {
            "name": "History Minor",
            "total_credits": 15,
            "elective_upper": {
                "credits": 15, "dept": "HIST",
                "min_level": 1000,
                "notes": "15 hrs from HIST courses; at least 2 from 3000/4000-level. HIST 4700 does not apply.",
            },
        },
    },
    "international_relations_minor": {
        "all_years": {
            "name": "International Relations Minor",
            "total_credits": 15,
            "required": [
                "POSC 2020", "POSC 2580", "POSC 3300", "POSC 3510",
            ],
            "elective_upper": {
                "credits": 3,
                "choose_from": [
                    "POSC 3310", "POSC 3320", "POSC 3330", "POSC 3450",
                ],
            },
        },
    },
    "legal_studies_minor": {
        "all_years": {
            "name": "Legal Studies Minor",
            "total_credits": 15,
            "required": ["POSC 3200"],
            "elective_upper": {
                "credits": 12,
                "choose_from": [
                    "POSC 3110", "POSC 3120", "POSC 3130",
                    "POSC 3150", "POSC 3210", "POSC 3220",
                ],
                "notes": "Additional legal studies courses",
            },
        },
    },
    "political_science_minor": {
        "all_years": {
            "name": "Political Science Minor",
            "total_credits": 15,
            "required": ["POSC 2020", "POSC 2100"],
            "elective_upper": {
                "credits": 9, "dept": "POSC",
                "min_level": 1000,
                "notes": "Remaining hrs from POSC; at least 6 upper-div. Max 3 hrs from 2810/4800/4810/4820.",
            },
        },
    },
    "public_history_minor": {
        "all_years": {
            "name": "Public History Minor",
            "total_credits": 18,
            "required": ["HIST 2000", "HIST 4800", "ARTH 2000", "ARTS 1250"],
            "elective_upper": {
                "credits": 8, "dept": "HIST",
                "notes": "Upper-division HIST electives for public history practice",
            },
        },
    },
}

# ── Kinesiology minors ────────────────────────
KINESIOLOGY_EXTRA = {
    "athletic_coaching_minor": {
        "all_years": {
            "name": "Athletic Coaching Minor",
            "total_credits": 15,
            "core": [
                "PEHS 1450", "PEHS 1550",
            ],
            "choose_one_atrg": ["ATRG 1530", "EXSC 4010"],
            "choose_one_pehs": ["PEHS 2340", "PEHS 3340"],
            "elective_upper": {
                "credits": 4,
                "dept": ["PEHS", "EXSC", "SPRL"],
                "notes": "4-5 hrs from coaching elective list",
            },
        },
    },
    "nutrition_minor": {
        "all_years": {
            "name": "Nutrition Minor",
            "total_credits": 16,
            "required": [
                "EXSC 2140", "EXSC 2580",
                "EXSC 3100", "EXSC 3200", "EXSC 3300",
            ],
        },
    },
    "sport_recreational_leadership_minor": {
        "all_years": {
            "name": "Sport and Recreational Leadership Minor",
            "total_credits": 16,
            "required": [
                "PETE 1300", "PEHS 1450",
                "SPRL 1350", "SPRL 2450", "SPRL 2550", "SPRL 3150",
            ],
            "choose_one_sprl": [
                "PETE 3720", "PETE 4900", "SPRL 3300", "SPRL 4850",
            ],
        },
    },
}

# ── Mathematics extra major ───────────────────
MATHEMATICS_EXTRA = {
    "math_decision_science_ba": {
        "all_years": {
            "name": "Mathematics-Decision Science Major, BA",
            "total_credits": 53,
            "required": [
                "MATH 2010", "MATH 2020", "MATH 2120",
                "MATH 3010", "MATH 3020", "MATH 3200",
                "MATH 4000", "MATH 4010",
                "BSNS 2710", "BSNS 2810", "BSNS 3240",
                "BSNS 3510", "BSNS 4110", "BSNS 4330",
            ],
            "choose_one_math": ["MATH 3100", "MATH 3300", "MATH 3400"],
            "elective_upper": {
                "credits": 3,
                "notes": "3-hr independent study combining math and decision science",
            },
        },
    },
}

# ── Modern Languages minor ────────────────────
MODERN_LANGUAGES_EXTRA = {
    "french_german_minor": {
        "all_years": {
            "name": "French/German Studies Minor",
            "total_credits": 15,
            "elective_upper": {
                "credits": 15,
                "dept": ["FREN", "GERM", "MLAN"],
                "notes": "15 hrs of French or German; MLAN 3400 (4 hrs) may substitute",
            },
        },
    },
    "spanish_minor": {
        "all_years": {
            "name": "Spanish Minor",
            "total_credits": 15,
            "elective_upper": {
                "credits": 15, "dept": "SPAN",
                "min_level": 1000,
                "notes": "15 hrs of SPAN courses; advanced courses strongly recommended",
            },
        },
    },
}

# ── Music / Theatre / Dance minors ────────────
MUSIC_THEATRE_DANCE_EXTRA = {
    "dance_minor": {
        "all_years": {
            "name": "Dance Minor",
            "total_credits": 18,
            "required": [
                "DANC 1580", "DANC 1590", "DANC 3000", "DANC 3510",
            ],
            "choose_one_danc": ["DANC 3010", "DANC 3020"],
            "elective_upper": {
                "credits": 6,
                "dept": "DANC",
                "notes": "1 hr DANC 1150, 1 hr DANC 1160, 2 hrs modern technique, 1 hr jazz, 2 hrs ballet",
            },
        },
    },
    "music_minor": {
        "all_years": {
            "name": "Music Minor",
            "total_credits": 18,
            "required": [
                "MUSC 1010", "MUSC 1020", "MUSC 1030",
                "MUSC 1040", "MUSC 2110",
            ],
            "applied_primary": {"credits": 4, "dept": "MUPF",
                                "notes": "4 hrs from MUPF 1050, 1060 and/or private piano"},
            "applied_music": {"credits": 2, "notes": "2 hrs applied study (private and/or class)"},
            "ensembles": {"credits": 2, "notes": "2 hrs music ensembles"},
        },
    },
    "music_performance_minor": {
        "all_years": {
            "name": "Music Performance Minor",
            "total_credits": 15,
            "notes": "Admission by audition. Track A: music majors (15-16 hrs). Track B: non-music majors (18 hrs).",
            "required_conducting": ["MUED 2470"],
            "applied_study": {"credits": 6, "dept": ["MUPF"],
                             "notes": "6-8 hrs additional applied + half recital"},
            "singers_choose": {
                "credits": 4,
                "choose_from": ["MUED 2510","MUED 2520","MUED 3350",
                                "MUPF 1150","MUPF 1160","MUPF 1170"],
            },
            "pianists_choose": {
                "credits": 5,
                "choose_from": ["MUED 3370","MUSC 3380",
                                "MUPF 1190","MUPF 1210","MUPF 1520","MUPF 1530"],
            },
            "instrumental_choose": {
                "credits": 5,
                "choose_from": ["MUPF 1190","MUPF 1230","MUPF 1250",
                                "MUPF 1360","MUPF 1370","MUPF 1380","MUPF 1390"],
            },
        },
    },
    "theatre_minor": {
        "all_years": {
            "name": "Theatre Minor",
            "total_credits": 17,
            "required": ["THEA 2350"],
            "choose_one_thea_a": ["THEA 3010", "THEA 3020", "THEA 4900"],
            "choose_one_thea_b": ["THEA 3500", "THEA 3550"],
            "elective_upper": {
                "credits": 2, "choose_from": ["THEA 2890"],
                "notes": "At least 2 hrs from THEA 2890; remaining hrs from THEA courses",
            },
        },
    },
}

# ── Social Work / CJ extras ───────────────────
SOCIAL_WORK_EXTRA = {
    "criminal_justice_minor": {
        "all_years": {
            "name": "Criminal Justice Minor",
            "total_credits": 17,
            "required": [
                "CRIM 2510", "CRIM 2520", "CRIM 3110", "CRIM 4900",
            ],
            "elective_upper": {
                "credits": 3, "dept": "CRIM",
                "notes": "3 additional hrs from CRIM courses",
            },
        },
    },
    "family_science_minor": {
        "2022-23": {
            "name": "Family Science Minor",
            "total_credits": 15,
            "required": [
                "SOCI 2100", "SOCI 3100", "SOCI 3140", "SOCI 3210",
            ],
            "choose_one_soci": [
                "BSNS 3150", "PSYC 2000", "PSYC 2510",
                "SOCI 2200", "SOCI 2450", "SOWK 3200",
            ],
        },
        "2023-24": None,
        "2024-25": None,
        "2025-26": None,
    },
    "social_work_minor": {
        "all_years": {
            "name": "Social Work Minor",
            "total_credits": 17,
            "required": [
                "SOCI 2020", "SOWK 2000", "SOWK 2200",
                "SOWK 3100", "BIOL 2040",
            ],
        },
    },
    "sociology_minor": {
        "all_years": {
            "name": "Sociology Minor",
            "total_credits": 15,
            "required": ["SOCI 2010"],
            "elective_upper": {
                "credits": 6, "dept": "SOCI", "min_level": 3000,
                "notes": "At least 6 hrs from 3000/4000-level SOCI",
            },
            "elective_lit": {
                "credits": 6, "dept": "SOCI",
                "notes": "Remaining hrs from any SOCI-captioned course",
            },
        },
    },
}

# ── Teacher Education extras ──────────────────
TEACHER_EDUCATION_EXTRA = {
    "special_ed_minor": {
        "all_years": {
            "name": "Special Education Minor (P-12)",
            "total_credits": 15,
            "required": [
                "SPED 2400", "SPED 2500", "SPED 2550",
                "SPED 3120", "SPED 3200",
            ],
            "notes": "Licensure requires additional testing and student teaching in special ed setting.",
        },
    },
    "education_minor": {
        "all_years": {
            "name": "Education Minor (Non-License)",
            "total_credits": 16,
            "required": [
                "EDUC 2000", "EDUC 2100", "EDUC 2110",
                "EDUC 2460", "EDUC 4810", "SPED 2400",
            ],
        },
    },
    "teaching_minor": {
        "all_years": {
            "name": "Teaching Minor",
            "total_credits": 15,
            "notes": "Special Education Mild Intervention focus. Contact Teacher Ed department for current course list.",
            "required": ["SPED 2400", "EDUC 2110"],
            "elective_upper": {
                "credits": 9, "dept": ["EDUC", "SPED"],
                "notes": "Remaining hrs from approved Teacher Ed courses",
            },
        },
    },
}

# ── FSB Complementary Majors ──────────────────
FSB_COMPLEMENTARY = {
    "business_admin_complementary": {
        "all_years": {
            "name": "Business Administration Complementary Major",
            "total_credits": 24,
            "required": [
                "BSNS 2010", "BSNS 2710", "BSNS 2810",
                "BSNS 3150", "BSNS 3550",
            ],
            "elective_upper": {
                "credits": 9, "dept": "BSNS",
                "notes": "Additional BSNS courses to reach 24 hrs",
            },
        },
    },
    "financial_planning_complementary": {
        "all_years": {
            "name": "Financial Planning Complementary Major",
            "total_credits": 24,
            "required": [
                "ACCT 2010",
                "BSNS 2510", "BSNS 3350", "BSNS 4150",
                "ECON 2010",
            ],
            "elective_upper": {
                "credits": 9, "dept": ["BSNS", "ACCT", "ECON"],
                "notes": "Additional finance/business courses to reach 24 hrs",
            },
        },
    },
    "business_info_systems_complementary": {
        "all_years": {
            "name": "Business Information Systems Complementary Major",
            "total_credits": 24,
            "required": [
                "CPSC 1100", "CPSC 1200",
                "BSNS 2710", "BSNS 3510",
            ],
            "elective_upper": {
                "credits": 12, "dept": ["CPSC", "BSNS"],
                "notes": "Additional CS/Business courses to reach 24 hrs",
            },
        },
    },
    "data_science_complementary": {
        "all_years": {
            "name": "Data Science Complementary Major",
            "total_credits": 30,
            "required": [
                "CPSC 1200", "CPSC 2100", "CPSC 2200",
                "MATH 2120", "MATH 4010",
            ],
            "elective_upper": {
                "credits": 15, "dept": ["CPSC", "MATH"],
                "notes": "Upper-division data science/math courses",
            },
        },
    },
}

# ── Liberal Arts and Intercultural Studies ─────
LIBERAL_ARTS_INTERCULTURAL = {
    "liberal_arts_intercultural": {
        "all_years": {
            "name": "Liberal Arts and Intercultural Studies BA",
            "total_credits": 120,
            "notes": "Flexible program designed for students pursuing interdisciplinary study. "
                     "Requires 30 hrs in a concentration area plus completion of LA requirements. "
                     "Administered by LART/Intercultural Studies dept.",
            "required": ["LART 1050"],
            "elective_upper": {
                "credits": 30,
                "dept": ["LART","HIST","COMM","ENGL","PSYC","SOCI","SPAN","POSC","RLGN","PHIL"],
                "notes": "30-hr concentration in approved subject area(s)",
            },
        },
    },
}

# ── Professional Development BA ────────────────
PROFESSIONAL_DEVELOPMENT = {
    "professional_development_ba": {
        "all_years": {
            "name": "Professional Development Major, BA",
            "total_credits": 120,
            "required": ["LART 4500"],
            "elective_upper": {
                "credits": 30, "dept": ["LEAD","BSNS","COMM","PSYC","EDUC"],
                "notes": "30-hr concentration in approved subject area (must have 2.0 GPA in concentration area); plan approved by program director",
            },
        },
    },
}


# ─────────────────────────────────────────────
# FSB MINORS (inlined from fsb_minors.py)
# ─────────────────────────────────────────────
FSB_MINORS = {
    "sport_marketing_minor": {'2022-23': {'name': 'Sport Marketing Minor', 'total_credits': 18, 'fsb_majors_track': {'required': ['BSNS 3130', 'BSNS 4360', 'BSNS 4560'], 'choose_6_from': ['BSNS 3210', 'BSNS 3220', 'BSNS 3550', 'BSNS 4400', 'BSNS 4550', 'BSNS 4800']}, 'non_fsb_track': {'required': ['BSNS 2810'], 'choose_12_from_sm_major': True, 'plus_3_from_core': True}}, '2023-24': {'name': 'Sport Marketing Minor', 'total_credits': 18, 'fsb_majors_track': {'required': ['BSNS 3130', 'BSNS 4360', 'BSNS 4560'], 'choose_6_from': ['BSNS 3210', 'BSNS 3220', 'BSNS 3550', 'BSNS 4400', 'BSNS 4550', 'BSNS 4800']}, 'non_fsb_track': {'required': ['BSNS 2810'], 'choose_12_from_sm_major': True, 'plus_3_from_core': True}}, '2024-25': {'name': 'Sport Marketing Minor', 'total_credits': 18, 'fsb_majors_track': {'required': ['BSNS 3130', 'BSNS 4360', 'BSNS 4560'], 'choose_6_from': ['BSNS 3210', 'BSNS 3220', 'BSNS 3550', 'BSNS 4400', 'BSNS 4550', 'BSNS 4800']}, 'non_fsb_track': {'required': ['BSNS 2810'], 'choose_12_from_sm_major': True, 'plus_3_from_core': True}}, '2025-26': {'name': 'Sports Management Minor', 'total_credits': 18, 'fsb_majors_track': {'required': ['BSNS 3130', 'BSNS 4360', 'BSNS 4560'], 'choose_6_from': ['COMM 2130', 'COMM 2140', 'SPRL 3300']}, 'non_fsb_track': {'required': ['BSNS 2810'], 'choose_12_from_sm_major': True, 'plus_3_from_core': True}}},
    "accounting_minor": {'2022-23': {'name': 'Accounting Minor', 'total_credits': 15, 'required': ['ACCT 2010', 'ACCT 2020'], 'choose_9_from': ['ACCT 3010', 'ACCT 3020', 'ACCT 3110', 'ACCT 3500', 'ACCT 4020', 'ACCT 4050', 'ACCT 4100']}, '2023-24': {'same_as': '2022-23', 'name': 'Accounting Minor', 'total_credits': 15}, '2024-25': {'same_as': '2022-23', 'name': 'Accounting Minor', 'total_credits': 15}, '2025-26': {'same_as': '2022-23', 'name': 'Accounting Minor', 'total_credits': 15}},
    "economics_minor": {'2022-23': {'name': 'Economics Minor', 'total_credits': 18, 'required': ['ECON 2010', 'ECON 2020', 'ECON 3020', 'ECON 3410'], 'choose_6_from': ['ECON 3110', 'ECON 3210', 'ECON 3850', 'ECON 4020', 'BSNS 4240', 'POSC 2200']}, '2023-24': {'same_as': '2022-23', 'name': 'Economics Minor', 'total_credits': 18}, '2024-25': {'same_as': '2022-23', 'name': 'Economics Minor', 'total_credits': 18}, '2025-26': {'same_as': '2022-23', 'name': 'Economics Minor', 'total_credits': 18}},
    "entrepreneurship_minor": {'2022-23': {'name': 'Entrepreneurship Minor', 'fsb_total': 18, 'non_fsb_total': 15, 'core_required': ['BSNS 2810', 'BSNS 3850'], 'choose_from': ['BSNS 3100', 'BSNS 3240', 'BSNS 3510', 'BSNS 4050']}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
    "finance_minor": {'2022-23': {'name': 'Finance Minor', 'total_credits': 18, 'required': ['ACCT 2010', 'BSNS 2510', 'BSNS 3350', 'BSNS 4150', 'ECON 3410'], 'elective': {'credits': 3, 'choose_from': ['BSNS 3150', 'BSNS 4160', 'BSNS 4240', 'BSNS 4320']}}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
    "global_business_minor": {'2022-23': {'name': 'Global Business Minor', 'fsb_total': 15, 'non_fsb_total': 18, 'required': ['BSNS 3120', 'BSNS 4120', 'BSNS 4250'], 'choose_from': ['BSNS 3550', 'BSNS 4400', 'BSNS 4550', 'ECON 3850']}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
    "management_minor": {'2022-23': {'name': 'Management Minor', 'fsb_total': 15, 'non_fsb_total': 18, 'required': ['BSNS 2810', 'BSNS 3230', 'BSNS 4010', 'BSNS 4480'], 'elective': {'credits': 3, 'choose_from': ['BSNS 3100', 'BSNS 3240', 'BSNS 3510', 'BSNS 4050']}}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
    "marketing_minor": {'2022-23': {'name': 'Marketing Minor', 'total_credits': 18, 'required': ['BSNS 2710', 'BSNS 3210', 'BSNS 3220', 'BSNS 4110', 'BSNS 4330'], 'elective': {'credits': 3, 'choose_from': ['BSNS 3400', 'BSNS 3550', 'BSNS 4400', 'COMM 2200']}}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
    "music_entertainment_business_minor": {'2022-23': {'name': 'Music & Entertainment Business Minor', 'total_credits': 18, 'required': ['BSNS 3320', 'BSNS 3330', 'BSNS 3360', 'MUBS 2010', 'MUBS 2020', 'MUBS 3100']}, '2023-24': None, '2024-25': None, '2025-26': None},
    "social_media_minor": {'2022-23': {'name': 'Social Media Minor', 'total_credits': 15, 'required': ['BSNS 3400', 'BSNS 4400', 'COMM 2200'], 'elective': {'credits': 6, 'choose_from': ['BSNS 3550', 'BSNS 4550', 'COMM 2240', 'COMM 3150']}}, '2023-24': {'same_as': '2022-23'}, '2024-25': {'same_as': '2022-23'}, '2025-26': {'same_as': '2022-23'}},
}

# ─────────────────────────────────────────────
# MASTER LOOKUP
# ─────────────────────────────────────────────

ALL_NON_FSB_PROGRAMS = {
    # Biology / Natural Sciences
    "biology_ba":           BIOLOGY["biology_ba"],
    "biology_bs":           BIOLOGY["biology_bs"],
    "biochemistry_ba":      BIOLOGY["biochemistry_ba"],
    "biochemistry_bs":      BIOLOGY["biochemistry_bs"],
    "biology_minor":        BIOLOGY["biology_minor"],
    # Chemistry
    "chemistry_ba":         CHEMISTRY["chemistry_ba"],
    "chemistry_bs":         CHEMISTRY["chemistry_bs"],
    "chemistry_minor":      CHEMISTRY["chemistry_minor"],
    # Physics
    "physics_ba":           PHYSICS["physics_ba"],
    "engineering_physics_bs": PHYSICS["engineering_physics_bs"],
    "physical_science_ba":  PHYSICS["physical_science_ba"],
    "physics_minor":        PHYSICS["physics_minor"],
    # CS & Math
    "cs_ba":                COMPUTER_SCIENCE["cs_ba"],
    "cs_bs":                COMPUTER_SCIENCE["cs_bs"],
    "cs_complementary":     COMPUTER_SCIENCE["cs_complementary"],
    "cs_minor":             COMPUTER_SCIENCE["cs_minor"],
    "cybersecurity_major":  COMPUTER_SCIENCE["cybersecurity_major"],
    "cybersecurity_minor":  COMPUTER_SCIENCE["cybersecurity_minor"],
    "data_science_ba":      COMPUTER_SCIENCE["data_science_ba"],
    "data_science_bs":      COMPUTER_SCIENCE["data_science_bs"],
    "data_science_minor":   COMPUTER_SCIENCE["data_science_minor"],
    "information_systems_minor": COMPUTER_SCIENCE["information_systems_minor"],
    "math_ba":              MATHEMATICS["math_ba"],
    "math_bs":              MATHEMATICS["math_bs"],
    "actuarial_science_ba": MATHEMATICS["actuarial_science_ba"],
    "math_economics_ba":    MATHEMATICS["math_economics_ba"],
    "math_finance_ba":      MATHEMATICS["math_finance_ba"],
    "math_teaching_ba":     MATHEMATICS["math_teaching_ba"],
    "math_minor":           MATHEMATICS["math_minor"],
    "statistics_minor":     MATHEMATICS["statistics_minor"],
    # Communication
    "cinema_media_arts":    COMMUNICATION["cinema_media_arts"],
    "journalism_multimedia": COMMUNICATION["journalism_multimedia"],
    "public_relations":     COMMUNICATION["public_relations"],
    "visual_communication_design": COMMUNICATION["visual_communication_design"],
    # English
    "literary_studies":     ENGLISH["literary_studies"],
    "writing":              ENGLISH["writing"],
    "language_arts_teaching": ENGLISH["language_arts_teaching"],
    "songwriting":          ENGLISH["songwriting"],
    # History & PolSci
    "history":              HISTORY_POLSCI["history"],
    "public_history":       HISTORY_POLSCI["public_history"],
    "social_studies_teaching": HISTORY_POLSCI["social_studies_teaching"],
    "political_science":    HISTORY_POLSCI["political_science"],
    "polsci_philosophy_economics": HISTORY_POLSCI["polsci_philosophy_economics"],
    "international_relations": HISTORY_POLSCI["international_relations"],
    "national_security":    HISTORY_POLSCI["national_security"],
    # Modern Languages
    "spanish":              MODERN_LANGUAGES["spanish"],
    "spanish_complementary": MODERN_LANGUAGES["spanish_complementary"],
    "spanish_education":    MODERN_LANGUAGES["spanish_education"],
    # Music / Theatre / Dance
    "voice_performance_bmus": MUSIC_THEATRE_DANCE["voice_performance_bmus"],
    "instrumental_performance_bmus": MUSIC_THEATRE_DANCE["instrumental_performance_bmus"],
    "music_education_bmus": MUSIC_THEATRE_DANCE["music_education_bmus"],
    "musical_theatre_bmus": MUSIC_THEATRE_DANCE["musical_theatre_bmus"],
    "worship_arts_ba":      MUSIC_THEATRE_DANCE["worship_arts_ba"],
    "musical_theatre_ba":   MUSIC_THEATRE_DANCE["musical_theatre_ba"],
    "music_ba":             MUSIC_THEATRE_DANCE["music_ba"],
    "music_business":       MUSIC_THEATRE_DANCE["music_business"],
    "theatre":              MUSIC_THEATRE_DANCE["theatre"],
    "dance":                MUSIC_THEATRE_DANCE["dance"],
    "complementary_music":  MUSIC_THEATRE_DANCE["complementary_music"],
    "complementary_dance":  MUSIC_THEATRE_DANCE["complementary_dance"],
    # Christian Ministry
    "christian_ministries": CHRISTIAN_MINISTRY["christian_ministries"],
    "youth_ministries":     CHRISTIAN_MINISTRY["youth_ministries"],
    "ministry_studies_online": CHRISTIAN_MINISTRY["ministry_studies_online"],
    "csf_minor":            CHRISTIAN_MINISTRY["christian_spiritual_formation_minor"],
    "csf_complementary":    CHRISTIAN_MINISTRY["christian_spiritual_formation_complementary"],
    # Kinesiology
    "exercise_science":     KINESIOLOGY["exercise_science"],
    "sport_recreational_leadership": KINESIOLOGY["sport_recreational_leadership"],
    # Nursing
    "nursing_bsn":          NURSING["bsn"],
    "nursing_rn_bsn":       NURSING["rn_bsn"],
    "nursing_accelerated":  NURSING["accelerated_bsn"],
    # Psychology
    "psychology":           PSYCHOLOGY["psychology_major"],
    "psychology_complementary": PSYCHOLOGY["psychology_complementary"],
    "youth_leadership":     PSYCHOLOGY["youth_leadership_development"],
    "psychology_minor":     PSYCHOLOGY["psychology_minor"],
    # Public Health
    "public_health_ba":     PUBLIC_HEALTH["public_health_ba"],
    "public_health_bs":     PUBLIC_HEALTH["public_health_bs"],
    "public_health_minor":  PUBLIC_HEALTH["public_health_minor"],
    # Social Work / CJ
    "social_work":          SOCIAL_WORK_CRIMINAL_JUSTICE["social_work"],
    "criminal_justice":     SOCIAL_WORK_CRIMINAL_JUSTICE["criminal_justice"],
    "criminal_justice_online": SOCIAL_WORK_CRIMINAL_JUSTICE["criminal_justice_online"],
    "criminal_justice_associate": SOCIAL_WORK_CRIMINAL_JUSTICE["criminal_justice_associate"],
    "family_science":       SOCIAL_WORK_CRIMINAL_JUSTICE["family_science_major"],
    # Teacher Education
    "elementary_education": TEACHER_EDUCATION["elementary_education"],
    "education_non_license": TEACHER_EDUCATION["education_non_license"],
    "education_minor":       TEACHER_EDUCATION["education_minor"],
    # Interdisciplinary
    "pact_minor":           INTERDISCIPLINARY["peace_conflict_transformation_minor"],
    "womens_studies_minor": INTERDISCIPLINARY["womens_studies_minor"],
    "honors_program":       INTERDISCIPLINARY["honors_program"],
    # Engineering
    "electrical_engineering_bs": ENGINEERING["electrical_engineering_bs"],
    "computer_engineering_bs": ENGINEERING["computer_engineering_bs"],
    "mechanical_engineering_bs": ENGINEERING["mechanical_engineering_bs"],
    "civil_engineering_bs": ENGINEERING["civil_engineering_bs"],
    "mechatronics_engineering_bs": ENGINEERING["mechatronics_engineering_bs"],
    "humanitarian_engineering_complementary": ENGINEERING["humanitarian_engineering_complementary"],
    "humanitarian_engineering_minor": ENGINEERING["humanitarian_engineering_minor"],
    # ── Christian Ministry extras ──────────────
    "bible_religion":                CHRISTIAN_MINISTRY_EXTRA["bible_religion"],
    "biblical_studies_minor":        CHRISTIAN_MINISTRY_EXTRA["biblical_studies_minor"],
    "christian_ministries_minor":    CHRISTIAN_MINISTRY_EXTRA["christian_ministries_minor"],
    "christian_ministries_complementary": CHRISTIAN_MINISTRY_EXTRA["christian_ministries_complementary"],
    "ethics_minor":                  CHRISTIAN_MINISTRY_EXTRA["ethics_minor"],
    "history_of_christianity_minor": CHRISTIAN_MINISTRY_EXTRA["history_of_christianity_minor"],
    "philosophy_minor":              CHRISTIAN_MINISTRY_EXTRA["philosophy_minor"],
    "religion_minor":                CHRISTIAN_MINISTRY_EXTRA["religion_minor"],
    # ── Communication extras ───────────────────
    "cinema_media_arts_minor":       COMMUNICATION_EXTRA["cinema_media_arts_minor"],
    "communication_minor":           COMMUNICATION_EXTRA["communication_minor"],
    "event_planning_minor":          COMMUNICATION_EXTRA["event_planning_minor"],
    "journalism_minor":              COMMUNICATION_EXTRA["journalism_minor"],
    "journalism_complementary":      COMMUNICATION_EXTRA["journalism_complementary"],
    "public_relations_minor":        COMMUNICATION_EXTRA["public_relations_minor"],
    "public_relations_complementary": COMMUNICATION_EXTRA["public_relations_complementary"],
    "visual_communication_design_minor": COMMUNICATION_EXTRA["visual_communication_design_minor"],
    # ── English extras ─────────────────────────
    "english_studies_minor":         ENGLISH_EXTRA["english_studies_minor"],
    "literary_studies_minor":        ENGLISH_EXTRA["literary_studies_minor"],
    "writing_minor":                 ENGLISH_EXTRA["writing_minor"],
    # ── History / PolSci extras ────────────────
    "history_minor":                 HISTORY_POLSCI_EXTRA["history_minor"],
    "international_relations_minor": HISTORY_POLSCI_EXTRA["international_relations_minor"],
    "legal_studies_minor":           HISTORY_POLSCI_EXTRA["legal_studies_minor"],
    "political_science_minor":       HISTORY_POLSCI_EXTRA["political_science_minor"],
    "public_history_minor":          HISTORY_POLSCI_EXTRA["public_history_minor"],
    # ── Kinesiology extras ─────────────────────
    "athletic_coaching_minor":       KINESIOLOGY_EXTRA["athletic_coaching_minor"],
    "nutrition_minor":               KINESIOLOGY_EXTRA["nutrition_minor"],
    "sport_recreational_leadership_minor": KINESIOLOGY_EXTRA["sport_recreational_leadership_minor"],
    # ── Mathematics extras ─────────────────────
    "math_decision_science_ba":      MATHEMATICS_EXTRA["math_decision_science_ba"],
    # ── Modern Languages extras ────────────────
    "french_german_minor":           MODERN_LANGUAGES_EXTRA["french_german_minor"],
    "spanish_minor":                 MODERN_LANGUAGES_EXTRA["spanish_minor"],
    # ── Music / Theatre / Dance extras ────────
    "dance_minor":                   MUSIC_THEATRE_DANCE_EXTRA["dance_minor"],
    "music_minor":                   MUSIC_THEATRE_DANCE_EXTRA["music_minor"],
    "music_performance_minor":       MUSIC_THEATRE_DANCE_EXTRA["music_performance_minor"],
    "theatre_minor":                 MUSIC_THEATRE_DANCE_EXTRA["theatre_minor"],
    # ── Social Work / CJ extras ───────────────
    "criminal_justice_minor":        SOCIAL_WORK_EXTRA["criminal_justice_minor"],
    "family_science_minor":          SOCIAL_WORK_EXTRA["family_science_minor"],
    "social_work_minor":             SOCIAL_WORK_EXTRA["social_work_minor"],
    "sociology_minor":               SOCIAL_WORK_EXTRA["sociology_minor"],
    # ── Teacher Education extras ──────────────
    "special_ed_minor":              TEACHER_EDUCATION_EXTRA["special_ed_minor"],
    "education_minor":               TEACHER_EDUCATION_EXTRA["education_minor"],
    "teaching_minor":                TEACHER_EDUCATION_EXTRA["teaching_minor"],
    # FSB Minors
    "accounting_minor":              FSB_MINORS["accounting_minor"],
    "economics_minor":               FSB_MINORS["economics_minor"],
    "entrepreneurship_minor":        FSB_MINORS["entrepreneurship_minor"],
    "finance_minor":                 FSB_MINORS["finance_minor"],
    "global_business_minor":         FSB_MINORS["global_business_minor"],
    "management_minor":              FSB_MINORS["management_minor"],
    "marketing_minor":               FSB_MINORS["marketing_minor"],
    "music_entertainment_business_minor": FSB_MINORS["music_entertainment_business_minor"],
    "social_media_minor":            FSB_MINORS["social_media_minor"],
    "sport_marketing_minor":         FSB_MINORS["sport_marketing_minor"],
    # ── FSB Complementary Majors ──────────────
    "business_admin_complementary":  FSB_COMPLEMENTARY["business_admin_complementary"],
    "financial_planning_complementary": FSB_COMPLEMENTARY["financial_planning_complementary"],
    "business_info_systems_complementary": FSB_COMPLEMENTARY["business_info_systems_complementary"],
    "data_science_complementary":    FSB_COMPLEMENTARY["data_science_complementary"],
    # ── Liberal Arts / Prof Dev ───────────────
    "liberal_arts_intercultural":    LIBERAL_ARTS_INTERCULTURAL["liberal_arts_intercultural"],
    "professional_development_ba":   PROFESSIONAL_DEVELOPMENT["professional_development_ba"],
}


def get_non_fsb_requirements(program_key: str, catalog_year: str):
    """Return requirements for a non-FSB program and catalog year."""
    program = ALL_NON_FSB_PROGRAMS.get(program_key)
    if program is None:
        raise ValueError(f"Unknown program: {program_key}")
    # Check for all_years shortcut
    if "all_years" in program:
        return program["all_years"]
    result = program.get(catalog_year)
    if isinstance(result, dict) and "same_as" in result:
        base = program[result["same_as"]].copy() if isinstance(program.get(result["same_as"]), dict) else {}
        base.update({k: v for k, v in result.items() if k != "same_as"})
        return base
    return result


def program_exists_in_year(program_key: str, catalog_year: str) -> bool:
    """Return True if a program exists for a given catalog year."""
    req = get_non_fsb_requirements(program_key, catalog_year)
    return req is not None


def list_programs_by_year(catalog_year: str) -> list:
    """Return list of all program keys available in a given catalog year."""
    available = []
    for key in ALL_NON_FSB_PROGRAMS:
        if program_exists_in_year(key, catalog_year):
            available.append(key)
    return available
