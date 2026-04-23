"""
Patch non_fsb_programs.py:
cybersecurity_major 2022-23: move MATH-2200 from required[] to choose_one[]
as {"name": "Discrete Mathematical Structures", "choose_from": ["MATH-2200", "CPSC-2250"]}
"""

with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'r') as f:
    lines = f.readlines()

# Line 961 (1-indexed) = index 960: '                "MATH-2200",\n'
# Line 974 (1-indexed) = index 973: '                {"name": "Homeland Security", ...}\n'
# Line 975 (1-indexed) = index 974: '            ],\n'  <- end of choose_one

assert lines[960].strip() == '"MATH-2200",', f"Unexpected line 961: {lines[960]!r}"
assert '"Homeland Security"' in lines[973], f"Unexpected line 974: {lines[973]!r}"
assert lines[974].strip() == '],', f"Unexpected line 975: {lines[974]!r}"

# Step 1: Remove MATH-2200 from required (line 961)
lines[960] = ''  # blank it out

# Step 2: Insert Discrete Math choose_one before the closing ], of choose_one
lines[974] = (
    '                {"name": "Discrete Mathematical Structures", '
    '"choose_from": ["MATH-2200", "CPSC-2250"]},\n'
    '            ],\n'
)

with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'w') as f:
    f.writelines(lines)

print("Patch applied. Verifying...")

with open('/home/ubuntu/au-original-restored/requirements/non_fsb_programs.py', 'r') as f:
    content = f.read()

# Verify the 2022-23 block no longer has MATH-2200 in required
# and has Discrete Math in choose_one
import re
block_2223 = re.search(
    r'"cybersecurity_major".*?"2022-23".*?"2023-24"',
    content, re.DOTALL
)
if block_2223:
    block = block_2223.group(0)
    has_math2200_in_required = '"MATH-2200"' in block.split('"choose_one"')[0]
    has_discrete_in_choose_one = 'Discrete Mathematical Structures' in block
    print(f"MATH-2200 still in required section: {has_math2200_in_required}")
    print(f"Discrete Mathematical Structures in choose_one: {has_discrete_in_choose_one}")
    if not has_math2200_in_required and has_discrete_in_choose_one:
        print("VERIFIED: Fix applied correctly")
    else:
        print("ERROR: Fix not applied correctly")
else:
    print("ERROR: Could not find 2022-23 block for verification")
