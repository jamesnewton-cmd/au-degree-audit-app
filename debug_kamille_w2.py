import sys
sys.path.insert(0, "/home/ubuntu/au-original-restored")
import engines.sport_marketing as sm
import importlib
importlib.reload(sm)

raw_courses = sm.parse_csv("/home/ubuntu/upload/KamilleRinas.csv")

# Find BIOL-2210 in parsed courses
print("=== BIOL-2210 entries ===")
for c in raw_courses:
    if "BIOL" in c.get("code", "").upper() or "BIOL" in c.get("raw", "").upper():
        print(c)
        print(f"  done={sm.done(c)}, drop={sm.drop(c)}, xfer={sm.xfer(c)}, ip={sm.ip(c)}")

print()
print("=== All T-grade courses ===")
for c in raw_courses:
    if c.get("grade", "").upper() == "T":
        print(f"  {c['raw']} code={c['code']} status={c['status']} done={sm.done(c)}")
