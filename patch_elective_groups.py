"""
Patch main.py to add Pass 3.5: elective_groups handling.
elective_groups is a list of dicts with structure:
  {name, credits, choose_from (optional), dept (optional), notes (optional)}
This is used by Criminal Justice and many other non-FSB majors.
"""

with open('/home/ubuntu/au-original-restored/main.py', 'r') as f:
    content = f.read()

ANCHOR = '    # -- Pass 4: choose_one groups (cross-listed / either-or courses) --'

INSERTION = '''    # -- Pass 3.5: elective_groups (list of dicts with name/credits/choose_from/dept) --
    # Many non-FSB programs use elective_groups: [{name, credits, choose_from, dept, notes}]
    # These are list-of-dicts so Pass 1 skips them (not list of strings).
    # Pass 2 also misses them (they are not top-level dict keys with 'credits').
    elective_groups = prog_reqs.get("elective_groups", [])
    for eg in elective_groups:
        eg_name = eg.get("name", "Elective")
        eg_credits = _safe_credits(eg.get("credits", 3))
        eg_dept = eg.get("dept", "")
        eg_choose_from = eg.get("choose_from", [])
        eg_notes = eg.get("notes", "")
        # Build label
        if eg_choose_from:
            preview = ", ".join(str(x) for x in eg_choose_from[:3])
            suffix = "..." if len(eg_choose_from) > 3 else ""
            eg_label = f"{eg_name} — {eg_credits} hrs ({preview}{suffix})"
        elif eg_dept:
            dept_str = "/".join(eg_dept) if isinstance(eg_dept, list) else eg_dept
            eg_label = f"{eg_name} — {eg_credits} hrs ({dept_str} elective)"
        else:
            eg_label = f"{eg_name} — {eg_credits} hrs"
        # Find matching course(s)
        if eg_choose_from:
            # Single-slot choose_from: find best match
            c = _find_course(eg_choose_from)
            if c is None and eg_dept:
                dept_list = [eg_dept] if isinstance(eg_dept, str) else eg_dept
                dept_prefixes = tuple(d.upper() for d in dept_list)
                c = next(
                    (x for x in raw_courses
                     if x["raw"].upper().startswith(dept_prefixes)
                     and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")),
                    None,
                )
        elif eg_dept:
            dept_list = [eg_dept] if isinstance(eg_dept, str) else eg_dept
            dept_prefixes = tuple(d.upper() for d in dept_list)
            # For multi-credit elective groups, count how many dept courses are needed
            course_size = 3
            num_needed = max(1, round(eg_credits / course_size))
            # Collect all matching dept courses
            matching = [
                x for x in raw_courses
                if x["raw"].upper().startswith(dept_prefixes)
                and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")
            ]
            if num_needed > 1:
                # Emit one row per slot, using distinct courses
                used_eg_codes = set()
                for slot in range(num_needed):
                    c = next(
                        (x for x in matching if x["code"] not in used_eg_codes),
                        None,
                    )
                    if c:
                        used_eg_codes.add(c["code"])
                    slot_label = f"{eg_label} ({slot+1} of {num_needed})"
                    rows.append({
                        "id": _norm_code(f"{eg_name}_{slot+1}"),
                        "label": slot_label,
                        "status": _status_of_c(c),
                        "course": c,
                        "dcr": course_size,
                        "note": eg_notes,
                    })
                continue  # skip the single-row append below
            else:
                c = matching[0] if matching else None
        else:
            c = None
        rows.append({
            "id": _norm_code(eg_name),
            "label": eg_label,
            "status": _status_of_c(c),
            "course": c,
            "dcr": eg_credits,
            "note": eg_notes,
        })

'''

if ANCHOR not in content:
    print("ERROR: Anchor not found in main.py!")
else:
    new_content = content.replace(ANCHOR, INSERTION + ANCHOR)
    with open('/home/ubuntu/au-original-restored/main.py', 'w') as f:
        f.write(new_content)
    print("SUCCESS: Pass 3.5 elective_groups handling inserted into main.py")
    # Verify
    with open('/home/ubuntu/au-original-restored/main.py', 'r') as f:
        verify = f.read()
    if 'Pass 3.5' in verify:
        print("VERIFIED: Pass 3.5 is in main.py")
    else:
        print("ERROR: Verification failed")
