"""
Patch: Add three concentrations to exercise_science 2022-23 (and 2023-24 via same_as).
Concentrations: Clinical Exercise Physiology, Pre-Health, Sports Performance
"""

with open("/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py", "r") as f:
    src = f.read()

OLD = '''            "notes": "One concentration required: Clinical Exercise Science, Fitness/Performance, or Research/Graduate.",
        },
        "2023-24": {"same_as": "2022-23"},'''

NEW = '''            "concentrations": {
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
        "2023-24": {"same_as": "2022-23"},'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    with open("/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py", "w") as f:
        f.write(src)
    print("SUCCESS: exercise_science concentrations added")
else:
    print("ERROR: anchor text not found")
    # Show context around the notes line
    idx = src.find("One concentration required")
    print(repr(src[idx-50:idx+200]))
