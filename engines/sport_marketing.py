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

def parse_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            rows.append({
                'code':     norm(r.get('Course Code','')),
                'raw':      r.get('Course Code','').strip().upper(),
                'name':     r.get('Course Name','').strip(),
                'cr':       _int(r.get('Credits','0')),
                'status':   r.get('Status','').strip().lower(),
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

        # SUB: TAKEN-CODE = REQUIRED-CODE
        if upper.startswith('SUB:'):
            try:
                body = line[4:].strip()
                taken_raw, req_raw = [x.strip() for x in body.split('=', 1)]
                taken_code = norm(taken_raw)
                req_code   = norm(req_raw)
                # Find the actual taken course record
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
     'F3 ENGL-1120 Writing II — ENGL-1120 (grade of C- or better required)', ['ENGL_1120'], 3),
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
    ('W4',None,'W4 Aesthetic Ways of Knowing',
     ['ARTS_1250','MUSC_2210','THEA_1000','ARTS_1210','ARTS_1230','MUSC_1000','ARTS_1000','ARTH_3040'], 3),
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
def build_la_rows_for_non_fsb(courses, catalog_year):
    """
    Build LA rows in the same dict shape as audit() produces, using the
    universal liberal_arts_requirements data (not FSB-specific LA_ROWS).
    Called by main.py for non-FSB major audits.
    """
    from requirements.liberal_arts_requirements import LA_OLD_FRAMEWORK, LA_NEW_FRAMEWORK

    cm = cmap(courses)

    # Exception rules (same as FSB audit)
    has_1110 = cm.get('ENGL_1110') or cm.get('ENGL_1100')
    has_1120 = cm.get('ENGL_1120')
    if not has_1110 and has_1120:
        synthetic = {'code':'ENGL_1110','raw':'ENGL-1110',
                     'name':'Rhetoric and Composition (tested out)',
                     'cr':3,'status':'grade posted','grade':'T','reg_date':''}
        courses = courses + [synthetic]
        cm['ENGL_1110'] = synthetic

    has_lart = cm.get('LART_1050')
    if not has_lart:
        synthetic = {'code':'LART_1050','raw':'LART-1050',
                     'name':'First-Year Seminar (exempt)',
                     'cr':0,'status':'grade posted','grade':'T','reg_date':''}
        courses = courses + [synthetic]
        cm['LART_1050'] = synthetic

    def find_any(code_list):
        return best(courses, [norm(c.replace(' ','_').replace('-','_')) for c in code_list])

    def make_row(area, course_col, req_txt, opts_raw, dcr, c, s):
        if course_col is None and c is not None:
            course_col = f"{c['raw']} {c['name']}"
        return {'area':area,'course_col':course_col or '','req':req_txt,
                'status':s,'course':c,'dcr':dcr}

    la = []

    if catalog_year == '2025-26':
        # Raven Core / AU Experience framework
        fw = LA_NEW_FRAMEWORK
        for area_key in ['RC1','RC2','RC3','RC4','RC5','RC6','AU1','AU2','AU3','AU4','AU5','AU6']:
            area_def = fw.get(area_key, {})
            label = area_def.get('label', area_key)
            dcr = area_def.get('credits', 3)
            if isinstance(dcr, dict): dcr = dcr.get(catalog_year, 3)
            opts_raw = area_def.get('courses', {}).get(catalog_year, [])
            c = find_any(opts_raw)
            s = status_of(c)
            la.append(make_row(area_key, None, label, opts_raw, dcr, c, s))
    else:
        # Old framework F1-F7, W1-W8
        fw = LA_OLD_FRAMEWORK
        yr = catalog_year

        # F1
        f1_opts = fw['F1']['courses'].get(yr, ['LART 1050'])
        f1_c = find_any(f1_opts)
        f1_ok = f1_c is not None and done(f1_c)
        f1_s = status_of(f1_c)
        la.append(make_row('F1', 'LART-1050 First-Year Exper Seminar',
                           'F1 LART-1050 Understanding College', f1_opts, 1, f1_c, f1_s))

        # F2
        f2_opts = fw['F2']['courses'].get(yr, [])
        f2_dcr = fw['F2']['credits'] if not isinstance(fw['F2']['credits'], dict) else fw['F2']['credits'].get(yr, 3)
        f2_c = find_any(f2_opts)
        la.append(make_row('F2', None, fw['F2']['label'], f2_opts, f2_dcr, f2_c, status_of(f2_c)))

        # F3 — ENGL-1110 and ENGL-1120 (two rows + WI tracking)
        f3_1_opts = fw['F3']['courses']['writing_1'].get(yr, ['ENGL 1110'])
        f3_2_opts = fw['F3']['courses']['writing_2'].get(yr, ['ENGL 1120'])
        f3_1_c = find_any(f3_1_opts)
        f3_2_c = find_any(f3_2_opts)
        la.append(make_row('F3', None, 'F3 Writing I — ENGL-1110 (or ENGL-1100/HNRS-2110)',
                           f3_1_opts, 3, f3_1_c, status_of(f3_1_c)))
        la.append(make_row('F3', None, 'F3 Writing II — ENGL-1120 (grade of C- or better required)',
                           f3_2_opts, 3, f3_2_c, status_of(f3_2_c)))

        # F4 — COMM-1000
        f4_opts = fw['F4']['courses'].get(yr, ['COMM 1000'])
        f4_c = find_any(f4_opts)
        la.append(make_row('F4', None, fw['F4']['label'], f4_opts, 3, f4_c, status_of(f4_c)))

        # F5
        f5_opts = fw['F5']['courses'].get(yr, [])
        f5_dcr = fw['F5']['credits'] if not isinstance(fw['F5']['credits'], dict) else fw['F5']['credits'].get(yr, 3)
        f5_c = find_any(f5_opts)
        la.append(make_row('F5', None, fw['F5']['label'], f5_opts, f5_dcr, f5_c, status_of(f5_c)))

        # F6
        f6_opts = fw['F6']['courses'].get(yr, ['BIBL 2000'])
        f6_c = find_any(f6_opts)
        la.append(make_row('F6', None, fw['F6']['label'], f6_opts, 3, f6_c, status_of(f6_c)))

        # F7
        f7_opts = fw['F7']['courses'].get(yr, ['PEHS 1000'])
        f7_dcr = fw['F7']['credits'] if not isinstance(fw['F7']['credits'], dict) else fw['F7']['credits'].get(yr, 2)
        f7_c = find_any(f7_opts)
        la.append(make_row('F7', None, fw['F7']['label'], f7_opts, f7_dcr, f7_c, status_of(f7_c)))

        # W1-W7
        for wkey in ['W1','W2','W3','W4','W5','W6','W7']:
            wdef = fw.get(wkey, {})
            w_opts = wdef.get('courses', {}).get(yr, [])
            w_dcr = wdef.get('credits', 3)
            if isinstance(w_dcr, dict): w_dcr = w_dcr.get(yr, 3)
            w_c = find_any(w_opts)
            la.append(make_row(wkey, None, wdef.get('label', wkey), w_opts, w_dcr, w_c, status_of(w_c)))

        # W8 — auto-satisfy if F1 done
        w8_opts = fw.get('W8', {}).get('courses', {}).get(yr, [])
        if f1_ok:
            w8_c = cm.get('BSNS_1050')
            la.append(make_row('W8', None, 'W8 Experiential Ways of Knowing',
                               w8_opts, 2,
                               w8_c or {'raw':'BSNS-1050','name':'Business as a Profession',
                                        'cr':3,'status':'grade posted','grade':'T','reg_date':''},
                               'Satisfied'))
        else:
            w8_c = find_any(w8_opts)
            la.append(make_row('W8', None, 'W8 Experiential Ways of Knowing',
                               w8_opts, 2, w8_c, status_of(w8_c)))

        # WI — two rows
        wi_opts = fw.get('WI', {}).get('courses', {}).get(yr, [])
        wi_c1 = find_any(wi_opts)
        la.append(make_row('WI', None,
                           'WI Writing Intensive #1 — must be from approved WI list',
                           wi_opts, 3, wi_c1, status_of(wi_c1)))
        la.append(make_row('WI', None,
                           'WI Writing Intensive #2 — at least one must be upper-division (3000+)',
                           [], 3, None, 'Not Satisfied'))

        # SI
        si_opts = fw.get('SI', {}).get('courses', {}).get(yr, [])
        si_dcr = fw.get('SI', {}).get('credits', 3)
        si_c = find_any(si_opts)
        la.append(make_row('SI', None,
                           'SI Speaking Intensive — 1 course required from approved SI list',
                           si_opts, si_dcr, si_c, status_of(si_c)))

    return la


# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    courses = parse_csv('/mnt/user-data/uploads/Nolan_Netter_Classes.csv')
    res     = audit(courses)
    build(res, 'Nolan Netter', 'Sport Marketing', '/mnt/user-data/outputs/Nolan_Netter_Sport_Marketing_Audit.pdf')
