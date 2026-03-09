"""
Anderson University — Falls School of Business
Business Core Requirements: All 4 Catalog Years

Every FSB major builds on this core (except Business & Integrative Leadership, which has its own structure).
"""

# ─────────────────────────────────────────────
# BUSINESS CORE
# ─────────────────────────────────────────────

BUSINESS_CORE = {
    "2022-23": {
        "total_credits": 43,
        "required": [
            {"code": "ACCT 2010", "name": "Financial Accounting",               "credits": 3},
            {"code": "ACCT 2020", "name": "Managerial Accounting",              "credits": 3},
            {"code": "BSNS 1050", "name": "Business as a Profession",           "credits": 2},
            {"code": "BSNS 2310", "name": "Business Analytics",                 "credits": 3},
            {"code": "BSNS 2450", "name": "Data Analysis & Decision-Making",    "credits": 3},
            {"code": "BSNS 2510", "name": "Business Law",                       "credits": 3},
            {"code": "BSNS 2710", "name": "Principles of Marketing",            "credits": 3},
            {"code": "BSNS 2810", "name": "Principles of Management",           "credits": 3},
            {"code": "BSNS 3270", "name": "Operations Management",              "credits": 3},
            {"code": "BSNS 3420", "name": "Business Ethics",                    "credits": 3,
             "also_satisfies": ["F2", "W5"]},
            {"code": "BSNS 4500", "name": "Business Finance",                   "credits": 3},
            {"code": "BSNS 4910", "name": "Senior Capstone in Business",        "credits": 2,
             "also_satisfies": ["WI"]},
            {"code": "ECON 2010", "name": "Macroeconomics",                     "credits": 3},
            {"code": "ECON 2020", "name": "Microeconomics",                     "credits": 3},
        ],
        "math_requirement": {
            "note": "One of the following (counts toward core total):",
            "choose_one": [
                {"code": "MATH 1300", "name": "College Algebra",                "credits": 3},
                {"code": "MATH 1400", "name": "Precalculus",                    "credits": 4},
                {"code": "MATH 2010", "name": "Applied Calculus",               "credits": 3},
            ]
        },
    },

    "2023-24": {
        "total_credits": 43,
        "required": [
            {"code": "ACCT 2010", "name": "Financial Accounting",               "credits": 3},
            {"code": "ACCT 2020", "name": "Managerial Accounting",              "credits": 3},
            {"code": "BSNS 1050", "name": "Business as a Profession",           "credits": 2},
            {"code": "BSNS 2310", "name": "Business Analytics",                 "credits": 3},
            {"code": "BSNS 2450", "name": "Data Analysis & Decision-Making",    "credits": 3},
            {"code": "BSNS 2510", "name": "Business Law",                       "credits": 3},
            {"code": "BSNS 2710", "name": "Principles of Marketing",            "credits": 3},
            {"code": "BSNS 2810", "name": "Principles of Management",           "credits": 3},
            {"code": "BSNS 3270", "name": "Operations Management",              "credits": 3},
            {"code": "BSNS 3420", "name": "Business Ethics",                    "credits": 3,
             "also_satisfies": ["F2", "W5"]},
            {"code": "BSNS 4500", "name": "Business Finance",                   "credits": 3},
            {"code": "BSNS 4910", "name": "Senior Capstone in Business",        "credits": 2,
             "also_satisfies": ["WI"]},
            {"code": "ECON 2010", "name": "Macroeconomics",                     "credits": 3},
            {"code": "ECON 2020", "name": "Microeconomics",                     "credits": 3},
        ],
        "math_requirement": {
            "note": "One of the following:",
            "choose_one": [
                {"code": "MATH 1300", "name": "College Algebra",                "credits": 3},
                {"code": "MATH 1400", "name": "Precalculus",                    "credits": 4},
                {"code": "MATH 2010", "name": "Applied Calculus",               "credits": 3},
            ]
        },
    },

    "2024-25": {
        "total_credits": 43,
        "required": [
            {"code": "ACCT 2010", "name": "Financial Accounting",               "credits": 3},
            {"code": "ACCT 2020", "name": "Managerial Accounting",              "credits": 3},
            {"code": "BSNS 1050", "name": "Business as a Profession",           "credits": 2},
            {"code": "BSNS 2310", "name": "Business Analytics",                 "credits": 3},
            {"code": "BSNS 2450", "name": "Data Analysis & Decision-Making",    "credits": 3},
            {"code": "BSNS 2510", "name": "Business Law",                       "credits": 3},
            {"code": "BSNS 2710", "name": "Principles of Marketing",            "credits": 3},
            {"code": "BSNS 2810", "name": "Principles of Management",           "credits": 3},
            {"code": "BSNS 3270", "name": "Operations Management",              "credits": 3},
            {"code": "BSNS 3420", "name": "Business Ethics",                    "credits": 3,
             "also_satisfies": ["F2", "W5"]},
            {"code": "BSNS 4500", "name": "Business Finance",                   "credits": 3},
            {"code": "BSNS 4910", "name": "Senior Capstone in Business",        "credits": 2,
             "also_satisfies": ["WI"]},
            {"code": "ECON 2010", "name": "Macroeconomics",                     "credits": 3},
            {"code": "ECON 2020", "name": "Microeconomics",                     "credits": 3},
        ],
        "math_requirement": {
            "note": "One of the following:",
            "choose_one": [
                {"code": "MATH 1300", "name": "College Algebra",                "credits": 3},
                {"code": "MATH 1400", "name": "Precalculus",                    "credits": 4},
                {"code": "MATH 2010", "name": "Applied Calculus",               "credits": 3},
            ]
        },
    },

    "2025-26": {
        "total_credits": 48,
        "required": [
            {"code": "ACCT 2010", "name": "Financial Accounting",               "credits": 3},
            {"code": "ACCT 2020", "name": "Managerial Accounting",              "credits": 3},
            {"code": "BSNS 1050", "name": "Business as a Profession",           "credits": 3},  # 3 hrs (was 2)
            {"code": "BSNS 2310", "name": "Spreadsheet Analytics",             "credits": 3},  # renamed
            {"code": "BSNS 2450", "name": "Principles of Business Analytics",  "credits": 3},  # renamed
            {"code": "BSNS 2510", "name": "Business Law",                       "credits": 3},
            {"code": "BSNS 2550", "name": "Business Communications",            "credits": 3,  # NEW
             "also_satisfies": ["SI"]},
            {"code": "BSNS 2710", "name": "Principles of Marketing",            "credits": 3},
            {"code": "BSNS 2810", "name": "Principles of Management",           "credits": 3},
            {"code": "BSNS 3120", "name": "Global Business",                    "credits": 3,  # NEW — also AU6
             "also_satisfies": ["AU6"]},
            {"code": "BSNS 3270", "name": "Operations Management",              "credits": 3},
            {"code": "BSNS 3420", "name": "Business Ethics",                    "credits": 3,
             "also_satisfies": ["RC5"]},
            {"code": "BSNS 4500", "name": "Business Finance",                   "credits": 3},
            {"code": "BSNS 4800", "name": "Business Internship",                "credits": 3,  # NEW required
             "also_satisfies": ["Experiential"]},
            {"code": "BSNS 4910", "name": "Senior Seminar in Business & Ethics","credits": 3},  # 3 hrs (was 2); no WI label
            {"code": "ECON 2010", "name": "Macroeconomics",                     "credits": 3},
            {"code": "ECON 2020", "name": "Microeconomics",                     "credits": 3},
        ],
        "math_requirement": None,  # No math requirement in 25-26 core
        "notes": [
            "BSNS 3270 is still in core for 25-26 per catalog listing",
            "No MATH courses required in 25-26 core",
            "BSNS 1050 increased to 3 credits",
            "BSNS 4910 increased to 3 credits, renamed",
            "BSNS 2550 (SI), BSNS 3120, BSNS 4800 are new required core courses",
        ],
    },
}


def get_business_core(catalog_year: str) -> dict:
    """Return the business core requirements for a given catalog year."""
    if catalog_year not in BUSINESS_CORE:
        raise ValueError(f"No business core defined for catalog year: {catalog_year}")
    return BUSINESS_CORE[catalog_year]


def get_core_course_codes(catalog_year: str) -> list:
    """Return a flat list of course codes in the business core for a given year."""
    core = get_business_core(catalog_year)
    codes = [c["code"] for c in core["required"]]
    if core.get("math_requirement"):
        codes += [c["code"] for c in core["math_requirement"]["choose_one"]]
    return codes


def is_core_course(course_code: str, catalog_year: str) -> bool:
    """Check if a course code is in the business core for a given year."""
    return course_code in get_core_course_codes(catalog_year)
