"""
Patch: Add elective_groups handling inside _process_conc_block in main.py.
The existing sub-block loop skips elective_groups because it's a list of dicts,
not a single dict with a 'credits' key. We insert a handler before the loop.
"""

with open("/home/ubuntu/au-original-restored/main.py", "r") as f:
    src = f.read()

OLD = '''                    # Process elective/choose sub-blocks
                    for sub_key, sub_val in cval.items():
                        if sub_key in ("required", "notes", "name"):
                            continue
                        if not isinstance(sub_val, dict) or "credits" not in sub_val:
                            continue'''

NEW = '''                    # Process elective_groups (list of dicts with label/credits/courses)
                    if "elective_groups" in cval:
                        for eg in cval["elective_groups"]:
                            eg_label = eg.get("label", "Elective")
                            eg_credits = _safe_credits(eg.get("credits", 3))
                            eg_courses = eg.get("courses", eg.get("choose_from", []))
                            eg_dept = eg.get("dept", "")
                            full_label = f"{label_prefix} {eg_label}"
                            # Sum credits of qualifying courses from pool
                            sm_norm = sm_mod.norm
                            pool_codes = [sm_norm(c.replace("-","_")) for c in eg_courses]
                            dept_list = [eg_dept] if isinstance(eg_dept, str) and eg_dept else (eg_dept if isinstance(eg_dept, list) else [])
                            dept_pfx = tuple(d.upper() for d in dept_list)
                            earned = 0.0
                            best_c = None
                            for rc in raw_courses:
                                if _status_of_c(rc) not in ("Satisfied", "Current", "Scheduled"):
                                    continue
                                if rc["code"] in pool_codes or (dept_pfx and rc["raw"].upper().startswith(dept_pfx)):
                                    earned += rc["cr"]
                                    if best_c is None:
                                        best_c = rc
                            if earned >= eg_credits:
                                status = "Satisfied"
                            elif earned > 0:
                                status = "Current"
                            else:
                                status = "Not Satisfied"
                            conc_rows.append({
                                "id": _norm_code(f"conc_eg_{eg_label}"),
                                "label": full_label,
                                "status": status,
                                "course": best_c,
                                "dcr": eg_credits,
                                "note": f"{earned:.0f}/{eg_credits:.0f} cr earned",
                            })
                    # Process elective/choose sub-blocks
                    for sub_key, sub_val in cval.items():
                        if sub_key in ("required", "notes", "name", "elective_groups"):
                            continue
                        if not isinstance(sub_val, dict) or "credits" not in sub_val:
                            continue'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    with open("/home/ubuntu/au-original-restored/main.py", "w") as f:
        f.write(src)
    print("SUCCESS: elective_groups handling added to _process_conc_block")
else:
    print("ERROR: anchor text not found")
    idx = src.find("# Process elective/choose sub-blocks")
    print(repr(src[idx:idx+300]))
