"""
Anderson University — Degree Audit Generator
Exact match to Isaac Bair template.
"""
import csv, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── EXACT COLORS FROM ISAAC BAIR ─────────────────────────────────────────────
MAROON      = colors.HexColor("#8B1A2B")   # title bar / page 4 section headers
GOLD_HEAD   = colors.HexColor("#B8860B")   # section headings text (gold/olive)
GOLD_BAR    = colors.HexColor("#C9A84C")   # page 4 LA/Major section bar bg
BLUE_BAR    = colors.HexColor("#1F3864")   # page 4 Credit/WI section bar bg
COL_HDR_BG  = colors.HexColor("#8B1A2B")   # table column header bg (maroon)
COL_HDR_TXT = colors.white
SUB_HDR_BG  = colors.HexColor("#D4C5A0")   # sub-section row (tan/gold)
SUB_HDR_TXT = colors.HexColor("#3B2A00")
ROW_ODD     = colors.HexColor("#F5F2EC")   # alternating row (warm off-white)
ROW_EVEN    = colors.white
SATISFIED   = colors.HexColor("#375623")   # green text
CURRENT_CLR = colors.HexColor("#7F4700")   # amber/orange text
NOT_SAT     = colors.HexColor("#8B1A2B")   # red/maroon text
TERM_CLR    = colors.HexColor("#1A1A1A")   # term column color (black)
TRANSFER_CLR= colors.HexColor("#8B6914")   # italic gold for Transfer
XMARK_CLR   = colors.HexColor("#CC3300")   # red-orange ✗ items
DARK        = colors.HexColor("#1A1A1A")
GRAY        = colors.HexColor("#555555")
LIGHT_GRAY  = colors.HexColor("#F0F0F0")
BORDER      = colors.HexColor("#CCCCCC")
WHITE       = colors.white

PAGE_W, PAGE_H = letter
LM = RM = 0.5 * inch
TM = BM = 0.5 * inch
CW = PAGE_W - LM - RM

# ── STYLES ────────────────────────────────────────────────────────────────────
def ps(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, leading=11,
             textColor=DARK, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

P = {
    # Title bar
    'title':      ps('title', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE, leading=13),
    # Section headings (gold, outside tables)
    'sec_gold':   ps('sec_gold', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD_HEAD, leading=13),
    # Table column headers
    'col_hdr':    ps('col_hdr', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, leading=11),
    # Sub-section rows inside tables
    'sub_hdr':    ps('sub_hdr', fontName='Helvetica-Bold', fontSize=8.5, textColor=SUB_HDR_TXT, leading=11, alignment=TA_CENTER),
    # Normal cell
    'cell':       ps('cell', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    'cell_b':     ps('cell_b', fontName='Helvetica-Bold', fontSize=8.5, textColor=DARK, leading=11),
    # Status colors
    'sat':        ps('sat', fontName='Helvetica-Bold', fontSize=8.5, textColor=SATISFIED, leading=11),
    'cur':        ps('cur', fontName='Helvetica-Bold', fontSize=8.5, textColor=CURRENT_CLR, leading=11),
    'nos':        ps('nos', fontName='Helvetica-Bold', fontSize=8.5, textColor=NOT_SAT, leading=11),
    # Course history term
    'term':       ps('term', fontName='Helvetica', fontSize=8, textColor=TERM_CLR, leading=10),
    'term_tr':    ps('term_tr', fontName='Helvetica-Oblique', fontSize=8, textColor=TRANSFER_CLR, leading=10),
    'code_b':     ps('code_b', fontName='Helvetica-Bold', fontSize=8, textColor=DARK, leading=10),
    'hist_cell':  ps('hist_cell', fontName='Helvetica', fontSize=8, textColor=DARK, leading=10),
    # Eligibility table
    'elig_lbl':   ps('elig_lbl', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    'elig_val':   ps('elig_val', fontName='Helvetica-Bold', fontSize=8.5, textColor=DARK, leading=11, alignment=TA_RIGHT),
    'elig_yes':   ps('elig_yes', fontName='Helvetica-Bold', fontSize=8.5, textColor=SATISFIED, leading=11, alignment=TA_RIGHT),
    'elig_no':    ps('elig_no',  fontName='Helvetica-Bold', fontSize=8.5, textColor=NOT_SAT, leading=11, alignment=TA_RIGHT),
    'elig_hdr':   ps('elig_hdr', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, leading=11),
    'elig_hdr_r': ps('elig_hdr_r', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, leading=11, alignment=TA_RIGHT),
    # Action plan
    'ap_cat_lbl': ps('ap_cat_lbl', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    'ap_cat_hdr': ps('ap_cat_hdr', fontName='Helvetica-Bold', fontSize=8.5, textColor=DARK, leading=11),
    'ap_x':       ps('ap_x', fontName='Helvetica', fontSize=8.5, textColor=XMARK_CLR, leading=11),
    'ap_rec':     ps('ap_rec', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    'ap_title':   ps('ap_title', fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=12),
    'ap_bar_gold':ps('ap_bar_gold', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=12),
    'ap_bar_blue':ps('ap_bar_blue', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=12),
    'summary':    ps('summary', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    # Footer
    'footer':     ps('footer', fontName='Helvetica', fontSize=7, textColor=GRAY, leading=9, alignment=TA_CENTER),
    # Metrics
    'met_lbl':    ps('met_lbl', fontName='Helvetica', fontSize=8.5, textColor=DARK, leading=11),
    'met_val':    ps('met_val', fontName='Helvetica-Bold', fontSize=8.5, textColor=DARK, leading=11, alignment=TA_RIGHT),
    'met_hdr_l':  ps('met_hdr_l', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, leading=11),
    'met_hdr_r':  ps('met_hdr_r', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, leading=11, alignment=TA_RIGHT),
    'note':       ps('note', fontName='Helvetica-Oblique', fontSize=7.5, textColor=GRAY, leading=10),
}

THIN = colors.HexColor("#CCCCCC")
PAD  = dict(TOPPADDING=3, BOTTOMPADDING=3, LEFTPADDING=6, RIGHTPADDING=6)

def padded(*extra):
    base = [
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('LINEBELOW',     (0,0),(-1,-1), 0.3, THIN),
    ]
    base.extend(extra)
    return TableStyle(base)

# ── CSV ───────────────────────────────────────────────────────────────────────
def norm(c): return c.strip().upper().replace('-','_')

def _resolve_transfer_code(course_code, equiv_course):
    """
    For ELCT-style transfer codes, try to extract the real AU course code.
    e.g. 'ELCT-1000-1628902-CHEM-119' -> try equiv_course field first,
    otherwise return original. Non-ELCT codes pass through unchanged.
    """
    code_upper = course_code.strip().upper()
    if not code_upper.startswith('ELCT'):
        return course_code
    # Try Equivalent Course field first (most reliable)
    if equiv_course and equiv_course.strip():
        eq = equiv_course.strip().upper()
        # Check it looks like a real AU course code (DEPT-1234 or DEPT 1234)
        import re as _re
        if _re.match(r'^[A-Z]{2,6}[-\x20]\d{3,4}', eq):
            return eq
    # Try to extract from the ELCT code itself: ELCT-XXXX-NNNNN-DEPT-NNN
    # Look for a dept+number pattern at the end
    import re as _re
    m = _re.search(r'-([A-Z]{2,6})-(\d{3,4}[A-Z]?)$', code_upper)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return course_code


def parse_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            raw_code = r.get('Course Code','').strip()
            equiv     = r.get('Equivalent Course','').strip()
            resolved  = _resolve_transfer_code(raw_code, equiv)
            rows.append({
                'code':     norm(resolved),
                'raw':      resolved.upper(),
                'name':     r.get('Course Name','').strip(),
                'cr':       _int(r.get('Credits','0')),
                'status':   r.get('Status','').strip().lower().replace('scheduled','current'),
                'grade':    r.get('Letter Grade','').strip(),
                'reg_date': r.get('Registration Date','').strip(),
            })
    # PEHS-1200 note: Co-Curricular Activity courses (PEHS-1200) are student-athlete
    # participation credits — 1 credit, earned once. NC grade = not satisfactory, excluded
    # by done() logic. These courses are never tracked as degree requirements.
    # Remove fully blank rows (no status AND no grade — phantom duplicates from export)
    rows = [c for c in rows if c['status'] or c['grade']]
    # Deduplicate: for each course code keep the best record
    # Priority: grade posted > current > dropped > not started/blank
    seen = {}
    def priority(c):
        g = c['grade'].upper()
        if c['status'] == 'grade posted' and g == 'T': return 0          # transfer always wins
        if c['status'] == 'grade posted' and g not in ('','W','DRP','NC','F'): return 1  # passing grade
        if c['status'] == 'current': return 2
        if c['status'] == 'scheduled': return 3
        if c['status'] == 'grade posted' and g == 'F': return 4           # F loses to transfer/passing
        if c['status'] == 'grade posted' and g == 'NC': return 5
        if c['status'] == 'dropped' or g in ('DRP','W'): return 6
        return 7
    for c in rows:
        k = c['code']
        if k not in seen or priority(c) < priority(seen[k]):
            seen[k] = c
    return list(seen.values())

# ── ADVISOR EXCEPTIONS ────────────────────────────────────────────────────────
def apply_exceptions(courses, exceptions_text):
    """
    Parse advisor exception notes and inject synthetic course records.

    Supported formats (one per line, case-insensitive):
      SUB: SPRL-3300 = BSNS-4560   → treat SPRL-3300 as satisfying BSNS-4560's slot
      WAIVE: PEHS-1000              → mark PEHS-1000 as satisfied (waived, 0 cr)
      STATUS: BSNS-4560 = current   → override a course's status (current/scheduled/satisfied)
    """
    courses = list(courses)
    cm = {c['code']: c for c in courses}

    for raw_line in exceptions_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue

        upper = line.upper()

        # SUB: REQUIRED-CODE = TAKEN-CODE
        # Registrar enters: the required course = the course the student actually took
        # e.g. SUB: EDUC-2100 = PSYC-2510 means student took PSYC-2510, counts for EDUC-2100
        if upper.startswith('SUB:'):
            try:
                body = line[4:].strip()
                req_raw, taken_raw = [x.strip() for x in body.split('=', 1)]
                req_code   = norm(req_raw)
                taken_code = norm(taken_raw)
                # Find the actually-taken course record
                taken = cm.get(taken_code)
                if taken:
                    # Inject a clone under the required code so audit() finds it
                    clone = dict(taken)
                    clone['code'] = req_code
                    clone['raw']  = req_raw.upper().replace('_', '-')
                    clone['name'] = taken['name'] + f' (sub for {req_raw.upper()})'
                    # Add or replace in courses list
                    courses = [c for c in courses if c['code'] != req_code]
                    courses.append(clone)
                    cm[req_code] = clone
            except Exception:
                pass

        # MAP: TAKEN-CODE = AREA-OR-KEY
        # Count a course toward an LA area or major requirement without naming
        # a specific course to replace. e.g. MAP: PSYC-2510 = W5
        elif upper.startswith('MAP:'):
            try:
                body = line[4:].strip()
                taken_raw, area_raw = [x.strip() for x in body.split('=', 1)]
                taken_code = norm(taken_raw)
                area_key   = area_raw.strip().upper().replace(' ','_').replace('-','_')
                taken = cm.get(taken_code)
                if taken:
                    synthetic = dict(taken)
                    synthetic['code'] = f'__MAP__{area_key}__{taken_code}'
                    synthetic['raw']  = taken['raw']
                    synthetic['name'] = taken['name'] + f' (mapped to {area_raw.upper()})'
                    synthetic['__map_area__'] = area_key
                    synthetic['__map_taken_code__'] = taken_code
                    courses.append(synthetic)
                    cm[synthetic['code']] = synthetic
            except Exception:
                pass

        # WAIVE: COURSE-CODE
        elif upper.startswith('WAIVE:'):
            try:
                waived_raw  = line[6:].strip()
                waived_code = norm(waived_raw)
                synthetic = {
                    'code':     waived_code,
                    'raw':      waived_raw.upper().replace('_', '-'),
                    'name':     f'{waived_raw.upper()} (Advisor Waiver)',
                    'cr':       0,
                    'status':   'grade posted',
                    'grade':    'W/V',
                    'reg_date': '',
                }
                courses = [c for c in courses if c['code'] != waived_code]
                courses.append(synthetic)
                cm[waived_code] = synthetic
            except Exception:
                pass

        # STATUS: COURSE-CODE = current|scheduled|satisfied
        elif upper.startswith('STATUS:'):
            try:
                body = line[7:].strip()
                code_raw, status_raw = [x.strip() for x in body.split('=', 1)]
                code   = norm(code_raw)
                status = status_raw.strip().lower()
                STATUS_MAP = {
                    'current':   'current',
                    'scheduled': 'scheduled',
                    'satisfied': 'grade posted',
                    'complete':  'grade posted',
                }
                mapped = STATUS_MAP.get(status)
                if mapped and code in cm:
                    cm[code]['status'] = mapped
                    if mapped == 'grade posted' and cm[code]['grade'].upper() in ('', 'W', 'DRP', 'NC', 'F'):
                        cm[code]['grade'] = 'T'  # treat as transfer/satisfied
            except Exception:
                pass

    return courses

def _int(v):
    try: return int(str(v).strip())
    except: return 0

def done(c):  return c['status']=='grade posted' and c['grade'].upper() not in ('','W','DRP','NC')
def ip(c):    return c['status']=='current'
def sched(c): return c['status']=='scheduled'
def xfer(c):  return c['grade'].upper()=='T'
def drop(c):  return c['grade'].upper() in ('DRP','W') or c['status']=='dropped'

def best(courses, codes):
    norms = [norm(x) for x in codes]
    found = [c for c in courses if c['code'] in norms and not drop(c)]
    # Prefer done records that aren't F (e.g. transfer T beats original F)
    for f in found:
        if done(f) and f['grade'].upper() != 'F': return f
    for f in found:
        if done(f): return f
    for f in found:
        if ip(f): return f
    return found[0] if found else None

def cmap(courses):
    m = {}
    for c in courses:
        k = c['code']
        if k not in m: m[k]=c
        else:
            e=m[k]
            if done(c) and not done(e): m[k]=c
            elif ip(c) and not done(e) and not ip(e): m[k]=c
    return m

# ── STATUS ────────────────────────────────────────────────────────────────────
def status_of(c):
    if c is None: return 'Not Satisfied'
    if done(c):   return 'Satisfied'
    if ip(c):     return 'Current'
    if sched(c):  return 'Scheduled'
    return 'Not Satisfied'

def status_para(s):
    if s == 'Satisfied':     return Paragraph(s, P['sat'])
    if s == 'Current':       return Paragraph(s, P['cur'])
    if s == 'Scheduled':     return Paragraph(s, P['cur'])  # same amber as Current
    return Paragraph(s, P['nos'])

def grade_disp(c):
    if c is None: return ''
    if ip(c): return 'IP'
    if xfer(c): return 'T'
    return c['grade'] if c['grade'] else ''

def cr_disp(c, fallback=''):
    if c is None: return str(fallback) if fallback else ''
    return str(c['cr'])

# ── REQUIREMENT LISTS ─────────────────────────────────────────────────────────
MATH_OPTS = ['MATH_1300','MATH_1400','MATH_2010']

BUS_CORE = [
    ('MATH_1300','MATH-1300 Finite Mathematics (or MATH-1400/2010)', MATH_OPTS, 3),
    ('ACCT_2010','ACCT-2010 Principles of Accounting I',    ['ACCT_2010'], 3),
    ('ACCT_2020','ACCT-2020 Principles of Accounting II',   ['ACCT_2020'], 3),
    ('BSNS_1050','BSNS-1050 Business as a Profession',      ['BSNS_1050'], 2),
    ('BSNS_2310','BSNS-2310 Business Analytics',            ['BSNS_2310'], 3),
    ('BSNS_2450','BSNS-2450 Data Analytics and Decision Making', ['BSNS_2450'], 3),
    ('BSNS_2510','BSNS-2510 Principles of Finance',         ['BSNS_2510'], 3),
    ('BSNS_2710','BSNS-2710 Principles of Management',      ['BSNS_2710'], 3),
    ('BSNS_2810','BSNS-2810 Principles of Marketing',       ['BSNS_2810'], 3),
    ('BSNS_3270','BSNS-3270 Project Management',            ['BSNS_3270'], 3),
    ('BSNS_3420','BSNS-3420 Business Law',                  ['BSNS_3420'], 3),
    ('BSNS_4500','BSNS-4500 Strategic Management',          ['BSNS_4500'], 3),
    ('BSNS_4910','BSNS-4910 Senior Seminar in Business / Ethics & Leadership', ['BSNS_4910'], 2),
    ('ECON_2010','ECON-2010 Principles of Macroeconomics',  ['ECON_2010'], 3),
    ('ECON_2020','ECON-2020 Principles of Microeconomics',  ['ECON_2020'], 3),
]

# ── 2025-26 BUSINESS CORE (48 hrs) ──────────────────────────────────────────
BUS_CORE_2526 = [
    ('ACCT_2010','ACCT-2010 Principles of Accounting I',       ['ACCT_2010'], 3),
    ('ACCT_2020','ACCT-2020 Principles of Accounting II',      ['ACCT_2020'], 3),
    ('BSNS_1050','BSNS-1050 Business as a Profession',         ['BSNS_1050'], 3),
    ('BSNS_2310','BSNS-2310 Business Analytics',               ['BSNS_2310'], 3),
    ('BSNS_2450','BSNS-2450 Data Analytics and Decision Making',['BSNS_2450'],3),
    ('BSNS_2510','BSNS-2510 Principles of Finance',            ['BSNS_2510'], 3),
    ('BSNS_2550','BSNS-2550 Professional Communication (SI)',  ['BSNS_2550'], 3),
    ('BSNS_2710','BSNS-2710 Principles of Management',         ['BSNS_2710'], 3),
    ('BSNS_2810','BSNS-2810 Principles of Marketing',          ['BSNS_2810'], 3),
    ('BSNS_3120','BSNS-3120 Global Business (AU6)',             ['BSNS_3120'], 3),
    ('BSNS_3270','BSNS-3270 Project Management',               ['BSNS_3270'], 3),
    ('BSNS_3420','BSNS-3420 Business Law',                     ['BSNS_3420'], 3),
    ('BSNS_4500','BSNS-4500 Strategic Management',             ['BSNS_4500'], 3),
    ('BSNS_4800','BSNS-4800 Experiential Learning',            ['BSNS_4800'], 3),
    ('BSNS_4910','BSNS-4910 Senior Seminar in Business & Ethics',['BSNS_4910'],3),
    ('ECON_2010','ECON-2010 Principles of Macroeconomics',     ['ECON_2010'], 3),
]

SMKT_REQ = [
    ('BSNS_3130','BSNS-3130 Sport Marketing',                        ['BSNS_3130'], 3),
    ('BSNS_3210','BSNS-3210 Buyer/Seller Relations',                 ['BSNS_3210'], 3),
    ('BSNS_3220','BSNS-3220 Consumer Behavior',                      ['BSNS_3220'], 3),
    ('BSNS_4110','BSNS-4110 Marketing Research',                     ['BSNS_4110'], 3),
    ('BSNS_4330','BSNS-4330 Marketing Management',                   ['BSNS_4330'], 3),
    ('BSNS_4360','BSNS-4360 Sport Sponsorship and Sales',            ['BSNS_4360'], 3),
    ('BSNS_4560','BSNS-4560 Business of Game-Day Experience',        ['BSNS_4560'], 3),
    ('BSNS_PRAC','BSNS-3850 Practicum / BSNS-4800 Internship',       ['BSNS_3850','BSNS_4800'], 3),
]

# Sport Marketing electives — 6 hrs from approved list
ELEC_OPTS = ['BSNS_3550','BSNS_3400','BSNS_4400','BSNS_3120',
             'BSNS_3240','BSNS_3510','BSNS_4050','BSNS_4120',
             'BSNS_4240','BSNS_4250','BSNS_4310','BSNS_4310_23']

# ── MINOR DEFINITIONS ─────────────────────────────────────────────────────────
# Athletic Coaching Minor (KINESIOLOGY_EXTRA version — 15 cr)
ATHLETIC_COACHING_MINOR = [
    # (id, label, options, default_cr, note)
    ('PEHS_1450', 'PEHS-1450 Care/Prevention of Injuries & Illnesses', ['PEHS_1450'], 3, ''),
    ('PEHS_1550', 'PEHS-1550 Care/Prevention of Injuries & Illnesses II', ['PEHS_1550'], 3, ''),
    ('ATRG_1530', 'ATRG-1530 or EXSC-4010 Strength & Conditioning', ['ATRG_1530','EXSC_4010'], 3, 'choose one'),
    ('PEHS_2340', 'PEHS-2340 or PEHS-3340 Psychology/Sociology of Sport', ['PEHS_2340','PEHS_3340'], 3, 'choose one'),
    ('ELEC',      'Coaching Elective — 4-5 hrs from PEHS/EXSC/SPRL upper-division', [], 4, 'elective'),
]

# Coaching elective pool (upper-division PEHS/EXSC/SPRL 3000+)
COACHING_ELEC_POOL = [
    'PEHS_3030','PEHS_3040','PEHS_3050','PEHS_3060','PEHS_3070','PEHS_3080',
    'PEHS_3340','PEHS_3410','EXSC_3100','EXSC_3200','EXSC_3300','EXSC_4010',
    'SPRL_3150','SPRL_3250','SPRL_3300','SPRL_4850',
]

# Liberal Arts rows (Area label, Course display, Requirement text, option codes, default_cr)
LA_ROWS = [
    ('F1','LART-1050 First-Year Exper Seminar',
     'F1 LART-1050 Understanding College', ['LART_1050'], 1),
    ('F2','BSNS-3420 Business Law',
     'F2 BSNS-3420 Civil Discourse & Critical Reasoning', ['BSNS_3420','ENGL_3190','ENGL_3580','HIST_2300','HNRS_2125','PSYC_3200','SOCI_2450'], 3),
    ('F3','ENGL-1110 Rhetoric and Composition',
     'F3 ENGL-1110 Writing I — ENGL-1110 (or ENGL-1100/HNRS-2110)', ['ENGL_1110','ENGL_1100','HNRS_2110'], 3),
    ('F3','ENGL-1120 Rhetoric and Research',
     'F3 ENGL-1120 Writing II — ENGL-1120 (or HNRS-2110)', ['ENGL_1120','HNRS_2110'], 3),
    ('F4','COMM-1000 Intro to Speech Communication',
     'F4 COMM-1000 Speaking & Listening (COMM-1000 + 1 SI)', ['COMM_1000'], 3),
    ('F5','MATH-1300 Finite Mathematics',
     'F5 MATH-1300 Quantitative Reasoning', MATH_OPTS, 3),
    ('F6','BIBL-2000 Intro to the Bible',
     'F6 BIBL-2000 Biblical Literacy', ['BIBL_2000'], 3),
    ('F7','PEHS-1000 Fitness/Wellness for Life',
     'F7 PEHS-1000 Personal Wellness', ['PEHS_1000'], 2),
    ('W1',None,'W1 BIBL-3410 Christian Ways of Knowing',
     ['BIBL_3410','RELI_3000','BIBL_3000','RLGN_3000'], 3),
    ('W2',None,'W2 Scientific Ways of Knowing (4 hrs)',
     ['BIOL_1000','CHEM_1000','PHYS_1000','EXSC_2140','ENVS_1000'], 4),
    ('W3',None,'W3 Civic Ways of Knowing',
     ['HIST_2030','HIST_2110','POLS_1000','SOCI_1000','CRIM_2520','HNRS_2110'], 3),
    ('W4', None, 'W4 Aesthetic Ways of Knowing',
 ['ARTS_1250','MUSC_2210','THEA_1000','ARTS_1210','ARTS_1230','MUSC_1000','ARTS_1000','ARTH_3040','HNRS_3000'], 3),
    ('W5',None,'W5 Social & Behavioral Ways of Knowing',
     ['ECON_2010','PSYC_1000','SOCI_1000'], 3),
    ('W6',None,'W6 Modern Language (1 course, placement-based)',
     ['GERM_1010','SPAN_1010','SPAN_1020','FREN_1010','GERM_1020','MLAN_2000','SPAN_3010'], 4),
    ('W7',None,'W7 Global/Intercultural Ways of Knowing',
     ['BSNS_3120','COMM_3050','HIST_3260','HIST_3300','HIST_3425','POSC_3320','POSC_3450','ENGR_2090','ENGL_2220','MLAN_2000','SPAN_3020','SOCI_2450'], 3),
    ('W8',None,'W8 Experiential Ways of Knowing',
     ['BSNS_1050','BSNS_4110','BSNS_4330','BSNS_4560','BSNS_4800'], 2),
    ('WI',None,'WI BSNS-3120 Writing Intensive #1 — must be from approved WI list',
     ['BSNS_3120','BSNS_4910','ENGL_3110','COMM_3130','HIST_3260','BIBL_3000','RLGN_3000','ENGL_2500','ENGL_3190','ENGL_3580','ENGR_2090','HIST_3300','HIST_3425','POSC_3320','POSC_3450','SPAN_3010'], 3),
    ('WI',None,'WI Writing Intensive #2 — at least one must be upper-division (3000+)',
     [], 3),
    ('SI',None,'SI BSNS-3210 Speaking Intensive — 1 course required from approved SI list | Found: 1',
     ['BSNS_3210','BSNS_4480','COMM_2000','ARTH_3040','ENGL_2220','HIST_2300','HNRS_2125','PSYC_3200','SPAN_3020'], 3),
]

# ── AUDIT ─────────────────────────────────────────────────────────────────────
# ── MINOR AUDIT DISPATCH ─────────────────────────────────────────────────────
# Maps minor_key → (requirement_rows, elective_pool)
# requirement_rows: list of (id, label, option_codes, default_cr, note)
#   note == 'elective' triggers pool-based elective logic
# elective_pool: set of norm'd course codes eligible as electives

MINOR_DEFS = {
    'athletic_coaching_minor': {
        'name': 'Athletic Coaching Minor',
        'rows': ATHLETIC_COACHING_MINOR,
        'elec_pool': COACHING_ELEC_POOL,
    },
    'sport_marketing_minor': {
        'name': 'Sport Marketing Minor',
        'rows': [
            ('BSNS_3130','BSNS-3130 Sport Marketing',              ['BSNS_3130'], 3, ''),
            ('BSNS_4360','BSNS-4360 Sport Sponsorship and Sales',  ['BSNS_4360'], 3, ''),
            ('BSNS_4560','BSNS-4560 Business of Game-Day Exper',   ['BSNS_4560'], 3, ''),
            ('ELEC',     'Sport Mktg Elective — 6 hrs from approved list',
             ['BSNS_3210','BSNS_3220','BSNS_3550','BSNS_4400','BSNS_4550','BSNS_4800'], 6, 'elective'),
        ],
        'elec_pool': {'BSNS_3210','BSNS_3220','BSNS_3550','BSNS_4400','BSNS_4550','BSNS_4800'},
        'elec_needed': 6,
    },
    'accounting_minor': {
        'name': 'Accounting Minor',
        'rows': [
            ('ACCT_2010','ACCT-2010 Principles of Accounting I',   ['ACCT_2010'], 3, ''),
            ('ACCT_2020','ACCT-2020 Principles of Accounting II',  ['ACCT_2020'], 3, ''),
            ('ELEC',     'Accounting Elective — 9 hrs from ACCT 3000+',
             ['ACCT_3010','ACCT_3020','ACCT_3110','ACCT_3500','ACCT_4020','ACCT_4050','ACCT_4100'], 9, 'elective'),
        ],
        'elec_pool': {'ACCT_3010','ACCT_3020','ACCT_3110','ACCT_3500','ACCT_4020','ACCT_4050','ACCT_4100'},
        'elec_needed': 9,
    },
    'management_minor': {
        'name': 'Management Minor',
        'rows': [
            ('BSNS_2710','BSNS-2710 Principles of Management',     ['BSNS_2710'], 3, ''),
            ('BSNS_3270','BSNS-3270 Project Management',           ['BSNS_3270'], 3, ''),
            ('ELEC',     'Management Elective — 9 hrs from approved list',
             ['BSNS_3240','BSNS_3550','BSNS_4050','BSNS_4240','BSNS_4250','BSNS_4310'], 9, 'elective'),
        ],
        'elec_pool': {'BSNS_3240','BSNS_3550','BSNS_4050','BSNS_4240','BSNS_4250','BSNS_4310'},
        'elec_needed': 9,
    },
    'marketing_minor': {
        'name': 'Marketing Minor',
        'rows': [
            ('BSNS_2810','BSNS-2810 Principles of Marketing',      ['BSNS_2810'], 3, ''),
            ('BSNS_4330','BSNS-4330 Marketing Management',         ['BSNS_4330'], 3, ''),
            ('ELEC',     'Marketing Elective — 9 hrs from approved list',
             ['BSNS_3210','BSNS_3220','BSNS_3130','BSNS_4110','BSNS_4240','BSNS_4310','BSNS_4360','BSNS_4400','BSNS_4550'], 9, 'elective'),
        ],
        'elec_pool': {'BSNS_3210','BSNS_3220','BSNS_3130','BSNS_4110','BSNS_4240','BSNS_4310','BSNS_4360','BSNS_4400','BSNS_4550'},
        'elec_needed': 9,
    },
    'finance_minor': {
        'name': 'Finance Minor',
        'rows': [
            ('BSNS_2510','BSNS-2510 Principles of Finance',        ['BSNS_2510'], 3, ''),
            ('ELEC',     'Finance Elective — 12 hrs from approved list',
             ['BSNS_3510','BSNS_4050','BSNS_4120','BSNS_4310','BSNS_4310_23'], 12, 'elective'),
        ],
        'elec_pool': {'BSNS_3510','BSNS_4050','BSNS_4120','BSNS_4310','BSNS_4310_23'},
        'elec_needed': 12,
    },
    'global_business_minor': {
        'name': 'Global Business Minor',
        'rows': [
            ('BSNS_3120','BSNS-3120 Global Business',              ['BSNS_3120'], 3, ''),
            ('ELEC',     'Global Business Elective — 12 hrs from approved list',
             ['BSNS_3400','BSNS_3550','BSNS_4050','BSNS_4240','BSNS_4400'], 12, 'elective'),
        ],
        'elec_pool': {'BSNS_3400','BSNS_3550','BSNS_4050','BSNS_4240','BSNS_4400'},
        'elec_needed': 12,
    },
    'economics_minor': {
        'name': 'Economics Minor',
        'rows': [
            ('ECON_2010','ECON-2010 Principles of Macroeconomics', ['ECON_2010'], 3, ''),
            ('ECON_2020','ECON-2020 Principles of Microeconomics', ['ECON_2020'], 3, ''),
            ('ELEC',     'Economics Elective — 9 hrs from ECON 3000+', [], 9, 'elective'),
        ],
        'elec_pool': set(),  # any ECON 3000+; checked dynamically
        'elec_needed': 9,
        'elec_dept_prefix': 'ECON_3',
    },
}

def _run_minor_rows(courses, rows, elec_pool, elec_needed, find, status_of, elec_dept_prefix=None):
    """Core logic shared by all minors. Returns list of minor_row dicts."""
    minor_rows = []
    core_used = set()

    for rid, label, opts, dcr, note in rows:
        if note == 'elective':
            # Build pool: explicit pool + optional dept prefix for open electives
            pool = set(elec_pool)
            if elec_dept_prefix:
                pool |= {c['code'] for c in courses if c['code'].startswith(elec_dept_prefix)}

            elec_done = [c for c in courses if c['code'] in pool
                         and done(c) and c['code'] not in core_used]
            elec_ip   = [c for c in courses if c['code'] in pool
                         and (ip(c) or sched(c)) and c['code'] not in core_used]
            elec_hrs     = sum(c['cr'] for c in elec_done)
            elec_hrs_ip  = sum(c['cr'] for c in elec_ip)
            needed = elec_needed if elec_needed else dcr

            if elec_hrs >= needed:
                s = 'Satisfied'
            elif elec_hrs + elec_hrs_ip >= needed:
                s = 'Current' if any(ip(c) for c in elec_ip) else 'Scheduled'
            elif elec_done or elec_ip:
                s = 'Not Satisfied'
            else:
                s = 'Not Satisfied'

            minor_rows.append({'id': rid, 'label': label, 'status': s, 'course': None,
                                'dcr': needed, 'elec_done': elec_done, 'elec_ip': elec_ip,
                                'elec_hrs': elec_hrs, 'elec_needed': needed})
        else:
            c = find(opts) if opts else None
            s = status_of(c)
            if c:
                core_used.add(c['code'])
            minor_rows.append({'id': rid, 'label': label, 'status': s, 'course': c,
                                'dcr': dcr, 'elec_done': [], 'elec_ip': [], 'elec_hrs': 0,
                                'elec_needed': dcr})

    return minor_rows


def audit_minor(courses, minor_key, find, status_of):
    """Dispatch to the right minor definition. Returns [] if no minor declared."""
    if not minor_key:
        return []
    defn = MINOR_DEFS.get(minor_key)
    if not defn:
        return []
    return _run_minor_rows(
        courses,
        defn['rows'],
        defn.get('elec_pool', set()),
        defn.get('elec_needed', 0),
        find,
        status_of,
        elec_dept_prefix=defn.get('elec_dept_prefix'),
    )


def audit(courses, minor_key=None):
    cm = cmap(courses)
    def find(codes): return best(courses, codes)

    # ── EXCEPTION RULE 1: ENGL-1110 tested out ──────────────────────────────────
    # If ENGL-1120 is present but ENGL-1110 is absent, the student tested out of
    # ENGL-1110. Inject a synthetic "Satisfied" record for ENGL-1110 (3 cr, T grade).
    has_1110 = cm.get('ENGL_1110') or cm.get('ENGL_1100')
    has_1120 = cm.get('ENGL_1120')
    if not has_1110 and has_1120:
        synthetic_1110 = {
            'code': 'ENGL_1110', 'raw': 'ENGL-1110',
            'name': 'Rhetoric and Composition (tested out)',
            'cr': 3, 'status': 'grade posted', 'grade': 'T',
            'reg_date': ''
        }
        courses = courses + [synthetic_1110]
        cm['ENGL_1110'] = synthetic_1110

    # ── EXCEPTION RULE 2: LART-1050 exemption ────────────────────────────────────
    # If LART-1050 is entirely absent from the uploaded transcript, the student
    # is exempt. Inject a synthetic Satisfied record so F1 shows as satisfied
    # and the W8 auto-satisfy chain fires correctly.
    has_lart = cm.get('LART_1050')
    if not has_lart:
        synthetic_lart = {
            'code': 'LART_1050', 'raw': 'LART-1050',
            'name': 'First-Year Seminar (exempt)',
            'cr': 0, 'status': 'grade posted', 'grade': 'T',
            'reg_date': ''
        }
        courses = courses + [synthetic_lart]
        cm['LART_1050'] = synthetic_lart

    # F1 for W8 auto-satisfy
    f1 = find(['LART_1050'])
    f1_ok = f1 is not None and done(f1)

    # W8 satisfying courses for Sport Marketing major (per Registrar 11/14/2023)
    W8_COURSES = ['BSNS_1050','BSNS_4110','BSNS_4330','BSNS_4560','BSNS_4800']

    # LA rows
    la = []
    for row in LA_ROWS:
        area, course_col, req_txt, opts, dcr = row
        if area == 'W8':
            if f1_ok:
                c = cm.get('BSNS_1050'); s = 'Satisfied'
            else:
                c = None; s = 'Not Satisfied'
                for code in W8_COURSES:
                    candidate = cm.get(code)
                    if candidate and done(candidate):
                        c = candidate; s = 'Satisfied'; break
                    elif candidate and ip(candidate) and s != 'Satisfied':
                        c = candidate; s = 'Current'
                    elif candidate and sched(candidate) and s not in ('Satisfied','Current'):
                        c = candidate; s = 'Scheduled'
        elif area == 'WI' and not opts:
            # WI #2 upper division — BSNS-4910 double-dips here first;
            # BSNS-3120 also qualifies as a WI-designated 3000+ course
            c4910 = cm.get('BSNS_4910')
            c3120 = cm.get('BSNS_3120')
            if c4910 and done(c4910):
                c = c4910; s = 'Satisfied'
            elif c4910 and ip(c4910):
                c = c4910; s = 'Current'
            elif c4910 and sched(c4910):
                c = c4910; s = 'Scheduled'
            elif c3120 and done(c3120):
                c = c3120; s = 'Satisfied'
            elif c3120 and ip(c3120):
                c = c3120; s = 'Current'
            elif c3120 and sched(c3120):
                c = c3120; s = 'Scheduled'
            else:
                c = None; s = 'Not Satisfied'
        else:
            c = find(opts) if opts else None
            s = status_of(c)
        # course_col override for W rows
        if course_col is None and c is not None:
            course_col = f"{c['raw']} {c['name']}"
        la.append({'area':area,'course_col':course_col or '','req':req_txt,
                   'status':s,'course':c,'dcr':dcr})

    # Business core
    bc = []
    for rid,label,opts,dcr in BUS_CORE:
        c = find(opts); s = status_of(c)
        bc.append({'id':rid,'label':label,'opts':opts,'status':s,'course':c,'dcr':dcr})

    # Mgmt required
    mr = []
    for rid,label,opts,dcr in SMKT_REQ:
        if rid=='BSNS_PRAC':
            c4=cm.get('BSNS_4800'); c3=cm.get('BSNS_3850')
            if c4 and done(c4): c=c4
            elif c3 and done(c3): c=c3
            elif c4 and ip(c4): c=c4
            elif c3 and ip(c3): c=c3
            elif c4 and sched(c4): c=c4
            elif c3 and sched(c3): c=c3
            else: c=None
        else:
            c = find(opts)
        s = status_of(c)
        mr.append({'id':rid,'label':label,'status':s,'course':c,'dcr':dcr})

    # Electives
    elecs=[]; elecs_ip=[]; ehrs=0; ehrs_ip=0
    for opt in ELEC_OPTS:
        c=cm.get(norm(opt))
        if c and done(c):  elecs.append(c); ehrs+=c['cr']
        elif c and (ip(c) or sched(c)): elecs_ip.append(c); ehrs_ip+=c['cr']

    # GPA
    major_codes=set()
    for _,_,opts,_ in BUS_CORE: major_codes.update([norm(o) for o in opts])
    for _,_,opts,_ in SMKT_REQ: major_codes.update([norm(o) for o in opts])
    for o in ELEC_OPTS: major_codes.add(norm(o))

    op,oh,mp,mh,qp=0.0,0,0.0,0,0.0
    earned=0; ip_hrs=0
    GP={'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,
        'C-':1.7,'D+':1.3,'D':1.0,'D-':0.7,'F':0.0}
    seen=set()
    for c in courses:
        if drop(c): continue
        if ip(c): ip_hrs+=c['cr']; continue
        if not done(c): continue
        earned+=c['cr']
        if xfer(c): continue
        g=GP.get(c['grade'].upper())
        if g is None: continue
        cr=c['cr']
        if c['code'] not in seen:
            op+=g*cr; oh+=cr; qp+=g*cr; seen.add(c['code'])
        if c['code'] in major_codes:
            mp+=g*cr; mh+=cr

    gpa_o=round(op/oh,2) if oh else 0.0
    gpa_m=round(mp/mh,2) if mh else 0.0
    proj=earned+ip_hrs

    # ── MINOR AUDIT ───────────────────────────────────────────────────────────
    minor_rows = audit_minor(courses, minor_key, find, status_of)

    return dict(la=la,bc=bc,mr=mr,elecs=elecs,elecs_ip=elecs_ip,ehrs=ehrs,ehrs_ip=ehrs_ip,
                gpa_o=gpa_o,gpa_m=gpa_m,qp=round(qp,1),
                gpa_hrs=oh,earned=earned,ip_hrs=ip_hrs,proj=proj,
                minor_key=minor_key,
                minor_rows=minor_rows,
                courses=courses)

# ── BUILD PDF ─────────────────────────────────────────────────────────────────
def build(res, student_name, major_label, out, exceptions=''):
    """Delegate to shared PDF template. All majors use the same layout."""
    from engines.pdf_template import build as template_build

    # Populate template-specific keys that sport_marketing audit() doesn't set
    res.setdefault('catalog_year', '2023-24')
    res.setdefault('current_term_label', '2025-26')
    res.setdefault('major_section_label', f"Sport Marketing Major — {res['catalog_year']}")
    res.setdefault('elec_required_hrs', 6)
    res.setdefault('elec_section_label',
        f"Sport Marketing Electives — 6 hrs required  (earned: {res.get('ehrs',0)} hrs)")
    res.setdefault('elec_opts', [
        'BSNS-3550','BSNS-3400','BSNS-4400','BSNS-3120','BSNS-3240',
        'BSNS-3510','BSNS-4050','BSNS-4120','BSNS-4240','BSNS-4250','BSNS-4310',
    ])
    res.setdefault('notes_row_text',
        "Note: BSNS-3210 (Buyer/Seller Relations) = SI  ·  BSNS-4110 (Marketing Research) = WI  ·  "
        "BSNS-4910 (Senior Seminar) = WI  ·  W8 satisfied by: BSNS-1050, 4110, 4330, 4560, 4800  ·  "
        "W8 auto-satisfied when F1 (LART-1050) complete")
    res.setdefault('advisor_notes', '')
    res.setdefault('additional_major_sections', [])

    # Build major_subsections list for template
    if 'major_subsections' not in res:
        # Add note annotations to bc rows
        bc_rows = []
        for r in res.get('bc', []):
            r2 = dict(r)
            if r2['id'] == 'BSNS_4910': r2['note'] = ' (WI)'
            else: r2.setdefault('note', '')
            bc_rows.append(r2)
        mr_rows = []
        for r in res.get('mr', []):
            r2 = dict(r)
            if r2['id'] == 'BSNS_3210': r2['note'] = ' (SI)'
            elif r2['id'] == 'BSNS_4110': r2['note'] = ' (WI)'
            else: r2.setdefault('note', '')
            mr_rows.append(r2)

        # Derive Business Core label from catalog year
        core_label = "Business Core Requirements (43 hrs)"
        if res.get('catalog_year') == '2025-26':
            core_label = "Business Core Requirements (48 hrs)"

        res['major_subsections'] = []
        if bc_rows:
            res['major_subsections'].append((core_label, bc_rows))
        if mr_rows:
            res['major_subsections'].append(("Sport Marketing Required Courses", mr_rows))

    # Minor name
    if minor_rows := res.get('minor_rows'):
        from requirements.fsb_minors import FSB_MINORS
        minor_key = res.get('minor_key', '')
        res.setdefault('minor_name', FSB_MINORS.get(minor_key, {}).get('name', 'Minor') if minor_key else 'Minor')

    template_build(res, student_name, major_label, out, exceptions=exceptions)


# ── NON-FSB LA ROW BUILDER ────────────────────────────────────────────────────
def build_la_rows_for_non_fsb(courses, catalog_year, major_key=''):
    """
    Build LA rows for non-FSB majors.
    - W8 auto-satisfy (F1->W8) is FSB-only; non-FSB uses the W8 course list per major.
    - Cross-listing rules from the LA Requirement Application sheet are applied.
    """
    from requirements.liberal_arts_requirements import LA_OLD_FRAMEWORK, LA_RAVEN_CORE_2526 as LA_NEW_FRAMEWORK

    # ── W8 COURSE LIST PER MAJOR (from W8 Experiential Ways of Knowing sheet) ──
    W8_BY_MAJOR = {
        # Source: W8_-_Experiential_Ways_of_Knowing.csv (updated 11/14/2023)
        'psychology':              ['PSYC_2850','PSYC_3450','PSYC_4100','PSYC_4210','PSYC_4520'],
        'cinema_media_arts':       ['COMM_4800'],
        'public_relations':        ['COMM_4800'],
        'multimedia_journalism_complementary': ['COMM_4800'],
        'visual_communication':    ['ARTH_4800'],
        'literary_studies':        ['ENGL_4910'],
        'writing':                 ['ENGL_4910'],
        'english':                 ['ENGL_4910'],
        'elementary_education':    ['EDUC_4010'],
        'social_studies_teaching': ['EDUC_4010'],
        'language_arts_teaching':  ['EDUC_4010'],
        'math_teaching_ba':        ['EDUC_4010'],
        'spanish_education':       ['EDUC_4010'],
        'christian_ministries':    ['CMIN_3340','CMIN_4810','CMIN_4850'],
        'youth_ministries':        ['CMIN_3340','CMIN_4810','CMIN_4850'],
        'ministry_studies':        ['CMIN_4810'],
        'christian_spiritual_formation_complementary': ['RLGN_4960'],
        'engineering_management':  ['BSNS_1050'],
        'math_ba':                 ['MATH_4000'],
        'math_bs':                 ['MATH_4000'],
        'math_teaching_ba':        ['EDUC_4010'],
        'exercise_science':        ['EXSC_4160','EXSC_4800'],
        'sport_recreational_leadership': ['SPRL_4850'],
        'nursing_bsn':             ['NURS_4560','NURS_4950','NURS_4960','NURS_4970'],
        'nursing_accelerated':     ['NURS_4560','NURS_4950','NURS_4960','NURS_4970'],
        'nursing_rn_bsn':          ['NURS_4560','NURS_4950','NURS_4960','NURS_4970'],
        'history':                 ['HIST_2300','HIST_3260','HIST_4700','HIST_4800','HIST_4915','HIST_4930',
                                    'POSC_2810','POSC_4800','POSC_4810','POSC_4820','POSC_4860','POSC_4915',
                                    'POSC_2840','EDUC_4010'],
        'public_history':          ['HIST_4800'],
        'political_science':       ['POSC_2810','POSC_4800','POSC_4810','POSC_4820','POSC_4860','POSC_4915',
                                    'POSC_2840'],
        'polsci_philosophy_economics': ['POSC_2810','POSC_4800','POSC_4810','POSC_4820','POSC_4860',
                                        'POSC_4915','POSC_2840'],
        'international_relations': ['HIST_2300','HIST_3260','HIST_4700','HIST_4800','HIST_4915','HIST_4930',
                                    'POSC_2810','POSC_4800','POSC_4810','POSC_4820','POSC_4860','POSC_4915',
                                    'POSC_2840','EDUC_4010'],
        'national_security':       ['POSC_4800','POSC_4810','POSC_4820','POSC_4860','POSC_4915','POSC_4930',
                                    'POSC_2840'],
        'criminal_justice_major':         ['CRIM_4810'],
        'criminal_justice_major_online':  ['CRIM_4810'],
        'social_work':             ['SOWK_4850'],
        'family_science_major':    ['SOWK_4850'],
        'spanish':                 ['FLAN_3500'],
        'voice_performance_bmus':  ['MUPF_4540','MUPF_4550','MUPF_4560','MUPF_4570','MUPF_4580','MUPF_4590'],
        'instrumental_performance_bmus': ['MUPF_4540','MUPF_4550','MUPF_4560','MUPF_4570','MUPF_4580','MUPF_4590'],
        'musical_theatre_bmus':    ['MUTR_4500','MUPF_4540'],
        'musical_theatre_ba':      ['MUPF_1170','MUPF_4910'],
        'worship_arts_ba':         ['MUSC_3800'],
        'music_ba':                ['MUBS_4800','BSNS_4810'],
        'music_education_bmus':    ['MUSC_4950','MUSC_4955'],
        'songwriting':             ['MUBS_4500'],
        'dance_major':             ['DANC_4800','DANC_4910'],
        'dance_complementary':     ['DANC_4800','DANC_4910'],
        'theatre_ba':              ['THEA_4800'],
        'cs_ba':                   ['CPSC_2800','CPSC_3800','CPSC_4800','CPSC_4960'],
        'cs_bs':                   ['CPSC_2800','CPSC_3800','CPSC_4800','CPSC_4960'],
        'cs_complementary':        ['CPSC_2800','CPSC_3800','CPSC_4800','CPSC_4960'],
        'business_info_systems_complementary': ['CPSC_2800','CPSC_3800','CPSC_4800','CPSC_4960'],
        'data_science_ba':         ['CPSC_4970'],
        'data_science_bs':         ['CPSC_4970'],
        'cybersecurity_major':     ['CPSC_4480','CPSC_4820','CPSC_4970'],
        'biochemistry_ba':         ['CHEM_4920'],
        'biochemistry_bs':         ['CHEM_4920'],
        'chemistry_ba':            ['CHEM_4920'],
        'chemistry_bs':            ['CHEM_4920'],
        'public_health_ba':        ['PUBH_4950','NURS_4950','PUBH_4810','SOCI_4810'],
        'public_health_bs':        ['PUBH_4950','NURS_4950','PUBH_4810','SOCI_4810'],
        # Engineering majors — W8 via ENGR senior design
        'electrical_engineering_bs':   ['ENGR_4960'],
        'mechanical_engineering_bs':   ['ENGR_4960'],
        'mechatronics_engineering_bs': ['ENGR_4960'],
        'civil_engineering_bs':        ['ENGR_4960'],
        'engineering_physics_bs':      ['ENGR_4960'],
        'computer_engineering_bs':     ['CPSC_2800','CPSC_3800','CPSC_4800','CPSC_4960','ENGR_4960'],
        # No W8 course required
        'biology_ba':              [],
        'biology_bs':              [],
        'sociology_minor':         [],
    }
    # Default W8 for unlisted majors — broad experiential list
    W8_DEFAULT = ['LART_4500','EDUC_4010','CMIN_4810','EXSC_4800','HIST_4800',
                  'CPSC_4800','POSC_4800','NURS_4950','SOWK_4850','SPRL_4850']

    w8_courses = W8_BY_MAJOR.get(major_key, W8_DEFAULT)

    cm = cmap(courses)

    # Exception rules
    has_1110 = cm.get('ENGL_1110') or cm.get('ENGL_1100')
    has_1120 = cm.get('ENGL_1120')
    if not has_1110 and has_1120:
        synthetic = {'code':'ENGL_1110','raw':'ENGL-1110',
                     'name':'Rhetoric and Composition (tested out)',
                     'cr':3,'status':'grade posted','grade':'T','reg_date':''}
        courses = courses + [synthetic]
        cm['ENGL_1110'] = synthetic

    # Auto-detect Honors student by presence of any HNRS course
    is_honors = any(c['code'].startswith('HNRS_') for c in courses)

    # Build MAP lookup: area_key -> list of taken course codes mapped to that area
    # These come from MAP: TAKEN = AREA exceptions injected by apply_exceptions
    map_by_area = {}
    for c in courses:
        area = c.get('__map_area__')
        if area:
            map_by_area.setdefault(area, []).append(c.get('__map_taken_code__', c['code']))

    has_lart = cm.get('LART_1050')
    if not has_lart:
        if is_honors:
            # Honors students are officially exempt from LART-1050
            # HNRS-2110 satisfies First Year Experience for Honors students
            hnrs_2110 = cm.get('HNRS_2110')
            synthetic = {
                'code': 'LART_1050', 'raw': 'LART-1050',
                'name': 'First-Year Seminar (Honors exempt — HNRS-2110)',
                'cr': 0, 'status': 'grade posted', 'grade': 'T', 'reg_date': ''
            }
            if hnrs_2110 and done(hnrs_2110):
                synthetic['name'] = 'First-Year Seminar (Honors exempt — HNRS-2110)'
            courses = courses + [synthetic]
            cm['LART_1050'] = synthetic
        # Non-Honors students without LART-1050: leave as missing (Not Satisfied)

    def find_any(code_list):
        return best(courses, [norm(c.replace(' ','_').replace('-','_')) for c in code_list])

    def make_row(area, course_col, req_txt, dcr, c, s):
        if course_col is None and c is not None:
            course_col = f"{c['raw']} {c['name']}"
        return {'area':area,'course_col':course_col or '','req':req_txt,
                'status':s,'course':c,'dcr':dcr}

    la = []

    if catalog_year == '2025-26':
        fw = LA_NEW_FRAMEWORK
        for area_key in ['RC1','RC2','RC3','RC4','RC5','RC6','AU1','AU2','AU3','AU4','AU5','AU6']:
            area_def = fw.get(area_key, {})
            label = area_def.get('label', area_key)
            dcr = area_def.get('credits', 3)
            if isinstance(dcr, dict): dcr = dcr.get(catalog_year, 3)
            opts_raw = area_def.get('courses', {}).get(catalog_year, [])
            if isinstance(opts_raw, dict): opts_raw = []
            c = find_any(opts_raw)
            la.append(make_row(area_key, None, label, dcr, c, status_of(c)))
    else:
        fw = LA_OLD_FRAMEWORK
        yr = catalog_year

        # F1
        f1_opts = fw['F1']['courses'].get(yr, ['LART 1050'])
        f1_c = find_any(f1_opts)
        la.append(make_row('F1', 'LART-1050 First-Year Exper Seminar',
                           'F1 LART-1050 Understanding College', 1, f1_c, status_of(f1_c)))

        # F2 — full list from LA framework (includes HNRS 2125, HIST 2300, PSYC 3200 cross-listings)
        f2_def = fw.get('F2', {})
        f2_opts = f2_def.get('courses', {}).get(yr, [])
        f2_dcr = f2_def.get('credits', 3)
        if isinstance(f2_dcr, dict): f2_dcr = f2_dcr.get(yr, 3)
        f2_c = find_any(f2_opts + map_by_area.get('F2',[]))
        la.append(make_row('F2', None, f2_def.get('label', 'F2 Civil Discourse & Critical Reasoning'), f2_dcr, f2_c, status_of(f2_c)))

        # F3 — two rows; HNRS 2110 satisfies BOTH Writing I AND Writing II (5-hr replacement)
        # Also satisfies F3 OR W3 (not both) — engine enforces single-use
        f3_req = fw['F3'].get('required_courses', ['ENGL 1100', 'ENGL 1110', 'ENGL 1120'])
        # Writing I: ENGL 1110, ENGL 1100, or HNRS 2110
        f3_1_opts = [c for c in f3_req if '1110' in c or '1100' in c or 'HNRS' in c] or ['ENGL 1110', 'ENGL 1100', 'HNRS 2110']
        f3_2_opts = [c for c in f3_req if '1120' in c] or ['ENGL 1120']
        f3_1_c = find_any(f3_1_opts)
        f3_2_c = find_any(f3_2_opts)
        # Check if student has HNRS-2110 regardless of what won Writing I slot
        hnrs_2110_c = cm.get('HNRS_2110')
        hnrs_2110_done = hnrs_2110_c is not None and done(hnrs_2110_c)
        # HNRS-2110 satisfies BOTH Writing I and Writing II (5-hr course)
        # Even if ENGL-1110 was matched for Writing I, HNRS-2110 covers Writing II
        hnrs_2110_used_for_f3 = (f3_1_c is not None and 'HNRS' in f3_1_c.get('raw','').upper() and '2110' in f3_1_c.get('raw',''))
        if f3_2_c is None and hnrs_2110_done:
            f3_2_c = hnrs_2110_c
        # For Honors students, HNRS-2110 can ALSO satisfy W3 (no OR restriction)
        hnrs_2110_blocks_w3 = (hnrs_2110_used_for_f3 or hnrs_2110_done) and not is_honors
        la.append(make_row('F3', None, 'F3 Writing I — ENGL-1110 (or ENGL-1100 / HNRS-2110)',
                           3, f3_1_c, status_of(f3_1_c)))
        la.append(make_row('F3', None, 'F3 Writing II — ENGL-1120 (or HNRS-2110)',
                           3, f3_2_c, status_of(f3_2_c)))

        # F4
        f4_req = fw['F4'].get('required_courses', ['COMM 1000'])
        f4_opts = [c for c in f4_req if 'COMM' in c] or ['COMM 1000']
        f4_c = find_any(f4_opts)
        la.append(make_row('F4', None, fw['F4']['label'], 3, f4_c, status_of(f4_c)))

        # F5
        f5_opts = fw['F5']['courses'].get(yr, [])
        f5_dcr = fw['F5'].get('credits', 3)
        if isinstance(f5_dcr, dict): f5_dcr = f5_dcr.get(yr, 3)
        f5_c = find_any(f5_opts + map_by_area.get('F5',[]))
        la.append(make_row('F5', None, fw['F5']['label'], f5_dcr, f5_c, status_of(f5_c)))

        # F6
        f6_opts = fw['F6']['courses'].get(yr, ['BIBL 2000'])
        f6_c = find_any(f6_opts)
        la.append(make_row('F6', None, fw['F6']['label'], 3, f6_c, status_of(f6_c)))

        # F7
        f7_opts = fw['F7']['courses'].get(yr, ['PEHS 1000'])
        f7_dcr = fw['F7'].get('credits', 2)
        if isinstance(f7_dcr, dict): f7_dcr = f7_dcr.get(yr, 2)
        f7_c = find_any(f7_opts)
        la.append(make_row('F7', None, fw['F7']['label'], f7_dcr, f7_c, status_of(f7_c)))

        # W1, W2, W3, W5, W6, W7
        for wkey in ['W1','W2','W3','W5','W6','W7']:
            wdef = fw.get(wkey, {})
            w_opts = wdef.get('courses', {}).get(yr, [])
            w_dcr = wdef.get('credits', 3)
            if isinstance(w_dcr, dict): w_dcr = w_dcr.get(yr, 3)
            # HNRS 2110 satisfies F3 OR W3 — exclude from W3 if already used for F3
            if wkey == 'W3' and hnrs_2110_blocks_w3:
                w_opts = [o for o in w_opts if 'HNRS' not in o.upper() or '2110' not in o]
            # Check MAP exceptions for this area
            mapped = map_by_area.get(wkey, [])
            w_c = find_any(w_opts + mapped) if mapped else find_any(w_opts)
            la.append(make_row(wkey, None, wdef.get('label', wkey), w_dcr, w_c, status_of(w_c)))

        # W4 — check integrative (3hr AE), then AP+AX courses
        # Integrative satisfies W4 alone; AP+AX together also satisfy it
        w4_def = fw.get('W4', {})
        w4_year_data = w4_def.get('courses', {}).get(yr, {})
        if isinstance(w4_year_data, dict):
            w4_ae = w4_year_data.get('integrative', [])
            w4_ap = w4_year_data.get('AP', [])
            w4_ax = w4_year_data.get('AX', [])
            w4_all = w4_ae + w4_ap + w4_ax
        else:
            w4_all = w4_year_data
        w4_c = find_any(w4_all + map_by_area.get('W4',[]))
        la.append(make_row('W4', None, w4_def.get('label', 'W4 Aesthetic Ways of Knowing'),
                           3, w4_c, status_of(w4_c)))

        # W8 — non-FSB: NO F1 auto-satisfy. Use major-specific course list from W8 sheet.
        if w8_courses or map_by_area.get('W8'):
            w8_c = find_any((w8_courses or []) + map_by_area.get('W8',[]))
            la.append(make_row('W8', None, 'W8 Experiential Ways of Knowing',
                               2, w8_c, status_of(w8_c)))
        else:
            # Major has no W8 course (Biology, Sociology) — exempt, show as Satisfied
            la.append(make_row('W8', None,
                               'W8 Experiential Ways of Knowing — No course required for this major',
                               0, None, 'Satisfied'))

        # WI — use full list from LA framework
        wi_def = fw.get('WI', {})
        wi_opts = wi_def.get('courses', {}).get(yr, [])
        if not wi_opts:
            wi_opts = ['ENGL_3110','ENGL_3190','ENGL_3580','COMM_3130',
                       'HIST_3260','HIST_3300','BIBL_3000','RLGN_3000',
                       'BSNS_3120','BSNS_4910','ENGR_2090','HIST_3425',
                       'POSC_3320','POSC_3450','SPAN_3010','ENGL_2500']
        wi_c1 = find_any(wi_opts + map_by_area.get('WI',[]))
        la.append(make_row('WI', None,
                           'WI Writing Intensive #1 — must be from approved WI list',
                           3, wi_c1, status_of(wi_c1)))
        wi_c1_code = wi_c1['raw'].upper().replace('-','_') if wi_c1 else None
        wi_c2 = None
        for opt in wi_opts:
            candidate = cm.get(norm(opt.replace(' ','_')))
            if candidate and (done(candidate) or ip(candidate)):
                if candidate['raw'].upper().replace('-','_') != wi_c1_code:
                    wi_c2 = candidate
                    break
        la.append(make_row('WI', None,
                           'WI Writing Intensive #2 — at least one must be upper-division (3000+)',
                           3, wi_c2, status_of(wi_c2) if wi_c2 else 'Not Satisfied'))

        # SI — pull from LA framework; cross-listed courses included
        si_def = fw.get('SI', {})
        si_opts = si_def.get('courses', {}).get(yr, [])
        # Fallback list if not in framework
        if not si_opts:
            si_opts = ['COMM_1000','COMM_2000','COMM_2130','COMM_2140',
                       'ARTH_3040','BSNS_3210','BSNS_4480',
                       'ENGL_2220','HIST_2300','HNRS_2125',
                       'PSYC_3200','SPAN_3020']
        si_c = find_any(si_opts + map_by_area.get('SI',[]))
        la.append(make_row('SI', None,
                           'SI Speaking Intensive — 1 course required from approved SI list',
                           3, si_c, status_of(si_c)))

    return la


# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    courses = parse_csv('/mnt/user-data/uploads/Nolan_Netter_Classes.csv')
    res     = audit(courses)
    build(res, 'Nolan Netter', 'Sport Marketing', '/mnt/user-data/outputs/Nolan_Netter_Sport_Marketing_Audit.pdf')
