"""
Anderson University — Major Requirement Definitions
Pilot majors: Political Science, Accounting, Visual Communication

Each major is defined as a dict with:
  - name: Display name
  - total_credits: Required major credits
  - required: List of individually required course codes
  - dist_groups: List of distribution groups (choose N credits from list)
  - elective_credits: Free elective credits from major dept
  - notes: Any special notes

All course codes are stored in DEPT_NNNN format (underscore, no dash).
"""

MAJOR_REQUIREMENTS = {

    # ─────────────────────────────────────────────────────────────────────────
    # POLITICAL SCIENCE
    # Source: Political Science Advising Sheet 2022-23
    # ─────────────────────────────────────────────────────────────────────────
    "political_science": {
        "2022-23": {
            "name": "Political Science",
            "total_credits": 36,
            "required": [
                "POSC_2020",   # Introduction to World Politics (3)
                "POSC_2100",   # American National Government (3)
                "POSC_2200",   # Public Policy (3)
                "POSC_2400",   # Social Science Research Methods (3)
                "MATH_2120",   # Introductory Statistics (3)
                "POSC_4930",   # Senior Seminar (3)
            ],
            "dist_groups": [
                {
                    "name": "American Politics",
                    "credits_required": 6,
                    "min_courses": 2,
                    "choose_from": ["POSC_3140", "POSC_3211", "POSC_3212"],
                },
                {
                    "name": "International/Comparative Politics",
                    "credits_required": 6,
                    "min_courses": 2,
                    "choose_from": ["POSC_3300", "POSC_3400", "POSC_3510"],
                },
            ],
            "elective_credits": 9,
            "elective_dept": ["POSC"],
            "elective_note": "9 credits of POSC electives (no more than 5 hrs from POSC-2810, 4800, 4810, 4820)",
            "notes": "No more than 5 hrs from POSC-2810, 4800, 4810, 4820.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ACCOUNTING
    # Source: Accounting Advising Sheet June 2022
    # ─────────────────────────────────────────────────────────────────────────
    "accounting": {
        "2022-23": {
            "name": "Accounting",
            "total_credits": 63,
            "required": [
                # Business Core (required for all FSB majors)
                "BSNS_1050",   # Business as a Profession (2)
                "BSNS_2010",   # Financial Accounting (3)
                "BSNS_2020",   # Managerial Accounting (3)
                "BSNS_2450",   # Data Analysis and Decision Making (3)
                "BSNS_2550",   # Organizational Behavior (3)
                "BSNS_2810",   # Principles of Marketing (3)
                "BSNS_3120",   # Business Communication (3)
                "BSNS_3210",   # Business Presentations (3)
                "BSNS_3420",   # Business Ethics (3)
                "BSNS_3510",   # Operations Management (3)
                "BSNS_4910",   # Business Strategy (3)
                "ECON_2010",   # Principles of Microeconomics (3)
                "ECON_2020",   # Principles of Macroeconomics (3)
                "MATH_1300",   # Finite Mathematics (3) — or higher
                # Accounting Major Core
                "ACCT_2020",   # Cost Accounting (3)
                "ACCT_3010",   # Intermediate Accounting I (3)
                "ACCT_3020",   # Intermediate Accounting II (3)
                "ACCT_3500",   # Accounting Information Systems (3)
                "ACCT_3860",   # Federal Income Tax (3)
                "ACCT_4020",   # Advanced Accounting (3)
                "ACCT_4900",   # Auditing (3)
            ],
            "dist_groups": [],
            "elective_credits": 0,
            "notes": "CPA track requires ACCT-4860 (Advanced Tax). 150-hour CPA requirement may require additional coursework.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },

    # ─────────────────────────────────────────────────────────────────────────
    # VISUAL COMMUNICATION
    # Source: Visual Communications Major Advising Sheet
    # ─────────────────────────────────────────────────────────────────────────
    "visual_communication": {
        "2022-23": {
            "name": "Visual Communication",
            "total_credits": 57,
            "required": [
                # Art Foundation (required)
                "ARTS_1100",   # Drawing I (3)
                "ARTS_1200",   # 2D Design (3)
                "ARTS_1300",   # 3D Design (3)
                "ARTH_2000",   # Art History Survey I (3)
                # Visual Communication Core
                "ARTS_2200",   # Typography (3)
                "ARTS_2210",   # Graphic Design I (3)
                "ARTS_2220",   # Digital Photography (3)
                "ARTS_3200",   # Graphic Design II (3)
                "ARTS_3210",   # Illustration (3)
                "ARTS_3220",   # Web Design (3)
                "ARTS_3230",   # Motion Graphics (3)
                "ARTS_4200",   # Advanced Graphic Design (3)
                "ARTS_4210",   # Portfolio Development (3)
                "ARTH_3030",   # Modern Art History (3)
                "ARTH_4800",   # Art Senior Seminar / Internship (3)
            ],
            "dist_groups": [
                {
                    "name": "Visual Communication Electives",
                    "credits_required": 9,
                    "min_courses": 3,
                    "choose_from": [
                        "ARTS_3240", "ARTS_3250", "ARTS_3260", "ARTS_3270",
                        "ARTS_4220", "ARTS_4230", "ARTS_4240", "ARTS_4250",
                        "COMM_2550", "COMM_3050",
                    ],
                },
            ],
            "elective_credits": 0,
            "notes": "Portfolio review required for graduation.",
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
    },
}


def get_major_requirements(major_key: str, catalog_year: str) -> dict | None:
    """
    Return the requirement dict for a given major and catalog year.
    Resolves 'same_as' references automatically.
    Returns None if not found.
    """
    major_data = MAJOR_REQUIREMENTS.get(major_key.lower())
    if not major_data:
        return None
    year_data = major_data.get(catalog_year)
    if not year_data:
        return None
    # Resolve same_as reference
    if "same_as" in year_data:
        year_data = major_data.get(year_data["same_as"])
    return year_data


def list_available_majors() -> list:
    """Return list of all defined major keys."""
    return list(MAJOR_REQUIREMENTS.keys())
