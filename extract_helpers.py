"""
Extracts shared helper functions from main_unified.py into audit_helpers.py
for use by run_tests.py. Run this whenever main_unified.py changes.

Usage: python3 extract_helpers.py
"""

import ast, sys

with open("main_unified.py") as f:
    src = f.read()

START = "# ── SHARED HELPERS ─────────────────────────────────────────────────────────"
END = "# ── SINGLE UNIFIED GENERATE ENDPOINT ─────────────────────────────────────────"

si = src.find(START)
ei = src.find(END)

if si == -1 or ei == -1:
    print("ERROR: Could not find helper section markers in main_unified.py")
    sys.exit(1)

helpers_src = src[si:ei].strip()

output = f'''"""
AU Degree Audit — Shared Helper Functions
Auto-extracted from main_unified.py by extract_helpers.py.
DO NOT EDIT DIRECTLY — run: python3 extract_helpers.py
"""
import sys
sys.path.insert(0, '/home/claude')

{helpers_src}
'''

try:
    ast.parse(output)
except SyntaxError as e:
    print(f"ERROR: extracted code has syntax error: {e}")
    sys.exit(1)

with open("audit_helpers.py", "w") as f:
    f.write(output)

print("✓ audit_helpers.py regenerated from main_unified.py")
