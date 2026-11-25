# -*- coding: utf-8 -*-
"""גרסה 2: הספרייה היא האוצר, והאיתור יושב בתוכה. מריצים: python -I mockups2.py <out_dir>"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mockups as m  # noqa
from kit import *  # noqa
from mockups import (W, H, WX, WY, WW, WH, RX, TOP, CX0, CX1, SW_R, frame, legend, desk_chip, tabs_row,
                     reader_toolbar, book, RAIL_NEW, DESK_X0)

TABS_R = SW_R - 131
N = WY - 16


def chrome(s, tabs, active, rail_items, rail_active, bottom=(('settings', 'הגדרות'),), find_row=False,
           desk=None, highlight=None, divider_after=None, switch=None):
    """שורת הכותרת בלי איתור: שם התוכנה, מתג השולחנות, כרטיסיות, ושם שולחן העבודה משמאל."""
    if switch is None:
        return _old_chrome(s, tabs, active, rail_items, rail_active, bottom, find_row, desk, highlight)
    s.add(f'<path d="M{WX+10} {WY} H{WX+WW-10} a10 10 0 0 1 10 10 V{TOP} H{WX} V{WY+10} a10 10 0 0 1 10 -10z" fill="{C["high"]}"/>')
    for i, g in enumerate(['×', '□', '—']):
        s.add(text(WX + 22 + i * 32, WY + 26, g, 14, C['onSurfaceVariant'], 'middle'))
    s.add(text(WX + WW - 16, WY + 26, 'אוצריא', 13, C['onSurfaceVariant'], 'end', 700))
    segmented(s, SW_R, WY + 6, ['עיון', 'חיפוש'], {'עיון': 0, 'חיפוש': 1}.get(switch, -1), h=28, pad=14, size=12.5)
    # אודות: מקום מרכזי, בשמאל שורת הכותרת
    s.add(icon('info', WX + 124, WY + 20.5, C['onSurfaceVariant'], 0.6))
    s.add(text(WX + 136, WY + 25, 'אודות', 12, C['onSurfaceVariant'], 'start', 600))
    if desk:
        w = 40 + len(desk) * 6.8
        desk_chip(s, DESK_X0 + 66 + w, desk)
    tabs_row(s, TABS_R, tabs, active)
    _rail(s, rail_items, rail_active, bottom, highlight)


_old_chrome = m.chrome


def _rail(s, rail_items, rail_active, bottom, highlight):
    s.add(f'<rect x="{RX}" y="{TOP}" width="76" height="{WY+WH-TOP-10}" fill="{C["high"]}"/>')
    s.add(f'<path d="M{RX} {WY+WH-10} V{WY+WH} H{RX+66} a10 10 0 0 0 10 -10z" fill="{C["high"]}"/>')
    s.add(line(RX, TOP, RX, WY + WH, C['outlineVariant']))
    cy = TOP + 14
    for ic, label in rail_items:
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


m.chrome = chrome   # כל ההדמיות הקיימות עוברות לכותרת החדשה
m.TABS_R = TABS_R


def find_field(s, x1, y, w, h=42, typed=None, focus=False, placeholder='איתור מראה מקום: ברכות ב., שו"ע או"ח נח, רמב"ם שבת ב ג'):
    s.add(rect(x1 - w, y, w, h, C['card'], r=8, stroke=C['primary'] if focus else C['outlineVariant'], sw=1.6 if focus else 1))
    s.add(icon('find', x1 - 20, y + h / 2, C['primary'], 0.85))
    if typed:
        s.add(text(x1 - 40, y + h / 2 + 5, typed, 15, C['onSurface'], 'end', 600))
        s.add(line(x1 - 40 - len(typed) * 8.2, y + 10, x1 - 40 - len(typed) * 8.2, y + h - 10, C['primary'], 1.5))
    else:
        s.add(text(x1 - 40, y + h / 2 + 5, placeholder, 14, C['onSurfaceVariant'], 'end'))
    s.add(rect(x1 - w + 8, y + h / 2 - 11, 88, 22, C['highest'], r=6))
    s.add(text(x1 - w + 52, y + h / 2 + 4, 'Ctrl+O', 11, C['onSurfaceVariant'], 'middle'))


def names_field(s, x1, y, w, h=32, placeholder='חיפוש מדף או ספר בספרייה'):
    s.add(rect(x1 - w, y, w, h, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', x1 - 18, y + h / 2, C['onSurfaceVariant'], 0.7))
    s.add(text(x1 - 34, y + h / 2 + 4.5, placeholder, 12.5, C['onSurfaceVariant'], 'end'))


SHELVES = ['תנ"ך', 'משנה', 'תלמוד בבלי', 'תלמוד ירושלמי', 'מדרש', 'הלכה', 'שו"ת', 'קבלה',
           'מחשבה ומוסר', 'חסידות', 'ספרות עזר', 'ספרים אישיים']


def library_screen(s, typed=None):
    """מסך הספרייה: שורת איתור, שורת כלים כמו היום, מדפים, ותצוגה מקדימה משמאל."""
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, C['panel'], r=0))
    s.add(f'<path d="M{CX0} {WY+WH-10} V{WY+WH} H{CX0+10}" fill="{C["panel"]}"/>')
    # שורת האיתור, בראש האוצר
    fy = TOP + 18
    find_field(s, CX1 - 24, fy, 560, typed=typed, focus=bool(typed))
    s.add(rect(CX0 + 24, fy + 7, 196, 28, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('calendar', CX0 + 206, fy + 21, C['primary'], 0.65))
    s.add(text(CX0 + 192, fy + 26, 'דף היומי · ברכות ב', 12.5, C['onSurface'], 'end', 600))
    # שורת הכלים של היום: מיקום, חיפוש בשמות, תצוגה
    ty = fy + 60
    s.add(line(CX0 + 16, ty - 8, CX1 - 16, ty - 8, C['outlineVariant']))
    s.add(text(CX1 - 26, ty + 21, 'ספרייה', 15, C['onSurface'], 'end', 700))
    names_field(s, CX1 - 96, ty, 300)
    for i, ic in enumerate(['tools', 'list', 'info']):
        s.add(icon(ic, CX0 + 36 + i * 34, ty + 16, C['onSurfaceVariant'], 0.8))
    # מדפים
    gx1 = CX1 - 24
    px0, pw = CX0 + 24, 228
    cols, gap = 4, 12
    tw = (gx1 - (px0 + pw + 18) - gap * (cols - 1)) / cols
    gy = ty + 50
    for i, name in enumerate(SHELVES):
        r_, c_ = divmod(i, cols)
        x = gx1 - (c_ + 1) * tw - c_ * gap
        y = gy + r_ * (92 + gap)
        sel = name == 'תלמוד בבלי'
        s.add(rect(x, y, tw, 92, C['secondaryContainer'] if sel else C['card'], r=8,
                   stroke=C['primary'] if sel else C['outlineVariant'], sw=1.4 if sel else 1))
        s.add(icon('library', x + tw - 24, y + 26, C['primary'], 0.9))
        s.add(text(x + tw - 14, y + 66, name, 14.5, C['onSurface'], 'end', 700 if sel else 600))
    # תצוגה מקדימה, משמאל
    py = gy
    s.add(rect(px0, py, pw, 3 * 92 + 2 * gap, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(px0 + pw - 14, py + 28, 'תלמוד בבלי', 15, C['onSurface'], 'end', 700))
    s.add(text(px0 + pw - 14, py + 48, 'שישה סדרים · 37 מסכתות', 12, C['onSurfaceVariant'], 'end'))
    for j, l in enumerate(['סדר זרעים', 'סדר מועד', 'סדר נשים', 'סדר נזיקין', 'סדר קדשים', 'סדר טהרות']):
        s.add(icon('chev', px0 + pw - 22, py + 78 + j * 28, C['onSurfaceVariant'], 0.5))
        s.add(text(px0 + pw - 36, py + 83 + j * 28, l, 13, C['onSurface'], 'end'))
    return fy, ty, gy, px0, pw


# ---------- 1. מבט כולל ----------
def m_overview():
    s = frame('בית המדרש: המבנה המוצע', 'האוצר והאיתור שבו, שולחן הלימוד, שולחן החיפוש וארון השירות')
    chrome(s, ['ברכות ב.', 'רש"י', 'שו"ע או"ח נח'], 0, RAIL_NEW, '', desk='הדף היומי',
           highlight=['ספרייה'], switch='עיון')
    y = reader_toolbar(s, CX0, CX1)
    book(s, CX0, CX1, y)
    note(s, 1, RX - 14, TOP + 30)
    note(s, 2, SW_R - 60, N)
    note(s, 3, DESK_X0 + 120, N)
    note(s, 4, RX - 14, TOP + 112)
    note(s, 5, RX - 14, WY + WH - 40)
    legend(s, [
        ('ספרייה: האוצר, הבית', ['המקום הקבוע, בראש העמודה.', 'בתוכו שורת האיתור.', 'חוזר בדיוק למקום שעזבת.']),
        ('עיון | חיפוש: מתג בראש החלון', ['מחליף את כל השולחן, ולכן', 'יושב בכותרת ולא בתוך המסך.', 'לכל שולחן הכרטיסיות שלו.']),
        ('שולחן עבודה בשם', ['שם הערימה הנוכחית גלוי,', 'ומעבר בין ערימות בלחיצה.']),
        ('כלים: מתחת לקו', ['הכלים והתוספים המוצמדים', 'בחלק משלהם, מתחת לספרייה.']),
        ('הגדרות: ארון שירות', ['נשאר בתחתית, ונפתח', 'כחלון צף מעל השולחן.']),
    ])
    return s


# ---------- 2. האוצר ----------
def m_library_home():
    s = frame('ספרייה: האוצר', 'המקום הקבוע. המדפים וחיפוש השמות כמו היום, ובראשם שורה לאיתור מראה מקום')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy, px0, pw = library_screen(s)
    note(s, 1, CX1 - 600, fy + 21)
    note(s, 2, CX1 - 412, ty + 16)
    note(s, 3, CX1 - 40, gy + 98)
    note(s, 4, px0 + pw + 4, gy + 160)
    note(s, 5, RX + 10, TOP + 20)
    legend(s, [
        ('שורת האיתור', ['מראה מקום, ו־Enter פותח מיד', 'בשולחן העיון. בולטת בראש', 'האוצר, ולא בשורת הכותרת.']),
        ('חיפוש מדף או ספר', ['השדה של היום, לשמות בלבד.', 'מוצע לשנות את התווית שלו,', 'כדי שלא תתחלף ב"איתור".']),
        ('המדפים, כמו היום', ['תיבות המדפים בלי שינוי.', 'רשת או רשימה, לפי ההגדרה.']),
        ('תצוגה מקדימה משמאל', ['מה שנבחר מוצג בצד שמאל,', 'לפי כלל ימין ושמאל.']),
        ('הבית', ['כפתור קבוע בראש העמודה.', 'החזרה אליו שומרת את המצב.']),
    ])
    return s


# ---------- 3. ארון הספרים כחלונית ----------
def m_library_panel():
    s = frame('ספרייה: מרימים את הראש מעל הסטנדר', 'האוצר נפתח כחלונית צד מימין, ובה גם שורת האיתור, בלי לעזוב את השולחן')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='עיון')
    px1, px0 = CX1, CX1 - 300
    s.add(rect(px0, TOP, 300, WY + WH - TOP, C['high'], r=0))
    s.add(line(px0, TOP, px0, WY + WH, C['outlineVariant']))
    s.add(icon('close', px0 + 22, TOP + 24, C['onSurfaceVariant'], 0.6))
    find_field(s, px1 - 14, TOP + 46, 272, h=36, placeholder='איתור מראה מקום…')
    names_field(s, px1 - 14, TOP + 90, 272, h=30, placeholder='סינון מדפים וספרים…')
    rows = [(0, 'תנ"ך', 0), (0, 'משנה', 0), (0, 'תלמוד בבלי', 1), (1, 'סדר זרעים', 1), (2, 'ברכות', 2),
            (2, 'פאה', 0), (2, 'דמאי', 0), (1, 'סדר מועד', 0), (1, 'סדר נשים', 0), (0, 'תלמוד ירושלמי', 0),
            (0, 'מדרש', 0), (0, 'הלכה', 0)]
    yy = TOP + 146
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
    fy = WY + WH - 46
    s.add(line(px0 + 12, fy - 8, px1 - 12, fy - 8, C['outlineVariant']))
    s.add(rect(px0 + 14, fy, 272, 32, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(px0 + 150, fy + 21, 'לאוצר המלא', 13, C['primary'], 'middle', 600))
    y = reader_toolbar(s, CX0, px0)
    book(s, CX0, px0, y, lines=12)
    note(s, 1, RX + 10, TOP + 20)
    note(s, 2, px0 + 30, TOP + 64)
    note(s, 3, px0 + 40, TOP + 250)
    note(s, 4, px0 + 40, WY + WH - 30)
    legend(s, [
        ('לחיצה על "ספרייה" בתוך העיון', ['פותחת את האוצר כחלונית מימין.', 'לחיצה נוספת: המסך המלא.']),
        ('האיתור בא עם האוצר', ['גם בחלונית שורת האיתור בראש.', 'Ctrl+O מהשולחן פותח אותה כאן,', 'בלי לעזוב את הלימוד.']),
        ('המדפים ברשימה', ['אותו עץ, בתצוגה צרה. ספר', 'שנבחר נפתח בכרטיסייה חדשה.']),
        ('"לאוצר המלא"', ['מעבר למסך הספרייה, באותו', 'מקום ובאותו סינון.']),
    ])
    return s


# ---------- 5. איתור ----------
def m_find():
    s = frame('איתור: כמו לפתוח סימנייה בספר', 'בתוך האוצר: מקלידים מראה מקום ונכנסים. גם סימניות ואחרונים באותה רשימה')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy, px0, pw = library_screen(s, typed='ברכות ב')
    fx1 = CX1 - 24
    fx0 = fx1 - 560
    s.add(f'<g filter="url(#sh)">{rect(fx0, fy + 48, 560, 352, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    yy = fy + 64

    def head(t):
        nonlocal yy
        yy += 8
        s.add(text(fx1 - 16, yy, t, 11.5, C['primary'], 'end', 700))
        yy += 10

    def item(t, sub, ic, sel=False):
        nonlocal yy
        if sel:
            s.add(rect(fx0 + 8, yy, 544, 40, C['secondaryContainer'], r=8))
        s.add(icon(ic, fx1 - 26, yy + 20, C['primary'] if sel else C['onSurfaceVariant'], 0.75))
        s.add(text(fx1 - 46, yy + 18, t, 13.5, C['onSurface'], 'end', 700 if sel else 500))
        s.add(text(fx1 - 46, yy + 34, sub, 11, C['onSurfaceVariant'], 'end'))
        yy += 44

    head('מראי מקום')
    item('ברכות ב.', 'תלמוד בבלי · סדר זרעים', 'reading', True)
    item('ברכות ב:', 'תלמוד בבלי · סדר זרעים', 'reading')
    item('ירושלמי ברכות ב', 'תלמוד ירושלמי · פרק ב', 'reading')
    head('סימניות')
    item('ברכות ב. — "מאימתי"', 'נשמר לפני שבוע', 'bookmark')
    head('נפתחו לאחרונה')
    item('רש"י על ברכות ב.', 'היום, 08:40', 'history')
    s.add(line(fx0 + 12, yy + 4, fx1 - 12, yy + 4, C['outlineVariant']))
    s.add(text(fx1 - 18, yy + 28, 'חפש "ברכות ב" בכל הספרים', 12.5, C['primary'], 'end', 600))
    s.add(text(fx0 + 18, yy + 28, 'איתור מתקדם…', 12.5, C['primary'], 'start', 600))
    note(s, 1, fx0 - 16, fy + 21)
    note(s, 2, fx0 - 16, fy + 96)
    note(s, 3, fx0 - 16, fy + 250)
    note(s, 4, fx0 - 16, yy + 24)
    legend(s, [
        ('השורה בראש האוצר', ['מקלידים מראה מקום. מכל מקום', 'בתוכנה, Ctrl+O מביא לכאן.']),
        ('מקלידים ונכנסים', ['Enter פותח את התוצאה הראשונה', 'בשולחן העיון.']),
        ('סימניות ואחרונים', ['גם הם גישה ישירה למקום ידוע,', 'ולכן יושבים באותה רשימה.']),
        ('שני מעברים', ['"חפש בכל הספרים" עובר', 'לשולחן החיפוש. "איתור מתקדם"', 'פותח את החלון של היום.']),
    ])
    return s


ALL = [('00-today', m.m_today), ('01-overview', m_overview), ('02-library-home', m_library_home),
       ('03-library-panel', m_library_panel), ('04-reading-desk', m.m_reading), ('05-find-row', m_find),
       ('06-search-desk', m.m_search), ('07-settings-window', m.m_settings)]

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(('.svg', '.png')):
            os.remove(os.path.join(out, f))
    for name, fn in ALL:
        with open(os.path.join(out, name + '.svg'), 'w', encoding='utf8') as f:
            f.write(fn().render())
        print(name)
