"""
Anderson University — Falls School of Business
Minor Requirements: All 4 Catalog Years

Minors:
  - Sport Marketing / Sports Management
  - Accounting
  - Economics
  - Entrepreneurship
  - Finance
  - Global Business
  - Management
  - Marketing
  - Music & Entertainment Business
  - Social Media
"""

FSB_MINORS = {
    "sport_marketing_minor": {
        "2022-23": {
            "name": "Sport Marketing Minor",
            "total_credits": 18,
            "fsb_majors_track": {
                "required": ["BSNS 3130", "BSNS 4360", "BSNS 4560"],
                "choose_6_from": ["BSNS 3210", "BSNS 3220", "BSNS 3550", "BSNS 4400", "BSNS 4550", "BSNS 4800"],
            },
            "non_fsb_track": {
                "required": ["BSNS 2810"],
                "choose_12_from_sm_major": True,
                "plus_3_from_core": True,
            },
        },
        "2023-24": {
            "name": "Sport Marketing Minor",
            "total_credits": 18,
            "fsb_majors_track": {
                "required": ["BSNS 3130", "BSNS 4360", "BSNS 4560"],
                "choose_6_from": ["BSNS 3210", "BSNS 3220", "BSNS 3550", "BSNS 4400", "BSNS 4550", "BSNS 4800"],
            },
            "non_fsb_track": {
                "required": ["BSNS 2810"],
                "choose_12_from_sm_major": True,
                "plus_3_from_core": True,
            },
        },
        "2024-25": {
            "name": "Sport Marketing Minor",
            "total_credits": 18,
            "fsb_majors_track": {
                "required": ["BSNS 3130", "BSNS 4360", "BSNS 4560"],
                "choose_6_from": ["BSNS 3210", "BSNS 3220", "BSNS 3550", "BSNS 4400", "BSNS 4550", "BSNS 4800"],
            },
            "non_fsb_track": {
                "required": ["BSNS 2810"],
                "choose_12_from_sm_major": True,
                "plus_3_from_core": True,
            },
        },
        "2025-26": {
            "name": "Sports Management Minor",
            "total_credits": 18,
            "fsb_majors_track": {
                "required": ["BSNS 3130", "BSNS 4360", "BSNS 4560"],
                "choose_6_from": ["COMM 2130", "COMM 2140", "SPRL 3300"],
            },
            "non_fsb_track": {
                "required": ["BSNS 2810"],
                "choose_12_from_sm_major": True,
                "plus_3_from_core": True,
            },
        },
    },

    "accounting_minor": {
        "2022-23": {
            "name": "Accounting Minor",
            "total_credits": 15,
            "required": ["ACCT 2010", "ACCT 2020"],
            "choose_9_from": ["ACCT 3010", "ACCT 3020", "ACCT 3110", "ACCT 3500", "ACCT 4020", "ACCT 4050", "ACCT 4100"],
        },
        "2023-24": {"same_as": "2022-23", "name": "Accounting Minor", "total_credits": 15},
        "2024-25": {"same_as": "2022-23", "name": "Accounting Minor", "total_credits": 15},
        "2025-26": {"same_as": "2022-23", "name": "Accounting Minor", "total_credits": 15},
    },

    "economics_minor": {
        "2022-23": {
            "name": "Economics Minor",
            "total_credits": 18,
            "required": ["ECON 2010", "ECON 2020", "ECON 3020", "ECON 3410"],
            "choose_6_from": [
                "ECON 3110", "ECON 3210", "ECON 3850", "ECON 4020",
                "BSNS 4240", "POSC 2200",
            ],
        },
        "2023-24": {"same_as": "2022-23", "name": "Economics Minor", "total_credits": 18},
        "2024-25": {"same_as": "2022-23", "name": "Economics Minor", "total_credits": 18},
        "2025-26": {"same_as": "2022-23", "name": "Economics Minor", "total_credits": 18},
    },

    "entrepreneurship_minor": {
        "2022-23": {
            "name": "Entrepreneurship Minor",
            "fsb_total": 18,
            "non_fsb_total": 15,
            "core_required": ["BSNS 2810", "BSNS 3850"],
            "choose_from": ["BSNS 3100", "BSNS 3240", "BSNS 3510", "BSNS 4050"],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },

    "finance_minor": {
        "2022-23": {
            "name": "Finance Minor",
            "total_credits": 18,
            "required": ["ACCT 2010", "BSNS 2510", "BSNS 3350", "BSNS 4150", "ECON 3410"],
            "elective": {
                "credits": 3,
                "choose_from": ["BSNS 3150", "BSNS 4160", "BSNS 4240", "BSNS 4320"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },

    "global_business_minor": {
        "2022-23": {
            "name": "Global Business Minor",
            "fsb_total": 15,
            "non_fsb_total": 18,
            "required": ["BSNS 3120", "BSNS 4120", "BSNS 4250"],
            "choose_from": ["BSNS 3550", "BSNS 4400", "BSNS 4550", "ECON 3850"],
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },

    "management_minor": {
        "2022-23": {
            "name": "Management Minor",
            "fsb_total": 15,
            "non_fsb_total": 18,
            "required": ["BSNS 2810", "BSNS 3230", "BSNS 4010", "BSNS 4480"],
            "elective": {
                "credits": 3,
                "choose_from": ["BSNS 3100", "BSNS 3240", "BSNS 3510", "BSNS 4050"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },

    "marketing_minor": {
        "2022-23": {
            "name": "Marketing Minor",
            "total_credits": 18,
            "required": ["BSNS 2710", "BSNS 3210", "BSNS 3220", "BSNS 4110", "BSNS 4330"],
            "elective": {
                "credits": 3,
                "choose_from": ["BSNS 3400", "BSNS 3550", "BSNS 4400", "COMM 2200"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },

    "music_entertainment_business_minor": {
        "2022-23": {
            "name": "Music & Entertainment Business Minor",
            "total_credits": 18,
            "required": ["BSNS 3320", "BSNS 3330", "BSNS 3360", "MUBS 2010", "MUBS 2020", "MUBS 3100"],
        },
        "2023-24": None,  # Major removed, minor may also be gone — verify
        "2024-25": None,
        "2025-26": None,
    },

    "social_media_minor": {
        "2022-23": {
            "name": "Social Media Minor",
            "total_credits": 15,
            "required": ["BSNS 3400", "BSNS 4400", "COMM 2200"],
            "elective": {
                "credits": 6,
                "choose_from": ["BSNS 3550", "BSNS 4550", "COMM 2240", "COMM 3150"],
            },
        },
        "2023-24": {"same_as": "2022-23"},
        "2024-25": {"same_as": "2022-23"},
        "2025-26": {"same_as": "2022-23"},
    },
}


def get_minor_requirements(minor_key: str, catalog_year: str) -> dict | None:
    minor = FSB_MINORS.get(minor_key)
    if minor is None:
        raise ValueError(f"Unknown minor key: {minor_key}")
    result = minor.get(catalog_year)
    # Resolve "same_as" references
    if isinstance(result, dict) and "same_as" in result:
        base = minor[result["same_as"]].copy()
        base.update({k: v for k, v in result.items() if k != "same_as"})
        return base
    return result
