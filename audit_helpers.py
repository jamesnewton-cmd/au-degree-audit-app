"""
AU Degree Audit — Shared Helper Functions
Auto-extracted from main_unified.py by extract_helpers.py.
DO NOT EDIT DIRECTLY — run: python3 extract_helpers.py
"""

import sys

sys.path.insert(0, "/home/claude")

# ── SHARED HELPERS ────────────────────────────────────────────────────────────
SKIP_KEYS = {
    "name",
    "total_credits",
    "delivery",
    "notes",
    "note",
    "teaching_fields",
    "department",
    "concentration_note",
    "special_rules",
    "same_as",
    "optional_cma",
    "concentrations",
    "tracks",
    "total_major_credits",
    "lead_courses_credits",
    "la_credits",
    "elective_credits",
    "min_level",
    "choose_one",
    "accreditation",
    "prerequisites",
    "dummy_2022_23",
    "dummy_elective",
    "required_old",
    "dept_dummy",
    "upper_div_psyc",
}


def _norm_code(c):
    return c.strip().upper().replace(" ", "_").replace("-", "_")


def _safe_credits(val, fallback=3):
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    if isinstance(val, str):
        try:
            return int(val.split("-")[0])
        except ValueError:
            return fallback
    return fallback


def _status_of_c(c):
    if c is None:
        return "Not Satisfied"
    if c["status"] == "grade posted" and c["grade"].upper() not in ("", "W", "DRP", "NC"):
        return "Satisfied"
    if c["status"] == "current":
        return "Current"
    if c["status"] == "scheduled":
        return "Scheduled"
    return "Not Satisfied"


def _build_major_rows(prog_reqs, raw_courses, sm_mod, concentration=""):
    """
    Dynamically build major requirement rows from a program definition dict.
    Handles: list keys (required courses), dict keys with 'credits' (electives/choose blocks).
    """
    sm_best = sm_mod.best
    sm_norm = sm_mod.norm

    def _find_course(code_list):
        normalized = [sm_norm(c.replace(" ", "_").replace("-", "_")) for c in code_list]
        return sm_best(raw_courses, normalized)

    course_name_lookup = {}
    for _c in raw_courses:
        key = _c["raw"].upper().replace("-", " ")
        if _c.get("name") and _c["name"].strip():
            course_name_lookup[key] = _c["name"].strip()

    def _course_label(course_id, found_course=None):
        code_clean = course_id.strip().upper().replace("-", " ")
        if found_course and found_course.get("name"):
            return f"{course_id} {found_course['name']}"
        name = course_name_lookup.get(code_clean, "")
        return f"{course_id} {name}" if name else course_id

    _skip_keys = {
        "name",
        "total_credits",
        "delivery",
        "notes",
        "teaching_fields",
        "department",
        "concentration_note",
        "special_rules",
        "same_as",
        "optional_cma",
        "concentrations",
        "tracks",
        "total_major_credits",
        "lead_courses_credits",
        "la_credits",
        "elective_credits",
        "min_level",
        "choose_one",
        "accreditation",
    }

    rows = []
    used_required_codes = set()  # track codes already used by required rows

    # Pass 1: list-type keys → individual required course rows
    for req_key, req_val in prog_reqs.items():
        if req_key in _skip_keys:
            continue
        if isinstance(req_val, list) and req_val:
            for course_id in req_val:
                if not isinstance(course_id, str):
                    continue
                if "xxx" in course_id.lower() or course_id.upper().count("X") >= 3:
                    continue
                c = _find_course([course_id])
                rows.append(
                    {
                        "id": _norm_code(course_id),
                        "label": _course_label(course_id, c),
                        "status": _status_of_c(c),
                        "course": c,
                        "dcr": 3,
                        "note": "",
                    }
                )

    # Pass 2: dict-type keys with 'credits' → elective/choose blocks
    for ekey, edef in prog_reqs.items():
        if ekey in _skip_keys:
            continue
        if not isinstance(edef, (dict, int, float)):
            continue
        if isinstance(edef, dict) and "credits" not in edef:
            continue

        if isinstance(edef, dict):
            credits = _safe_credits(edef.get("credits", 3))
            dept = edef.get("dept", "")
            course = edef.get("course", "")
            choose_from = edef.get("choose_from", edef.get("options", edef.get("courses", [])))
            label = edef.get("label", "")
            if not label:
                if course:
                    label = f"{course} ({credits} cr)"
                elif dept:
                    dept_str = "/".join(dept) if isinstance(dept, list) else dept
                    label = f"{dept_str} elective — {credits} hrs"
                elif choose_from:
                    preview = ", ".join(str(x) for x in choose_from[:3])
                    suffix = "..." if len(choose_from) > 3 else ""
                    label = f"Choose from: {preview}{suffix} ({credits} cr)"
                else:
                    label = f"{ekey.replace('_',' ').title()} ({credits} cr)"
            # Skip notes-only blocks with nothing matchable
            if not course and not dept and not choose_from:
                continue
            opts = [course] if course else (choose_from if isinstance(choose_from, list) else [])

            # For multi-course choose blocks (e.g. credits=6 = 2 x 3cr courses),
            # generate one row per required course so each shows separately
            course_size = 3  # most AU courses are 3 credits
            num_needed = max(1, round(credits / course_size)) if not course else 1

            if num_needed > 1 and opts:
                # Find up to num_needed distinct matching courses
                sm_norm = sm_mod.norm
                used_codes = set()
                for slot in range(num_needed):
                    remaining_opts = [
                        o
                        for o in opts
                        if sm_norm(o.replace(" ", "_").replace("-", "_")) not in used_codes
                    ]
                    c = _find_course(remaining_opts) if remaining_opts else None
                    if c:
                        used_codes.add(c["code"])
                    slot_label = f"{label} ({slot+1} of {num_needed})" if c or slot == 0 else label
                    rows.append(
                        {
                            "id": _norm_code(f"{ekey}_{slot+1}"),
                            "label": slot_label,
                            "status": _status_of_c(c),
                            "course": c,
                            "dcr": course_size,
                            "note": "",
                        }
                    )
            else:
                c = _find_course(opts) if opts else None
                if c is None and dept:
                    dept_list = [dept] if isinstance(dept, str) else dept
                    dept_prefixes = tuple(d.upper() for d in dept_list)
                    c = next(
                        (
                            x
                            for x in raw_courses
                            if x["raw"].upper().startswith(dept_prefixes)
                            and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")
                        ),
                        None,
                    )
                rows.append(
                    {
                        "id": _norm_code(ekey),
                        "label": label,
                        "status": _status_of_c(c),
                        "course": c,
                        "dcr": credits,
                        "note": "",
                    }
                )
                if c:
                    used_required_codes.add(c["code"])
        elif isinstance(edef, (int, float)):
            rows.append(
                {
                    "id": _norm_code(ekey),
                    "label": f"{ekey.replace('_',' ').title()} ({int(edef)} hrs)",
                    "status": "Not Satisfied",
                    "course": None,
                    "dcr": int(edef),
                    "note": "",
                }
            )

    # Apply concentration courses if one was selected
    if concentration and isinstance(prog_reqs.get("concentrations"), dict):
        conc_data = prog_reqs["concentrations"].get(concentration)
        if conc_data and isinstance(conc_data, dict):
            conc_rows = []

            def _process_conc_block(ckey, cval, prefix=""):
                """Recursively process a concentration block into audit rows."""
                label_prefix = (
                    f"[{concentration}]" if not prefix else f"[{concentration} — {prefix}]"
                )
                if isinstance(cval, list):
                    for course_id in cval:
                        if not isinstance(course_id, str):
                            continue
                        c = _find_course([course_id])
                        conc_rows.append(
                            {
                                "id": _norm_code(f"conc_{course_id}"),
                                "label": f"{label_prefix} {_course_label(course_id, c)}",
                                "status": _status_of_c(c),
                                "course": c,
                                "dcr": 3,
                                "note": "",
                            }
                        )
                elif isinstance(cval, dict):
                    # Has 'required' list and/or elective sub-blocks
                    if "required" in cval:
                        for course_id in cval["required"]:
                            if not isinstance(course_id, str):
                                continue
                            c = _find_course([course_id])
                            conc_rows.append(
                                {
                                    "id": _norm_code(f"conc_{course_id}"),
                                    "label": f"{label_prefix} {_course_label(course_id, c)}",
                                    "status": _status_of_c(c),
                                    "course": c,
                                    "dcr": 3,
                                    "note": "",
                                }
                            )
                    # Process elective/choose sub-blocks
                    for sub_key, sub_val in cval.items():
                        if sub_key in ("required", "notes", "name"):
                            continue
                        if not isinstance(sub_val, dict) or "credits" not in sub_val:
                            continue
                        credits = _safe_credits(sub_val.get("credits", 3))
                        dept = sub_val.get("dept", "")
                        course = sub_val.get("course", "")
                        choose_from = sub_val.get("choose_from", [])
                        note_txt = sub_val.get("notes", sub_key.replace("_", " ").title())
                        label = f"{label_prefix} {note_txt} ({credits} cr)"
                        if not course and not dept and not choose_from:
                            continue
                        opts = (
                            [course]
                            if course
                            else (choose_from if isinstance(choose_from, list) else [])
                        )
                        # For multi-course blocks find multiple matches
                        course_size = 3
                        num_needed = max(1, round(credits / course_size)) if not course else 1
                        if num_needed > 1 and opts:
                            sm_norm = sm_mod.norm
                            used = set()
                            for slot in range(num_needed):
                                remaining = [
                                    o
                                    for o in opts
                                    if sm_norm(o.replace(" ", "_").replace("-", "_")) not in used
                                ]
                                c = _find_course(remaining) if remaining else None
                                if c is None and dept:
                                    dept_list = [dept] if isinstance(dept, str) else dept
                                    dept_pfx = tuple(d.upper() for d in dept_list)
                                    c = next(
                                        (
                                            x
                                            for x in raw_courses
                                            if x["raw"].upper().startswith(dept_pfx)
                                            and x["code"] not in used
                                            and x["code"] not in used_required_codes
                                            and _status_of_c(x)
                                            in ("Satisfied", "Current", "Scheduled")
                                        ),
                                        None,
                                    )
                                if c:
                                    used.add(c["code"])
                                slot_lbl = (
                                    f"{label} ({slot+1} of {num_needed})"
                                    if num_needed > 1
                                    else label
                                )
                                conc_rows.append(
                                    {
                                        "id": _norm_code(f"conc_{sub_key}_{slot+1}"),
                                        "label": slot_lbl,
                                        "status": _status_of_c(c),
                                        "course": c,
                                        "dcr": course_size,
                                        "note": "",
                                    }
                                )
                        else:
                            c = _find_course(opts) if opts else None
                            if c is None and dept:
                                dept_list = [dept] if isinstance(dept, str) else dept
                                dept_pfx = tuple(d.upper() for d in dept_list)
                                c = next(
                                    (
                                        x
                                        for x in raw_courses
                                        if x["raw"].upper().startswith(dept_pfx)
                                        and x["code"] not in used_required_codes
                                        and _status_of_c(x) in ("Satisfied", "Current", "Scheduled")
                                    ),
                                    None,
                                )
                            conc_rows.append(
                                {
                                    "id": _norm_code(f"conc_{sub_key}"),
                                    "label": label,
                                    "status": _status_of_c(c),
                                    "course": c,
                                    "dcr": credits,
                                    "note": "",
                                }
                            )

            for ckey, cval in conc_data.items():
                if ckey in SKIP_KEYS:
                    continue
                _process_conc_block(ckey, cval)

            rows.extend(conc_rows)

    # Apply MAP exceptions to major rows
    # MAP entries targeting a specific course code inject a satisfied clone
    for c in raw_courses:
        area = c.get("__map_area__")
        if not area:
            continue
        taken_code = c.get("__map_taken_code__", c["code"])
        # Check if any existing row has an id matching the area (normalized)
        area_norm = area.strip().upper().replace("-", "_").replace(" ", "_")
        matched = False
        for row in rows:
            if row["id"] == area_norm:
                # Override this row with the mapped course
                sm_norm = sm_mod.norm
                taken = next((x for x in raw_courses if x["code"] == sm_norm(taken_code)), None)
                if taken:
                    row["course"] = taken
                    row["status"] = _status_of_c(taken)
                matched = True
                break
        if not matched:
            # No existing row for this area — add a new one
            sm_norm = sm_mod.norm
            taken = next((x for x in raw_courses if x["code"] == sm_norm(taken_code)), None)
            if taken:
                rows.append(
                    {
                        "id": area_norm,
                        "label": f"{taken.get('name', taken_code)} (mapped to {area})",
                        "status": _status_of_c(taken),
                        "course": taken,
                        "dcr": taken.get("cr", 3),
                        "note": f"Advisor exception: mapped to {area}",
                    }
                )

    return rows


def _compute_gpa(raw_courses, major_codes_set):
    """Compute overall and major GPA from raw_courses."""
    GP = {
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "D-": 0.7,
        "F": 0.0,
    }
    op = oh = mp = mh = qp = 0.0
    earned = ip_hrs = 0
    seen = set()
    for c in raw_courses:
        g = c["grade"].upper()
        if g in ("W", "DRP") or c["status"] == "dropped":
            continue
        if c["status"] == "current":
            ip_hrs += c["cr"]
            continue
        if c["status"] != "grade posted":
            continue
        earned += c["cr"]
        if g in ("T", "CR", "NC", ""):
            continue
        gp = GP.get(g)
        if gp is None:
            continue
        cr = c["cr"]
        if c["code"] not in seen:
            op += gp * cr
            oh += cr
            qp += gp * cr
            seen.add(c["code"])
        if c["code"] in major_codes_set or c["raw"].upper().replace("-", "_") in major_codes_set:
            mp += gp * cr
            mh += cr
    return (
        round(op / oh, 2) if oh else 0.0,
        round(mp / mh, 2) if mh else 0.0,
        int(oh),
        earned,
        ip_hrs,
        round(qp, 1),
        earned + ip_hrs,
    )
