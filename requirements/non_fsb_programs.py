"""
Anderson University — Non-FSB Program Requirements
2022-23 catalog rebuilt from official PDF (Au_Audit_-_22-23_Catalog.pdf).
Other years retain previous definitions pending their own rebuilds.
"""


def _yr(d, year):
    """Resolve a year-keyed dict, following same_as chains."""
    entry = d.get(year) or d.get("all_years")
    if entry is None:
        return None
    if isinstance(entry, dict) and "same_as" in entry:
        return _yr(d, entry["same_as"])
    return entry


# ─────────────────────────────────────────────────────────────────────────
# BIOLOGY
# ─────────────────────────────────────────────────────────────────────────
BIOLOGY = {
    "biology_ba": {
        "2022-23": {
            "name": "Biology (BA)",
            "total_credits": 48,
            "required": [
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-3030",
                "BIOL-4050",
                "BIOL-4070",
                "BIOL-4910",
                "BIOL-4920",
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
            ],
            "choose_one": [
                {"name": "Bioethics or Integration of Faith and Science", "choose_from": ["BIOL-3510", "BIOL-3920"]},
                {"name": "Additional CHEM (2120, 2220, or 3100)", "choose_from": ["CHEM-2120", "CHEM-2220", "CHEM-3100"]},
            ],
            "elective_groups": [
                {
                    "name": "Upper-division BIOL electives",
                    "credits": 8,
                    "dept": "BIOL",
                    "min_level": 3000,
                    "notes": "8 hrs upper-div BIOL; BIOL-2410+2420 substitute for 4 hrs",
                },
            ],
            "notes": "BIOL-2230, 3800, 4700 do not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Biology (BA)",
            "total_credits": 49,
            "required": [
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-3030",
                "BIOL-3510",
                "BIOL-4050",
                "BIOL-4070",
                "BIOL-4910",
                "BIOL-4920",
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
            ],
            "elective_groups": [
                {
                    "name": "Upper-division BIOL electives",
                    "credits": 8,
                    "dept": "BIOL",
                    "min_level": 3000,
                    "notes": "8 hrs upper-div BIOL; BIOL-2410+2420 substitute for 4 hrs",
                },
            ],
            "notes": "BIOL-2230 does not apply toward the major.",
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "biology_bs": {
        "2022-23": {
            "name": "Biology (BS)",
            "total_credits": 72,
            "required": [
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-3030",
                "BIOL-3510",
                "BIOL-4050",
                "BIOL-4070",
                "BIOL-4910",
                "BIOL-4920",
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "MATH-2120",
            ],
            "choose_one": [
                {"name": "Physics I", "choose_from": ["PHYS-2140", "PHYS-2240"]},
                {"name": "Physics II", "choose_from": ["PHYS-2150", "PHYS-2250"]},
                {"name": "Stats/Research Methods", "choose_from": ["MATH-2120", "PSYC-2440"]},
            ],
            "elective_groups": [
                {
                    "name": "Upper-division BIOL electives",
                    "credits": 12,
                    "dept": "BIOL",
                    "min_level": 3000,
                    "notes": "12 hrs upper-div BIOL; BIOL-2410+2420 substitute for 4 hrs",
                },
            ],
            "notes": "BIOL-2230, 3800, 4700 do not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Biology (BS)",
            "total_credits": 73,
            "required": [
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-3030",
                "BIOL-3510",
                "BIOL-4050",
                "BIOL-4070",
                "BIOL-4910",
                "BIOL-4920",
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "MATH-2120",
            ],
            "choose_one": [
                {"name": "Physics I", "choose_from": ["PHYS-2140", "PHYS-2240"]},
                {"name": "Physics II", "choose_from": ["PHYS-2150", "PHYS-2250"]},
            ],
            "elective_groups": [
                {
                    "name": "Upper-division BIOL electives",
                    "credits": 12,
                    "dept": "BIOL",
                    "min_level": 3000,
                    "notes": "12 hrs upper-div BIOL; BIOL-2410+2420 substitute for 4 hrs",
                },
            ],
            "notes": "BIOL-2230 does not apply toward the major.",
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "biology_minor": {
        "2022-23": {
            "name": "Biology Minor",
            "total_credits": 16,
            "required": ["BIOL-2210", "BIOL-2220"],
            "elective_groups": [
                {
                    "name": "Biology electives",
                    "credits": 8,
                    "dept": "BIOL",
                    "notes": "BIOL-3800 and 4700 do not apply toward the minor",
                },
            ],
            "notes": "BIOL-3800 and 4700 do not apply toward the minor.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Biology Minor",
            "total_credits": 16,
            "required": ["BIOL-2210", "BIOL-2220", "CHEM-2110"],
            "elective_groups": [
                {
                    "name": "Biology electives",
                    "credits": 5,
                    "dept": "BIOL",
                    "notes": "Upper-division BIOL courses",
                },
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# BIOCHEMISTRY
# ─────────────────────────────────────────────────────────────────────────
BIOCHEMISTRY = {
    "biochemistry_ba": {
        "2022-23": {
            "name": "Biochemistry (BA)",
            "total_credits": 56,
            "required": [
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "CHEM-3100",
                "CHEM-4510",
                "CHEM-4520",
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-4050",
                "BIOL-4310",
                "BIOL-4210",
                "CHEM-4210",
                "BIOL-4910",
                "BIOL-4920",
            ],
            "elective_groups": [
                {
                    "name": "Biochemistry electives",
                    "credits": 4,
                    "choose_from": [
                        "CHEM-3140",
                        "CHEM-4090",
                        "CHEM-4110",
                        "BIOL-3030",
                        "BIOL-4120",
                    ],
                    "notes": "Elective hours from CHEM-3140, 4090, 4110; BIOL-3030, 4120",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "biochemistry_bs": {
        "2022-23": {
            "name": "Biochemistry (BS)",
            "total_credits": 76,
            "required": [
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "CHEM-3100",
                "CHEM-4110",
                "CHEM-4510",
                "CHEM-4520",
                "BIOL-2210",
                "BIOL-2220",
                "BIOL-2240",
                "BIOL-3030",
                "BIOL-4050",
                "BIOL-4310",
                "MATH-2010",
            ],
            "choose_one": [
                {"name": "Biochemistry I", "choose_from": ["BIOL-4210", "CHEM-4210"]},
                {"name": "Biochemistry II", "choose_from": ["BIOL-4220", "CHEM-4220"]},
                {"name": "Science Seminar I", "choose_from": ["BIOL-4910", "CHEM-4910", "PHYS-4910"]},
                {"name": "Science Seminar II", "choose_from": ["BIOL-4920", "CHEM-4920", "PHYS-4920"]},
                {"name": "Physics I", "choose_from": ["PHYS-2140", "PHYS-2240"]},
                {"name": "Physics II", "choose_from": ["PHYS-2150", "PHYS-2250"]},
                {"name": "Stats/Research Methods", "choose_from": ["MATH-2120", "PSYC-2440"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# CHEMISTRY
# ─────────────────────────────────────────────────────────────────────────
CHEMISTRY = {
    "chemistry_ba": {
        "2022-23": {
            "name": "Chemistry (BA)",
            "total_credits": 52,
            "required": [
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "CHEM-3100",
                "CHEM-4510",
                "CHEM-4520",
                "CHEM-4910",
                "CHEM-4920",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
            ],
            "choose_one": [
                {"name": "Organic Lab", "choose_from": ["CHEM-4110", "CHEM-4120"]},
            ],
            "notes": "CHEM-1000 and 2700 do not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "chemistry_bs": {
        "2022-23": {
            "name": "Chemistry (BS)",
            "total_credits": 60,
            "required": [
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-2220",
                "CHEM-3100",
                "CHEM-4110",
                "CHEM-4510",
                "CHEM-4520",
                "CHEM-4910",
                "CHEM-4920",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
            ],
            "elective_groups": [
                {
                    "name": "Advanced Chemistry electives",
                    "credits": 16,
                    "choose_from": [
                        "CHEM-3140",
                        "CHEM-4090",
                        "CHEM-4100",
                        "CHEM-4120",
                        "CHEM-4210",
                        "CHEM-4650",
                    ],
                    "notes": "Minimum 16 hrs from CHEM-3140, 4090, 4100, 4120, 4210, 4650",
                },
            ],
            "notes": "CHEM-1000 and 2700 do not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "chemistry_minor": {
        "2022-23": {
            "name": "Chemistry Minor",
            "total_credits": 16,
            "required": ["CHEM-3100"],
            "notes": "Must include CHEM-3100. CHEM-1000 and 2700 do not apply.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# PHYSICS / PHYSICAL SCIENCE
# ─────────────────────────────────────────────────────────────────────────
PHYSICS = {
    "physics_ba": {
        "2022-23": {
            "name": "Physics (BA)",
            "total_credits": 60,
            "required": [
                "PHYS-2240",
                "PHYS-2250",
                "PHYS-3130",
                "PHYS-4130",
                "PHYS-4210",
                "PHYS-4220",
                "PHYS-4410",
                "PHYS-4510",
                "PHYS-4520",
                "PHYS-4910",
                "PHYS-4920",
                "ENGR-2030",
                "ENGR-2070",
                "ENGR-2310",
                "CHEM-2110",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
            ],
            "choose_one": [
                {
                    "name": "CS/Eng Computing",
                    "choose_from": ["CPSC-2320", "CPSC-1400", "CPSC-2500"],
                },
            ],
        },
    },
    "physical_science_ba": {
        "2022-23": {
            "name": "Physical Science (BA)",
            "total_credits": 50,
            "required": [
                "PHYS-1000",
                "PHYS-1020",
                "PHYS-1240",
                "PHYS-2240",
                "PHYS-2250",
                "PHYS-3130",
                "PHYS-4510",
                "PHYS-4520",
                "PHYS-4910",
                "PHYS-4920",
                "CHEM-2110",
                "CHEM-2120",
                "CHEM-2210",
                "CHEM-3100",
                "MATH-2010",
                "MATH-2020",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "physics_minor": {
        "2022-23": {
            "name": "Physics Minor",
            "total_credits": 16,
            "required": ["PHYS-2240", "PHYS-2250", "PHYS-3130"],
            "notes": "May include ENGR-2070",
        },
        "2023-24": {
            "name": "Physics Minor",
            "total_credits": 16,
            "required": ["PHYS-2240", "PHYS-2250", "PHYS-1000", "PHYS-1020"],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Physics Minor",
            "total_credits": 16,
            "required": ["PHYS-2240", "PHYS-2250", "PHYS-1020", "PHYS-1240"],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# COMPUTER SCIENCE
# ─────────────────────────────────────────────────────────────────────────
CS = {
    "cs_ba": {
        "2022-23": {
            "name": "Computer Science (BA)",
            "total_credits": 59,
            "required": [
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2420",
                "CPSC-2430",
                "CPSC-2500",
                "ENGR-2200",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4420",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
            ],
            "choose_one": [
                {"name": "Discrete Mathematical Structures", "choose_from": ["MATH-2200", "CPSC-2250"]},
            ],
            "elective_groups": [
                {
                    "name": "CS/Engr electives",
                    "credits": 6,
                    "dept": "CPSC",
                    "min_level": 2000,
                    "notes": "6 hrs from CPSC/ENGR-2000 and above",
                },
                {
                    "name": "Math elective",
                    "credits": 3,
                    "dept": "MATH",
                    "min_level": 1300,
                    "notes": "3-4 hrs from MATH 1300 or above",
                },
            ],
        },
        "2023-24": {
            "name": "Computer Science (BA)",
            "total_credits": 59,
            "required": [
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2420",
                "CPSC-2430",
                "CPSC-2500",
                "ENGR-2200",
                "MATH-2200",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4420",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
            ],
            "elective_groups": [
                {
                    "name": "CS/Engr electives",
                    "credits": 6,
                    "dept": "CPSC",
                    "min_level": 2000,
                    "notes": "6 hrs from CPSC/ENGR-2000 and above",
                },
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "cs_bs": {
        "2022-23": {
            "name": "Computer Science (BS)",
            "total_credits": 82,
            "required": [
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2420",
                "CPSC-2430",
                "CPSC-2500",
                "ENGR-2200",
                "MATH-2200",
                "CPSC-3380",
                "CPSC-4420",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-4010",
                "PHYS-2240",
            ],
            "choose_one": [
                {"name": "Networks/Systems", "choose_from": ["CPSC-3410", "ENGR-4050"]},
                {"name": "OS/Embedded", "choose_from": ["CPSC-3500", "CPSC-3520"]},
            ],
        },
        "2023-24": {
            "name": "Computer Science (BS)",
            "total_credits": 82,
            "required": [
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2420",
                "CPSC-2430",
                "CPSC-2500",
                "ENGR-2200",
                "MATH-2200",
                "CPSC-3380",
                "CPSC-4420",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-4010",
                "PHYS-2240",
            ],
            "choose_one": [
                {"name": "Networks/Systems", "choose_from": ["CPSC-3410", "ENGR-4050"]},
                {"name": "OS/Embedded", "choose_from": ["CPSC-3500", "CPSC-3520"]},
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "cs_complementary": {
        "2022-23": {
            "name": "Computer Science Complementary Major",
            "total_credits": 32,
            "required": ["CPSC-1400", "CPSC-1500", "CPSC-2100", "CPSC-2500"],
            "choose_one": [
                {
                    "name": "Math elective",
                    "choose_from": ["MATH-2010", "MATH-2020", "MATH-2120", "MATH-2200"],
                },
            ],
            "elective_groups": [
                {
                    "name": "CS electives",
                    "credits": 12,
                    "dept": "CPSC",
                    "min_level": 1200,
                    "notes": "12 hrs from CPSC-1200 or above",
                },
            ],
        },
        "2023-24": {
            "name": "Computer Science Complementary Major",
            "total_credits": 32,
            "required": ["CPSC-2020", "CPSC-2030", "CPSC-2100", "CPSC-2500"],
            "choose_one": [
                {
                    "name": "Math elective",
                    "choose_from": ["MATH-2010", "MATH-2020", "MATH-2120", "MATH-2200"],
                },
            ],
            "elective_groups": [
                {
                    "name": "CS electives",
                    "credits": 12,
                    "dept": "CPSC",
                    "min_level": 1200,
                    "notes": "12 hrs from CPSC-1200 or above",
                },
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "cs_minor": {
        "2022-23": {
            "name": "Computer Science Minor",
            "total_credits": 16,
            "required": ["CPSC-1400", "CPSC-1500"],
            "elective_groups": [
                {
                    "name": "CS electives",
                    "credits": 8,
                    "dept": "CPSC",
                    "min_level": 1200,
                    "notes": "8 hrs from CPSC-1200 and above",
                },
            ],
        },
        "2023-24": {
            "name": "Computer Science Minor",
            "total_credits": 16,
            "required": ["CPSC-2020", "CPSC-2030"],
            "elective_groups": [
                {
                    "name": "CS electives",
                    "credits": 8,
                    "dept": "CPSC",
                    "min_level": 1200,
                    "notes": "8 hrs from CPSC-1200 and above",
                },
            ],
        },
        "2024-25": {
            "name": "Computer Science Minor",
            "total_credits": 16,
            "required": ["CPSC-2020", "CPSC-2030", "CPSC-2000"],
            "elective_groups": [
                {"name": "CS electives", "credits": 6, "dept": "CPSC", "min_level": 1200},
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# DATA SCIENCE
# ─────────────────────────────────────────────────────────────────────────
DATA_SCIENCE = {
    "data_science_ba": {
        "2022-23": {
            "name": "Data Science (BA)",
            "total_credits": 57,
            "required": [
                "MATH-2010",
                "MATH-2120",
                "POSC-2420",
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2040",
                "CPSC-2080",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2500",
                "CPSC-3520",
                "CPSC-4100",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "PHIL-3250",
            ],
        },
        "2023-24": {
            "name": "Data Science (BA)",
            "total_credits": 60,
            "required": [
                "MATH-2010",
                "MATH-2120",
                "POSC-2420",
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2080",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2500",
                "CPSC-3520",
                "CPSC-4100",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "PHIL-3250",
            ],
        },
        "2024-25": {
            "name": "Data Science (BA)",
            "total_credits": 64,
            "required": [
                "MATH-2010",
                "MATH-2120",
                "MATH-3010",
                "POSC-2420",
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2080",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2500",
                "CPSC-3520",
                "CPSC-4100",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "PHIL-3250",
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "data_science_bs": {
        "2022-23": {
            "name": "Data Science (BS)",
            "total_credits": 72,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-4010",
                "POSC-2420",
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2040",
                "CPSC-2080",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2500",
                "CPSC-3520",
                "CPSC-4100",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "PHIL-3250",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Data Science (BS)",
            "total_credits": 81,
            "required": [
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2080",
                "CPSC-2100",
                "CPSC-2330",
                "CPSC-2500",
                "MATH-2010",
                "MATH-2020",
                "MATH-2120",
                "MATH-3010",
                "MATH-3020",
                "MATH-4010",
                "POSC-2420",
                "CPSC-3520",
                "CPSC-4100",
                "CPSC-4430",
                "CPSC-4950",
                "CPSC-4960",
                "PHIL-3250",
            ],
        },
    },
    "data_science_complementary": {
        "2022-23": {
            "name": "Data Science Complementary Major",
            "total_credits": 34,
            "required": [
                "MATH-2120",
                "POSC-2420",
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2040",
                "CPSC-2100",
                "CPSC-4100",
            ],
            "elective_groups": [
                {"name": "Advanced CS", "credits": 4, "dept": "CPSC", "min_level": 3000},
            ],
        },
        "2023-24": {
            "name": "Data Science Complementary Major",
            "total_credits": 34,
            "required": [
                "MATH-2120",
                "POSC-2420",
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2100",
                "CPSC-4100",
            ],
            "elective_groups": [
                {"name": "Advanced CS", "credits": 4, "dept": "CPSC", "min_level": 3000},
            ],
        },
        "2024-25": {
            "name": "Data Science Complementary Major",
            "total_credits": 37,
            "required": [
                "MATH-2010",
                "MATH-2120",
                "POSC-2420",
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2100",
                "CPSC-4100",
            ],
            "elective_groups": [
                {"name": "Advanced CS", "credits": 4, "dept": "CPSC", "min_level": 3000},
            ],
        },
        "2025-26": {
            "name": "Data Science Complementary Major",
            "total_credits": 37,
            "required": [
                "CPSC-2020",
                "CPSC-2030",
                "CPSC-2040",
                "CPSC-2100",
                "MATH-2120",
                "POSC-2420",
                "CPSC-4100",
            ],
            "elective_groups": [
                {"name": "Advanced CS", "credits": 4, "dept": "CPSC", "min_level": 3000},
            ],
        },
    },
    "data_science_minor": {
        "2022-23": {
            "name": "Data Science Minor",
            "total_credits": 15,
            "required": ["MATH-2120", "CPSC-1400", "CPSC-2040", "CPSC-2100"],
            "elective_groups": [
                {
                    "name": "Domain application course",
                    "credits": 3,
                    "choose_from": [
                        "ARTS-2100",
                        "COMM-2200",
                        "ENGL-3140",
                        "ENGL-3160",
                        "BIOL-4050",
                        "CHEM-3100",
                        "CHEM-4110",
                        "ENGR-4120",
                        "PHYS-4220",
                        "PHYS-4410",
                        "SOCI-3700",
                        "POSC-3140",
                        "POSC-3360",
                        "PSYC-3240",
                        "ACCT-3110",
                        "BSNS-2450",
                        "BSNS-3240",
                        "MATH-3400",
                        "BIBL-2050",
                        "HIST-2300",
                        "RLGN-3120",
                    ],
                },
            ],
        },
        "2023-24": {
            "name": "Data Science Minor",
            "total_credits": 16,
            "required": ["MATH-2120", "CPSC-2020", "CPSC-2040", "CPSC-2100"],
            "elective_groups": [
                {
                    "name": "Domain application course",
                    "credits": 3,
                    "choose_from": [
                        "ARTS-2100",
                        "COMM-2200",
                        "ENGL-3140",
                        "ENGL-3160",
                        "BIOL-4050",
                        "CHEM-3100",
                        "CHEM-4110",
                        "ENGR-4120",
                        "PHYS-4220",
                        "PHYS-4410",
                        "SOCI-3700",
                        "POSC-3140",
                        "POSC-3360",
                        "PSYC-3240",
                        "ACCT-3110",
                        "BSNS-2450",
                        "BSNS-3240",
                        "MATH-3400",
                        "BIBL-2050",
                        "HIST-2300",
                        "RLGN-3120",
                    ],
                },
            ],
        },
        "2025-26": {
            "name": "Data Science Minor",
            "total_credits": 17,
            "required": ["CPSC-2020", "CPSC-2040", "CPSC-2100", "MATH-2120"],
            "elective_groups": [
                {
                    "name": "Domain application course",
                    "credits": 3,
                    "choose_from": [
                        "ARTS-2100",
                        "COMM-2200",
                        "ENGL-3140",
                        "ENGL-3160",
                    ],
                },
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# CYBERSECURITY
# ─────────────────────────────────────────────────────────────────────────
CYBERSECURITY = {
    "cybersecurity_major": {
        "2022-23": {
            "name": "Cybersecurity Major",
            "total_credits": 56,
            "required": [
                "CPSC-2080",
                "CPSC-2180",
                "CPSC-2300",
                "MATH-2120",
                "POSC-2030",
                "POSC-2200",
                "POSC-2400",
                "POSC-2420",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4080",
                "CPSC-4480",
                "POSC-3370",
                "PHIL-3250",
            ],
            "choose_one": [
                {"name": "Homeland Security", "choose_from": ["POSC-3350", "CRIM-3350"]},
                {"name": "Discrete Mathematical Structures", "choose_from": ["MATH-2200", "CPSC-2250"]},
            ],
            "elective_groups": [
                {
                    "name": "CS/Policy elective",
                    "credits": 3,
                    "choose_from": ["CRIM-2520", "POSC-3310", "POSC-3250"],
                    "dept": "CPSC",
                    "notes": "Any CPSC 2000+ course, or CRIM-2520, POSC-3310, POSC-3250",
                },
            ],
        },
        "2023-24": {
            "name": "Cybersecurity Major",
            "total_credits": 56,
            "required": [
                "CPSC-2020",
                "CPSC-2080",
                "CPSC-2180",
                "CPSC-2300",
                "MATH-2120",
                "MATH-2200",
                "POSC-2030",
                "POSC-2200",
                "POSC-2400",
                "POSC-2420",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4080",
                "CPSC-4480",
                "POSC-3370",
                "PHIL-3250",
            ],
            "choose_one": [
                {"name": "Homeland Security", "choose_from": ["POSC-3350", "CRIM-3350"]},
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Cybersecurity Major",
            "total_credits": 64,
            "required": [
                "CPSC-1080",
                "CPSC-2020",
                "CPSC-2080",
                "CPSC-2300",
                "MATH-2120",
                "MATH-2200",
                "POSC-2030",
                "POSC-2200",
                "POSC-2400",
                "POSC-2420",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4080",
                "CPSC-4480",
                "POSC-3370",
                "PHIL-3250",
            ],
        },
    },
    "cybersecurity_minor": {
        "2022-23": {
            "name": "Cybersecurity Minor",
            "total_credits": 16,
            "required": [
                "CPSC-2080",
                "POSC-2030",
                "CPSC-2180",
                "CPSC-2300",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4480",
                "POSC-2200",
                "POSC-3350",
            ],
        },
        "2023-24": {
            "name": "Cybersecurity Minor",
            "total_credits": 16,
            "required": [
                "CPSC-2020",
                "CPSC-2080",
                "POSC-2020",
                "CPSC-2180",
                "CPSC-2300",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4480",
                "POSC-2200",
                "POSC-3350",
            ],
        },
        "2025-26": {
            "name": "Cybersecurity Minor",
            "total_credits": 16,
            "required": [
                "CPSC-2020",
                "CPSC-2080",
                "POSC-2020",
                "CPSC-2300",
                "CPSC-3380",
                "CPSC-3410",
                "CPSC-4480",
                "POSC-2200",
                "POSC-3350",
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# EXERCISE SCIENCE
# ─────────────────────────────────────────────────────────────────────────
EXERCISE_SCIENCE = {
    "exercise_science": {
        "2022-23": {
            "name": "Exercise Science",
            "total_credits": 70,
            "required": [
                "BIOL-2410",
                "BIOL-2420",
                "EXSC-1360",
                "EXSC-2455",
                "EXSC-2580",
                "EXSC-3470",
                "EXSC-3480",
                "EXSC-3520",
                "EXSC-3530",
                "EXSC-4150",
                "EXSC-4800",
                "EXSC-4910",
                "EXSC-4920",
                "PEHS-1550",
                "PSYC-2000",
            ],
            "chemistry_choose": {
                "credits": 4,
                "choose_from": ["CHEM-1000", "CHEM-2110"],
                "label": "Chemistry (CHEM-1000 or 2110)",
            },
            "concentrations": {
                "Clinical Exercise Physiology": {
                    "required": [
                        "EXSC-4050",   # EKG and Cardiovascular Disease, 3 cr
                        "EXSC-4160",   # Clinical Experience in Exercise Testing and Prescription, 1 cr
                    ],
                    "elective_groups": [
                        {
                            "label": "Clinical Electives (10 cr from list)",
                            "credits": 10,
                            "courses": [
                                "BIOL-2010",   # Medical Terminology, 2 cr
                                "EXSC-4010",   # Advanced Resistance Training and Conditioning, 3 cr
                                "EXSC-2440",   # Stress Management, 3 cr
                                "PSYC-3450",   # Health Psychology, 4 cr
                                "EXSC-2550",   # Health, Exercise, and Aging, 2 cr
                                "EXSC-3300",   # Health Implications of Obesity, 3 cr
                            ],
                        }
                    ],
                },
                "Pre-Health": {
                    "elective_groups": [
                        {
                            "label": "Pre-Health Electives (14 cr from list)",
                            "credits": 14,
                            "courses": [
                                "BIOL-2010",   # Medical Terminology, 2 cr
                                "BIOL-2210",   # Foundations of Modern Biology I, 4 cr
                                "BIOL-2220",   # Foundations of Modern Biology II, 4 cr
                                "CHEM-2120",   # General Chemistry II, 4 cr
                                "MATH-2120",   # Introduction to Statistics with Application, 4 cr
                                "PHYS-2140",   # General Physics I, 4 cr
                                "PHYS-2150",   # General Physics II, 4 cr
                                "PSYC-2510",   # Developmental Psychology, 4 cr
                                "PSYC-3120",   # Abnormal Psychology, 4 cr
                                "PSYC-3450",   # Health Psychology, 4 cr
                                "SOCI-2010",   # Intro to Sociology, 3 cr
                            ],
                        }
                    ],
                },
                "Sports Performance": {
                    "required": [
                        "ATRG-1530",   # Theory of Conditioning, 3 cr
                        "EXSC-4010",   # Advanced Resistance Training and Conditioning, 3 cr
                    ],
                    "elective_groups": [
                        {
                            "label": "Sports Performance Electives (8 cr from list)",
                            "credits": 8,
                            "courses": [
                                "BIOL-2010",   # Medical Terminology, 2 cr
                                "BIOL-2040",   # Personal and Community Health, 3 cr
                                "EXSC-2440",   # Stress Management, 3 cr
                                "EXSC-2550",   # Health, Exercise, and Aging, 2 cr
                                "PETE-2250",   # Motor Behavior, 3 cr
                                "SPRL-3150",   # Recreational Leadership, 2 cr
                                "SPRL-3250",   # Legal Aspects of Sport and Recreation, 3 cr
                                "SPRL-3300",   # Management of Sport Facilities and Events, 3 cr
                            ],
                        }
                    ],
                },
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Exercise Science",
            "total_credits": 70,
            "required": [
                "BIOL-2410",
                "BIOL-2420",
                "EXSC-1360",
                "EXSC-1530",
                "EXSC-2455",
                "EXSC-2580",
                "EXSC-3470",
                "EXSC-3480",
                "EXSC-3520",
                "EXSC-3530",
                "EXSC-4150",
                "EXSC-4800",
                "EXSC-4910",
                "EXSC-4920",
                "PEHS-1550",
                "PSYC-2000",
            ],
            "chemistry_choose": {
                "credits": 4,
                "choose_from": ["CHEM-1000", "CHEM-2110"],
                "label": "Chemistry (CHEM-1000 or 2110)",
            },
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "nutrition_minor": {
        "all_years": {
            "name": "Nutrition Minor",
            "total_credits": 16,
            "required": [
                "EXSC-2140",
                "EXSC-2580",
                "EXSC-3100",
                "EXSC-3200",
                "EXSC-3300",
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# EDUCATION
# ─────────────────────────────────────────────────────────────────────────
EDUCATION = {
    "elementary_education": {
        "2022-23": {
            "name": "Elementary Education",
            "total_credits": 83,
            "required": [
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
                "EDUC-4850",
                "EDUC-4910",
                "EDUC-4010",
                "EDUC-4930",
                "SPED-2400",
                "SPED-3120",
                "SPED-3200",
                "MUED-2110",
                "HIST-2000",
                "MATH-1110",
                "PETE-3710",
                "PHYS-1030",
                "BIOL-1000",
                "ENGL-3590",
                "HIST-2110",
                "MATH-1100",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Elementary Education",
            "total_credits": 83,
            "required": [
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
                "EDUC-4850",
                "EDUC-4910",
                "EDUC-4010",
                "EDUC-4930",
                "SPED-2400",
                "SPED-3120",
                "SPED-3200",
                "MUED-2110",
                "CPSC-1030",
                "HIST-2000",
                "MATH-1110",
                "PETE-3710",
                "PHYS-1030",
                "BIOL-1000",
                "ENGL-3590",
                "HIST-2110",
                "MATH-1100",
            ],
        },
        "2025-26": {
            "name": "Elementary Education",
            "total_credits": 102,
            "required": [
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
                "EDUC-4850",
                "EDUC-4910",
                "EDUC-4010",
                "EDUC-4930",
                "SPED-2400",
                "SPED-3120",
                "SPED-3200",
                "MUED-2110",
                "MATH-1100",
                "BIOL-1000",
                "PHYS-1020",
            ],
        },
    },
    "language_arts_teaching": {
        "2022-23": {
            "name": "Language Arts Teaching",
            "total_credits": 44,
            "required": [
                "ENGL-2220",
                "ENGL-2400",
                "ENGL-3000",
                "ENGL-3050",
                "ENGL-3580",
                "ENGL-3590",
                "ENGL-4700",
                "COMM-2200",
                "COMM-4750",
                "PSYC-2100",
            ],
            "choose_one": [
                {"name": "Grammar", "choose_from": ["ENGL-3110", "ENGL-3120"]},
                {"name": "Composition", "choose_from": ["ENGL-3180", "ENGL-3190"]},
            ],
            "dist_groups": [
                {
                    "name": "British Literature",
                    "credits": 6,
                    "choose_from": ["ENGL-3320", "ENGL-3540", "ENGL-3560"],
                },
                {"name": "American Literature", "credits": 3, "choose_from": ["ENGL-3570"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "math_teaching_ba": {
        "2022-23": {
            "name": "Mathematics Teaching (BA)",
            "total_credits": 40,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-2200",
                "MATH-2300",
                "MATH-3010",
                "MATH-3020",
                "MATH-4000",
                "MATH-4100",
                "MATH-4200",
                "MATH-4700",
            ],
            "choose_one": [
                {"name": "Stats/Calculus", "choose_from": ["MATH-2120", "MATH-4010"]},
            ],
            "elective_groups": [
                {
                    "name": "Upper Math elective",
                    "credits": 3,
                    "choose_from": ["MATH-3100", "MATH-3200", "MATH-3300", "MATH-3400"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Mathematics Teaching (BA)",
            "total_credits": 44,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-2200",
                "MATH-2300",
                "MATH-3010",
                "MATH-3020",
                "MATH-4000",
                "MATH-4100",
                "MATH-4200",
                "MATH-4700",
            ],
            "choose_one": [
                {"name": "Stats/Calculus", "choose_from": ["MATH-2120", "MATH-4010"]},
            ],
        },
    },
    "social_studies_teaching": {
        "2022-23": {
            "name": "Social Studies Teaching",
            "total_credits": 94,
            # ── SSE Major Courses (51 cr) ─────────────────────────────────────
            "required": [
                # Major core
                "HIST-4700",
                "HIST-2000",   # Global History required
                "HIST-2110",   # US History I required
                "HIST-2120",   # US History II required
                # Government and Citizenship required
                "POSC-2020",
                "POSC-2100",
                "POSC-2580",
                # Education core (43 cr)
                "EDUC-2000",
                "EDUC-2100",
                "EDUC-2110",
                "EDUC-2460",
                "EDUC-2520",
                "EDUC-2860",
                "EDUC-3000",
                "EDUC-3100",
                "EDUC-3120",
                "EDUC-4010",
                "EDUC-4710",
                "EDUC-4930",
                "SPED-2400",
                "ENGL-3590",
            ],
            "dist_groups": [
                {
                    "name": "European History survey (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["HIST-2030", "HIST-2040"],
                },
                {
                    "name": "European History upper-div (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": [
                        "HIST-3010", "HIST-3100", "HIST-3110", "HIST-3130",
                        "HIST-3135", "HIST-3150", "HIST-3190", "HIST-3220", "HIST-3240",
                    ],
                },
                {
                    "name": "Global History upper-div (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": [
                        "HIST-3260", "HIST-3280", "HIST-3300",
                        "HIST-3320", "HIST-3360", "HIST-3370",
                    ],
                },
                {
                    "name": "Additional European or Global History 3000-level (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": [
                        "HIST-3010", "HIST-3100", "HIST-3110", "HIST-3130",
                        "HIST-3135", "HIST-3150", "HIST-3190", "HIST-3220", "HIST-3240",
                        "HIST-3260", "HIST-3280", "HIST-3300",
                        "HIST-3320", "HIST-3360", "HIST-3370",
                    ],
                },
                {
                    "name": "US History upper-div (choose 2)",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": [
                        "HIST-3420", "HIST-3425", "HIST-3440",
                        "HIST-3451", "HIST-3452", "HIST-3455", "HIST-3470",
                        "HIST-3510", "HIST-3540", "HIST-4030",
                    ],
                },
                {
                    "name": "Government and Citizenship elective (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["POSC-2120", "POSC-3010"],
                },
                {
                    "name": "Third Field: Economics (choose if declared)",
                    "credits": 9,
                    "min_courses": 3,
                    "choose_from": [
                        "ECON-2010", "ECON-2020", "ECON-3210", "ECON-3410",
                    ],
                },
                {
                    "name": "Third Field: Psychology (choose if declared)",
                    "credits": 11,
                    "min_courses": 3,
                    "choose_from": [
                        "PSYC-2000", "PSYC-2510", "PSYC-3010", "PSYC-3120", "PSYC-4140",
                    ],
                },
                {
                    "name": "Third Field: Sociology (choose if declared)",
                    "credits": 9,
                    "min_courses": 3,
                    "choose_from": [
                        "SOCI-2010", "SOCI-2020", "SOCI-2120", "SOCI-2200",
                        "SOCI-3400", "SOCI-4020",
                    ],
                },
                {
                    "name": "Third Field: Special Education (choose if declared)",
                    "credits": 15,
                    "min_courses": 5,
                    "choose_from": [
                        "SPED-2400", "SPED-2500", "SPED-3000", "SPED-3120", "SPED-3500",
                    ],
                },
            ],
            "notes": "51 SSE cr + 43 Education cr = 94 total. Third field: choose ONE of Economics (9 cr), Psychology (11 cr), Sociology (9 cr), or Special Education (15 cr). HIST-3455 accepted as equivalent to HIST-3451/3452.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Social Studies Teaching",
            "total_credits": 51,
            "required": [
                "HIST-4700",
                "ECON-2010",
                "PSYC-2000",
                "SOCI-2010",
            ],
            "dist_groups": [
                {
                    "name": "World History",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": ["HIST-2110", "HIST-2120"],
                },
                {
                    "name": "US History",
                    "credits": 12,
                    "min_courses": 4,
                    "choose_from": [
                        "HIST-2030",
                        "HIST-2040",
                        "HIST-3420",
                        "HIST-3425",
                        "HIST-3440",
                        "HIST-3451",
                        "HIST-3452",
                        "HIST-3470",
                        "HIST-3510",
                        "HIST-3540",
                        "HIST-4030",
                    ],
                },
                {
                    "name": "Political Science",
                    "credits": 9,
                    "min_courses": 3,
                    "choose_from": ["POSC-2020", "POSC-2100", "POSC-2580"],
                },
            ],
        },
    },
    "spanish_education": {
        "2022-23": {
            "name": "Spanish Education",
            "total_credits": 91,
            "required": [
                "SPAN-2020",
                "SPAN-3010",
                "SPAN-3020",
                "SPAN-3140",
                "SPAN-3200",
                "SPAN-3400",
                "SPAN-3440",
                "MLAN-3500",
                "MLAN-4700",
                "MLAN-4900",
                "EDUC-2000",
                "EDUC-2100",
                "EDUC-2110",
                "EDUC-2460",
                "EDUC-2520",
                "EDUC-2860",
                "EDUC-3000",
                "EDUC-3100",
                "EDUC-3120",
                "EDUC-4010",
                "EDUC-4930",
                "SPED-2400",
            ],
            "choose_one": [
                {"name": "Student Teaching Placement", "choose_from": ["EDUC-4710", "EDUC-4120"]},
            ],
            "notes": "35 SPAN hrs beyond 2010 required; 7 hrs via MLAN-3500, 4700, 4900",
        },
    },
    "dyslexia_program": {
        "2022-23": {
            "name": "Dyslexia Program",
            "total_credits": 15,
            "required": [
                "EDUC-2200",
                "EDUC-2730",
                "EDUC-3300",
                "EDUC-4850",
                "EDUC-4910",
                "SPED-3120",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# HISTORY & POLITICAL SCIENCE
# ─────────────────────────────────────────────────────────────────────────
HISTORY_POLS = {
    "history": {
        "2022-23": {
            "name": "History",
            "total_credits": 36,
            "required_foundational": ["HIST-2000", "HIST-2300", "HIST-2350"],
            "required_capstone": ["HIST-4930", "HIST-4800"],
            "foundational_west_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2030", "HIST-2040"],
            },
            "foundational_us_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2110", "HIST-2120"],
            },
            "american_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3420",
                    "HIST-3425",
                    "HIST-3440",
                    "HIST-3451",
                    "HIST-3452",
                    "HIST-3470",
                    "HIST-3510",
                    "HIST-3520",
                    "HIST-3540",
                    "HIST-3560",
                    "HIST-4030",
                ],
            },
            "european_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3100",
                    "HIST-3135",
                    "HIST-3150",
                    "HIST-3190",
                    "HIST-3220",
                    "HIST-3280",
                ],
            },
            "world_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3240",
                    "HIST-3250",
                    "HIST-3260",
                    "HIST-3300",
                    "HIST-3360",
                    "HIST-3370",
                ],
            },
            "notes": "HIST-4700 does not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "History",
            "total_credits": 36,
            "required_foundational": ["HIST-2000", "HIST-2300", "HIST-2350"],
            "required_capstone": ["HIST-4930", "HIST-4800"],
            "foundational_west_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2030", "HIST-2040"],
            },
            "foundational_us_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2110", "HIST-2120"],
            },
            "american_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3420",
                    "HIST-3425",
                    "HIST-3440",
                    "HIST-3451",
                    "HIST-3452",
                    "HIST-3470",
                    "HIST-3510",
                    "HIST-3520",
                    "HIST-3540",
                    "HIST-3560",
                    "HIST-4030",
                ],
            },
            "european_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3100",
                    "HIST-3135",
                    "HIST-3150",
                    "HIST-3190",
                    "HIST-3220",
                    "HIST-3280",
                ],
            },
            "world_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3240",
                    "HIST-3250",
                    "HIST-3260",
                    "HIST-3300",
                    "HIST-3360",
                    "HIST-3370",
                ],
            },
        },
    },
    "history_minor": {
        "2022-23": {
            "name": "History Minor",
            "total_credits": 15,
            "required": ["HIST-2000"],
            "elective_groups": [
                {
                    "name": "History electives",
                    "credits": 15,
                    "dept": "HIST",
                    "notes": "HIST-4700 does not apply toward the minor",
                },
            ],
            "notes": "HIST-4700 does not apply.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "History Minor",
            "total_credits": 15,
            "required": ["HIST-3000"],
            "elective_groups": [
                {
                    "name": "History electives",
                    "credits": 12,
                    "dept": "HIST",
                    "notes": "HIST-4700 does not apply toward the minor",
                },
            ],
        },
    },
    "public_history": {
        "2022-23": {
            "name": "Public History",
            "total_credits": 60,
            # ── History Major (36 cr) ────────────────────────────────────────
            "required_foundational": ["HIST-2000", "HIST-2300", "HIST-2350"],
            "required_capstone": ["HIST-4930", "HIST-4800"],
            "foundational_west_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2030", "HIST-2040"],
            },
            "foundational_us_choose": {
                "credits": 3,
                "min_courses": 1,
                "choose_from": ["HIST-2110", "HIST-2120"],
            },
            "american_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3420", "HIST-3425", "HIST-3440", "HIST-3451",
                    "HIST-3452", "HIST-3470", "HIST-3510", "HIST-3520",
                    "HIST-3540", "HIST-3560", "HIST-4030",
                ],
            },
            "european_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3100", "HIST-3135", "HIST-3150",
                    "HIST-3190", "HIST-3220", "HIST-3280",
                ],
            },
            "world_hist_choose": {
                "credits": 6,
                "min_courses": 2,
                "choose_from": [
                    "HIST-3240", "HIST-3250", "HIST-3260",
                    "HIST-3300", "HIST-3360", "HIST-3370",
                ],
            },
            # ── Public History Core (24 cr) ──────────────────────────────────
            "required": [
                "COMM-2240",
                "ARTH-2000",
                "ARTS-1250",
                "HIST-3480",
                "HIST-3490",
            ],
            "dist_groups": [
                {
                    "name": "Professional Skills (choose 2)",
                    "credits": 5,
                    "min_courses": 2,
                    "choose_from": ["BSNS-2710", "BSNS-2810", "COMM-3250"],
                },
                {
                    "name": "Media/Communications (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["COMM-3370", "BSNS-4400"],
                },
            ],
            "notes": "Includes full History major (36 cr) plus public history core (24 cr). HIST-4700 does not apply toward the major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Public History",
            "total_credits": 59,
            "required": [
                "ARTH-3040",
                "COMM-2200",
                "COMM-2240",
                "HIST-3480",
            ],
        },
    },
    "political_science": {
        "2022-23": {
            "name": "Political Science",
            "total_credits": 36,
            "required": [
                "POSC-2020",
                "POSC-2100",
                "POSC-2200",
                "POSC-2400",
                "MATH-2120",
                "POSC-4930",
            ],
            "dist_groups": [
                {
                    "name": "American Politics",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": ["POSC-3140", "POSC-3211", "POSC-3212"],
                },
                {
                    "name": "International/Comparative",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": ["POSC-3300", "POSC-3400", "POSC-3510"],
                },
            ],
            "elective_groups": [
                {
                    "name": "Political Science Electives",
                    "credits": 7,
                    "dept": "POSC",
                    "notes": "7 cr from POSC courses; at least 6 cr must be upper-division (3000+). No more than 5 cr from POSC-2810, 4800, 4810, 4820.",
                },
            ],
            "notes": "No more than 5 hrs from POSC-2810, 4800, 4810, 4820 may apply toward major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "polsci_philosophy_economics": {
        "2022-23": {
            "name": "Political Science, Philosophy & Economics",
            "total_credits": 54,
            "required": [
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
                "PHIL-3250",
                "POSC-4930",
            ],
            "choose_one": [
                {
                    "name": "Political Theory",
                    "choose_from": ["PHIL-3010", "POSC-3010", "HIST-3010"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "international_relations": {
        "2022-23": {
            "name": "International Relations",
            "total_credits": 42,
            "required": [
                "POSC-2020",
                "POSC-2200",
                "POSC-2400",
                "POSC-2580",
                "MATH-2120",
                "POSC-3300",
                "POSC-3400",
                "POSC-3510",
                "POSC-2840",
                "POSC-4820",
                "POSC-4930",
                "ECON-3210",
                "HIST-3190",
                "HIST-3220",
                "HIST-3240",
                "HIST-3250",
                "HIST-3260",
                "HIST-3300",
                "HIST-3360",
                "HIST-3370",
                "HIST-3520",
            ],
            "choose_one": [
                {
                    "name": "Comparative Politics",
                    "choose_from": [
                        "POSC-3310",
                        "POSC-3320",
                        "POSC-3330",
                        "POSC-3360",
                        "POSC-3450",
                    ],
                },
            ],
            "elective_groups": [
                {
                    "name": "Foreign language",
                    "credits": 3,
                    "choose_from": ["SPAN-2010"],
                    "notes": "SPAN-2010 or above",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "national_security": {
        "2022-23": {
            "name": "National Security",
            "total_credits": 44,
            # Foundational (16 cr) + Ethics (3 cr) + Capstone (1 cr) = 20 required cr
            "required": [
                "POSC-2030",   # Intro to National Security Studies (3 cr)
                "POSC-2100",   # American National Government (3 cr) [W3]
                "POSC-2200",   # Public Policy (3 cr)
                "POSC-2400",   # Political Science Research Methods (3 cr) [WI]
                "MATH-2120",   # Introductory Statistics with Applications (4 cr) [F5]
                "PHIL-3250",   # Ethics and Morality for Professionals (3 cr) [W1]
                "POSC-4930",   # Senior Seminar (1 cr)
            ],
            # National Security Policy Courses: choose 3 of 4 (9 cr)
            # National Security Electives: choose 5 courses (15 cr)
            "dist_groups": [
                {
                    "name": "National Security Policy Courses",
                    "credits": 9,
                    "choose_from": [
                        "POSC-3300",   # International Security (3 cr)
                        "POSC-3310",   # Political Violence and Terrorism (3 cr) [WI]
                        "POSC-3350",   # Homeland Security (3 cr)
                        "CRIM-3350",   # Homeland Security (cross-listed)
                        "POSC-3370",   # Intelligence and Security Studies (3 cr) [SI]
                    ],
                    "notes": "Choose 3 courses (9 cr) from POSC-3300, POSC-3310, POSC/CRIM-3350, POSC-3370",
                },
                {
                    "name": "National Security Electives",
                    "credits": 15,
                    "choose_from": [
                        "CRIM-2510",   # The Nature of Crime and Social Deviance (4 cr)
                        "SOCI-2510",   # The Nature of Crime and Social Deviance (cross-listed)
                        "CRIM-2520",   # Introduction to Criminal Justice (3 cr)
                        "CRIM-3050",   # Drugs and American Society (3 cr)
                        "HIST-3220",   # The Age of World Wars, 1900-1950 (3 cr)
                        "HIST-3240",   # History of Russia and the Soviet Union (3 cr) [W7]
                        "HIST-3250",   # History of the Cold War (3 cr) [W7]
                        "HIST-3300",   # Middle East (3 cr) [W7, WI]
                        "HIST-3360",   # History of Modern Asia (3 cr) [W7]
                        "HIST-3370",   # General History of Latin America (3 cr) [W7]
                        "HIST-3510",   # Law, the Constitution and War in American History (3 cr) [WI]
                        "HIST-3520",   # History of the Vietnam War (3 cr)
                        "POSC-3212",   # The Presidency (3 cr) [SI]
                        "POSC-3250",   # Constitutional Law (3 cr)
                        "POSC-3300",   # International Security (3 cr) [also Policy]
                        "POSC-3310",   # Political Violence and Terrorism (3 cr) [also Policy]
                        "POSC-3330",   # American Foreign Policy (3 cr)
                        "POSC-3350",   # Homeland Security (3 cr) [also Policy]
                        "CRIM-3350",   # Homeland Security (cross-listed)
                        "POSC-3360",   # War, Peace, and Security (3 cr)
                        "POSC-3370",   # Intelligence and Security Studies (3 cr) [also Policy]
                        "PSYC-3010",   # Social Psychology (4 cr)
                        "SOCI-3010",   # Social Psychology (cross-listed)
                    ],
                    "notes": "Choose 5 courses (15 cr) from approved National Security elective list",
                },
            ],
        },
        "2023-24": {
            "name": "National Security",
            "total_credits": 44,
            # Same structure as 2022-23 but POSC-2020 replaces POSC-2030
            "required": [
                "POSC-2020",   # Introduction to World Politics (3 cr) [replaces POSC-2030 in 23-24]
                "POSC-2100",   # American National Government (3 cr) [W3]
                "POSC-2200",   # Public Policy (3 cr)
                "POSC-2400",   # Political Science Research Methods (3 cr) [WI]
                "MATH-2120",   # Introductory Statistics with Applications (4 cr) [F5]
                "PHIL-3250",   # Ethics and Morality for Professionals (3 cr) [W1]
                "POSC-4930",   # Senior Seminar (1 cr)
            ],
            "dist_groups": [
                {
                    "name": "National Security Policy Courses",
                    "credits": 9,
                    "choose_from": [
                        "POSC-3300", "POSC-3310", "POSC-3350", "CRIM-3350", "POSC-3370",
                    ],
                    "notes": "Choose 3 courses (9 cr) from POSC-3300, POSC-3310, POSC/CRIM-3350, POSC-3370",
                },
                {
                    "name": "National Security Electives",
                    "credits": 15,
                    "choose_from": [
                        "CRIM-2510", "SOCI-2510", "CRIM-2520", "CRIM-3050",
                        "HIST-3220", "HIST-3240", "HIST-3250", "HIST-3300",
                        "HIST-3360", "HIST-3370", "HIST-3510", "HIST-3520",
                        "POSC-3212", "POSC-3250", "POSC-3300", "POSC-3310",
                        "POSC-3330", "POSC-3350", "CRIM-3350", "POSC-3360",
                        "POSC-3370", "PSYC-3010", "SOCI-3010",
                    ],
                    "notes": "Choose 5 courses (15 cr) from approved National Security elective list",
                },
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# PSYCHOLOGY / SOCIAL SCIENCES
# ─────────────────────────────────────────────────────────────────────────
SOCIAL_SCIENCES = {
    "psychology": {
        "2022-23": {
            "name": "Psychology",
            "total_credits": 30,
            "required": [
                "PSYC-2000",
                "PSYC-2010",
                "PSYC-4900",
            ],
            "elective_groups": [
                {
                    "name": "Psychology electives",
                    "credits": 12,
                    "dept": "PSYC",
                    "min_level": 3000,
                    "notes": "At least 12 hrs from PSYC-3010, 3030, 3040, 3060, 3100, "
                    "3120, 3200, 3210, 3240, 3330, 3400, 3450, 4030, 4100, 4110, "
                    "4140, 4150, 4510, 4520, 4650; SOCI-3050, 3140, 3150",
                },
            ],
            "notes": "PSYC-4900 does NOT count toward the 15 elective hours.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "psychology_complementary": {
        "2022-23": {
            "name": "Psychology Complementary Major",
            "total_credits": 26,
            "required": ["PSYC-2000", "PSYC-2010", "PSYC-4900"],
            "elective_groups": [
                {"name": "Psychology electives", "credits": 12, "dept": "PSYC", "min_level": 3000},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "psychology_minor": {
        "all_years": {
            "name": "Psychology Minor",
            "total_credits": 16,
            "required": ["PSYC-2000"],
            "elective_groups": [
                {"name": "Psychology electives", "credits": 12, "dept": "PSYC"},
            ],
        },
    },
    "social_work": {
        "2022-23": {
            "name": "Social Work",
            "total_credits": 64,
            "required": [
                "SOCI-2010",
                "SOCI-2020",
                "SOWK-2000",
                "SOWK-2100",
                "BIOL-2040",
                "POSC-2100",
                "PSYC-2000",
                "PSYC-2440",
                "SOCI-3100",
                "SOCI-3400",
                "SOWK-2200",
                "SOWK-3100",
                "SOWK-4710",
                "SOWK-4720",
                "SOWK-4730",
                "SOWK-4850",
                "SOCI-3700",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Social Work",
            "total_credits": 64,
            "required": [
                "SOCI-2010",
                "SOWK-2000",
                "SOWK-2100",
                "BIOL-2040",
                "PSYC-2000",
                "PSYC-2440",
                "SOCI-3100",
                "SOCI-3400",
                "SOWK-2200",
                "SOWK-3100",
                "SOWK-4710",
                "SOWK-4720",
                "SOWK-4730",
                "SOWK-4850",
                "SOCI-3700",
            ],
        },
    },
    "family_science_major": {
        "2022-23": {
            "name": "Family Science",
            "total_credits": 48,
            "required": [
                "SOCI-2100",
                "SOCI-3100",
                "SOCI-3140",
                "SOCI-3210",
                "SOCI-3700",
                "SOCI-3850",
                "SOCI-4350",
                "SOCI-4820",
                "SOCI-4910",
                "SOCI-4950",
                "BSNS-3150",
                "PSYC-2000",
                "PSYC-2100",
                "PSYC-2510",
                "SOWK-3200",
            ],
        },
    },
    "criminal_justice_major": {
        "2022-23": {
            "name": "Criminal Justice",
            "total_credits": 120,
            "required": [
                "CRIM-2510",
                "CRIM-2520",
                "CRIM-3110",
                "CRIM-4900",
                "SOCI-3700",
            ],
            "choose_one": [
                {"name": "Sociology", "choose_from": ["SOCI-2010", "SOCI-2020"]},
            ],
            "elective_groups": [
                {
                    "name": "CRIM internship",
                    "credits": 4,
                    "choose_from": ["CRIM-4810"],
                    "notes": "4 hrs from CRIM-4810",
                },
                {
                    "name": "CRIM electives",
                    "credits": 9,
                    "dept": "CRIM",
                    "notes": "9 hrs from additional CRIM courses",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "criminal_justice_major_online": {
        "2022-23": {
            "name": "Criminal Justice (Online)",
            "total_credits": 120,
            "required": [
                "CRIM-2510",
                "CRIM-2520",
                "CRIM-3110",
                "CRIM-4900",
                "SOCI-3700",
            ],
            "choose_one": [
                {"name": "Sociology", "choose_from": ["SOCI-2010", "SOCI-2020"]},
            ],
            "elective_groups": [
                {
                    "name": "CRIM internship",
                    "credits": 4,
                    "choose_from": ["CRIM-4810"],
                    "notes": "4 hrs from CRIM-4810 (professional experience counts)",
                },
                {
                    "name": "CRIM electives",
                    "credits": 9,
                    "dept": "CRIM",
                    "notes": "9 hrs from additional CRIM courses",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "criminal_justice_minor": {
        "2022-23": {
            "name": "Criminal Justice Minor",
            "total_credits": 17,
            "required": [
                "CRIM-2510",
                "CRIM-2520",
                "CRIM-3110",
                "CRIM-4900",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# CHRISTIAN MINISTRIES / THEOLOGY
# ─────────────────────────────────────────────────────────────────────────
MINISTRY = {
    "christian_ministries": {
        "2022-23": {
            "name": "Christian Ministries",
            "total_credits": 46,
            "required": [
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
            ],
            # CMIN-4810 is the only catalog-listed internship course; CMIN-4850 not in 2022-23 catalog
            "elective_groups": [
                {
                    "name": "Departmental elective",
                    "credits": 3,
                    "dept_options": ["BIBL", "RLGN", "CMIN"],
                    "notes": "3 additional credit hours from BIBL, RLGN, or CMIN dept",
                },
            ],
            "notes": "24 hrs departmental core + 19 hrs ministry core + 3 hrs dept elective",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Christian Ministries",
            "total_credits": 46,
            "required": [
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
            ],
        },
    },
    "christian_ministries_complementary": {
        "2022-23": {
            "name": "Christian Ministries Complementary Major",
            "total_credits": 28,
            "required": [
                "BIBL-2000",
                "RLGN-2130",
                "RLGN-2150",
                "RLGN-3040",
                "RLGN-3060",
                "CMIN-2000",
            ],
            "elective_groups": [
                {
                    "name": "Ministry practice",
                    "credits": 1,
                    "choose_from": ["CMIN-2810", "CMIN-4810", "CMIN-3340"],
                },
                {
                    "name": "Ministry elective",
                    "credits": 3,
                    "choose_from": ["CMIN-3050", "CMIN-3080", "CMIN-3910"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "youth_ministries": {
        "2022-23": {
            "name": "Youth Ministries",
            "total_credits": 49,
            "required": [
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
                "CMIN-4250",
                "CMIN-4810",
                "CMIN-2260",
                "CMIN-3260",
            ],
            "elective_groups": [
                {
                    "name": "Ministry elective",
                    "credits": 3,
                    "choose_from": ["CMIN-3050", "CMIN-3080", "CMIN-3910"],
                },
                {
                    "name": "Family ministry",
                    "credits": 3,
                    "choose_from": ["CMIN-3230", "HIST-4030", "SOCI-2100"],
                },
                {
                    # 3 additional hours from any courses offered by the department
                    "name": "Dept elective (BIBL/RLGN/CMIN)",
                    "credits": 3,
                    "choose_from": [
                        "BIBL-3391", "BIBL-3392", "BIBL-3410", "BIBL-3420",
                        "BIBL-3430", "BIBL-3440", "BIBL-3450", "BIBL-3460",
                        "BIBL-4410", "BIBL-4420",
                        "RLGN-2410", "RLGN-2430", "RLGN-3010", "RLGN-3120",
                        "RLGN-3150", "RLGN-3200", "RLGN-3320", "RLGN-3420",
                        "RLGN-3430", "RLGN-4000", "RLGN-4100", "RLGN-4200",
                        "CMIN-2270", "CMIN-3100", "CMIN-3200", "CMIN-3300",
                        "CMIN-3400", "CMIN-3500", "CMIN-4000", "CMIN-4100",
                        "CMIN-4200", "CMIN-4300", "CMIN-4400", "CMIN-4500",
                        "CMIN-4850",
                    ],
                    "notes": "3 additional hours from any courses offered by the department (BIBL/RLGN/CMIN)",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Youth Ministries",
            "total_credits": 49,
            "required": [
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
                "CMIN-4250",
                "CMIN-4810",
                "CMIN-2260",
                "CMIN-3260",
            ],
        },
    },
    "ministry_studies": {
        "2022-23": {
            "name": "Ministry Studies",
            "total_credits": 34,
            "required": [
                "BIBL-2000",
                "CMIN-2000",
                "RLGN-1100",
                "CMIN-2810",
                "CMIN-4810",
                "RLGN-3040",
                "CMIN-4250",
            ],
            "elective_groups": [
                {
                    "name": "Biblical studies elective",
                    "credits": 3,
                    "choose_from": ["BIBL-2050", "BIBL-2150", "RLGN-2150"],
                },
                {
                    "name": "History of Christianity elective",
                    "credits": 3,
                    "choose_from": [
                        "HIST-3060",
                        "RLGN-3060",
                        "HIST-3420",
                        "RLGN-3420",
                        "RLGN-3300",
                    ],
                },
                {
                    "name": "Ethics elective",
                    "credits": 3,
                    "choose_from": ["RLGN-2130", "RLGN-3120"],
                },
                {
                    "name": "Ministry elective",
                    "credits": 3,
                    "choose_from": ["CMIN-2260", "CMIN-3260"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "bible_religion": {
        "2022-23": {
            "name": "Bible and Religion",
            "total_credits": 36,
            "required": [
                "BIBL-2000",
                "BIBL-2050",
                "RLGN-2000",
                "RLGN-2130",
                "RLGN-2150",
                "RLGN-3040",
                "RLGN-3060",
                "RLGN-3300",
                "RLGN-3320",
            ],
        },
    },
    "christian_spiritual_formation_complementary": {
        "2022-23": {
            "name": "Christian Spiritual Formation Complementary Major",
            "total_credits": 28,
            "required": ["RLGN-1100", "RLGN-4960"],
            "choose_one": [
                {"name": "Spiritual Formation survey", "choose_from": ["RLGN-2410", "RLGN-2430"]},
            ],
            "dist_groups": [
                {
                    "name": "Fine Arts/Formation",
                    "credits": 3,
                    "choose_from": [
                        "ENGL-2580",
                        "MUSC-3150",
                        "PACT-2400",
                        "PSYC-3500",
                        "SOCI-3500",
                        "PSYC-3200",
                    ],
                },
                {
                    "name": "Scripture",
                    "credits": 3,
                    "choose_from": ["BIBL-3000", "RLGN-3000", "BIBL-2150"],
                },
                {
                    "name": "Tradition",
                    "credits": 3,
                    "choose_from": ["HIST-3060", "RLGN-3060", "HIST-3540", "RLGN-2270"],
                },
                {
                    "name": "Reason",
                    "credits": 3,
                    "choose_from": ["RLGN-3250", "PHIL-3250", "PHIL-2000", "RLGN-3120"],
                },
                {
                    "name": "Experience",
                    "credits": 3,
                    "choose_from": ["RLGN-2310", "RLGN-3100", "RLGN-3530"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "christian_spiritual_formation_minor": {
        "2022-23": {
            "name": "Christian Spiritual Formation Minor",
            "total_credits": 15,
            "required": ["RLGN-1100", "RLGN-4960"],
            "choose_one": [
                {"name": "Spiritual Formation survey", "choose_from": ["RLGN-2410", "RLGN-2430"]},
            ],
            "dist_groups": [
                {
                    "name": "Scripture",
                    "credits": 3,
                    "choose_from": ["BIBL-3000", "RLGN-3000", "BIBL-2150"],
                },
                {
                    "name": "Tradition",
                    "credits": 3,
                    "choose_from": ["HIST-3060", "RLGN-3060", "HIST-3540", "RLGN-2270"],
                },
                {
                    "name": "Reason",
                    "credits": 3,
                    "choose_from": ["RLGN-3250", "PHIL-3250", "PHIL-2000", "RLGN-3120"],
                },
                {
                    "name": "Experience",
                    "credits": 3,
                    "choose_from": ["RLGN-2310", "RLGN-3100", "RLGN-3530"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "christian_ministries_minor": {
        "2022-23": {
            "name": "Christian Ministries Minor",
            "total_credits": 16,
            "required": ["CMIN-2000", "CMIN-2810"],
            "elective_groups": [
                {"name": "CMIN electives", "credits": 11, "dept": "CMIN"},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "biblical_studies_minor": {
        "2022-23": {
            "name": "Biblical Studies Minor",
            "total_credits": 15,
            "required": ["BIBL-2050", "RLGN-2150"],
            "elective_groups": [
                {"name": "BIBL electives", "credits": 9, "dept": "BIBL"},
            ],
            "notes": "BIBL-2110, 2120, 2210, 2220 may be applied.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "history_of_christianity_minor": {
        "2022-23": {
            "name": "History of Christianity Minor",
            "total_credits": 15,
            "required": ["RLGN-3060", "HIST-3060", "BIBL-3000", "RLGN-3000"],
            "elective_groups": [
                {
                    "name": "History of Christianity electives",
                    "credits": 9,
                    "choose_from": [
                        "RLGN-2250",
                        "RLGN-2270",
                        "RLGN-3135",
                        "HIST-3135",
                        "RLGN-3300",
                        "RLGN-3420",
                        "HIST-3420",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "religion_minor": {
        "all_years": {
            "name": "Religion Minor",
            "total_credits": 15,
            "required": ["RLGN-2000", "RLGN-3060", "RLGN-3320"],
            "elective_groups": [
                {"name": "RLGN electives", "credits": 6, "dept": "RLGN"},
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# ENGLISH / WRITING / LITERARY STUDIES
# ─────────────────────────────────────────────────────────────────────────
ENGLISH = {
    "literary_studies": {
        "2022-23": {
            "name": "Literary Studies",
            "total_credits": 35,
            "required": [
                "ENGL-2400",
                "ENGL-2220",
                "ENGL-3540",
                "ENGL-3560",
                "ENGL-3570",
                "ENGL-3580",
                "ENGL-3320",
                "ENGL-4910",
            ],
            "choose_one": [
                {"name": "Language/Linguistics", "choose_from": ["ENGL-3000", "ENGL-3050"]},
            ],
            "elective_groups": [
                {"name": "ENGL electives", "credits": 6, "dept": "ENGL", "min_level": 2000},
            ],
            "notes": "ENGL-1100, 1110, 1120, 1400, 4700 do not apply.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "literary_studies_minor": {
        "2022-23": {
            "name": "Literary Studies Minor",
            "total_credits": 15,
            "required": ["ENGL-2400"],
            "dist_groups": [
                {
                    "name": "British Literature",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": ["ENGL-3320", "ENGL-3540", "ENGL-3560"],
                },
                {
                    "name": "American Literature",
                    "credits": 6,
                    "min_courses": 2,
                    "choose_from": ["ENGL-3570", "ENGL-3580"],
                },
            ],
            "elective_groups": [
                {
                    "name": "Writing elective",
                    "credits": 3,
                    "choose_from": [
                        "ENGL-3110",
                        "ENGL-3120",
                        "ENGL-3140",
                        "ENGL-3160",
                        "ENGL-3180",
                        "ENGL-3190",
                    ],
                },
            ],
            "notes": "ENGL-1100, 1110, 1120, 1400, 4700 do not apply.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "writing": {
        "2022-23": {
            "name": "Writing",
            "total_credits": 35,
            "required": ["ENGL-4910"],
            "elective_groups": [
                {
                    # Section A: 18-25 cr from writing/editing/publishing courses
                    "name": "Writing courses",
                    "credits": 18,
                    "choose_from": [
                        "ENGL-2500",
                        "ENGL-2510",
                        "ENGL-2580",
                        "ENGL-3000",
                        "ENGL-3110",
                        "ENGL-3120",
                        "ENGL-3140",
                        "ENGL-3160",
                        "ENGL-3180",
                        "ENGL-3190",
                        "ENGL-3870",
                        "ENGL-3880",
                    ],
                },
                {
                    # Section B: 3-8 cr from any other ENGL 2000+ course (not in Section A)
                    "name": "ENGL elective (2000+)",
                    "credits": 3,
                    "choose_from": [
                        "ENGL-2220",
                        "ENGL-2400",
                        "ENGL-2550",
                        "ENGL-3050",
                        "ENGL-3320",
                        "ENGL-3420",
                        "ENGL-3500",
                        "ENGL-3520",
                        "ENGL-3530",
                        "ENGL-3540",
                        "ENGL-3560",
                        "ENGL-3570",
                        "ENGL-3580",
                        "ENGL-4800",
                        "ENGL-4850",
                    ],
                    "notes": "3-8 cr from any ENGL course 2000+ not listed in Section A",
                },
                {
                    # Section C: 1-3 cr Writing Internship (required)
                    "name": "Internship",
                    "credits": 1,
                    "choose_from": ["ENGL-4800"],
                    "notes": "1-3 hrs writing internship required; must be approved by dept chair",
                },
                {
                    # Section D: 3-4 cr design/tech
                    "name": "Design/digital elective",
                    "credits": 3,
                    "choose_from": [
                        "ARTS-2100",
                        "ARTS-1250",
                        "CPSC-1100",
                        "CPSC-1200",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Writing",
            "total_credits": 35,
            "required": [],
            "elective_groups": [
                {
                    "name": "Writing courses",
                    "credits": 18,
                    "choose_from": [
                        "ENGL-2500",
                        "ENGL-2510",
                        "ENGL-2580",
                        "ENGL-3000",
                        "ENGL-3110",
                        "ENGL-3120",
                        "ENGL-3140",
                        "ENGL-3160",
                        "ENGL-3180",
                        "ENGL-3190",
                        "ENGL-3870",
                        "ENGL-3880",
                    ],
                },
                {
                    "name": "Media/Comm elective",
                    "credits": 3,
                    "choose_from": ["COMM-3220", "COMM-3260"],
                },
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "writing_minor": {
        "2022-23": {
            "name": "Writing Minor",
            "total_credits": 15,
            "required": [
                "ENGL-2500",
                "ENGL-2510",
                "ENGL-2580",
                "ENGL-3000",
            ],
            "elective_groups": [
                {
                    "name": "Writing electives",
                    "credits": 6,
                    "choose_from": [
                        "ENGL-3110",
                        "ENGL-3120",
                        "ENGL-3140",
                        "ENGL-3160",
                        "ENGL-3180",
                        "ENGL-3190",
                        "ENGL-3870",
                    ],
                },
                {
                    "name": "Cross-discipline writing",
                    "credits": 3,
                    "choose_from": ["COMM-2130", "FREN-3240", "SPAN-3010", "MUBS-2070"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "english_studies_minor": {
        "2022-23": {
            "name": "English Studies Minor",
            "total_credits": 15,
            "required": ["ENGL-2220"],
            "dist_groups": [
                {
                    "name": "Literature",
                    "credits": 9,
                    "min_courses": 3,
                    "choose_from": [
                        "ENGL-2400",
                        "ENGL-2220",
                        "ENGL-3320",
                        "ENGL-3540",
                        "ENGL-3560",
                        "ENGL-3570",
                        "ENGL-3580",
                    ],
                },
                {
                    "name": "Language",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["ENGL-3000", "MLAN-2000", "ENGL-3050"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "songwriting": {
        "2022-23": {
            "name": "Songwriting",
            "total_credits": 44,
            "required": [
                "MUSC-1010",
                "MUSC-1030",
                "MUSC-2110",
                "MUPF-1050",
                "MUBS-2010",
                "MUBS-2020",
                "MUBS-2070",
                "MUBS-4500",
                "ENGL-2400",
                "ENGL-2500",
                "ENGL-3120",
            ],
            "elective_groups": [
                {"name": "MUPF performance", "credits": 2, "choose_from": ["MUPF-2900"]},
                {
                    "name": "Music Business electives",
                    "credits": 6,
                    "choose_from": [
                        "MUBS-3100",
                        "MUBS-3210",
                        "MUBS-3220",
                        "MUBS-3310",
                        "MUBS-4800",
                        "MUBS-4900",
                        "BSNS-3330",
                        "BSNS-3360",
                    ],
                },
                {
                    "name": "Literature electives",
                    "credits": 6,
                    "choose_from": [
                        "ENGL-2580",
                        "ENGL-3320",
                        "ENGL-3540",
                        "ENGL-3560",
                        "ENGL-3570",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# MUSIC
# ─────────────────────────────────────────────────────────────────────────
MUSIC = {
    "music_education_bmus": {
        "2022-23": {
            "name": "Music Education (BMus)",
            "total_credits": 101,
            "required": [
                # Music Theory & Literature
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUSC-2010",
                "MUSC-2020",
                "MUSC-2030",
                "MUSC-2040",
                "MUSC-2110",
                "MUSC-2330",
                "MUSC-3030",
                "MUSC-3040",
                # Keyboard
                "MUPF-1050",
                "MUPF-1060",
                # Music Education Core
                "MUED-1000",
                "MUED-1100",
                "MUED-1200",
                "MUED-1300",
                "MUED-1400",
                "MUED-2470",
                "MUED-3100",
                "MUED-3110",
                "MUED-3120",
                "MUED-3130",
                "MUED-3470",
                "MUED-3480",
                "MUED-4700",
                # Secondary Education Requirements
                "EDUC-2100",
                "EDUC-2110",
                "EDUC-3120",
                "EDUC-4010",
                "SPED-2400",
            ],
            "choose_one": [
                {
                    "name": "Upper MUSC group",
                    "credits": 6,
                    "choose_from": ["MUSC-3110", "MUSC-3120", "MUSC-3130"],
                },
                {
                    "name": "Performance area (Piano)",
                    "credits": 2,
                    "choose_from": ["MUPF-1710", "MUPF-2030", "MUPF-2040"],
                },
                {
                    "name": "Pedagogy",
                    "credits": 2,
                    "choose_from": ["MUED-3330", "MUED-3350", "MUED-3370"],
                },
                {
                    # Singers need BOTH MUED-2510 AND MUED-2520;
                    # Instrumentalists need only MUED-3460.
                    # Engine models as choose-one to flag the slot; registrar
                    # must verify singers have completed both 2510 and 2520.
                    "name": "Singer/Instrumentalist track",
                    "credits": 2,
                    "choose_from": ["MUED-2510", "MUED-2520", "MUED-3460"],
                    "notes": "Singers require BOTH MUED-2510 and MUED-2520; Instrumentalists require only MUED-3460",
                },
                {"name": "Classroom Mgmt", "choose_from": ["EDUC-4120", "EDUC-4710"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "instrumental_performance_bmus": {
        "2022-23": {
            "name": "Instrumental Performance (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUSC-2010",
                "MUSC-2020",
                "MUSC-2030",
                "MUSC-2040",
                "MUSC-2110",
                "MUSC-2330",
                "MUSC-3040",
                "MUSC-3120",
                "MUSC-3130",
                "MUED-2470",
                "MUED-3480",
                "MUBS-3470",
            ],
            "elective_groups": [
                {
                    "name": "Performance hours",
                    "credits": 6,
                    "choose_from": [
                        "MUPF-1050",
                        "MUPF-1060",
                        "MUPF-1710",
                        "MUPF-2030",
                        "MUPF-2040",
                    ],
                },
                {
                    "name": "Upper MUSC/MUED",
                    "credits": 2,
                    "choose_from": ["MUSC-3030", "MUSC-3100", "MUSC-4900", "MUBS-2050"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "voice_performance_bmus": {
        "2022-23": {
            "name": "Voice Performance (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUSC-2010",
                "MUSC-2020",
                "MUSC-2030",
                "MUSC-2040",
                "MUSC-2110",
                "MUSC-2330",
                "MUSC-3120",
                "MUSC-3130",
                "MUED-2470",
                "MUBS-3470",
                "MUPF-4910",
                "MUED-2510",
                "MUED-2520",
                "MUED-3350",
                "MUSC-3390",
                "THEA-2110",
                "THEA-2120",
                "THEA-2210",
            ],
            "elective_groups": [
                {
                    "name": "Voice study",
                    "credits": 4,
                    "choose_from": [
                        "MUPF-1050",
                        "MUPF-1060",
                        "MUPF-1710",
                        "MUPF-2030",
                        "MUPF-2040",
                        "MUPF-2710",
                    ],
                },
                {
                    "name": "Secondary instrument",
                    "credits": 4,
                    "choose_from": ["MUPF-1150", "MUPF-1160", "MUPF-1170"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "musical_theatre_bmus": {
        "2022-23": {
            "name": "Musical Theatre (BMus)",
            "total_credits": 80,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUTR-2410",
                "MUTR-2420",
                "MUTR-3210",
                "MUTR-3220",
                "MUPF-4910",
                "THEA-2110",
                "THEA-2120",
                "THEA-2210",
                "THEA-3110",
            ],
            "elective_groups": [
                {"name": "Voice study", "credits": 6, "choose_from": ["MUPF-2700", "MUPF-4700"]},
                {
                    "name": "Piano study",
                    "credits": 2,
                    "choose_from": [
                        "MUPF-1050",
                        "MUPF-1060",
                        "MUPF-1710",
                        "MUPF-1720",
                        "MUPF-2030",
                    ],
                },
                {
                    "name": "Ballet",
                    "credits": 2,
                    "choose_from": ["DANC-1420", "DANC-2420", "DANC-3420"],
                },
                {
                    "name": "Jazz dance",
                    "credits": 1,
                    "choose_from": ["DANC-1320", "DANC-2320", "DANC-3320"],
                },
                {
                    "name": "Dance performance",
                    "credits": 2,
                    "choose_from": ["DANC-2110", "DANC-1120", "DANC-2120", "DANC-3120"],
                },
                {"name": "Vocal performance", "credits": 2, "choose_from": ["MUPF-1170"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "music_minor": {
        "all_years": {
            "name": "Music Minor",
            "total_credits": 18,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUSC-2110",
            ],
            "elective_groups": [
                {
                    "name": "Performance hours",
                    "credits": 4,
                    "choose_from": ["MUPF-1050", "MUPF-1060"],
                    "notes": "4 hrs from MUPF-1050, 1060 and/or private piano",
                },
            ],
        },
    },
    "worship_arts_ba": {
        "2022-23": {
            "name": "Worship Arts (BA)",
            "total_credits": 53,
            "required": [
                "MUSC-1010",
                "MUSC-1030",
                "MUSC-3150",
                "MUSC-3160",
                "MUSC-3800",
                "MUED-2470",
                "MUPF-1050",
                "MUPF-1410",
                "MUBS-2020",
                "MUBS-3450",
                "THEA-2350",
                "DANC-1580",
                "DANC-1590",
                "COMM-2140",
                "COMM-2200",
                "CMIN-2000",
                "CMIN-2270",
                "CMIN-3050",
                "RLGN-3040",
            ],
            "choose_one": [
                {
                    "name": "Religious History",
                    "choose_from": ["RLGN-2060", "HIST-2060", "RLGN-3420", "HIST-3420"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "music_ba": {
        "2022-23": {
            "name": "Music Business (BA)",
            "total_credits": 53,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUSC-2210",
                "MUBS-2010",
                "MUBS-2020",
                "MUPF-1050",
                "MUPF-1060",
                "BSNS-3320",
                "BSNS-3330",
                "CRIM-2520",
                "MUBS-3210",
                "MUBS-3550",
                "MUBS-4850",
                "MUBS-4870",
            ],
            "elective_groups": [
                {"name": "MUBS senior", "credits": 4, "choose_from": ["MUBS-4900"]},
                {"name": "MUBS business", "credits": 2, "choose_from": ["MUBS-4800"]},
                {"name": "Accounting/Business", "credits": 3, "choose_from": ["BSNS-4400"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# THEATRE / DANCE
# ─────────────────────────────────────────────────────────────────────────
THEATRE_DANCE = {
    "visual_communication_design": {
        "2022-23": {
            "name": "Visual Communication Design",
            "total_credits": 53,
            "required": [
                # Art History (9 cr)
                "ARTH-3010",   # Ancient to Medieval Art (3)
                "ARTH-3020",   # Renaissance to Modern Art (3)
                "ARTH-3030",   # Contemporary Art and Design (3; WI)
                # Art Foundation (12 cr)
                "ARTS-2010",   # Introduction to Drawing (3)
                "ARTS-2011",   # Two-Dimensional Design (3)
                "ARTS-2060",   # Illustration (3)
                "ARTS-2100",   # Intro to Graphic Design (3)
                # Design Core (9 cr)
                "ARTS-3110",   # Visual Design Studio I (3)
                "ARTS-3114",   # Visual Design Studio II (3)
                "ARTS-3310",   # Typography Studio (3)
                # Advanced Design (9 cr)
                "ARTS-4114",   # Design for Digital Media (3)
                "ARTS-4310",   # Design Thinking (3)
                "ARTS-4420",   # Design Methodology (3)
                # Capstone (8 cr)
                "ARTS-4820",   # Internship (2)
                "ARTS-4930",   # Comprehensive Projects I Preparation (2)
                "ARTS-4950",   # Comprehensive Projects II (4; SI)
            ],
            "dist_groups": [
                {
                    "name": "Special Topics / Motion Graphics (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["ARTS-4450", "COMM-3160"],
                },
                {
                    "name": "Branding / Social Media (choose 1)",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["BSNS-3550", "COMM-3370"],
                },
            ],
            "notes": "ARTH-3030 is WI; ARTS-4950 is SI. ARTS-4820 internship is 2 cr on advising sheet.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "theatre_ba": {
        "2022-23": {
            "name": "Theatre (BA)",
            "total_credits": 42,
            "required": [
                "THEA-2110",
                "THEA-2210",
                "THEA-2220",
                "THEA-2410",
                "THEA-3010",
                "THEA-3020",
                "THEA-3400",
                "THEA-3500",
                "THEA-3550",
                "THEA-4800",
            ],
            "elective_groups": [
                {"name": "Theatre practicum", "credits": 8, "choose_from": ["THEA-2890"]},
                {
                    "name": "Theatre/Performance electives",
                    "credits": 8,
                    "choose_from": [
                        "THEA-2120",
                        "THEA-2420",
                        "THEA-3110",
                        "THEA-3120",
                        "MUPF-1070",
                        "MUPF-2700",
                        "MUPF-4910",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "theatre_minor": {
        "all_years": {
            "name": "Theatre Minor",
            "total_credits": 17,
            "required": ["THEA-2350"],
            "dist_groups": [
                {
                    "name": "Theory/Criticism",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["THEA-3010", "THEA-3020", "THEA-4900"],
                },
                {
                    "name": "Design/Stagecraft",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["THEA-3500", "THEA-3550"],
                },
            ],
            "elective_groups": [
                {"name": "Theatre practicum", "credits": 2, "choose_from": ["THEA-2890"]},
            ],
        },
    },
    "dance_major": {
        "2022-23": {
            "name": "Dance",
            "total_credits": 54,
            # ── Shared required courses (22 credit hours, all tracks) ──────────
            "required": [
                "DANC-1580",   # Dance Improvisation I (1 cr)
                "DANC-1590",   # Dance Composition I (2 cr)
                "DANC-3000",   # Global Dance Forms (3 cr)
                "DANC-3020",   # Dance History II (3 cr)
                "DANC-4500",   # Dance Anatomy and Kinesiology (3 cr)
            ],
            # ── Nutrition/First Aid: either NURS-1210 or PEHS-1450 ────────────
            "choose_one": [
                {"name": "Nutrition / First Aid", "choose_from": ["NURS-1210", "PEHS-1450"]},
            ],
            # ── Shared technique elective groups (all tracks) ─────────────────
            "elective_groups": [
                {
                    "name": "Modern technique (1220-4220)",
                    "credits": 3,
                    "dept": "DANC",
                    "choose_from": [
                        "DANC-1220", "DANC-2220", "DANC-3220", "DANC-4220",
                    ],
                    "notes": "3 hrs from DANC 1220-4220 (modern technique)",
                },
                {
                    "name": "Ballet technique (1420-4420)",
                    "credits": 3,
                    "dept": "DANC",
                    "choose_from": [
                        "DANC-1420", "DANC-2420", "DANC-3420", "DANC-4420",
                    ],
                    "notes": "3 hrs from DANC 1420-4420 (ballet technique)",
                },
                {
                    "name": "Jazz technique (1320-4320)",
                    "credits": 2,
                    "dept": "DANC",
                    "choose_from": [
                        "DANC-1320", "DANC-2320", "DANC-3320", "DANC-4320",
                    ],
                    "notes": "2 hrs from DANC 1320-4320 (jazz technique)",
                },
            ],
            # ── Track concentrations (32 credit hours each) ───────────────────
            "concentrations": {
                "Performance": {
                    "required": [
                        "DANC-2110",   # Musical Theatre Dance Forms (1 cr)
                        "DANC-2580",   # Dance Improvisation II (1 cr)
                        "DANC-2590",   # Dance Composition II (2 cr)
                        "DANC-3010",   # Dance History I (3 cr)
                        "DANC-3530",   # Partnering for Ballet and Modern Dance (1 cr)
                        "DANC-3580",   # Dance Improvisation III (1 cr)
                        "DANC-3590",   # Dance Composition III (2 cr)
                        "DANC-4590",   # Dance Composition IV (2 cr)
                        "DANC-4910",   # Seminar in Professional Praxis for Dancers (2 cr)
                    ],
                    "pedagogy_or_movement": {
                        "credits": 3,
                        "choose_from": ["DANC-3050", "DANC-3060"],
                        "notes": "DANC-3050 Dance Pedagogy OR DANC-3060 Movement Analysis",
                    },
                    "additional_modern": {
                        "credits": 3,
                        "choose_from": [
                            "DANC-2220", "DANC-3220", "DANC-4220",
                        ],
                        "notes": "3 additional hrs from DANC 2220-4220 (modern technique)",
                    },
                    "additional_ballet": {
                        "credits": 3,
                        "choose_from": [
                            "DANC-2420", "DANC-3420", "DANC-4420",
                        ],
                        "notes": "3 additional hrs from DANC 2420-4420 (ballet technique)",
                    },
                    "repertory": {
                        "credits": 6,
                        "choose_from": ["DANC-1150"],
                        "notes": "6 hrs of DANC-1150 Dance Repertory",
                    },
                    "production": {
                        "credits": 2,
                        "choose_from": ["DANC-1160"],
                        "notes": "2 hrs of DANC-1160 Dance Production",
                    },
                },
                "Business": {
                    "required": [
                        "DANC-2110",   # Musical Theatre Dance Forms (1 cr)
                        "DANC-3530",   # Partnering for Ballet and Modern Dance (1 cr)
                        "DANC-4800",   # Internship in Dance (1 cr)
                        "DANC-2580",   # Dance Improvisation II (1 cr)
                        "DANC-2590",   # Dance Composition II (2 cr)
                        "DANC-3590",   # Dance Composition III (2 cr)
                        "ACCT-2010",   # Principles of Accounting I (3 cr)
                        "BSNS-2710",   # Principles of Management (3 cr)
                        "BSNS-2810",   # Principles of Marketing (3 cr)
                    ],
                    "additional_modern": {
                        "credits": 1,
                        "choose_from": [
                            "DANC-2220", "DANC-3220", "DANC-4220",
                        ],
                        "notes": "1 additional hr from DANC 2220-4220 (modern technique)",
                    },
                    "additional_ballet": {
                        "credits": 1,
                        "choose_from": [
                            "DANC-2420", "DANC-3420", "DANC-4420",
                        ],
                        "notes": "1 additional hr from DANC 2420-4420 (ballet technique)",
                    },
                    "repertory": {
                        "credits": 4,
                        "choose_from": ["DANC-1150"],
                        "notes": "4 hrs of DANC-1150 Dance Repertory",
                    },
                    "production": {
                        "credits": 4,
                        "choose_from": ["DANC-1160"],
                        "notes": "4 hrs of DANC-1160 Dance Production",
                    },
                    "related_electives": {
                        "credits": 5,
                        "dept": "DANC",
                        "notes": "5 additional hrs of approved related courses",
                    },
                },
                "Pedagogy": {
                    "required": [
                        "DANC-2580",   # Dance Improvisation II (1 cr)
                        "DANC-2590",   # Dance Composition II (2 cr)
                        "DANC-3010",   # Dance History I (3 cr)
                        "DANC-3050",   # Dance Pedagogy I (3 cr)
                        "DANC-3055",   # Dance Pedagogy II (3 cr)
                        "DANC-3590",   # Dance Composition III (2 cr)
                        "DANC-4590",   # Dance Composition IV (2 cr)
                        "EDUC-2110",   # Educational Psychology (3 cr)
                    ],
                    "additional_modern": {
                        "credits": 1,
                        "choose_from": [
                            "DANC-2220", "DANC-3220", "DANC-4220",
                        ],
                        "notes": "1 additional hr from DANC 2220-4220 (modern technique)",
                    },
                    "additional_ballet": {
                        "credits": 1,
                        "choose_from": [
                            "DANC-2420", "DANC-3420", "DANC-4420",
                        ],
                        "notes": "1 additional hr from DANC 2420-4420 (ballet technique)",
                    },
                    "additional_jazz": {
                        "credits": 1,
                        "choose_from": ["DANC-2330", "DANC-3320"],
                        "notes": "1 additional hr from DANC-2330 or DANC-3320 (jazz technique)",
                    },
                    "repertory": {
                        "credits": 4,
                        "choose_from": ["DANC-1150"],
                        "notes": "4 hrs of DANC-1150 Dance Repertory",
                    },
                    "production": {
                        "credits": 2,
                        "choose_from": ["DANC-1160"],
                        "notes": "2 hrs of DANC-1160 Dance Production",
                    },
                    "practice_teaching": {
                        "credits": 2,
                        "choose_from": ["DANC-2850"],
                        "notes": "2 hrs of DANC-2850 Practice in Teaching",
                    },
                    "related_electives": {
                        "credits": 2,
                        "dept": "DANC",
                        "notes": "2 hrs of additional related courses",
                    },
                },
                "Science": {
                    "required": [
                        "CHEM-1000",   # Introduction to Chemistry (4 cr)
                        "PSYC-2000",   # General Psychology (3 cr)
                        "SOCI-2010",   # Introduction to Sociology (3 cr)
                        "MATH-2120",   # Introductory Statistics with Applications (4 cr)
                        "PHYS-2140",   # General Physics I Algebra-based (4 cr)
                        "DANC-3060",   # Movement Analysis (3 cr)
                        "DANC-4060",   # Motor Control (3 cr)
                    ],
                    "repertory": {
                        "credits": 2,
                        "choose_from": ["DANC-1150"],
                        "notes": "2 hrs of DANC-1150 Dance Repertory",
                    },
                    "production": {
                        "credits": 1,
                        "choose_from": ["DANC-1160"],
                        "notes": "1 hr of DANC-1160 Dance Production",
                    },
                    "related_electives": {
                        "credits": 5,
                        "dept": "DANC",
                        "notes": "5 hrs of approved related courses",
                    },
                },
            },
            "notes": "Select one track concentration: Performance, Business, Pedagogy, or Science.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "dance_minor": {
        "2022-23": {
            "name": "Dance Minor",
            "total_credits": 18,
            "required": ["DANC-1580", "DANC-1590", "DANC-3000", "DANC-3510"],
            "choose_one": [
                {"name": "Dance technique", "choose_from": ["DANC-3010", "DANC-3020"]},
            ],
            "elective_groups": [
                {"name": "Modern technique", "credits": 2, "choose_from": []},
                {"name": "Jazz technique", "credits": 1, "choose_from": []},
                {"name": "Ballet technique", "credits": 2, "choose_from": []},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "dance_complementary": {
        "2022-23": {
            "name": "Dance Complementary Major",
            "total_credits": 33,
            "required": ["DANC-1580", "DANC-1590"],
            "choose_one": [
                {
                    "name": "Theory/Choreography",
                    "choose_from": ["DANC-3000", "DANC-3010", "DANC-3020"],
                },
                {"name": "Composition/Pedagogy", "choose_from": ["DANC-3050", "DANC-4060"]},
            ],
            "elective_groups": [
                {"name": "Modern technique", "credits": 2, "choose_from": []},
                {"name": "Jazz technique", "credits": 2, "choose_from": []},
                {"name": "Ballet technique", "credits": 2, "choose_from": []},
                {"name": "Dance lecture", "credits": 3, "choose_from": ["DANC-1150"]},
                {"name": "Dance lab", "credits": 3, "choose_from": ["DANC-1160"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "musical_theatre_ba": {
        "2022-23": {
            "name": "Musical Theatre (BA)",
            "total_credits": 45,
            "required": [
                "MUSC-1010",
                "MUSC-1020",
                "MUSC-1030",
                "MUSC-1040",
                "MUTR-2410",
                "MUTR-2420",
                "MUTR-3210",
                "MUTR-3220",
                "MUPF-4910",
                "THEA-2110",
                "THEA-2120",
                "THEA-2210",
                "THEA-3110",
            ],
            "elective_groups": [
                {"name": "Voice", "credits": 6, "choose_from": ["MUPF-2700", "MUPF-4700"]},
                {
                    "name": "Piano",
                    "credits": 2,
                    "choose_from": [
                        "MUPF-1050",
                        "MUPF-1060",
                        "MUPF-1710",
                        "MUPF-1720",
                        "MUPF-2030",
                    ],
                },
                {
                    "name": "Ballet",
                    "credits": 2,
                    "choose_from": ["DANC-1420", "DANC-2420", "DANC-3420"],
                },
                {
                    "name": "Jazz dance",
                    "credits": 1,
                    "choose_from": ["DANC-1320", "DANC-2320", "DANC-3320"],
                },
                {
                    "name": "Dance studies",
                    "credits": 2,
                    "choose_from": ["DANC-2110", "DANC-1120", "DANC-2120", "DANC-3120"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# MATHEMATICS
# ─────────────────────────────────────────────────────────────────────────
MATHEMATICS = {
    "math_ba": {
        "2022-23": {
            "name": "Mathematics (BA)",
            "total_credits": 30,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-4000",
            ],
            "elective_groups": [
                {
                    "name": "Upper Math course",
                    "credits": 3,
                    "dept": "MATH",
                    "min_level": 4010,
                    "notes": "One course numbered MATH-4010 or above",
                },
                {
                    "name": "Additional upper Math",
                    "credits": 6,
                    "dept": "MATH",
                    "min_level": 3100,
                    "notes": "At least two additional courses numbered MATH-3100 or above",
                },
            ],
            "notes": "MATH-1000, 1100, 1110, 1220, 1250, 1300, 1400, 4700 do not apply.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Mathematics (BA)",
            "total_credits": 41,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-2200",
                "MATH-3010",
                "MATH-3020",
                "MATH-4000",
            ],
            "elective_groups": [
                {"name": "Upper Math course", "credits": 3, "dept": "MATH", "min_level": 4010},
                {"name": "Additional upper Math", "credits": 6, "dept": "MATH", "min_level": 3100},
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "math_bs": {
        "2022-23": {
            "name": "Mathematics (BS)",
            "total_credits": 47,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-2200",
                "MATH-3010",
                "MATH-3020",
                "MATH-3300",
                "MATH-4000",
                "ENGR-2310",
                "CPSC-2320",
                "PHYS-2240",
            ],
            "choose_one": [
                {"name": "Stats/Calc", "choose_from": ["MATH-2120", "MATH-4010"]},
                {"name": "Analysis", "choose_from": ["MATH-4100", "MATH-4200"]},
            ],
            "elective_groups": [
                {
                    "name": "Upper Math elective",
                    "credits": 3,
                    "dept": "MATH",
                    "min_level": 3100,
                    "notes": "Additional 3 hrs from MATH-3100 or higher (not MATH-4700)",
                },
                {
                    "name": "Science elective",
                    "credits": 4,
                    "choose_from": ["CHEM-2110", "PHYS-2250", "BIOL-2210"],
                    "notes": "4 hrs from CHEM-2110+, PHYS-2250+, BIOL-2210+",
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "math_minor": {
        "2022-23": {
            "name": "Mathematics Minor",
            "total_credits": 16,
            "required": ["MATH-2010", "MATH-2020"],
            "elective_groups": [
                {"name": "Upper math courses", "credits": 9, "dept": "MATH", "min_level": 2000},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "decision_science_ba": {
        "2022-23": {
            "name": "Decision Science (BA)",
            "total_credits": 53,
            "required": [
                "MATH-2010",
                "MATH-2020",
                "MATH-2120",
                "MATH-3010",
                "MATH-3020",
                "MATH-3200",
                "MATH-4000",
                "MATH-4010",
                "BSNS-2710",
                "BSNS-2810",
                "BSNS-3240",
                "BSNS-3510",
                "BSNS-4110",
                "BSNS-4330",
            ],
            "choose_one": [
                {"name": "Advanced Math", "choose_from": ["MATH-3100", "MATH-3300", "MATH-3400"]},
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────
# ENGINEERING
# ─────────────────────────────────────────────────────────────────────────
ENGINEERING = {
    "mechanical_engineering_bs": {
        "2022-23": {
            "name": "Mechanical Engineering (BS)",
            "total_credits": 84,
            "required": [
                # Mathematics and Basic Sciences (31 cr)
                "CHEM-2110",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
                # Common Engineering Core (21 cr)
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
                "ENGR-4950",  # Senior Design I, 2 cr (WI)
                "ENGR-4960",  # Senior Design II, 2 cr (WI+SI)
                # Major Specific Requirements (32 cr)
                "ENGR-2070",
                "ENGR-3030",
                "ENGR-3100",
                "ENGR-3110",  # Kinematics and Robotics, 3 cr
                "ENGR-3160",  # Vibrations, 2 cr
                "ENGR-3180",  # Materials and Processes, 3 cr
                "ENGR-3190",  # Thermodynamics: Cycle Analysis, 2 cr
                "ENGR-3510",  # Solid Mechanics, 3 cr
                "ENGR-4100",  # Thermal-Fluids Lab, 2 cr
                "ENGR-4110",  # Machine Design, 3 cr
                "ENGR-4130",  # Fluid Mechanics, 3 cr
                "ENGR-4160",  # Heat and Mass Transfer, 3 cr
            ],
            "choose_one": [
                {"name": "Computing", "choose_from": ["CPSC-2320", "CPSC-2500"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Mechanical Engineering (BS)",
            "total_credits": 84,
            "required": [
                "MATH-3020",
                "ENGR-2070",
                "ENGR-2110",
                "ENGR-3030",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3100",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "electrical_engineering_bs": {
        "2022-23": {
            "name": "Electrical Engineering (BS)",
            "total_credits": 84,
            # ── Common Engineering Core (21 cr) ────────────────────────────
            # ── Mathematics and Basic Sciences (31 cr) ─────────────────────
            # ── Major Specific Requirements (32 cr) ────────────────────────
            "required": [
                # Math & Basic Sciences
                "CHEM-2110",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
                "MATH-4010",
                # Common Engineering Core
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
                # Major Specific
                "ENGR-3030",
                "ENGR-3220",
                "ENGR-3230",
                "ENGR-3240",
                "ENGR-3270",
                "ENGR-3280",
                "ENGR-4230",
                "ENGR-4240",
                "ENGR-4250",
            ],
            "choose_one": [
                {"name": "C++ / Computing", "choose_from": ["CPSC-2320", "CPSC-2500"]},
                {"name": "Computer Architecture", "choose_from": ["CPSC-2420"]},
            ],
        },
        "2023-24": {
            "name": "Electrical Engineering (BS)",
            "total_credits": 84,
            "required": [
                "CPSC-2320",
                "CPSC-2500",
                "ENGR-3260",
                "CHEM-2110",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
                "MATH-4010",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
                "ENGR-3030",
            ],
        },
        "2024-25": {
            "name": "Electrical Engineering (BS)",
            "total_credits": 92,
            "required": [
                "MATH-3020",
                "MATH-4010",
                "ENGR-2200",
                "ENGR-3030",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "computer_engineering_bs": {
        "2022-23": {
            "name": "Computer Engineering (BS)",
            "total_credits": 82,
            "required": [
                "CPSC-2420",
                "CPSC-2430",
                "CPSC-2500",
                "CPSC-4420",
                "CHEM-2110",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3100",
                "MATH-4010",
                "PHYS-2240",
                "PHYS-2250",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
                "ENGR-3030",
                "ENGR-3220",
                "ENGR-3260",
                "ENGR-3270",
                "ENGR-3280",
                "ENGR-4950",
                "ENGR-4960",
            ],
            "choose_one": [
                {"name": "Computing core", "choose_from": ["CPSC-2250", "CPSC-2320", "CPSC-2500"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Computer Engineering (BS)",
            "total_credits": 91,
            "required": [
                "MATH-2200",
                "MATH-4010",
                "ENGR-2200",
                "ENGR-3030",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3100",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "civil_engineering_bs": {
        "2023-24": {
            "name": "Civil Engineering (BS)",
            "total_credits": 83,
            "required": [
                "CPSC-2320",
                "CPSC-2500",
                "CHEM-2110",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
                "ENGR-3030",
                "ENGR-3100",
            ],
        },
        "2024-25": {
            "name": "Civil Engineering (BS)",
            "total_credits": 92,
            "required": [
                "MATH-2120",
                "ENGR-2110",
                "ENGR-3100",
                "ENGR-3330",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
        "2025-26": {
            "name": "Civil Engineering (BS)",
            "total_credits": 92,
            "required": [
                "MATH-2120",
                "ENGR-2110",
                "ENGR-3140",
                "ENGR-3330",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
    },
    "mechatronics_engineering_bs": {
        "2022-23": {
            "name": "Mechatronics Engineering (BS)",
            "total_credits": 83,
            "required": [
                # Mathematics and Basic Sciences (31 cr)
                "CHEM-2110",
                "PHYS-2240",
                "PHYS-2250",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3100",
                # Common Engineering Core (21 cr)
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
                "ENGR-4950",  # Senior Design I, 2 cr (WI)
                "ENGR-4960",  # Senior Design II, 2 cr (WI+SI)
                # Major Specific Requirements (31 cr)
                "ENGR-3030",
                "ENGR-3110",  # Kinematics and Robotics
                "ENGR-3220",  # Electronics
                "ENGR-3280",  # Microcontrollers
                "ENGR-3510",  # Solid Mechanics
                "ENGR-4020",  # Mechatronics System Design
            ],
            "choose_one": [
                {"name": "Computing", "choose_from": ["CPSC-2320", "CPSC-2500"]},
                {"name": "Upper Math", "choose_from": ["MATH-3020", "MATH-4010", "CPSC-2250"]},
            ],
            "elective_groups": [
                {
                    "name": "MxE Electives (3000+ level CPSC, ENGR, MATH, or PHYS)",
                    "dept": ["CPSC", "ENGR", "MATH", "PHYS"],
                    "credits": 3,
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {
            "name": "Mechatronics Engineering (BS)",
            "total_credits": 92,
            "required": [
                "MATH-2120",
                "MATH-3020",
                "ENGR-2110",
                "ENGR-2200",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3100",
                "PHYS-2240",
                "PHYS-2250",
                "CHEM-2110",
            ],
        },
        "2025-26": {"same_as": "2024-25"},
    },
    "engineering_physics_bs": {
        "2022-23": {
            "name": "Engineering Physics (BS)",
            "total_credits": 76,
            "required": [
                "CHEM-2110",
                "MATH-2010",
                "MATH-2020",
                "MATH-3010",
                "MATH-3020",
                "MATH-3100",
                "PHYS-2240",
                "PHYS-2250",
                "PHYS-3130",
                "PHYS-4130",
                "PHYS-4220",
                "PHYS-4410",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2310",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2070",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-3240",
                "ENGR-4950",
                "ENGR-4960",
            ],
            "choose_one": [
                {"name": "Computing", "choose_from": ["CPSC-2320", "CPSC-1400", "CPSC-2500"]},
            ],
        },
    },
    "engineering_management": {
        "2022-23": {
            "name": "Engineering Management",
            "total_credits": 63,
            "required": [
                "BSNS-1100",
                "BSNS-2710",
                "BSNS-2810",
                "BSNS-4500",
                "BSNS-4910",
                "ACCT-2010",
                "PSYC-2100",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2060",
                "ENGR-2090",
            ],
            "choose_one": [
                {"name": "Math", "choose_from": ["MATH-1300", "MATH-1400", "MATH-2010"]},
                {"name": "Stats/Business", "choose_from": ["BSNS-2450", "MATH-2120"]},
                {"name": "Physics", "choose_from": ["PHYS-2140", "PHYS-2240"]},
                {"name": "Computing", "choose_from": ["ENGR-2130", "CPSC-2040"]},
                {"name": "Economics", "choose_from": ["ECON-2010", "ECON-2020"]},
            ],
        },
        "2023-24": {
            "name": "Engineering Management",
            "total_credits": 61,
            "required": [
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2003",
                "ENGR-2090",
                "BSNS-1100",
                "BSNS-2710",
                "BSNS-2810",
                "BSNS-4500",
                "BSNS-4910",
                "ACCT-2010",
                "PSYC-2100",
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
    "humanitarian_engineering_complementary": {
        "2022-23": {
            "name": "Humanitarian Engineering Complementary Major",
            "total_credits": 47,
            "required": [
                "PHYS-2240",
                "MATH-2010",
                "MATH-2020",
                "ENGR-2001",
                "ENGR-2002",
                "ENGR-2010",
                "ENGR-2030",
                "ENGR-2060",
                "ENGR-2080",
                "ENGR-2090",
                "ENGR-2110",
                "ENGR-2310",
            ],
            "choose_one": [
                {"name": "ENGR core", "choose_from": ["ENGR-2003", "ENGR-2200"]},
            ],
            "elective_groups": [
                {
                    "name": "Cultural/Social electives",
                    "credits": 7,
                    "choose_from": [
                        "BSNS-2710",
                        "BSNS-3120",
                        "BSNS-4480",
                        "CMIN-2000",
                        "CMIN-3910",
                        "RLGN-2130",
                        "RLGN-3040",
                        "RLGN-3120",
                        "PSYC-2000",
                        "PSYC-2100",
                        "PSYC-3200",
                        "SOCI-2020",
                        "SOCI-2100",
                        "SOCI-4350",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "humanitarian_engineering_minor": {
        "2022-23": {
            "name": "Humanitarian Engineering Minor",
            "total_credits": 15,
            "required": [
                "ENGR-2060",
                "ENGR-2080",
                "ENGR-2090",
                "ENGR-3080",
            ],
            "elective_groups": [
                {
                    "name": "Cultural/Social electives",
                    "credits": 4,
                    "choose_from": [
                        "BSNS-2710",
                        "BSNS-3120",
                        "BSNS-4480",
                        "CMIN-2000",
                        "CMIN-3910",
                        "RLGN-2130",
                        "RLGN-3040",
                        "RLGN-3120",
                        "PSYC-2000",
                        "PSYC-2100",
                        "PSYC-3200",
                        "SOCI-2020",
                        "SOCI-2100",
                        "SOCI-4350",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# SPORT / RECREATION
# ─────────────────────────────────────────────────────────────────────────
SPORT_REC = {
    "sport_recreational_leadership": {
        "2022-23": {
            "name": "Sport and Recreational Leadership",
            "total_credits": 52,
            "required": [
                "SPRL-1350",
                "SPRL-2450",
                "SPRL-2550",
                "SPRL-3150",
                "SPRL-3250",
                "SPRL-3300",
                "SPRL-4850",
                "PETE-1300",
                "PETE-2250",
                "PETE-3720",
                "PETE-4900",
                "PEHS-1450",
                "PEHS-3340",
                "PEHS-3410",
                "ATRG-1530",
                "EXSC-2580",
                "ACCT-2010",
                "BSNS-2710",
                "BSNS-2810",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "sport_recreational_leadership_minor": {
        "2022-23": {
            "name": "Sport and Recreational Leadership Minor",
            "total_credits": 16,
            "required": [
                "PETE-1300",
                "PEHS-1450",
                "SPRL-1350",
                "SPRL-2450",
                "SPRL-2550",
                "SPRL-3150",
            ],
            "elective_groups": [
                {
                    "name": "SPRL/PETE electives",
                    "credits": 3,
                    "choose_from": ["PETE-3720", "PETE-4900", "SPRL-3300", "SPRL-4850"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "athletic_coaching_minor": {
        "2022-23": {
            "name": "Athletic Coaching Minor",
            "total_credits": 15,
            "required": [
                "PEHS-1450",
                "PEHS-1550",
                "EXSC-2580",
                "SPRL-1350",
                "SPRL-2550",
                "SPRL-3300",
            ],
            "choose_one": [
                {"name": "Injury prevention", "choose_from": ["ATRG-1530", "EXSC-4010"]},
                {"name": "Coaching theory", "choose_from": ["PEHS-2340", "PEHS-3340"]},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# PUBLIC HEALTH
# ─────────────────────────────────────────────────────────────────────────
PUBLIC_HEALTH = {
    "public_health_ba": {
        "2022-23": {
            "name": "Public Health (BA)",
            "total_credits": 37,
            # Core (31 cr) + B.A. track (6 cr) + elective (2-4 cr) = 37-39 cr major
            # (total degree = 48-51 cr including LA framework)
            "required": [
                "PSYC-2000",           # 3 cr
                "BIOL-2070",           # 4 cr
                "MATH-2120",           # 4 cr
                "PUBH-3020",           # 3 cr
                "PUBH-4360",           # 3 cr
                "SOCI-2020",           # 3 cr  (B.A. track)
            ],
            "choose_one": [
                # PUBH-2040 or BIOL-2040 (Personal & Community Health)
                {"name": "Personal & Community Health",
                 "choose_from": ["PUBH-2040", "BIOL-2040"]},
                # Social Psychology (WI)
                {"name": "Social Psychology (WI)",
                 "choose_from": ["PUBH-3010", "SOCI-3010", "PSYC-3010"]},
                # Introduction to Social Research
                {"name": "Introduction to Social Research",
                 "choose_from": ["PUBH-3700", "SOCI-3700"]},
                # Program Planning and Grant Writing
                {"name": "Program Planning and Grant Writing",
                 "choose_from": ["PUBH-4350", "SOCI-4350", "SOWK-4350"]},
                # Community Health Internship (W8)
                {"name": "Community Health Internship (W8)",
                 "choose_from": ["PUBH-4810", "SOCI-4810"]},
                # B.A. track: Sociology of Health or Family (choose 1)
                {"name": "Sociology of Health or Family (BA track)",
                 "choose_from": ["PUBH-3260", "SOCI-3260", "SOCI-2100"]},
            ],
            "elective_groups": [
                {
                    "name": "Selected elective (2-4 cr)",
                    "credits": 2,
                    "choose_from": [
                        "BIOL-2010",
                        "BSNS-4400",
                        "PUBH-3510",
                        "BIOL-3510",
                        "CHEM-1000",
                        "COMM-3370",
                        "ECON-2010",
                        "ECON-2020",
                        "ECON-3110",
                        "NURS-1210",
                        "POSC-2200",
                        "PSYC-2100",
                        "PSYC-3450",
                        "SOCI-3100",
                        "SOCI-3400",
                        "SPAN-3101",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "public_health_bs": {
        "2022-23": {
            "name": "Public Health (BS)",
            "total_credits": 43,
            # Core (31 cr) + B.S. track (12 cr) + elective (2-4 cr) = 43-45 cr major
            "required": [
                "PSYC-2000",           # 3 cr
                "BIOL-2070",           # 4 cr
                "MATH-2120",           # 4 cr
                "PUBH-3020",           # 3 cr
                "PUBH-4360",           # 3 cr
                "BIOL-2410",           # 4 cr  (B.S. track)
                "BIOL-2420",           # 4 cr  (B.S. track)
                "BIOL-2230",           # 4 cr  (B.S. track)
            ],
            "choose_one": [
                {"name": "Personal & Community Health",
                 "choose_from": ["PUBH-2040", "BIOL-2040"]},
                {"name": "Social Psychology (WI)",
                 "choose_from": ["PUBH-3010", "SOCI-3010", "PSYC-3010"]},
                {"name": "Introduction to Social Research",
                 "choose_from": ["PUBH-3700", "SOCI-3700"]},
                {"name": "Program Planning and Grant Writing",
                 "choose_from": ["PUBH-4350", "SOCI-4350", "SOWK-4350"]},
                {"name": "Community Health Internship (W8)",
                 "choose_from": ["PUBH-4810", "SOCI-4810"]},
            ],
            "elective_groups": [
                {
                    "name": "Selected elective (2-4 cr)",
                    "credits": 2,
                    "choose_from": [
                        "BIOL-2010",
                        "BSNS-4400",
                        "PUBH-3510",
                        "BIOL-3510",
                        "CHEM-1000",
                        "COMM-3370",
                        "ECON-2010",
                        "ECON-2020",
                        "ECON-3110",
                        "NURS-1210",
                        "POSC-2200",
                        "PSYC-2100",
                        "PSYC-3450",
                        "SOCI-3100",
                        "SOCI-3400",
                        "SPAN-3101",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "public_health_minor": {
        "2022-23": {
            "name": "Public Health Minor",
            "total_credits": 16,
            "required": [
                "PSYC-2000",
                "PUBH-3010",
                "PUBH-3020",
                "PUBH-3260",
                "ECON-3110",
                "PSYC-3450",
                "SOCI-3100",
                "SOCI-3400",
                "PUBH-3510",
                "PUBH-3700",
                "SOCI-3700",
                "PUBH-4350",
                "SOCI-4350",
                "PUBH-4360",
                "PUBH-4810",
                "SOCI-4810",
            ],
            "notes": "See catalog for exact credit hour selection",
        },
        "2023-24": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# NURSING
# ─────────────────────────────────────────────────────────────────────────
NURSING = {
    "nursing_bsn": {
        "2022-23": {
            "name": "Nursing (BSN)",
            "total_credits": 83,
            "required": [
                "NURS-2140",
                "NURS-2231",
                "NURS-2250",
                "NURS-2241",
                "NURS-2270",
                "NURS-2340",
                "NURS-3351",
                "NURS-3361",
                "NURS-3391",
                "NURS-4451",
                "NURS-4470",
                "NURS-4510",
                "NURS-4521",
                "NURS-4950",
                "NURS-4960",
                "NURS-4970",
                "BIOL-2230",
                "BIOL-2410",
                "BIOL-2420",
                "PSYC-2000",
                "PSYC-2510",
                "CHEM-1000",
            ],
            "notes": "Admission to the Nursing program required. NURS-2130 strongly recommended before entering major.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "nursing_accelerated": {
        "2022-23": {
            "name": "Nursing Accelerated (BSN)",
            "total_credits": 124,
            "required": [
                "NURS-1100",
                "NURS-1210",
                "NURS-2100",
                "NURS-2200",
                "NURS-3100",
                "NURS-3200",
                "NURS-3300",
                "NURS-3400",
                "NURS-4100",
                "NURS-4200",
                "NURS-4300",
                "NURS-4400",
            ],
            "notes": "Accelerated track for students with prior bachelor's degree.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "nursing_rn_bsn": {
        "2022-23": {
            "name": "Nursing RN-to-BSN",
            "total_credits": 30,
            "required": [
                "NURS-3050",
                "NURS-3300",
                "NURS-4200",
                "NURS-4950",
            ],
            "notes": "For licensed RNs. Credit awarded for prior nursing education.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# COMMUNICATION / CINEMA / JOURNALISM
# ─────────────────────────────────────────────────────────────────────────
COMMUNICATION = {
    "cinema_media_arts": {
        "2022-23": {
            "name": "Cinema & Media Arts",
            "total_credits": 52,
            "required": [
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
            ],
            "elective_groups": [
                {
                    "name": "CMA practicum",
                    "credits": 4,
                    "choose_from": ["COMM-2860"],
                    "notes": "4 hrs of COMM-2860",
                },
                {
                    "name": "CMA internship",
                    "credits": 1,
                    "choose_from": ["COMM-4800"],
                    "notes": "1-4 hrs COMM-4800",
                },
                {
                    "name": "CMA electives",
                    "credits": 3,
                    "choose_from": [
                        "COMM-3050",
                        "COMM-3160",
                        "COMM-3260",
                        "COMM-4120",
                        "COMM-4900",
                        "ENGL-3140",
                        "THEA-2110",
                        "THEA-2210",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Cinema & Media Arts",
            "total_credits": 52,
            "required": [
                "COMM-2000",
                "COMM-2010",
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
            ],
        },
    },
    "journalism_complementary": {
        "2022-23": {
            "name": "Journalism Complementary Major",
            "total_credits": 30,
            "required": [
                "COMM-2000",
                "COMM-2010",
                "COMM-2130",
                "COMM-2200",
                "COMM-2850",
                "COMM-3130",
                "COMM-3200",
                "COMM-3230",
                "COMM-4000",
                "COMM-4800",
            ],
            "elective_groups": [
                {
                    "name": "Media electives",
                    "credits": 3,
                    "choose_from": ["COMM-2140", "COMM-3330", "COMM-3370"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "multimedia_journalism_complementary": {
        "2023-24": {
            "name": "Multimedia Journalism Complementary Major",
            "total_credits": 35,
            "required": [
                "COMM-2000",
                "COMM-2010",
                "COMM-2130",
                "COMM-2200",
                "COMM-2240",
                "COMM-2840",
                "COMM-3050",
                "COMM-3200",
                "COMM-3240",
                "COMM-3250",
                "COMM-3330",
                "COMM-4000",
                "COMM-4900",
            ],
            "elective_groups": [
                {
                    "name": "Journalism elective",
                    "credits": 3,
                    "choose_from": ["COMM-3130", "COMM-3230", "ENGL-3160"],
                },
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {
            "name": "Multimedia Journalism Major",
            "total_credits": 42,
            "required": [
                "COMM-2000",
                "COMM-2010",
                "COMM-2130",
                "COMM-2200",
                "COMM-2240",
                "COMM-2840",
                "COMM-3050",
                "COMM-3200",
                "COMM-3240",
                "COMM-3250",
                "COMM-3330",
                "COMM-4000",
                "COMM-4900",
            ],
        },
    },
    "public_relations_complementary": {
        "2023-24": {
            "name": "Public Relations Complementary Major",
            "total_credits": 35,
            "required": [
                "COMM-2000",
                "COMM-2010",
                "COMM-2200",
                "COMM-2240",
                "COMM-3240",
                "COMM-3250",
                "COMM-3370",
                "COMM-4340",
            ],
            "elective_groups": [
                {"name": "PR electives", "credits": 6, "dept": "COMM"},
            ],
        },
        "2024-25": {"same_as": "2023-24"},
        "2025-26": {"same_as": "2023-24"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# SPANISH / LANGUAGES
# ─────────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "spanish": {
        "2022-23": {
            "name": "Spanish",
            "total_credits": 43,
            "required": ["SPAN-2010", "SPAN-3240", "MLAN-3500", "MLAN-4900"],
            "notes": "At least 6 hrs from study abroad or internship/SPAN-3240",
        },
        "2023-24": {
            "name": "Spanish",
            "total_credits": 43,
            "required": ["SPAN-2010", "SPAN-3240", "MLAN-4900"],
        },
        "2024-25": {"same_as": "2023-24"},
    },
    "spanish_minor": {
        "2022-23": {
            "name": "Spanish Minor",
            "total_credits": 18,
            "required": ["SPAN-2010"],
            "elective_groups": [
                {"name": "SPAN courses", "credits": 14, "dept": "SPAN"},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
    "french_studies_minor": {
        "2023-24": {
            "name": "French Studies Minor",
            "total_credits": 15,
            "required": ["MLAN-2000"],
            "notes": "French Studies Minors may opt to take MLAN-3400 instead.",
        },
        "2024-25": {"same_as": "2023-24"},
    },
    "german_studies_minor": {
        "2023-24": {
            "name": "German Studies Minor",
            "total_credits": 15,
            "required": ["MLAN-2000"],
        },
        "2024-25": {"same_as": "2023-24"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# MINORS: MISCELLANEOUS
# ─────────────────────────────────────────────────────────────────────────
MISC_MINORS = {
    "ethics_minor": {
        "2022-23": {
            "name": "Ethics Minor",
            "total_credits": 15,
            "required": ["PHIL-2120"],
            "elective_groups": [
                {
                    "name": "Ethics electives",
                    "credits": 12,
                    "choose_from": [
                        "BIBL-3420",
                        "PHIL-3210",
                        "RLGN-2130",
                        "RLGN-3120",
                        "PHIL-3250",
                        "RLGN-3250",
                        "COMM-3200",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "philosophy_minor": {
        "2022-23": {
            "name": "Philosophy Minor",
            "total_credits": 15,
            "required": ["PHIL-2000"],
            "elective_groups": [
                {"name": "PHIL courses", "credits": 15, "dept": "PHIL"},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "economics_minor": {
        "2022-23": {
            "name": "Economics Minor",
            "total_credits": 18,
            "required": ["ECON-2010", "ECON-2020", "ECON-3020", "ECON-3410"],
            "elective_groups": [
                {
                    "name": "Economics electives",
                    "credits": 6,
                    "choose_from": [
                        "ECON-3110",
                        "ECON-3210",
                        "ECON-3850",
                        "ECON-4020",
                        "BSNS-4240",
                        "POSC-2200",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "legal_studies_minor": {
        "2022-23": {
            "name": "Legal Studies Minor",
            "total_credits": 15,
            "required": ["POSC-2210", "POSC-4810", "ENGL-3190"],
            "dist_groups": [
                {
                    "name": "Law elective",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": ["BSNS-3420", "COMM-4000", "CRIM-3110", "POSC-3250"],
                },
                {
                    "name": "Ethics elective",
                    "credits": 3,
                    "min_courses": 1,
                    "choose_from": [
                        "BIBL-3420",
                        "PHIL-2120",
                        "PHIL-3250",
                        "POSC-3010",
                        "HIST-3010",
                        "PHIL-3010",
                        "RLGN-3120",
                        "RLGN-3250",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "international_relations_minor": {
        "all_years": {
            "name": "International Relations Minor",
            "total_credits": 15,
            "required": ["POSC-2020", "POSC-2580", "POSC-3300", "POSC-3510"],
            "elective_groups": [
                {
                    "name": "Comparative Politics elective",
                    "credits": 3,
                    "choose_from": [
                        "POSC-3310",
                        "POSC-3320",
                        "POSC-3330",
                        "POSC-3400",
                        "POSC-3450",
                    ],
                },
            ],
        },
    },
    "political_science_minor": {
        "2022-23": {
            "name": "Political Science Minor",
            "total_credits": 15,
            "required": ["POSC-2020", "POSC-2100"],
            "elective_groups": [
                {"name": "POSC electives", "credits": 10, "dept": "POSC"},
            ],
            "notes": "No more than 3 hrs from POSC-2810, 4800, 4810, 4820.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "sociology_minor": {
        "all_years": {
            "name": "Sociology Minor",
            "total_credits": 15,
            "required": ["SOCI-2010"],
            "elective_groups": [
                {"name": "SOCI courses", "credits": 12, "dept": "SOCI"},
            ],
        },
    },
    "social_work_minor": {
        "all_years": {
            "name": "Social Work Minor",
            "total_credits": 17,
            "required": ["SOCI-2020", "SOWK-2000", "SOWK-2200", "SOWK-3100", "BIOL-2040"],
        },
    },
    "statistics_minor": {
        "all_years": {
            "name": "Statistics Minor",
            "total_credits": 16,
            "required": ["MATH-4010"],
            "choose_one": [
                {"name": "Intro Stats", "choose_from": ["MATH-2120", "PSYC-2440"]},
            ],
            "elective_groups": [
                {
                    "name": "Statistics electives",
                    "credits": 9,
                    "choose_from": [
                        "PSYC-3240",
                        "PSYC-4650",
                        "POSC-2420",
                        "POSC-3140",
                        "MATH-3400",
                    ],
                },
            ],
        },
    },
    "peace_conflict_minor": {
        "2022-23": {
            "name": "Peace and Conflict Transformation Minor",
            "total_credits": 18,
            "required": ["PACT-2100", "PACT-2200", "PACT-2300", "PACT-2400"],
            "elective_groups": [
                {
                    "name": "Electives",
                    "credits": 9,
                    "choose_from": [
                        "BSNS-3230",
                        "BSNS-3300",
                        "CMIN-3340",
                        "CRIM-3010",
                        "DANC-3000",
                        "ECON-2010",
                        "ENGL-3190",
                        "ENGL-3580",
                        "MLAN-2000",
                        "HIST-3190",
                        "PHIL-3210",
                        "POSC-3300",
                        "POSC-3310",
                        "POSC-3320",
                        "POSC-3360",
                        "PSYC-2100",
                        "RLGN-3020",
                        "RLGN-3120",
                        "RLGN-3320",
                        "SOCI-2010",
                        "SOCI-2020",
                        "SOCI-3400",
                    ],
                },
            ],
        },
        "2023-24": {
            "name": "Peace and Conflict Transformation Minor",
            "total_credits": 16,
            "required": ["PACT-2100", "PACT-2200", "PACT-2300", "PACT-2400"],
            "elective_groups": [
                {
                    "name": "Electives",
                    "credits": 6,
                    "choose_from": [
                        "BSNS-3230",
                        "BSNS-3300",
                        "CMIN-3340",
                        "CRIM-3010",
                        "ECON-2010",
                        "ENGL-3190",
                        "ENGL-3580",
                        "HIST-3190",
                        "PHIL-3210",
                        "POSC-3300",
                        "POSC-3310",
                        "PSYC-2100",
                    ],
                },
            ],
        },
    },
    "information_systems_minor": {
        "2022-23": {
            "name": "Information Systems Minor",
            "total_credits": 15,
            "required": ["CPSC-1400"],
            "choose_one": [
                {"name": "Systems intro", "choose_from": ["CPSC-1100", "BSNS-3400"]},
                {"name": "Systems pair", "choose_from": ["CPSC-1200", "CPSC-1500"]},
            ],
            "notes": "Either CPSC-1200+2300 or CPSC-1500+2100",
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "public_history_minor": {
        "all_years": {
            "name": "Public History Minor",
            "total_credits": 18,
            "required": [
                "HIST-2350",
                "ARTH-3480",
                "HIST-3490",
                "ARTH-2000",
                "ARTS-1250",
                "COMM-2240",
            ],
            "elective_groups": [
                {"name": "Public History internship", "credits": 3, "choose_from": ["HIST-4800"]},
            ],
        },
    },
    "honors_program": {
        "all_years": {
            "name": "Honors Program",
            "total_credits": 0,
            "required": [],
            "notes": "Honors courses (HNRS prefix) tracked separately.",
        },
    },
    "youth_leadership_development_complementary": {
        "2022-23": {
            "name": "Youth Leadership Development Complementary Major",
            "total_credits": 28,
            "required": [
                "PSYC-2000",
                "PSYC-2100",
                "PSYC-2510",
                "PSYC-4210",
                "SOCI-3210",
                "SOCI-3100",
            ],
            "elective_groups": [
                {
                    "name": "Sociology elective",
                    "credits": 3,
                    "choose_from": ["SOCI-3050", "SOCI-3140", "SOCI-3150"],
                },
                {
                    "name": "Practicum",
                    "credits": 3,
                    "choose_from": ["EDUC-2850", "PSYC-2850", "SOCI-2850"],
                },
                {
                    "name": "Capstone",
                    "credits": 3,
                    "choose_from": ["EDUC-4800", "PSYC-4800", "SOCI-4800"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2025-26": {
            "name": "Youth Leadership Complementary Major",
            "total_credits": 28,
            "required": [
                "PSYC-2000",
                "PSYC-2100",
                "PSYC-2510",
                "PSYC-4210",
                "SOCI-3210",
                "SOCI-3100",
            ],
        },
    },
    "financial_planning_complementary": {
        "2022-23": {
            "name": "Financial Planning Complementary Major",
            "total_credits": 27,
            "required": [
                "ACCT-2010",
                "BSNS-2510",
                "BSNS-3350",
                "BSNS-4150",
                "ACCT-4020",
                "BSNS-4260",
                "BSNS-4350",
                "BSNS-4510",
                "BSNS-3360",
            ],
            "elective_groups": [
                {
                    "name": "Finance elective",
                    "credits": 3,
                    "choose_from": ["BSNS-3100", "BSNS-3210", "BSNS-4310"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
    "business_info_systems_complementary": {
        "2022-23": {
            "name": "Business Information Systems Complementary Major",
            "total_credits": 31,
            "required": [
                "ACCT-2010",
                "BSNS-2710",
                "BSNS-2810",
                "BSNS-3400",
                "BSNS-4400",
                "CPSC-1400",
                "CPSC-1500",
                "CPSC-2100",
            ],
            "elective_groups": [
                {"name": "CS elective", "credits": 4, "dept": "CPSC", "min_level": 1100},
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "spanish_complementary": {
        "2022-23": {
            "name": "Spanish Complementary Major",
            "total_credits": 30,
            "required": ["MLAN-3500", "MLAN-4900"],
            "notes": "At least 6 hrs from study abroad or internship/SPAN-3240",
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "accounting_minor": {
        "all_years": {
            "name": "Accounting Minor",
            "total_credits": 15,
            "required": ["ACCT-2010", "ACCT-2020"],
            "elective_groups": [
                {
                    "name": "Accounting electives",
                    "credits": 9,
                    "choose_from": [
                        "ACCT-3010",
                        "ACCT-3020",
                        "ACCT-3110",
                        "ACCT-3500",
                        "ACCT-4020",
                        "ACCT-4050",
                        "ACCT-4100",
                        "ACCT-4310",
                    ],
                },
            ],
        },
    },
    "family_science_minor": {
        "2022-23": {
            "name": "Family Science Minor",
            "total_credits": 15,
            "required": ["SOCI-2100", "SOCI-3100", "SOCI-3140", "SOCI-3210"],
            "elective_groups": [
                {
                    "name": "Family science elective",
                    "credits": 3,
                    "choose_from": [
                        "BSNS-3150",
                        "PSYC-2000",
                        "PSYC-2510",
                        "SOCI-2200",
                        "SOCI-2450",
                        "SOWK-3200",
                    ],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "marketing_minor": {
        "all_years": {
            "name": "Marketing Minor",
            "total_credits": 15,
            "required": ["BSNS-2710", "BSNS-3220"],
            "elective_groups": [
                {
                    "name": "Marketing electives",
                    "credits": 9,
                    "choose_from": [
                        "BSNS-3210",
                        "BSNS-3510",
                        "BSNS-3550",
                        "BSNS-4110",
                        "BSNS-4330",
                        "BSNS-4400",
                        "BSNS-4550",
                    ],
                },
            ],
        },
    },
    "special_education_minor": {
        "2022-23": {
            "name": "Special Education Minor",
            "total_credits": 15,
            "required": [
                "SPED-2400",
                "SPED-2500",
                "SPED-2550",
                "SPED-3120",
                "SPED-3200",
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "womens_studies_minor": {
        "all_years": {
            "name": "Women's Studies Minor",
            "total_credits": 15,
            "required": ["SOCI-2450"],
            "elective_groups": [
                {"name": "Women's Studies electives", "credits": 12, "dept": "SOCI"},
            ],
        },
    },
    "french_german_studies_minor": {
        "2022-23": {
            "name": "French/German Studies Minor",
            "total_credits": 15,
            "required": ["MLAN-2000"],
            "notes": "French Studies may substitute MLAN-3400.",
        },
        "2023-24": {"same_as": "2022-23"},
    },
    "sport_marketing_minor": {
        "2022-23": {
            "name": "Sport Marketing Minor",
            "total_credits": 18,
            "required": [
                "BSNS-3210",
                "BSNS-3220",
                "BSNS-4110",
                "BSNS-4330",
            ],
            "elective_groups": [
                {
                    "name": "Sport marketing elective",
                    "credits": 3,
                    "choose_from": ["BSNS-3130", "BSNS-4360", "BSNS-4560", "BSNS-4800"],
                },
            ],
        },
        "2023-24": {"same_as": "2022-23"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# COMBINED LOOKUP TABLE
# ─────────────────────────────────────────────────────────────────────────
ALL_NON_FSB_PROGRAMS = {}
for _section in [
    BIOLOGY,
    BIOCHEMISTRY,
    CHEMISTRY,
    PHYSICS,
    CS,
    DATA_SCIENCE,
    CYBERSECURITY,
    EXERCISE_SCIENCE,
    EDUCATION,
    HISTORY_POLS,
    SOCIAL_SCIENCES,
    MINISTRY,
    ENGLISH,
    MUSIC,
    THEATRE_DANCE,
    MATHEMATICS,
    ENGINEERING,
    SPORT_REC,
    PUBLIC_HEALTH,
    NURSING,
    COMMUNICATION,
    LANGUAGES,
    MISC_MINORS,
]:
    ALL_NON_FSB_PROGRAMS.update(_section)


def get_non_fsb_requirements(program_key: str, year: str):
    """Return the requirements dict for a given program and catalog year."""
    prog = ALL_NON_FSB_PROGRAMS.get(program_key)
    if not prog:
        return None
    return _yr(prog, year)


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
