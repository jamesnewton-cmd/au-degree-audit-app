"""
Anderson University — Falls School of Business
Major Requirements: All 4 Catalog Years

Majors included:
  - Sport Marketing / Sports Management
  - Marketing
  - Management
  - Accounting
  - Finance
  - Business Analytics (23-24+)
  - Engineering Management
  - Global Business (22-23, 23-24 only)
  - Music & Entertainment Business (22-23 only)
  - Business & Integrative Leadership (adult online, all years)
"""

# ─────────────────────────────────────────────
# SPORT MARKETING / SPORTS MANAGEMENT
# ─────────────────────────────────────────────

SPORT_MARKETING = {
    "2022-23": {
        "name": "Sport Marketing",
        "total_credits": 66,
        "uses_business_core": True,
        "major_courses": [
            {"code": "BSNS 3130", "name": "Sport Marketing",                    "credits": 3},
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations (SI)",        "credits": 3,
             "also_satisfies": ["F4 SI"]},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 4110", "name": "Marketing Research (WI)",            "credits": 3},
            {"code": "BSNS 4330", "name": "Marketing Management",               "credits": 3},
            {"code": "BSNS 4360", "name": "Sport Sponsorship and Sales",        "credits": 3},
            {"code": "BSNS 4560", "name": "Business of Game-Day Experience",    "credits": 3},
            {"code": "BSNS 4800", "name": "BSNS-3850 Practicum / BSNS-4800 Internship", "credits": 4,
             "also_satisfies": ["W8"]},
        ],
        "elective_notes": None,
    },
    "2023-24": {
        "name": "Sport Marketing",
        "total_credits": 66,
        "uses_business_core": True,
        "major_courses": [
            {"code": "BSNS 3130", "name": "Sport Marketing",                    "credits": 3},
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations (SI)",        "credits": 3,
             "also_satisfies": ["F4 SI"]},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 4110", "name": "Marketing Research (WI)",            "credits": 3},
            {"code": "BSNS 4330", "name": "Marketing Management",               "credits": 3},
            {"code": "BSNS 4360", "name": "Sport Sponsorship and Sales",        "credits": 3},
            {"code": "BSNS 4560", "name": "Business of Game-Day Experience",    "credits": 3},
            {"code": "BSNS 4800", "name": "BSNS-3850 Practicum / BSNS-4800 Internship", "credits": 4,
             "also_satisfies": ["W8"]},
        ],
        "elective_notes": None,
    },
    "2024-25": {
        "name": "Sport Marketing",
        "total_credits": 66,
        "uses_business_core": True,
        "major_courses": [
            {"code": "BSNS 3130", "name": "Sport Marketing",                    "credits": 3},
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations (SI)",        "credits": 3,
             "also_satisfies": ["F4 SI"]},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 4110", "name": "Marketing Research (WI)",            "credits": 3},
            {"code": "BSNS 4330", "name": "Marketing Management",               "credits": 3},
            {"code": "BSNS 4360", "name": "Sport Sponsorship and Sales",        "credits": 3},
            {"code": "BSNS 4560", "name": "Business of Game-Day Experience",    "credits": 3},
            {"code": "BSNS 4800", "name": "BSNS-3850 Practicum / BSNS-4800 Internship", "credits": 4,
             "also_satisfies": ["W8"]},
        ],
        "elective_notes": None,
    },
    "2025-26": {
        "name": "Sports Management",
        "total_credits": 66,
        "uses_business_core": True,  # 48-hr core
        "major_courses": [
            {"code": "BSNS 3130", "name": "Sports Management",                  "credits": 3},  # renamed
            {"code": "BSNS 4360", "name": "Sports Sponsorship and Sales",       "credits": 3},
            {"code": "BSNS 4560", "name": "Game Day Experience Management",     "credits": 3},  # renamed; prereq: BSNS 3130 only
            {"code": "COMM 2130", "name": "Sports Media",                       "credits": 3},  # NEW
            {"code": "COMM 2140", "name": "Sports Broadcasting",                "credits": 3},  # NEW
            {"code": "SPRL 3300", "name": "Sport and Recreation Leadership",    "credits": 3},  # NEW
        ],
        "notes": [
            "BSNS 3210, 3220, 4110, 4330 removed from major",
            "BSNS 4800 now part of the 48-hr business core (no longer listed separately here)",
            "Pivots from marketing electives to sport facility/event operations + communication",
        ],
    },
}

# ─────────────────────────────────────────────
# MARKETING
# ─────────────────────────────────────────────

MARKETING = {
    "2022-23": {
        "name": "Marketing",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 4110", "name": "Marketing Research",                 "credits": 3},
            {"code": "BSNS 4330", "name": "Integrated Marketing Communications","credits": 3},
        ],
        "concentrations": {
            "Marketing Strategy": [
                {"code": "BSNS 3210", "credits": 3},
                {"code": "BSNS 3510", "credits": 3},
                {"code": "BSNS 3550", "credits": 3},
            ],
            "Social Media": [
                {"code": "BSNS 3400", "credits": 3},
                {"code": "BSNS 4400", "credits": 3},
            ],
            "Integrated Brand Promotion": [
                {"code": "BSNS 3550", "credits": 3},
                {"code": "BSNS 4550", "credits": 3},
            ],
            "Global": [
                {"code": "BSNS 3120", "credits": 3},
                {"code": "BSNS 4250", "credits": 3},
            ],
            "Music & Entertainment": [
                {"code": "BSNS 3360", "credits": 3},
                {"code": "BSNS 3330", "credits": 3},
            ],
        },
    },
    "2023-24": {
        "name": "Marketing",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations",             "credits": 3,
             "also_satisfies": ["F4 SI"]},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 3400", "name": "Digital Marketing & Social Media",   "credits": 3},
            {"code": "BSNS 3550", "name": "Brand Strategy",                     "credits": 3},
            {"code": "BSNS 4330", "name": "Integrated Marketing Communications","credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["BSNS 4400", "BSNS 3550", "COMM 2200", "COMM 2240"],
        },
        "concentrations": None,
    },
    "2024-25": {
        "name": "Marketing",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations",             "credits": 3,
             "also_satisfies": ["F4 SI"]},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 3400", "name": "Digital Marketing & Social Media",   "credits": 3},
            {"code": "BSNS 3550", "name": "Brand Strategy",                     "credits": 3},
            {"code": "BSNS 4330", "name": "Integrated Marketing Communications","credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["BSNS 3550", "BSNS 4400", "COMM 2200", "COMM 2240"],
        },
        "concentrations": None,
    },
    "2025-26": {
        "name": "Marketing",
        "total_credits": 66,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "BSNS 3210", "name": "Buyer/Seller Relations",             "credits": 3},
            {"code": "BSNS 3220", "name": "Consumer Behavior",                  "credits": 3},
            {"code": "BSNS 3400", "name": "Digital Marketing & Social Media",   "credits": 3},
            {"code": "BSNS 3550", "name": "Brand Strategy",                     "credits": 3},
            {"code": "BSNS 4110", "name": "Marketing Research",                 "credits": 3},
            {"code": "BSNS 4330", "name": "Integrated Marketing Communications","credits": 3},
        ],
        "elective": None,  # No elective — all 6 courses required
        "concentrations": None,
    },
}

# ─────────────────────────────────────────────
# MANAGEMENT
# ─────────────────────────────────────────────

MANAGEMENT = {
    "2022-23": {
        "name": "Management",
        "total_credits": 63,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3120", "name": "Global Business",                    "credits": 3,
             "also_satisfies": ["W7", "WI"]},
            {"code": "BSNS 3230", "name": "Human Resource Management",         "credits": 3},
            {"code": "BSNS 4010", "name": "Organizational Behavior",            "credits": 3},
            {"code": "BSNS 4480", "name": "Leadership",                         "credits": 3,
             "also_satisfies": ["F4 SI"]},
        ],
        "choose_one": {
            "note": "BSNS 3850 or BSNS 4800",
            "options": [
                {"code": "BSNS 3850", "name": "Entrepreneurship",              "credits": 3},
                {"code": "BSNS 4800", "name": "Business Internship",           "credits": 3,
                 "also_satisfies": ["W8"]},
            ]
        },
        "electives": {
            "credits": 6,
            "choose_from": [
                "BSNS 3100", "BSNS 3240", "BSNS 3510", "BSNS 4050",
                "BSNS 4120", "BSNS 4240", "BSNS 4310",
            ],
        },
    },
    "2023-24": {
        "name": "Management",
        "total_credits": 63,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3120", "name": "Global Business",                    "credits": 3,
             "also_satisfies": ["W7", "WI"]},
            {"code": "BSNS 3230", "name": "Human Resource Management",         "credits": 3},
            {"code": "BSNS 4010", "name": "Organizational Behavior",            "credits": 3},
            {"code": "BSNS 4480", "name": "Leadership",                         "credits": 3,
             "also_satisfies": ["F4 SI"]},
        ],
        "choose_one": {
            "note": "BSNS 3850 or BSNS 4800",
            "options": [
                {"code": "BSNS 3850", "name": "Entrepreneurship",              "credits": 3},
                {"code": "BSNS 4800", "name": "Business Internship",           "credits": 3,
                 "also_satisfies": ["W8"]},
            ]
        },
        "electives": {
            "credits": 6,
            "choose_from": [
                "BSNS 3100", "BSNS 3240", "BSNS 3510", "BSNS 4050",
                "BSNS 4120", "BSNS 4240", "BSNS 4310",
            ],
        },
    },
    "2024-25": {
        "name": "Management",
        "total_credits": 63,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3120", "name": "Global Business",                    "credits": 3,
             "also_satisfies": ["W7", "WI"]},
            {"code": "BSNS 3230", "name": "Human Resource Management",         "credits": 3},
            {"code": "BSNS 4010", "name": "Organizational Behavior",            "credits": 3},
            {"code": "BSNS 4480", "name": "Leadership",                         "credits": 3,
             "also_satisfies": ["F4 SI"]},
        ],
        "choose_one": {
            "note": "BSNS 3850 or BSNS 4800",
            "options": [
                {"code": "BSNS 3850", "name": "Entrepreneurship",              "credits": 3},
                {"code": "BSNS 4800", "name": "Business Internship",           "credits": 3,
                 "also_satisfies": ["W8"]},
            ]
        },
        "electives": {
            "credits": 6,
            "choose_from": [
                "BSNS 3100", "BSNS 3240", "BSNS 3510", "BSNS 4050",
                "BSNS 4120", "BSNS 4240", "BSNS 4310",
            ],
        },
    },
    "2025-26": {
        "name": "Management",
        "total_credits": 68,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "BSNS 3230", "name": "Human Resource Management",         "credits": 3},
            {"code": "BSNS 3240", "name": "Project Management",                "credits": 3},
            {"code": "BSNS 3270", "name": "Operations Management",             "credits": 3},
            {"code": "BSNS 4010", "name": "Organizational Behavior",            "credits": 3},
            {"code": "BSNS 4310", "name": "Negotiations",                       "credits": 3},
            {"code": "BSNS 4480", "name": "Leadership",                         "credits": 3},
        ],
        "choose_one": None,
        "electives": None,  # No electives — all courses required
        "notes": [
            "BSNS 3120 removed from major (now in core)",
            "BSNS 3240, 3270, 4310 added as required",
            "No 3850/4800 choice — BSNS 4800 now in core",
            "No elective block",
        ],
    },
}

# ─────────────────────────────────────────────
# ACCOUNTING
# ─────────────────────────────────────────────

ACCOUNTING = {
    "2022-23": {
        "name": "Accounting",
        "total_credits": 68,
        "uses_business_core": True,
        "required_courses": [
            {"code": "ACCT 3010", "name": "Intermediate Accounting I",          "credits": 3},
            {"code": "ACCT 3020", "name": "Intermediate Accounting II",         "credits": 3},
            {"code": "ACCT 3110", "name": "Cost Accounting",                    "credits": 3},
            {"code": "ACCT 3500", "name": "Accounting Information Systems",     "credits": 3},
            {"code": "ACCT 4020", "name": "Federal Taxation",                   "credits": 3},
            {"code": "ACCT 4050", "name": "Advanced Accounting",                "credits": 3},
            {"code": "ACCT 4100", "name": "Auditing",                           "credits": 3},
            {"code": "ACCT 4310", "name": "Advanced Topics in Accounting",      "credits": 3},
            {"code": "ACCT 4900", "name": "Accounting Capstone",                "credits": 1},
        ],
        "optional_cma": {
            "note": "Optional CMA pathway adds:",
            "courses": [
                {"code": "BSNS 3240", "credits": 3},
                {"code": "BSNS 3350", "credits": 3},
                {"code": "BSNS 4150", "credits": 3},
            ]
        },
    },
    "2023-24": {
        "name": "Accounting",
        "total_credits": 68,
        "uses_business_core": True,
        "required_courses": [
            {"code": "ACCT 3010", "credits": 3},
            {"code": "ACCT 3020", "credits": 3},
            {"code": "ACCT 3110", "credits": 3},
            {"code": "ACCT 3500", "credits": 3},
            {"code": "ACCT 4020", "credits": 3},
            {"code": "ACCT 4050", "credits": 3},
            {"code": "ACCT 4100", "credits": 3},
            {"code": "ACCT 4310", "credits": 3},
            {"code": "ACCT 4900", "credits": 1},
        ],
        "optional_cma": {
            "courses": ["BSNS 3240", "BSNS 3350", "BSNS 4150"]
        },
    },
    "2024-25": {
        "name": "Accounting",
        "total_credits": 68,
        "uses_business_core": True,
        "required_courses": [
            {"code": "ACCT 3010", "credits": 3},
            {"code": "ACCT 3020", "credits": 3},
            {"code": "ACCT 3110", "credits": 3},
            {"code": "ACCT 3500", "credits": 3},
            {"code": "ACCT 4020", "credits": 3},
            {"code": "ACCT 4050", "credits": 3},
            {"code": "ACCT 4100", "credits": 3},
            {"code": "ACCT 4310", "credits": 3},
            {"code": "ACCT 4900", "credits": 1},
        ],
        "optional_cma": {
            "courses": ["BSNS 3240", "BSNS 3350", "BSNS 4150"]
        },
    },
    "2025-26": {
        "name": "Accounting",
        "total_credits": 73,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "ACCT 3010", "credits": 3},
            {"code": "ACCT 3020", "credits": 3},
            {"code": "ACCT 3110", "credits": 3},
            {"code": "ACCT 3500", "credits": 3},
            {"code": "ACCT 4020", "credits": 3},
            {"code": "ACCT 4050", "credits": 3},
            {"code": "ACCT 4100", "credits": 3},
            {"code": "ACCT 4310", "credits": 3},
            {"code": "ACCT 4900", "credits": 1},
        ],
        "optional_cma": {
            "courses": ["BSNS 3240", "BSNS 3350", "BSNS 4150"]
        },
        "notes": ["Total hours increased from 68 to 73 due to expanded 48-hr core"],
    },
}

# ─────────────────────────────────────────────
# FINANCE
# ─────────────────────────────────────────────

FINANCE = {
    "2022-23": {
        "name": "Finance",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3150", "name": "Investments",                        "credits": 3},
            {"code": "BSNS 3350", "name": "Financial Management",               "credits": 3},
            {"code": "BSNS 4150", "name": "Advanced Financial Management",      "credits": 3},
            {"code": "BSNS 4160", "name": "Capital Markets",                    "credits": 3},
            {"code": "ECON 3410", "name": "Money & Banking",                    "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": [
                "BSNS 3850", "BSNS 4240", "BSNS 4320", "BSNS 4800", "ACCT 4020",
            ],
        },
    },
    "2023-24": {
        "name": "Finance",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3150", "credits": 3},
            {"code": "BSNS 3350", "credits": 3},
            {"code": "BSNS 4150", "credits": 3},
            {"code": "BSNS 4160", "credits": 3},
            {"code": "ECON 3410", "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["BSNS 3850", "BSNS 4240", "BSNS 4320", "BSNS 4800", "ACCT 4020"],
        },
    },
    "2024-25": {
        "name": "Finance",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3150", "credits": 3},
            {"code": "BSNS 3350", "credits": 3},
            {"code": "BSNS 4150", "credits": 3},
            {"code": "BSNS 4160", "credits": 3},
            {"code": "ECON 3410", "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["BSNS 3850", "BSNS 4240", "BSNS 4800", "ACCT 4020"],  # BSNS 4320 removed
        },
    },
    "2025-26": {
        "name": "Finance",
        "total_credits": 66,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "BSNS 3150", "credits": 3},
            {"code": "BSNS 3350", "credits": 3},
            {"code": "BSNS 4150", "credits": 3},
            {"code": "BSNS 4160", "credits": 3},
            {"code": "ECON 3410", "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["BSNS 4160", "ACCT 4020"],  # Narrowed in 25-26
        },
    },
}

# ─────────────────────────────────────────────
# BUSINESS ANALYTICS (New in 23-24)
# ─────────────────────────────────────────────

BUSINESS_ANALYTICS = {
    "2022-23": None,  # Does not exist
    "2023-24": {
        "name": "Business Analytics",
        "total_credits": 64,
        "uses_business_core": True,
        "required_courses": [
            {"code": "CPSC 2020", "name": "Intro to Programming",               "credits": 3},
            {"code": "CPSC 2040", "name": "Introduction to Data Science",       "credits": 3},
            {"code": "CPSC 2100", "name": "Database Management",                "credits": 3},
            {"code": "BSNS 3390", "name": "Business Analytics Applications",    "credits": 3},
            {"code": "BSNS 4390", "name": "Advanced Business Analytics",        "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["CPSC 2080", "CPSC 2330", "CPSC 4100"],
        },
    },
    "2024-25": {
        "name": "Business Analytics",
        "total_credits": 64,
        "uses_business_core": True,
        "required_courses": [
            {"code": "CPSC 2020", "credits": 3},
            {"code": "CPSC 2040", "credits": 3},
            {"code": "CPSC 2100", "credits": 3},
            {"code": "BSNS 3390", "credits": 3},
            {"code": "BSNS 4390", "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["CPSC 2080", "CPSC 2330", "CPSC 4100"],
        },
    },
    "2025-26": {
        "name": "Business Analytics",
        "total_credits": 67,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "CPSC 2020", "credits": 3},
            {"code": "CPSC 2040", "credits": 3},
            {"code": "CPSC 2100", "credits": 3},
            {"code": "BSNS 3390", "credits": 3},
            {"code": "BSNS 4390", "credits": 3},
        ],
        "elective": {
            "credits": 3,
            "choose_from": ["CPSC 2080", "CPSC 2330", "CPSC 4100"],
        },
    },
}

# ─────────────────────────────────────────────
# ENGINEERING MANAGEMENT
# ─────────────────────────────────────────────

ENGINEERING_MANAGEMENT = {
    "2022-23": {
        "name": "Engineering Management",
        "total_credits": 63,
        "uses_business_core": False,  # Stand-alone core in 22-23
        "standalone_core": [
            {"code": "MATH 1300", "credits": 3},  # or MATH 1400 or MATH 2010
            {"code": "BSNS 2450", "credits": 3},  # or MATH 2120
            {"code": "PHYS 2140", "credits": 4},  # or PHYS 2240
            {"code": "ENGR 2130", "credits": 3},  # or CPSC 2040
            {"code": "ECON 2010", "credits": 3},
            {"code": "ECON 2020", "credits": 3},
            {"code": "ENGR 2001", "credits": 1},
            {"code": "ENGR 2002", "credits": 1},
            {"code": "ENGR 2003", "credits": 1},
            {"code": "ENGR 2060", "credits": 2},
            {"code": "ENGR 2090", "credits": 3},
            {"code": "BSNS 1100", "credits": 1},
            {"code": "BSNS 2710", "credits": 3},
            {"code": "BSNS 2810", "credits": 3},
            {"code": "BSNS 4500", "credits": 3},
            {"code": "BSNS 4910", "credits": 2},
            {"code": "ACCT 2010", "credits": 3},
            {"code": "PSYC 2100", "credits": 4},
        ],
        "concentrations": {
            "note": "Plus a concentration",
            "options": ["Construction Management", "General Engineering Management"],
        },
    },
    "2023-24": {
        "name": "Engineering Management",
        "total_credits": 61,
        "uses_business_core": True,  # Switched to FSB core starting 23-24
        "required_courses": [
            {"code": "ENGR 2001", "credits": 1},
            {"code": "ENGR 2002", "credits": 1},
            {"code": "ENGR 2003", "credits": 1},
            {"code": "ENGR 2090", "credits": 3},
        ],
        "choose_one_tech": {
            "note": "One of:",
            "options": ["ENGR 2310", "CPSC 1400", "CPSC 2180"],
        },
        "electives": {
            "credits": 6,
            "courses": ["BSNS 3510", "BSNS 4050"],
            "choose_from": ["BSNS 3230", "BSNS 3850", "BSNS 4010", "BSNS 4480", "BSNS 4800"],
        },
    },
    "2024-25": {
        "name": "Engineering Management",
        "total_credits": 61,
        "uses_business_core": True,
        "required_courses": [
            {"code": "ENGR 2001", "credits": 1},
            {"code": "ENGR 2002", "credits": 1},
            {"code": "ENGR 2003", "credits": 1},
            {"code": "ENGR 2090", "credits": 3},
        ],
        "choose_one_tech": {
            "options": ["ENGR 2310", "CPSC 1400", "CPSC 2180"],
        },
        "electives": {
            "credits": 6,
            "courses": ["BSNS 3510", "BSNS 4050"],
            "choose_from": ["BSNS 3230", "BSNS 3850", "BSNS 4010", "BSNS 4480", "BSNS 4800"],
        },
    },
    "2025-26": {
        "name": "Engineering Management",
        "total_credits": 66,
        "uses_business_core": True,  # 48-hr core
        "required_courses": [
            {"code": "ENGR 2001", "credits": 1},
            {"code": "ENGR 2002", "credits": 1},
            {"code": "ENGR 2003", "credits": 1},
            {"code": "ENGR 2090", "credits": 3},
            {"code": "ENGR 2310", "credits": 3},
            {"code": "BSNS 3240", "credits": 3},
            {"code": "BSNS 3270", "credits": 3},
            {"code": "BSNS 4480", "credits": 3},
        ],
        "notes": [
            "All courses now required — no elective choice block",
            "48-hr business core used",
        ],
    },
}

# ─────────────────────────────────────────────
# GLOBAL BUSINESS (22-23 and 23-24 only)
# ─────────────────────────────────────────────

GLOBAL_BUSINESS = {
    "2022-23": {
        "name": "Global Business",
        "total_credits": 65,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3120", "name": "Global Business",                    "credits": 3,
             "also_satisfies": ["W7", "WI"]},
            {"code": "BSNS 4120", "name": "International Business",             "credits": 3},
        ],
        "concentration_elective": {
            "credits": 3,
            "note": "3 hrs from one concentration: Accounting, Economics, Finance, Management, Marketing, or IBI",
        },
    },
    "2023-24": {
        "name": "Global Business",
        "total_credits": 65,
        "uses_business_core": True,
        "required_courses": [
            {"code": "BSNS 3120", "credits": 3, "also_satisfies": ["W7", "WI"]},
            {"code": "BSNS 4120", "credits": 3},
        ],
        "concentration_elective": {
            "credits": 3,
            "note": "3 hrs from concentration",
        },
    },
    "2024-25": None,  # Removed
    "2025-26": None,  # Removed
}

# ─────────────────────────────────────────────
# MUSIC & ENTERTAINMENT BUSINESS (22-23 only)
# ─────────────────────────────────────────────

MUSIC_ENTERTAINMENT_BUSINESS = {
    "2022-23": {
        "name": "Music and Entertainment Business",
        "total_credits": 52,
        "uses_business_core": False,  # Partial core only
        "required_courses": [
            {"code": "ACCT 2010", "credits": 3},
            {"code": "ECON 2010", "credits": 3},
            {"code": "BSNS 2310", "credits": 3},
            {"code": "BSNS 2450", "credits": 3},
            {"code": "BSNS 2510", "credits": 3},
            {"code": "BSNS 2710", "credits": 3},
            {"code": "BSNS 3270", "credits": 3},
            {"code": "BSNS 3320", "credits": 3},
            {"code": "BSNS 3330", "credits": 3},
            {"code": "BSNS 3360", "credits": 3},
            {"code": "BSNS 3550", "credits": 3},
            {"code": "BSNS 4400", "credits": 3},
            {"code": "BSNS 4500", "credits": 3},
            {"code": "BSNS 4550", "credits": 3},
            {"code": "MUBS 2010", "credits": 3},
            {"code": "MUBS 2020", "credits": 3},
            {"code": "MUBS 3100", "credits": 3},
        ],
        "internship": {
            "note": "4 hrs from BSNS 4810 or BSNS 4800",
            "options": ["BSNS 4810", "BSNS 4800"],
            "credits": 4,
        },
    },
    "2023-24": None,  # Removed
    "2024-25": None,
    "2025-26": None,
}

# ─────────────────────────────────────────────
# BUSINESS & INTEGRATIVE LEADERSHIP (Adult Online)
# ─────────────────────────────────────────────

BUSINESS_INTEGRATIVE_LEADERSHIP = {
    "2022-23": {
        "name": "Business & Integrative Leadership",
        "delivery": "Adult Online",
        "total_credits": 120,  # Full degree
        "lead_courses_credits": 39,
        "lead_courses": [
            "LEAD 2300", "LEAD 3000", "LEAD 3100", "LEAD 3200",
            "LEAD 3260", "LEAD 3280", "LEAD 3300", "LEAD 3500",
            "LEAD 4000", "LEAD 4100", "LEAD 4300", "LEAD 4550", "LEAD 4990",
        ],
        "la_credits": 43,
        "elective_credits": 38,
    },
    "2023-24": {
        "name": "Business & Integrative Leadership",
        "delivery": "Adult Online",
        "total_credits": 120,
        "lead_courses": [
            "LEAD 2300", "LEAD 3000", "LEAD 3100", "LEAD 3200",
            "LEAD 3260", "LEAD 3280", "LEAD 3300", "LEAD 3500",
            "LEAD 4000", "LEAD 4100", "LEAD 4300", "LEAD 4550", "LEAD 4990",
        ],
    },
    "2024-25": {
        "name": "Business & Integrative Leadership",
        "delivery": "Adult Online",
        "total_credits": 120,
        "lead_courses": [
            "LEAD 2300", "LEAD 3000", "LEAD 3100", "LEAD 3200",
            "LEAD 3260", "LEAD 3280", "LEAD 3300", "LEAD 3500",
            "LEAD 4000", "LEAD 4100", "LEAD 4300", "LEAD 4550", "LEAD 4990",
        ],
    },
    "2025-26": {
        "name": "Business & Integrative Leadership",
        "delivery": "Adult Online",
        "total_credits": 120,
        "lead_courses": [
            "LEAD 2300", "LEAD 3000", "LEAD 3100", "LEAD 3200",
            "LEAD 3260", "LEAD 3280", "LEAD 3300", "LEAD 3500",
            "LEAD 4000", "LEAD 4100", "LEAD 4300", "LEAD 4550", "LEAD 4990",
        ],
    },
}


# ─────────────────────────────────────────────
# MASTER LOOKUP
# ─────────────────────────────────────────────

FSB_MAJORS = {
    "sport_marketing":              SPORT_MARKETING,
    "marketing":                    MARKETING,
    "management":                   MANAGEMENT,
    "accounting":                   ACCOUNTING,
    "finance":                      FINANCE,
    "business_analytics":           BUSINESS_ANALYTICS,
    "engineering_management":       ENGINEERING_MANAGEMENT,
    "global_business":              GLOBAL_BUSINESS,
    "music_entertainment_business": MUSIC_ENTERTAINMENT_BUSINESS,
    "business_integrative_leadership": BUSINESS_INTEGRATIVE_LEADERSHIP,
}


def get_major_requirements(major_key: str, catalog_year: str) -> dict | None:
    """
    Return requirements for a given major and catalog year.
    Returns None if the major does not exist in that catalog year.
    """
    major = FSB_MAJORS.get(major_key)
    if major is None:
        raise ValueError(f"Unknown major key: {major_key}")
    return major.get(catalog_year)


def get_major_course_codes(major_key: str, catalog_year: str) -> list:
    """Return a flat list of required course codes for a major/year."""
    req = get_major_requirements(major_key, catalog_year)
    if not req:
        return []
    codes = [c["code"] for c in req.get("required_courses", [])]
    for opt in req.get("choose_one", {}).get("options", []):
        codes.append(opt["code"])
    return codes


def major_exists(major_key: str, catalog_year: str) -> bool:
    """Check if a major exists for a given catalog year."""
    req = get_major_requirements(major_key, catalog_year)
    return req is not None
