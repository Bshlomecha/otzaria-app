# -*- coding: utf-8 -*-
"""הדמיות למסמך היסוד "בית המדרש". מריצים: python -I mockups.py <out_dir>"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *  # noqa

W, H = 1320, 800
WX, WY, WW, WH = 310, 96, 990, 684
RX = WX + WW - 76            # עמודת הניווט
TOP = WY + 40                # תחתית שורת הכותרת
CX0, CX1 = WX, RX            # אזור התוכן
SW_R = WX + WW - 80           # מתג עיון/חיפוש: בראש החלון, מימין, אחרי שם התוכנה
FIND_R = SW_R - 131           # שורת האיתור: מקור, ולכן מימין
FIND_W = 200
TABS_R = FIND_R - FIND_W - 8  # הכרטיסיות של השולחן הנוכחי
DESK_X0 = WX + 112            # שם שולחן העבודה: משמאל, ליד כפתורי החלון


def frame(title, sub):
    s = Svg(W, H, title)
    s.add(rect(0, 0, W, H, '#FBF7F1', r=0))
    caption_bar(s, W, 40, title, sub)
    s.add(f'<g filter="url(#sh)">{rect(WX, WY, WW, WH, C["surface"], r=10, stroke=C["outlineVariant"])}</g>')
    return s


def legend(s, items, y=120):
    xr = 286
    for i, (t, lines) in enumerate(items, 1):
        s.add(f'<circle cx="{xr-12}" cy="{y}" r="12" fill="{C["note"]}"/>')
        s.add(text(xr - 12, y + 4.5, str(i), 13, '#FFFFFF', 'middle', 700))
        s.add(text(xr - 32, y + 5, t, 14, C['note'], 'end', 700))
        for j, l in enumerate(lines):
            s.add(text(xr - 32, y + 26 + j * 18, l, 12.5, C['onSurfaceVariant'], 'end'))
        y += 44 + len(lines) * 18
    return y


def title_left_group(s, find_row=False, find_text='איתור: ברכות ב…'):
    """צד שמאל של שורת הכותרת: אחרי כפתורי החלון."""
    x = WX + 118
    if find_row:
        x = FIND_R - FIND_W
        s.add(rect(x, WY + 7, FIND_W, 27, C['card'], r=8, stroke=C['outlineVariant']))
        s.add(icon('find', x + FIND_W - 14, WY + 20, C['onSurfaceVariant'], 0.7))
        s.add(text(x + FIND_W - 28, WY + 25, find_text, 12, C['onSurfaceVariant'], 'end'))
        s.add(text(x + 10, WY + 25, 'Ctrl+O', 10.5, C['onSurfaceVariant'], 'start'))
        return x
    for i, ic in enumerate(['history', 'bookmark', 'desk']):
        s.add(icon(ic, x + 12 + i * 30, WY + 20, C['onSurfaceVariant'], 0.8))
    return x + 100


def desk_chip(s, x_right, label):
    w = 40 + len(label) * 6.8
    s.add(rect(x_right - w, WY + 8, w, 25, C['highest'], r=8))
    s.add(icon('desk', x_right - 13, WY + 20.5, C['primary'], 0.6))
    s.add(text(x_right - 26, WY + 25, label, 11.5, C['onSurface'], 'end', 600))
    s.add(icon('chev', x_right - w + 12, WY + 21, C['onSurfaceVariant'], 0.55))
    return x_right - w - 8


def tabs_row(s, x_right, tabs, active):
    xs = x_right
    for i, t in enumerate(tabs):
        label, kind = (t if isinstance(t, tuple) else (t, 'book'))
        tw = min(130, 36 + len(label) * 6.6)
        bx = xs - tw
        if i == active:
            s.add(f'<path d="M{bx} {TOP} V{WY+12} a6 6 0 0 1 6 -6 H{bx+tw-6} a6 6 0 0 1 6 6 V{TOP}z" fill="{C["surface"]}"/>')
        s.add(icon({'search': 'search', 'tool': 'calendar'}.get(kind, 'reading'), bx + tw - 15, WY + 23,
                   C['primary'] if i == active else C['onSurfaceVariant'], 0.62))
        s.add(text(bx + tw - 28, WY + 27, label, 12, C['onSurface'], 'end', 600 if i == active else 400))
        s.add(icon('close', bx + 11, WY + 23, C['onSurfaceVariant'], 0.42))
        xs = bx - 3
    s.add(icon('chev', xs - 12, WY + 22, C['onSurfaceVariant'], 0.7))   # רשימת הכרטיסיות
    return xs - 26


def chrome(s, tabs, active, rail_items, rail_active, bottom=(('settings', 'הגדרות'),), find_row=False,
           desk=None, highlight=None, divider_after=None, switch=None):
    s.add(f'<path d="M{WX+10} {WY} H{WX+WW-10} a10 10 0 0 1 10 10 V{TOP} H{WX} V{WY+10} a10 10 0 0 1 10 -10z" fill="{C["high"]}"/>')
    for i, g in enumerate(['×', '□', '—']):
        s.add(text(WX + 22 + i * 32, WY + 26, g, 14, C['onSurfaceVariant'], 'middle'))
    s.add(text(WX + WW - 16, WY + 26, 'אוצריא', 13, C['onSurfaceVariant'], 'end', 700))
    if not find_row:
        title_left_group(s, False)
        xr = WX + WW - 92
        if desk:
            xr = desk_chip(s, xr, desk)
        tabs_row(s, xr, tabs, active)
    else:
        segmented(s, SW_R, WY + 6, ['עיון', 'חיפוש'], {'עיון': 0, 'חיפוש': 1}.get(switch, -1), h=28, pad=14, size=12.5)
        title_left_group(s, True)
        if desk:
            w = 40 + len(desk) * 6.8
            desk_chip(s, DESK_X0 + w, desk)
        tabs_row(s, TABS_R, tabs, active)
    # עמודת הניווט
    s.add(f'<rect x="{RX}" y="{TOP}" width="76" height="{WY+WH-TOP-10}" fill="{C["high"]}"/>')
    s.add(f'<path d="M{RX} {WY+WH-10} V{WY+WH} H{RX+66} a10 10 0 0 0 10 -10z" fill="{C["high"]}"/>')
    s.add(line(RX, TOP, RX, WY + WH, C['outlineVariant']))
    cy = TOP + 14
    for idx, (ic, label) in enumerate(rail_items):
        if ic == '-':
            s.add(line(RX + 18, cy + 4, RX + 58, cy + 4, C['outlineVariant']))
            cy += 12
            continue
        act = label == rail_active
        if act:
            s.add(rect(RX + 14, cy - 2, 48, 32, C['secondaryContainer'], r=8))
        s.add(icon(ic, RX + 38, cy + 14, C['primary'] if act else C['onSurfaceVariant']))
        s.add(text(RX + 38, cy + 46, label, 11, C['onSurface'], 'middle', 700 if act else 400))
        if highlight and label in highlight:
            s.add(rect(RX + 5, cy - 8, 66, 64, 'none', r=10, stroke=C['note'], sw=2, extra='stroke-dasharray="5 4"'))
        cy += 62
    by = WY + WH - 68
    for ic, label in bottom:
        act = label == rail_active
        s.add(line(RX + 18, by - 6, RX + 58, by - 6, C['outlineVariant']))
        if act:
            s.add(rect(RX + 14, by + 2, 48, 32, C['secondaryContainer'], r=8))
        s.add(icon(ic, RX + 38, by + 18, C['primary'] if act else C['onSurfaceVariant']))
        s.add(text(RX + 38, by + 50, label, 11, C['onSurface'], 'middle', 700 if act else 400))
        if highlight and label in highlight:
            s.add(rect(RX + 5, by - 4, 66, 64, 'none', r=10, stroke=C['note'], sw=2, extra='stroke-dasharray="5 4"'))


def reader_toolbar(s, x0, x1, title='ברכות ב.', extra_right=None):
    s.add(rect(x0, TOP, x1 - x0, 42, C['high'], r=0))
    s.add(line(x0, TOP + 42, x1, TOP + 42, C['outlineVariant']))
    s.add(text((x0 + x1) / 2, TOP + 27, title, 14, C['onSurface'], 'middle', 600))
    xr = x1 - 16
    for ic in (extra_right or ['list', 'search', 'bookmark']):
        s.add(icon(ic, xr - 8, TOP + 21, C['onSurfaceVariant'], 0.85))
        xr -= 36
    for i, ic in enumerate(['more', 'notes', 'reading']):
        s.add(icon(ic, x0 + 22 + i * 36, TOP + 21, C['onSurfaceVariant'], 0.85))
    return TOP + 42


def book(s, x0, x1, y, lines=13, title='ברכות ב.'):
    width = min(560, x1 - x0 - 120)
    xr = (x0 + x1) / 2 + width / 2
    return book_text(s, xr, y + 44, width, lines=lines, size=17, first_title=title)


ALL_RAIL_TODAY = [('library', 'ספרייה'), ('find', 'איתור'), ('reading', 'עיון'), ('search', 'חיפוש'),
                  ('tools', 'כלים'), ('calendar', 'לוח שנה')]
RAIL_NEW = [('library', 'ספרייה'), ('-', ''), ('tools', 'כלים'), ('calendar', 'לוח שנה')]


# ---------- 0. היום ----------
def m_today():
    s = frame('היום: עמודה אחת לכל הדברים כאחד', 'מקומות, פעולות, כלים והגדרות יושבים באותה עמודה, ותוצאות החיפוש מעורבבות בין הספרים')
    chrome(s, ['ברכות ב.', ('חיפוש: קריאת שמע', 'search'), 'רש"י על ברכות', ('לוח שנה', 'tool')], 0,
           ALL_RAIL_TODAY, 'עיון', highlight=['איתור', 'הגדרות'])
    y = reader_toolbar(s, CX0, CX1)
    book(s, CX0, CX1, y)
    note(s, 1, RX - 14, TOP + 92)
    note(s, 2, 860, WY + 52)
    note(s, 3, RX - 14, WY + WH - 40)
    note(s, 4, RX - 14, TOP + 284)
    legend(s, [
        ('איתור הוא פעולה, לא מקום', ['לחיצה בעמודה פותחת חלון צף,', 'ולא עוברת לשום מסך.']),
        ('החיפוש והעיון בערבוביה', ['רשימת תוצאות היא כרטיסייה', 'בין הספרים, בלי הבדל ביניהן.']),
        ('ההגדרות הן מסך שלם', ['כמו עיון וספרייה, אף שמשנים', 'אותן לעיתים רחוקות.']),
        ('כלים ותוספים בתוך הניווט', ['הם נכנסים בין המקומות,', 'והעמודה מתארכת עד שמתמלאת.']),
    ])
    return s


# ---------- 1. מבט כולל ----------
def m_overview():
    s = frame('בית המדרש: המבנה המוצע', 'ארון הספרים, שולחן הלימוד, שולחן החיפוש, סימנייה ביד וארון שירות')
    chrome(s, ['ברכות ב.', 'רש"י', 'שו"ע או"ח נח'], 0, RAIL_NEW, '',
           find_row=True, desk='הדף היומי', highlight=['ספרייה'], switch='עיון')
    y = reader_toolbar(s, CX0, CX1)
    book(s, CX0, CX1, y)
    note(s, 1, RX - 14, TOP + 30)
    note(s, 2, SW_R - 60, WY - 16)
    note(s, 3, FIND_R - 100, WY - 16)
    note(s, 4, DESK_X0 + 55, WY - 16)
    note(s, 5, RX - 14, TOP + 112)
    note(s, 6, RX - 14, WY + WH - 40)
    legend(s, [
        ('ספרייה: הבית', ['כפתור קבוע בראש העמודה.', 'חוזר בדיוק למקום שעזבת.']),
        ('עיון | חיפוש: מתג בראש החלון', ['מחליף את כל השולחן, ולכן', 'יושב בכותרת ולא בתוך המסך.', 'לכל שולחן הכרטיסיות שלו.']),
        ('איתור: סימנייה ביד', ['שורה בכותרת, תמיד זמינה.', 'מקלידים מקום ונכנסים אליו.']),
        ('שולחן עבודה בשם', ['שם הערימה הנוכחית גלוי,', 'ומעבר בין ערימות בלחיצה.']),
        ('כלים: מתחת לקו', ['הכלים והתוספים המוצמדים', 'בחלק משלהם, מתחת לספרייה.']),
        ('הגדרות: ארון שירות', ['נשאר בתחתית, ונפתח', 'כחלון צף מעל השולחן.']),
    ])
    return s


# ---------- 2. ספרייה כחלונית ----------
def m_library_panel():
    s = frame('ספרייה: מרימים את הראש מעל הסטנדר', 'ארון הספרים נפתח כחלונית צד ברשימה, ליד הספר הפתוח, בלי לעזוב את השולחן')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, 'ספרייה', find_row=True, desk='הדף היומי', switch='עיון')
    px1, px0 = CX1, CX1 - 300
    s.add(rect(px0, TOP, 300, WY + WH - TOP, C['high'], r=0))
    s.add(line(px0, TOP, px0, WY + WH, C['outlineVariant']))
    s.add(text(px1 - 18, TOP + 30, 'ארון הספרים', 15, C['onSurface'], 'end', 700))
    s.add(icon('close', px0 + 22, TOP + 24, C['onSurfaceVariant'], 0.6))
    fy = WY + WH - 46
    s.add(line(px0 + 12, fy - 8, px1 - 12, fy - 8, C['outlineVariant']))
    s.add(rect(px0 + 14, fy, 272, 32, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(px0 + 150, fy + 21, 'לספרייה המלאה', 13, C['primary'], 'middle', 600))
    s.add(rect(px0 + 14, TOP + 50, 272, 32, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', px1 - 30, TOP + 66, C['onSurfaceVariant'], 0.7))
    s.add(text(px1 - 46, TOP + 71, 'סינון ספרים…', 12.5, C['onSurfaceVariant'], 'end'))
    rows = [(0, 'תנ"ך', 0), (0, 'משנה', 0), (0, 'תלמוד בבלי', 1), (1, 'סדר זרעים', 1), (2, 'ברכות', 2),
            (2, 'פאה', 0), (2, 'דמאי', 0), (1, 'סדר מועד', 0), (1, 'סדר נשים', 0), (0, 'תלמוד ירושלמי', 0),
            (0, 'מדרש', 0), (0, 'הלכה', 0), (0, 'קבלה', 0), (0, 'מחשבה ומוסר', 0)]
    yy = TOP + 104
    for lvl, name, state in rows:
        xr = px1 - 20 - lvl * 18
        if state == 2:
            s.add(rect(px0 + 10, yy - 17, 280, 26, C['secondaryContainer'], r=8))
        if lvl < 2:
            s.add(f'<g transform="rotate({0 if state else 90} {xr-6} {yy-5})">{icon("chev", xr - 6, yy - 5, C["onSurfaceVariant"], 0.5)}</g>')
            s.add(text(xr - 18, yy, name, 13, C['onSurface'], 'end', 600 if state else 400))
        else:
            s.add(icon('reading', xr - 6, yy - 5, C['primary'] if state else C['onSurfaceVariant'], 0.55))
            s.add(text(xr - 18, yy, name, 13, C['onSurface'], 'end', 700 if state else 400))
        yy += 30
    y = reader_toolbar(s, CX0, px0)
    book(s, CX0, px0, y, lines=12)
    note(s, 1, RX + 10, TOP + 20)
    note(s, 2, px0 + 40, WY + WH - 30)
    note(s, 3, px0 + 34, TOP + 66)
    note(s, 4, px0 + 120, TOP + 254)
    legend(s, [
        ('לחיצה שנייה על "ספרייה"', ['בתוך העיון פותחת את הארון', 'כחלונית. לחיצה ארוכה: מסך מלא.']),
        ('"לספרייה המלאה"', ['מעבר למסך הספרייה, באותו', 'מקום ובאותו סינון.']),
        ('רשימה בלבד, עם סינון', ['אותו עץ קטגוריות של הספרייה,', 'בתצוגת רשימה צרה.']),
        ('פתיחה בכרטיסייה חדשה', ['הספר נוסף לשולחן הנוכחי,', 'והחלונית נשארת פתוחה.']),
    ])
    return s


# ---------- 3. שולחן העיון ----------
def m_reading():
    s = frame('עיון: השולחן נשאר כמו היום', 'מלוא המסך, כרטיסיות, שולחנות עבודה כערימות של ספרים, והמפרשים משמאל לספר')
    chrome(s, ['ברכות ב.', 'רש"י', 'תוספות'], 0, RAIL_NEW, '',
           find_row=True, desk='הדף היומי', switch='עיון')
    PX = CX0 + 300
    y = reader_toolbar(s, PX, CX1)
    book(s, PX, CX1, y, lines=13)
    s.add(rect(CX0, TOP, 300, WY + WH - TOP, C['high'], r=0))
    s.add(line(PX, TOP, PX, WY + WH, C['outlineVariant']))
    for i in range(4):   # קצה הדפים: קווים דקיקים ובהירים, בלי כותרת
        s.add(f'<line x1="{CX0+2.5+i*2}" y1="{TOP+3+i*2}" x2="{CX0+2.5+i*2}" y2="{WY+WH-3-i*2}" '
              f'stroke="{C["onSurfaceVariant"]}" stroke-opacity="0.1" stroke-width="0.7"/>')
    s.add(icon('close', CX0 + 20, TOP + 22, C['onSurfaceVariant'], 0.55))
    cy = TOP + 50
    for name, lines_ in [('רש"י', ['מאימתי קורין את שמע בערבין. משעה', 'שהכהנים נכנסים לאכול בתרומתן:', 'כהנים שנטמאו וטבלו והעריב שמשן']),
                          ('תוספות', ['מאימתי קורין את שמע בערבית. פירש', 'רש"י ואנן היכי קרינן מבעוד יום ואין', 'אנו ממתינין לצאת הכוכבים']),
                          ('מהרש"א', ['בא"ד ואין אנו ממתינין כו׳ ונראה', 'דלא קשיא להו אלא מהא דלא'])]:
        s.add(rect(CX0 + 10, cy, 280, 30 + 22 * len(lines_), C['card'], r=8, stroke=C['outlineVariant']))
        s.add(text(PX - 24, cy + 22, name, 13, C['primary'], 'end', 700))
        for j, l in enumerate(lines_):
            s.add(text(PX - 24, cy + 46 + j * 22, l, 14, C['onSurface'], 'end', 400, RASHI))
        cy += 44 + 22 * len(lines_)
    # רשימת שולחנות פתוחה
    dx0 = DESK_X0
    dx1 = dx0 + 250
    s.add(f'<g filter="url(#sh)">{rect(dx0, WY + 38, 250, 210, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(text(dx1 - 14, WY + 62, 'שולחנות עבודה', 12, C['onSurfaceVariant'], 'end', 700))
    desks = [('הדף היומי', '4 ספרים', True), ('הכנה לשיעור', '7 ספרים', False), ('הלכות שבת', '3 ספרים', False)]
    yy = WY + 74
    for name, cnt, act in desks:
        if act:
            s.add(rect(dx0 + 8, yy, 234, 38, C['primaryContainer'], r=8, stroke=C['primary'], sw=1.2))
        s.add(icon('desk', dx1 - 24, yy + 19, C['primary'] if act else C['onSurfaceVariant'], 0.75))
        s.add(text(dx1 - 42, yy + 18, name, 13, C['onSurface'], 'end', 700 if act else 400))
        s.add(text(dx1 - 42, yy + 33, cnt, 11, C['onSurfaceVariant'], 'end'))
        yy += 44
    s.add(line(dx0 + 12, yy + 2, dx1 - 12, yy + 2, C['outlineVariant']))
    s.add(text(dx1 - 22, yy + 24, '+ שולחן עבודה חדש', 12.5, C['primary'], 'end', 600))
    note(s, 1, DESK_X0 + 55, WY - 16)
    note(s, 2, TABS_R - 150, WY - 16)
    note(s, 3, PX + 14, TOP + 420)
    legend(s, [
        ('שולחנות עבודה', ['שם השולחן תמיד גלוי בכותרת.', 'לחיצה פותחת את רשימת', 'השולחנות, בלי חלון נפרד.']),
        ('רשימת הכרטיסיות', ['החץ שבסוף הכרטיסיות, כמו', 'היום: פתוחים ונסגרו לאחרונה.']),
        ('מימין המקור, משמאל הפירוש', ['הספר והניווט בו מימין.', 'מפרשים, תוצאות ומסקנות', 'יוצאים תמיד בצד שמאל.']),
    ])
    return s


# ---------- 4. איתור ----------
def m_find():
    s = frame('איתור: כמו לפתוח סימנייה בספר', 'שורה בכותרת שממנה נגללות האפשרויות. מראה מקום, סימניות ואחרונים, במקום אחד')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, '', find_row=True, desk='הדף היומי', switch='עיון')
    y = reader_toolbar(s, CX0, CX1)
    book(s, CX0, CX1, y)
    fx1 = FIND_R
    fx0 = fx1 - 420
    s.add(rect(FIND_R - FIND_W, WY + 7, FIND_W, 27, C['card'], r=8, stroke=C['primary'], sw=1.6))
    s.add(rect(FIND_R - FIND_W + 56, WY + 12, FIND_W - 62, 17, C['card'], r=0))
    s.add(text(FIND_R - 28, WY + 25, 'ברכות ב', 12.5, C['onSurface'], 'end', 600))
    s.add(f'<g filter="url(#sh)">{rect(fx0, WY + 38, 420, 352, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    yy = WY + 62

    def head(t):
        nonlocal yy
        yy += 8
        s.add(text(fx1 - 16, yy, t, 11.5, C['primary'], 'end', 700))
        yy += 10

    def item(t, sub, ic, sel=False):
        nonlocal yy
        if sel:
            s.add(rect(fx0 + 8, yy, 404, 40, C['secondaryContainer'], r=8))
        s.add(icon(ic, fx1 - 26, yy + 20, C['primary'] if sel else C['onSurfaceVariant'], 0.75))
        s.add(text(fx1 - 46, yy + 18, t, 13.5, C['onSurface'], 'end', 700 if sel else 500))
        s.add(text(fx1 - 46, yy + 34, sub, 11, C['onSurfaceVariant'], 'end'))
        yy += 44

    head('מראי מקום')
    item('ברכות ב.', 'תלמוד בבלי · סדר זרעים', 'reading', True)
    item('ברכות ב:', 'תלמוד בבלי · סדר זרעים', 'reading')
    item('ירושלמי ברכות ב', 'תלמוד ירושלמי · פרק ב', 'reading')
    yy += 6
    head('סימניות')
    item('ברכות ב. — "מאימתי"', 'נשמר לפני שבוע', 'bookmark')
    yy += 6
    head('נפתחו לאחרונה')
    item('רש"י על ברכות ב.', 'היום, 08:40', 'history')
    s.add(line(fx0 + 12, yy + 4, fx1 - 12, yy + 4, C['outlineVariant']))
    s.add(text(fx1 - 18, yy + 28, 'חפש "ברכות ב" בכל הספרים', 12.5, C['primary'], 'end', 600))
    s.add(text(fx0 + 18, yy + 28, 'איתור מתקדם…', 12.5, C['primary'], 'start', 600))
    note(s, 1, FIND_R - 100, WY - 16)
    note(s, 2, fx0 - 14, WY + 90)
    note(s, 3, fx0 - 14, WY + 272)
    note(s, 4, fx0 - 14, yy + 24)
    legend(s, [
        ('שורת האיתור בכותרת', ['תמיד במקום, בכל מסך.', 'Ctrl+O ממקד אותה, כמו היום.']),
        ('מקלידים ונכנסים', ['Enter פותח את התוצאה הראשונה', 'בשולחן הנוכחי.']),
        ('סימניות ואחרונים', ['גם הם גישה ישירה למקום ידוע,', 'ולכן יושבים באותה רשימה.']),
        ('שני מעברים', ['"חפש בכל הספרים" עובר', 'לשולחן החיפוש. "איתור מתקדם"', 'פותח את החלון של היום.']),
    ])
    return s


# ---------- 5. שולחן החיפוש ----------
def m_search():
    s = frame('חיפוש: השולחן השני', 'כל רשימות התוצאות על שולחן משלהן, נשמרות, וזמינות בלחיצה מכל מקום')
    chrome(s, [('קריאת שמע', 'search'), ('עמוד השחר', 'search')], 0, RAIL_NEW, '',
           find_row=True, desk='הדף היומי', switch='חיפוש')
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, '#F5EEE1', r=0))   # גוון רקע מעט שונה מן העיון
    # סרגל החיפוש
    s.add(rect(CX0, TOP, CX1 - CX0, 54, C['high'], r=0))
    s.add(line(CX0, TOP + 54, CX1, TOP + 54, C['outlineVariant']))
    s.add(rect(CX0 + 250, TOP + 11, CX1 - CX0 - 270, 32, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', CX1 - 36, TOP + 27, C['onSurfaceVariant'], 0.8))
    s.add(text(CX1 - 54, TOP + 32, 'קריאת שמע', 14, C['onSurface'], 'end', 600))
    s.add(text(CX0 + 262, TOP + 32, 'מרחק 2 · כל הספרייה', 11.5, C['onSurfaceVariant'], 'start'))
    for i, (ic, lab) in enumerate([('save', 'שמור'), ('filter', 'סינון'), ('more', '')]):
        s.add(icon(ic, CX0 + 30 + i * 70, TOP + 27, C['onSurfaceVariant'], 0.8))
        if lab:
            s.add(text(CX0 + 46 + i * 70, TOP + 32, lab, 12, C['onSurface'], 'start'))
    # עץ סינון
    fx0 = CX1 - 220
    s.add(rect(fx0, TOP + 55, 220, WY + WH - TOP - 55, C['high'], r=0))
    s.add(line(fx0, TOP + 55, fx0, WY + WH, C['outlineVariant']))
    s.add(text(CX1 - 16, TOP + 84, 'סינון לפי ספרים', 12, C['primary'], 'end', 700))
    for i, (n, c) in enumerate([('תלמוד בבלי', 212), ('תלמוד ירושלמי', 64), ('משנה', 31), ('הלכה', 145), ('מפרשים', 380), ('מדרש', 52)]):
        yy = TOP + 112 + i * 30
        s.add(rect(CX1 - 34, yy - 12, 14, 14, C['primary'] if i in (0, 3) else C['card'], r=3, stroke=C['primary']))
        s.add(text(CX1 - 42, yy, n, 13, C['onSurface'], 'end'))
        s.add(text(fx0 + 16, yy, str(c), 11.5, C['onSurfaceVariant'], 'start'))
    # תוצאות
    rx1, rx0 = fx0 - 18, CX0 + 18
    s.add(text(rx1, TOP + 82, '357 תוצאות', 12.5, C['onSurfaceVariant'], 'end', 600))
    res = [('ברכות ב.', 'תלמוד בבלי', ['מאימתי קורין את ', 'שמע', ' בערבין משעה שהכהנים נכנסים']),
           ('ברכות י.', 'תלמוד בבלי', ['הקורא את ', 'שמע', ' בשחרית מברך שתים לפניה ואחת']),
           ('שולחן ערוך או"ח נח, א', 'הלכה', ['זמן ', 'קריאת שמע', ' של שחרית משיכיר בין תכלת']),
           ('משנה ברורה נח', 'הלכה', ['ומצוה מן המובחר לקרות ', 'קריאת שמע', ' כותיקין'])]
    yy = TOP + 96
    for ref, cat, parts in res:
        s.add(rect(rx0, yy, rx1 - rx0, 92, C['card'], r=8, stroke=C['outlineVariant']))
        s.add(text(rx1 - 14, yy + 24, ref, 14, C['onSurface'], 'end', 700))
        s.add(text(rx0 + 14, yy + 24, cat, 11.5, C['onSurfaceVariant'], 'start'))
        t = ''.join(f'<tspan fill="#B3261E" font-weight="700">{escape(p)}</tspan>' if i == 1 else escape(p)
                    for i, p in enumerate(parts))
        s.add(f'<text x="{rx1-14}" y="{yy+56}" font-size="16" fill="{C["onSurface"]}" text-anchor="start" font-family="{SERIF}">{t}</text>')
        s.add(text(rx1 - 14, yy + 79, 'פתח · פתח לצד הספר', 11.5, C['primary'], 'end', 600))
        yy += 104
    note(s, 1, SW_R - 60, WY - 16)
    note(s, 2, TABS_R - 120, WY - 16)
    note(s, 3, CX0 + 96, TOP + 46)
    note(s, 4, rx1 - 170, TOP + 175)
    legend(s, [
        ('המתג "חיפוש" בראש החלון', ['מחליף את כל השולחן לשולחן', 'החיפוש, עם הכרטיסייה האחרונה.', 'חיפוש חדש: + או Ctrl+Shift+F.']),
        ('רק רשימות תוצאות', ['הכרטיסיות כאן הן חיפושים.', 'גוון הרקע שונה מעט מן העיון,', 'כדי שהלב ירגיש את ההבדל.']),
        ('רשימה נשמרת', ['"שמור" שומר את הרשימה עם', 'הסינון, לחזור אליה אחר כך.']),
        ('ספר המפתח ליד הגמרא', ['"פתח לצד הספר" מניח את', 'רשימת התוצאות משמאל לספר', 'בעיון, בחלון מפוצל.']),
    ])
    return s


# ---------- 6. הגדרות ----------
def m_settings():
    s = frame('הגדרות: ארון השירות', 'חלון צף מעל השולחן. הלימוד נשאר מאחור, ו־Esc מחזיר אליו')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, 'הגדרות', find_row=True, desk='הדף היומי', switch='עיון')
    y = reader_toolbar(s, CX0, CX1)
    book(s, CX0, CX1, y)
    s.add(rect(WX, TOP, WW, WY + WH - TOP, C['scrim'], r=0))
    dx0, dy0, dw, dh = WX + 90, WY + 70, 740, 560
    dx1 = dx0 + dw
    s.add(f'<g filter="url(#sh)">{rect(dx0, dy0, dw, dh, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(f'<path d="M{dx0+8} {dy0} H{dx1-8} a8 8 0 0 1 8 8 V{dy0+52} H{dx0} V{dy0+8} a8 8 0 0 1 8 -8z" fill="{C["highest"]}"/>')
    s.add(rect(dx1 - 48, dy0 + 10, 32, 32, C['primaryContainer'], r=8))
    s.add(icon('settings', dx1 - 32, dy0 + 26, C['primary'], 0.85))
    s.add(text(dx1 - 60, dy0 + 33, 'הגדרות', 17, C['onSurface'], 'end', 700))
    s.add(icon('close', dx0 + 24, dy0 + 26, C['onSurfaceVariant'], 0.7))
    s.add(rect(dx0 + 48, dy0 + 12, 200, 28, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', dx0 + 234, dy0 + 26, C['onSurfaceVariant'], 0.65))
    s.add(text(dx0 + 220, dy0 + 31, 'חיפוש בהגדרות…', 12, C['onSurfaceVariant'], 'end'))
    # ניווט פנימי
    nx0 = dx1 - 180
    s.add(line(nx0, dy0 + 52, nx0, dy0 + dh, C['outlineVariant']))
    groups = [('תצוגה וקריאה', ['מראה', 'כתב', 'עיון בספר']), ('ספרייה וכלים', ['ספרייה', 'חיפוש', 'כלים']),
              ('התוכנה', ['קיצורי מקשים', 'מערכת'])]
    yy = dy0 + 80
    for g, items in groups:
        s.add(text(dx1 - 18, yy, g, 11, C['onSurfaceVariant'], 'end', 700))
        yy += 12
        for it in items:
            act = it == 'כתב'
            if act:
                s.add(rect(nx0 + 8, yy, 164, 30, C['secondaryContainer'], r=8))
            s.add(text(dx1 - 22, yy + 20, it, 13.5, C['onSurface'], 'end', 700 if act else 400))
            yy += 34
        yy += 16
    s.add(line(nx0 + 14, dy0 + dh - 50, dx1 - 14, dy0 + dh - 50, C['outlineVariant']))
    # תוכן
    cx1, cx0 = nx0 - 20, dx0 + 20
    s.add(text(cx1, dy0 + 84, 'כתב', 19, C['onSurface'], 'end', 700))
    s.add(text(cx1, dy0 + 106, 'איך הטקסט עצמו נראה, מוצג ומועתק', 12.5, C['onSurfaceVariant'], 'end'))
    cardy = dy0 + 122
    s.add(rect(cx0, cardy, cx1 - cx0, 168, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(cx1 - 16, cardy + 26, 'גופן וגודל', 13, C['primary'], 'end', 700))
    rows = [('גופן הספר', 'סוג הגופן לטקסט הספרים', 'dd'), ('גודל גופן הספר', 'גודל הטקסט בספרים', 'sl'),
            ('גודל טקסט בתוצאות החיפוש', 'בנפרד מגודל הספר', 'sl')]
    ry = cardy + 40
    for t_, sub, kind in rows:
        s.add(text(cx1 - 16, ry + 18, t_, 14, C['onSurface'], 'end', 600))
        s.add(text(cx1 - 16, ry + 35, sub, 11.5, C['onSurfaceVariant'], 'end'))
        if kind == 'dd':
            s.add(rect(cx0 + 16, ry + 8, 170, 28, C['card'], r=8, stroke=C['outlineVariant']))
            s.add(text(cx0 + 176, ry + 27, 'Frank Ruhl', 12.5, C['onSurface'], 'end'))
            s.add(icon('chev', cx0 + 30, ry + 22, C['onSurfaceVariant'], 0.55))
        else:
            s.add(line(cx0 + 56, ry + 22, cx0 + 186, ry + 22, C['outlineVariant'], 4, 'stroke-linecap="round"'))
            s.add(line(cx0 + 110, ry + 22, cx0 + 186, ry + 22, C['primary'], 4, 'stroke-linecap="round"'))
            s.add(f'<circle cx="{cx0+110}" cy="{ry+22}" r="8" fill="{C["primary"]}"/>')
            s.add(text(cx0 + 16, ry + 27, '22', 12.5, C['onSurfaceVariant'], 'start'))
        ry += 42
    cardy += 182
    s.add(rect(cx0, cardy, cx1 - cx0, 150, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(cx1 - 16, cardy + 26, 'תצוגת הטקסט', 13, C['primary'], 'end', 700))
    rows = [('ניקוד', True), ('טעמי המקרא', False), ('ציוני הערות שוליים', True)]
    ry = cardy + 40
    for t_, on in rows:
        s.add(text(cx1 - 16, ry + 22, t_, 14, C['onSurface'], 'end', 600))
        toggle(s, cx0 + 16, ry + 8, on)
        ry += 34
    note(s, 1, dx0 - 16, dy0 + 120)
    note(s, 2, dx0 + 266, dy0 + 26)
    note(s, 3, nx0 - 4, dy0 + 200)
    note(s, 4, nx0 - 4, dy0 + dh - 25)
    legend(s, [
        ('חלון צף, לא מסך', ['גודל "גדול" של מערכת העיצוב.', 'מתחת לרוחב 600 נפתח במסך מלא.']),
        ('חיפוש בהגדרות', ['כמו היום: קפיצה לכרטיס', 'ולהגדרה, עם הבהוב.']),
        ('שמונה לשוניות, שלוש קבוצות', ['לפי ההצעה למבנה ההגדרות.', 'אודות יוצא מהרשימה.']),
        ('אודות יצא מההגדרות', ['עבר לשמאל שורת הכותרת,', 'למקום מרכזי. אינו הגדרה.']),
    ])
    return s


ALL = [('00-today', m_today), ('01-overview', m_overview), ('02-library-panel', m_library_panel),
       ('03-reading-desk', m_reading), ('04-find-row', m_find), ('05-search-desk', m_search),
       ('06-settings-window', m_settings)]

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, fn in ALL:
        with open(os.path.join(out, name + '.svg'), 'w', encoding='utf8') as f:
            f.write(fn().render())
        print(name)
