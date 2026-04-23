import sys
sys.path.insert(0, "/home/ubuntu/au-original-restored")
import engines.sport_marketing as sm
import importlib
importlib.reload(sm)

sm.MAJOR_KEY = "finance"
sm.CATALOG_YEAR = "2022-23"

raw_courses = sm.parse_csv("/home/ubuntu/upload/KamilleRinas.csv")

# Simulate what build_la_rows_for_non_fsb does for W2
from requirements.liberal_arts_requirements import LA_OLD_FRAMEWORK as fw

yr = "2022-23"
w2_opts = fw["W2"]["courses"].get(yr, [])
print("W2 course options:", w2_opts)
print()

# Check best() for W2 options
result = sm.best(raw_courses, [sm.norm(c.replace(" ", "_").replace("-", "_")) for c in w2_opts])
print(f"best() result for W2 opts: {result}")
print()

# Check status_of
if result:
    print(f"status_of: {sm.done(result)}, grade={result.get('grade')}, status={result.get('status')}")
else:
    print("No match found — checking each option manually:")
    cm = {c["code"]: c for c in raw_courses}
    for opt in w2_opts:
        code = sm.norm(opt.replace(" ", "_").replace("-", "_"))
        c = cm.get(code)
        if c:
            print(f"  {code}: found, done={sm.done(c)}, drop={sm.drop(c)}, grade={c.get('grade')}")
        else:
            print(f"  {code}: NOT in transcript")
