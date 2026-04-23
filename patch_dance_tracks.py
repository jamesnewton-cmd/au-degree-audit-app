"""
Patch non_fsb_programs.py:
Rebuild dance_major 2022-23 with all four tracks as concentrations.

The advising sheet (Rev'd 5/2022) defines:
  - 22 shared required credit hours (all tracks)
  - 32 track-specific credit hours (one of four tracks)

The old engine had only the Performance track requirements hardcoded
in required[] with no track-selection mechanism.

New structure uses:
  required[]    = 22 shared courses (minus the technique elective groups)
  choose_one[]  = NURS-1210 or PEHS-1450 (Nutrition/First Aid)
  elective_groups[] = technique hour requirements (shared across all tracks)
  concentrations{} = four track dicts, each with required[] and elective sub-blocks
"""

OLD_BLOCK = '''    "dance_major": {
        "2022-23": {
            "name": "Dance",
            "total_credits": 54,
            "required": [
                "DANC-1580",
                "DANC-1590",
                "DANC-3000",
                "DANC-3020",
                "DANC-4500",
                "DANC-2110",
                "DANC-2580",
                "DANC-2590",
                "DANC-3010",
                "DANC-3530",
                "DANC-3580",
                "DANC-3590",
                "DANC-4590",
                "DANC-4910",
                "PEHS-1450",
            ],
            "elective_groups": [
                {"name": "Modern technique", "credits": 3, "choose_from": []},
                {"name": "Ballet technique", "credits": 3, "choose_from": []},
                {"name": "Jazz technique", "credits": 2, "choose_from": []},
                {"name": "Dance performance", "credits": 6, "choose_from": ["DANC-1150"]},
                {"name": "Accompaniment", "credits": 2, "choose_from": ["DANC-1160"]},
                {
                    "name": "Elective one of",
                    "credits": 3,
                    "choose_from": ["DANC-3050", "DANC-3060"],
                },
            ],
            "notes": "One concentration required; see advisor",
        },
        "2023-24": {"same_as": "2022-23"},
    },'''

NEW_BLOCK = '''    "dance_major": {
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
    },'''

with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'r') as f:
    content = f.read()

if OLD_BLOCK not in content:
    print("ERROR: OLD_BLOCK not found in file. Check for whitespace differences.")
    # Show first 200 chars of the dance_major section
    idx = content.find('"dance_major"')
    print("Found dance_major at index:", idx)
    print("Content around it:")
    print(repr(content[idx:idx+500]))
else:
    new_content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
    with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'w') as f:
        f.write(new_content)
    print("Patch applied successfully.")

    # Quick verification
    with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'r') as f:
        verify = f.read()
    if '"Performance"' in verify and '"Business"' in verify and '"Pedagogy"' in verify and '"Science"' in verify:
        print("VERIFIED: All four dance tracks present in file.")
    else:
        print("ERROR: Not all four tracks found after patch.")
