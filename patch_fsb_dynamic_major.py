"""
Patch: Make the FSB audit engine dynamic for all non-Sport-Marketing majors.
"""

with open("/home/ubuntu/au-original-restored/engines/sport_marketing.py", "r") as f:
    src = f.read()

OLD = '# Mgmt required\n    mr = []\n    for rid, label, opts, dcr in SMKT_REQ:\n        if rid == "BSNS_PRAC":\n            c4 = cm.get("BSNS_4800")\n            c3 = cm.get("BSNS_3850")\n            if c4 and done(c4):\n                c = c4\n            elif c3 and done(c3):\n                c = c3\n            elif c4 and ip(c4):\n                c = c4\n            elif c3 and ip(c3):\n                c = c3\n            elif c4 and sched(c4):\n                c = c4\n            elif c3 and sched(c3):\n                c = c3\n            else:\n                c = None\n        else:\n            c = find(opts)\n        if map_by_area.get(rid):\n            mapped = find(map_by_area.get(rid, []))\n            if mapped:\n                c = mapped\n        s = status_of(c)\n        mr.append({"id": rid, "label": label, "status": s, "course": c, "dcr": dcr})\n\n    # Electives (none required for Sport Marketing)\n    elecs = []\n    elecs_ip = []\n    ehrs = 0\n    ehrs_ip = 0\n\n    # GPA\n    major_codes = set()\n    for _, _, opts, _ in BUS_CORE:\n        major_codes.update([norm(o) for o in opts])\n    for _, _, opts, _ in SMKT_REQ:\n        major_codes.update([norm(o) for o in opts])\n\n'

NEW = '''# Major-specific required rows — dynamic for all FSB majors
    mr = []
    _major_key = globals().get("MAJOR_KEY", "sport_marketing")
    _catalog_year = globals().get("CATALOG_YEAR", "2022-23")
    _mr_req_tuples = []
    if _major_key in ("sport_marketing", ""):
        # Legacy Sport Marketing path
        for rid, label, opts, dcr in SMKT_REQ:
            if rid == "BSNS_PRAC":
                c4 = cm.get("BSNS_4800")
                c3 = cm.get("BSNS_3850")
                if c4 and done(c4):
                    c = c4
                elif c3 and done(c3):
                    c = c3
                elif c4 and ip(c4):
                    c = c4
                elif c3 and ip(c3):
                    c = c3
                elif c4 and sched(c4):
                    c = c4
                elif c3 and sched(c3):
                    c = c3
                else:
                    c = None
            else:
                c = find(opts)
            if map_by_area.get(rid):
                mapped = find(map_by_area.get(rid, []))
                if mapped:
                    c = mapped
            s = status_of(c)
            mr.append({"id": rid, "label": label, "status": s, "course": c, "dcr": dcr})
            _mr_req_tuples.append((rid, label, opts, dcr))
    else:
        # Dynamic path for all other FSB majors (Finance, Accounting, Management, etc.)
        import importlib as _importlib
        _fsb_mod = _importlib.import_module("requirements.fsb_majors")
        _fsb_reqs = _fsb_mod.get_fsb_requirements(_major_key, _catalog_year) or {}
        for _rc in _fsb_reqs.get("required_courses", []):
            _code = _rc.get("code", "").replace(" ", "-")
            _name = _rc.get("name", _code)
            _cr = _rc.get("credits", 3)
            _opts = [_code.replace("-", "_")]
            _rid = _code.replace("-", "_")
            _label = f"{_code} {_name}"
            c = find(_opts)
            if map_by_area.get(_rid):
                mapped = find(map_by_area.get(_rid, []))
                if mapped:
                    c = mapped
            s = status_of(c)
            mr.append({"id": _rid, "label": _label, "status": s, "course": c, "dcr": _cr})
            _mr_req_tuples.append((_rid, _label, _opts, _cr))
        # Elective block
        _elec = _fsb_reqs.get("elective")
        if _elec:
            _elec_cr = _elec.get("credits", 3)
            _elec_opts = [c.replace(" ", "_") for c in _elec.get("choose_from", [])]
            _elec_names = " / ".join(c.replace(" ", "-") for c in _elec.get("choose_from", []))
            _elec_label = f"Major Elective — {_elec_names} ({_elec_cr} cr)"
            c = None
            for _ec in _elec_opts:
                _candidate = cm.get(_ec)
                if _candidate and not drop(_candidate):
                    c = _candidate
                    break
            s = status_of(c)
            mr.append({"id": "MAJOR_ELEC", "label": _elec_label, "status": s, "course": c, "dcr": _elec_cr})
            _mr_req_tuples.append(("MAJOR_ELEC", _elec_label, _elec_opts, _elec_cr))

    # Electives (none required for Sport Marketing; other majors handled above)
    elecs = []
    elecs_ip = []
    ehrs = 0
    ehrs_ip = 0

    # GPA — use the actual major's course codes
    major_codes = set()
    for _, _, opts, _ in BUS_CORE:
        major_codes.update([norm(o) for o in opts])
    for _, _, opts, _dcr in _mr_req_tuples:
        major_codes.update([norm(o) for o in opts])

'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    with open("/home/ubuntu/au-original-restored/engines/sport_marketing.py", "w") as f:
        f.write(src)
    print("SUCCESS: FSB dynamic major routing added to sport_marketing.py")
else:
    print("ERROR: anchor text not found — checking partial match")
    # Debug: find how much matches
    for i in range(len(OLD), 0, -10):
        if OLD[:i] in src:
            print(f"First {i} chars match, break at: {repr(OLD[i:i+50])}")
            break
