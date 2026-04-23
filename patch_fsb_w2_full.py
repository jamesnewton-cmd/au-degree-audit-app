"""
Patch: In the FSB audit() LA_ROWS loop, expand W2 opts to use the full
liberal_arts_requirements.py course list (same as build_la_rows_for_non_fsb).
Also expand W7 similarly so all FSB students get the full course list.
"""

with open("/home/ubuntu/au-original-restored/engines/sport_marketing.py", "r") as f:
    src = f.read()

OLD = '''        else:
            c = find(opts) if opts else None
            # Allow MAP: TAKEN = AREA overrides for LA rows.
            if map_by_area.get(area):
                mapped = find(map_by_area.get(area, []))
                if mapped:
                    c = mapped
            s = status_of(c)'''

NEW = '''        else:
            # For W2 and W7, supplement the hardcoded opts with the full
            # framework course list from liberal_arts_requirements.py so that
            # any qualifying course (including transfer equivalents) is recognized.
            _effective_opts = list(opts) if opts else []
            if area in ("W2", "W7"):
                try:
                    from requirements.liberal_arts_requirements import LA_OLD_FRAMEWORK as _fw
                    _cy = globals().get("CATALOG_YEAR", "2022-23")
                    _extra = _fw.get(area, {}).get("courses", {}).get(_cy, [])
                    for _eo in _extra:
                        _eo_norm = _eo.replace(" ", "_").replace("-", "_").upper()
                        if _eo_norm not in [o.upper() for o in _effective_opts]:
                            _effective_opts.append(_eo)
                except Exception:
                    pass
            c = find(_effective_opts) if _effective_opts else None
            # Allow MAP: TAKEN = AREA overrides for LA rows.
            if map_by_area.get(area):
                mapped = find(map_by_area.get(area, []))
                if mapped:
                    c = mapped
            s = status_of(c)'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    with open("/home/ubuntu/au-original-restored/engines/sport_marketing.py", "w") as f:
        f.write(src)
    print("SUCCESS: W2/W7 full framework opts patch applied")
else:
    print("ERROR: anchor text not found")
    for i in range(len(OLD), 0, -10):
        if OLD[:i] in src:
            print(f"First {i} chars match, break at: {repr(OLD[i:i+60])}")
            break
