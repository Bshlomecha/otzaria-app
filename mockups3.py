# -*- coding: utf-8 -*-
"""גרסה 3: אוצר הספרים כארונות, נתיב מלא, תצוגה מקדימה עם מחבר וציר תקופות, וחלון חיפוש מעל האוצר."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mockups as m  # noqa
import mockups2 as m2  # noqa
from kit import *  # noqa
from mockups import (W, H, WX, WY, WW, WH, RX, TOP, CX0, CX1, SW_R, frame, legend, RAIL_NEW, DESK_X0)
from mockups2 import chrome, find_field, N

SPINE_W = [7, 9, 6, 10, 8, 7, 9, 6, 8, 10, 7, 9, 6, 8]


def bookcase(s, x, y, w, h, name, sel=False, dim=False, rows=1, labels=None, sel_label=None, plaque=True, glow=False):
    """כרטיס מדף נקי, וברקעו ארון ספרים בקו דק וקלוש, כסימן מים. השם הוא העיקר."""
    op = ' opacity="0.4"' if dim else ''
    g = [f'<g{op}>']
    if glow:
        # סימן מים: שטיפה חמה וקלושה סביב המדף, כמעט לא מורגשת
        g.append(rect(x - 6, y - 6, w + 12, h + 12, C['gold'], r=12, extra='fill-opacity="0.10"'))
    g.append(rect(x, y, w, h, C['secondaryContainer'] if sel and not labels else C['card'], r=8,
                  stroke=C['primary'] if sel else C['outlineVariant'], sw=1.2 if sel else 1))
    wm = C['primary']
    inner_x0, inner_x1 = x + 14, x + w - 14
    plaque_h = 32 if plaque else 10
    row_h = (h - 24 - plaque_h) / rows
    for r_ in range(rows):
        base = y + 18 + (r_ + 1) * row_h - 4
        xx = inner_x1
        i = 0
        if labels and r_ == 0:
            # כריכות בקו דק. הנבחרת: מילוי בגוון הבחירה ושם בולט מעט. כל השאר שקט.
            sw_ = (inner_x1 - inner_x0) / len(labels)
            for lab in labels:
                hh = row_h - 10 - (i % 3) * 5
                is_sel = lab == sel_label
                g.append(f'<rect x="{xx-sw_+2}" y="{base-hh}" width="{sw_-4}" height="{hh}" rx="2" '
                         f'fill="{C["secondaryContainer"] if is_sel else "none"}" stroke="{C["primary"] if is_sel else wm}" '
                         f'stroke-opacity="{0.9 if is_sel else 0.28}" stroke-width="1"/>')
                cx_ = xx - sw_ / 2
                cy_ = base - hh / 2
                g.append(f'<text x="{cx_}" y="{cy_}" font-size="12.5" fill="{C["onSurface"] if is_sel else C["onSurfaceVariant"]}" '
                         f'text-anchor="middle" dominant-baseline="central" font-weight="{700 if is_sel else 400}" '
                         f'transform="rotate(90 {cx_} {cy_})">{escape(lab)}</text>')
                xx -= sw_
                i += 1
        else:
            # סימן מים: קווי מתאר של כריכות, בלי מילוי
            while True:
                sw_ = SPINE_W[i % len(SPINE_W)] * (w / 140)
                if xx - sw_ < inner_x0:
                    break
                hh = (row_h - 10) * (0.72 + 0.28 * ((i * 7) % 5) / 4)
                g.append(f'<rect x="{xx-sw_+1}" y="{base-hh}" width="{sw_-2}" height="{hh}" rx="1" fill="none" '
                         f'stroke="{wm}" stroke-opacity="0.2" stroke-width="0.9"/>')
                xx -= sw_
                i += 1
        g.append(f'<line x1="{x+10}" y1="{base+1}" x2="{x+w-10}" y2="{base+1}" stroke="{wm}" stroke-opacity="0.22" stroke-width="1"/>')
    if plaque:
        g.append(text(x + w / 2, y + h - 12, name, 14 if w < 200 else 16, C['onSurface'], 'middle', 700 if sel else 600))
    g.append('</g>')
    s.add(''.join(g))


def scope_search(s, x1, y, w=250, active=0, typed=None):
    s.add(rect(x1 - w, y, w, 32, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', x1 - 18, y + 16, C['onSurfaceVariant'], 0.7))
    if typed:
        s.add(text(x1 - 34, y + 21, typed, 13, C['onSurface'], 'end', 600))
    else:
        s.add(text(x1 - 34, y + 20.5, 'חיפוש מדף, חיבור או מחבר', 12.5, C['onSurfaceVariant'], 'end'))
    return segmented(s, x1 - w - 8, y + 2, ['הכול', 'מדף', 'חיבור', 'מחבר'], active, h=28, pad=9, size=11.5)


def crumbs(s, x1, y, parts):
    xx = x1
    for i, p in enumerate(parts):
        last = i == len(parts) - 1
        s.add(text(xx, y, p, 14 if last else 13, C['onSurface'] if last else C['primary'], 'end', 700 if last else 500))
        xx -= len(p) * (7.8 if last else 7.5) + 10
        if not last:
            s.add(text(xx, y, '>', 14, C['onSurfaceVariant'], 'end'))
            xx -= 16


def otzar_header(s, path, typed_find=None, search_typed=None, scope=0):
    """ראש אוצר הספרים: שורת איתור וכפתור חיפוש, ומתחתיהם הנתיב המלא וחיפוש השמות."""
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, C['panel'], r=0))
    fy = TOP + 16
    find_field(s, CX1 - 24, fy, 470, typed=typed_find, focus=bool(typed_find),
               placeholder='איתור מראה מקום: ברכות ב., שו"ע או"ח נח…')
    bx1 = CX1 - 24 - 470 - 12
    s.add(rect(bx1 - 168, fy + 4, 168, 34, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('search', bx1 - 18, fy + 21, C['primary'], 0.75))
    s.add(text(bx1 - 34, fy + 26, 'חיפוש בכל הספרים', 13, C['onSurface'], 'end', 600))
    s.add(rect(CX0 + 20, fy + 7, 150, 28, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(icon('calendar', CX0 + 156, fy + 21, C['primary'], 0.6))
    s.add(text(CX0 + 144, fy + 26, 'דף היומי · ברכות ב', 11.5, C['onSurface'], 'end', 600))
    ty = fy + 56
    s.add(line(CX0 + 16, ty - 6, CX1 - 16, ty - 6, C['outlineVariant']))
    crumbs(s, CX1 - 26, ty + 22, path)
    scope_search(s, CX0 + 24 + 250 + 200, ty + 4, 250, scope, search_typed)
    return fy, ty, ty + 50


SHELVES = ['תנ"ך', 'משנה', 'תלמוד בבלי', 'תלמוד ירושלמי', 'מדרש', 'הלכה', 'שו"ת', 'קבלה',
           'מחשבה ומוסר', 'חסידות', 'ספרות עזר', 'ספרים אישיים']


def preview_shelf(s, px0, pw, py, ph, title, desc, groups, author=None):
    s.add(rect(px0, py, pw, ph, C['card'], r=8, stroke=C['outlineVariant']))
    xr = px0 + pw - 16
    s.add(text(xr, py + 30, title, 16, C['onSurface'], 'end', 700))
    y = py + 30
    if author:
        y += 22
        s.add(text(xr, y, author, 13, C['primary'], 'end', 600, extra='text-decoration="underline"'))
    y += 24
    for l in desc:
        s.add(text(xr, y, l, 12, C['onSurfaceVariant'], 'end'))
        y += 18
    y += 6
    for head, items in groups:
        s.add(text(xr, y + 8, head, 11.5, C['primary'], 'end', 700))
        y += 16
        for ic, it in items:
            s.add(icon(ic, xr - 6, y + 9, C['onSurfaceVariant'], 0.55))
            s.add(text(xr - 20, y + 14, it, 13, C['onSurface'], 'end'))
            y += 23
        y += 6
    return y


def library_screen(s, typed=None):
    """תואם את החתימה של mockups2.library_screen, לשימוש בהדמיית האיתור."""
    fy, ty, gy = otzar_header(s, ['אוצר הספרים'], typed_find=typed)
    px0, pw = CX0 + 20, 232
    _grid(s, gy, px0 + pw + 18)
    preview_shelf(s, px0, pw, gy, 380, 'תלמוד בבלי', ['שישה סדרים, 37 מסכתות,', 'ומפרשיהם לפי הדורות.'],
                  [('מדפים', [('library', 'סדר זרעים'), ('library', 'סדר מועד'), ('library', 'סדר נשים'), ('library', 'מפרשים')])])
    return fy, ty, gy, px0, pw


def _grid(s, gy, x0, sel='תלמוד בבלי', glow=None):
    gx1 = CX1 - 20
    cols, gap = 4, 12
    tw = (gx1 - x0 - gap * (cols - 1)) / cols
    th = 122
    for i, name in enumerate(SHELVES):
        r_, c_ = divmod(i, cols)
        bookcase(s, gx1 - (c_ + 1) * tw - c_ * gap, gy + r_ * (th + gap), tw, th, name, sel=name == sel, glow=name == glow)
    return tw, th


m2.library_screen = library_screen


# ---------- 2. אוצר הספרים ----------
def m_library_home():
    s = frame('אוצר הספרים: הבית', 'כל מדף הוא ארון ספרים מרומז. בראשו האיתור והחיפוש, ומתחתיהם הנתיב המלא, תמיד')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy, px0, pw = library_screen(s)
    m.note(s, 1, CX1 - 270, ty + 16)
    m.note(s, 2, CX0 + 520, ty + 20)
    m.note(s, 3, CX1 - 40, gy + 128)
    m.note(s, 4, px0 + pw + 4, gy + 150)
    m.note(s, 5, CX1 - 515, fy + 21)
    legend(s, [
        ('הנתיב המלא, תמיד', ['בראש האוצר, בכל עומק.', 'כל חוליה בו לחיצה.']),
        ('חיפוש מדף, חיבור או מחבר', ['השדה של היום, עם בחירת', 'סוג: הכול, מדף, חיבור, מחבר.']),
        ('המדפים כארונות ספרים', ['וקטורי ומעודן: כריכות, פסי', 'זהב ושלט. לחיצה מתמקדת בו.']),
        ('תצוגה מקדימה משמאל', ['כותרת, תיאור ותוכן המדף:', 'תתי־מדפים, סדרות וספרים.']),
        ('איתור וחיפוש בראש הבית', ['האיתור במקום. החיפוש', 'נפתח בחלון מעל האוצר.']),
    ])
    return s


# ---------- 3. התמקדות במדף ----------
def m_shelf_focus():
    s = frame('התמקדות במדף: הארון בא למרכז', 'בחירת מדף מביאה אותו למרכז המסך. השכנים מתעמעמים בצדדים, והנתיב המלא נשאר בראש')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy = otzar_header(s, ['אוצר הספרים', 'משנה', 'סדר מועד'])
    px0, pw = CX0 + 20, 232
    area0, area1 = px0 + pw + 18, CX1 - 20
    mid = (area0 + area1) / 2
    bw, bh = 330, 360
    bookcase(s, area1 - 96, gy + 40, 96, 280, 'סדר זרעים', dim=True, rows=2)
    bookcase(s, area0, gy + 40, 96, 280, 'סדר נשים', dim=True, rows=2)
    bookcase(s, mid - bw / 2, gy + 6, bw, bh, 'סדר מועד', sel=True,
             labels=['שבת', 'עירובין', 'פסחים', 'שקלים', 'יומא', 'סוכה', 'ביצה', 'ראש השנה', 'תענית', 'מגילה', 'מועד קטן', 'חגיגה'],
             sel_label='שבת')
    preview_shelf(s, px0, pw, gy, 380, 'סדר מועד', ['שנים עשר מסכתות: שבת, מועדים', 'ותעניות.'],
                  [('מסכתות', [('reading', 'שבת'), ('reading', 'עירובין'), ('reading', 'פסחים'), ('more', 'ועוד 9')]),
                   ('מפרשים', [('library', 'ברטנורא'), ('library', 'תוספות יום טוב')])])
    m.note(s, 1, CX1 - 300, ty + 16)
    m.note(s, 2, mid + bw / 2 + 4, gy + 120)
    m.note(s, 3, area1 - 48, gy + 336)
    m.note(s, 4, px0 + pw + 4, gy + 110)
    legend(s, [
        ('הנתיב: משנה > סדר מועד', ['ההקשר הכללי לא אובד.', 'לחיצה על "משנה" חוזרת שלב.']),
        ('המדף שנבחר במרכז', ['הכריכות הן המסכתות.', 'לחיצה על כריכה בוחרת אותה.']),
        ('השכנים בצדדים', ['מעומעמים, כדי שיהיה ברור', 'איפה עומדים בתוך הארון.']),
        ('התצוגה המקדימה', ['כותרת, תיאור ותוכן: המסכתות', 'ומדף המפרשים של הסדר.']),
    ])
    return s


# ---------- 4. חיבור ומחבר, וציר התקופות ----------
def timeline(s, x, y0, y1):
    """ציר תקופות אנכי ועדין, לצד שמאל של התצוגה המקדימה."""
    eras = ['תנאים', 'אמוראים', 'גאונים', 'ראשונים', 'אחרונים', 'בדורנו']
    s.add('<g opacity="0.5">')  # סימן מים: הציר כמעט לא מורגש
    s.add(line(x, y0, x, y1, C['outlineVariant'], 1.2))
    step = (y1 - y0) / (len(eras) - 1)
    pos = {}
    for i, e in enumerate(eras):
        yy = y0 + i * step
        pos[e] = yy
        s.add(line(x - 4, yy, x + 4, yy, C['outlineVariant'], 1))
        s.add(text(x - 9, yy + 4, e, 10.5, C['onSurfaceVariant'], 'end'))
    # רש"י בתוך תקופת הראשונים. רבותיו ממש מעליו ותלמידיו ממש אחריו, כולם ראשונים.
    ry = pos['ראשונים'] + step * 0.5
    for k, (lab, dy) in enumerate([('ר\' יעקב בן יקר', -25), ('ר\' יצחק בן יהודה', -13)]):
        s.add(f'<circle cx="{x}" cy="{ry+dy}" r="2.4" fill="{C["onSurfaceVariant"]}" fill-opacity="0.55"/>')
        s.add(text(x + 8, ry + dy + 3.5, lab, 10, C['onSurfaceVariant'], 'start'))
    s.add(f'<circle cx="{x}" cy="{ry}" r="4.5" fill="{C["primary"]}" fill-opacity="0.8"/>')
    s.add(text(x + 9, ry + 4, 'רש"י', 11.5, C['primary'], 'start', 700))
    s.add(text(x - 9, ry + 4, 'ד\'תת–ד\'תתס"ה', 9.5, C['onSurfaceVariant'], 'end'))
    for k, (lab, dy) in enumerate([('ר\' שמחה מויטרי', 13), ('רשב"ם', 25)]):
        s.add(f'<circle cx="{x}" cy="{ry+dy}" r="2.4" fill="{C["onSurfaceVariant"]}" fill-opacity="0.55"/>')
        s.add(text(x + 8, ry + dy + 3.5, lab, 10, C['onSurfaceVariant'], 'start'))
    s.add('</g>')
    return ry


def m_work_author():
    s = frame('חיבור ומחבר: המקום ברצף המסורה', 'שם המחבר מתחת לשם החיבור, כרטיס מידע בלחיצה, וציר תקופות עדין בצד שמאל')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy = otzar_header(s, ['אוצר הספרים', 'תלמוד בבלי', 'מפרשים', 'ראשונים', 'רש"י'], scope=0)
    px0, pw = CX0 + 20, 330
    area0, area1 = px0 + pw + 18, CX1 - 20
    mid = (area0 + area1) / 2
    bookcase(s, mid - 150, gy + 6, 300, 340, 'רש"י על הש"ס', sel=True,
             labels=['ברכות', 'שבת', 'עירובין', 'פסחים', 'יומא', 'סוכה', 'ביצה', 'ר"ה', 'תענית', 'מגילה'], sel_label='ברכות')
    s.add(rect(px0, gy, pw, 380, C['card'], r=8, stroke=C['outlineVariant']))
    xr = px0 + pw - 16
    s.add(text(xr, gy + 30, 'פירוש רש"י על התלמוד', 16, C['onSurface'], 'end', 700))
    s.add(text(xr, gy + 52, 'רבי שלמה יצחקי · רש"י', 13, C['primary'], 'end', 600, extra='text-decoration="underline"'))
    for j, l in enumerate(['פירוש רציף על לשון הגמרא,', 'מלווה את הדף בכל המהדורות.']):
        s.add(text(xr, gy + 78 + j * 18, l, 12, C['onSurfaceVariant'], 'end'))
    s.add(text(xr, gy + 128, 'בספרייה', 11.5, C['primary'], 'end', 700))
    for j, it in enumerate(['על 30 מסכתות', 'בצורת הדף, לצד הגמרא']):
        s.add(icon('reading', xr - 6, gy + 145 + j * 23, C['onSurfaceVariant'], 0.55))
        s.add(text(xr - 20, gy + 150 + j * 23, it, 13, C['onSurface'], 'end'))
    timeline(s, px0 + 82, gy + 30, gy + 350)
    # כרטיס המחבר, נפתח מהשם
    cw = 300
    cx1, cy0 = xr - 110 + cw, gy + 62
    s.add(f'<g filter="url(#sh)">{rect(cx1 - cw, cy0, cw, 228, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(text(cx1 - 14, cy0 + 26, 'רבי שלמה יצחקי (רש"י)', 15, C['onSurface'], 'end', 700))
    s.add(text(cx1 - 14, cy0 + 46, 'ד\'תת–ד\'תתס"ה (1040–1105) · טרויש', 12, C['onSurfaceVariant'], 'end'))
    rows = [('תקופה', 'ראשונים'), ('רבותיו', 'ר\' יעקב בן יקר, ר\' יצחק בן יהודה'),
            ('תלמידיו', 'ר\' שמחה מויטרי, רשב"ם'), ('מחיבוריו', 'פירוש על התורה, פירוש על התלמוד')]
    for j, (k, v) in enumerate(rows):
        s.add(text(cx1 - 14, cy0 + 74 + j * 30, k, 11, C['primary'], 'end', 700))
        s.add(text(cx1 - 14, cy0 + 89 + j * 30, v, 12, C['onSurface'], 'end'))
    s.add(line(cx1 - cw + 10, cy0 + 192, cx1 - 10, cy0 + 192, C['outlineVariant']))
    s.add(text(cx1 - 14, cy0 + 214, 'כל ספרי המחבר', 12.5, C['primary'], 'end', 600))
    s.add(text(cx1 - cw + 14, cy0 + 214, 'לביוגרפיה המלאה', 12.5, C['primary'], 'start', 600))
    m.note(s, 1, xr - 170, gy + 48)
    m.note(s, 2, cx1 - cw + 4, cy0 - 4)
    m.note(s, 3, px0 + 82, gy + 372)
    m.note(s, 4, CX1 - 445, ty + 16)
    legend(s, [
        ('המחבר בשורה השנייה', ['כשהחיבור או המדף מיוחדים', 'למחבר, שמו מתחת לכותרת.']),
        ('כרטיס המחבר', ['לחיצה על השם: שנים, מקום,', 'תקופה, רבותיו ותלמידיו, וקישור', 'לכל ספריו ולביוגרפיה המלאה.']),
        ('ציר התקופות, כסימן מים', ['קו קלוש משמאל, כמעט לא', 'מורגש: היכן החיבור ברצף', 'המסורה, רבותיו ותלמידיו.']),
        ('הנתיב המלא', ['תלמוד בבלי > מפרשים >', 'ראשונים > רש"י.']),
    ])
    return s


# ---------- 6. חלון החיפוש מעל האוצר ----------
def m_search_window():
    s = frame('חיפוש: חלון ייעודי מעל הבית', 'הכפתור פותח חלון חיפוש מעל האוצר. האוצר נשאר מאחור, מובהר: לא מסיח, ולא נעלם')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    library_screen(s)
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, '#FFFFFF', r=0, extra='fill-opacity="0.62"'))
    dx0, dw, dy0, dh = CX0 + 120, 620, TOP + 50, 470
    dx1 = dx0 + dw
    s.add(f'<g filter="url(#sh)">{rect(dx0, dy0, dw, dh, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(f'<path d="M{dx0+8} {dy0} H{dx1-8} a8 8 0 0 1 8 8 V{dy0+52} H{dx0} V{dy0+8} a8 8 0 0 1 8 -8z" fill="{C["highest"]}"/>')
    s.add(rect(dx1 - 48, dy0 + 10, 32, 32, C['primaryContainer'], r=8))
    s.add(icon('search', dx1 - 32, dy0 + 26, C['primary'], 0.85))
    s.add(text(dx1 - 60, dy0 + 33, 'חיפוש בכל הספרים', 17, C['onSurface'], 'end', 700))
    s.add(icon('close', dx0 + 24, dy0 + 26, C['onSurfaceVariant'], 0.7))
    s.add(rect(dx0 + 20, dy0 + 72, dw - 40, 42, C['card'], r=8, stroke=C['primary'], sw=1.6))
    s.add(text(dx1 - 34, dy0 + 99, 'קריאת שמע', 16, C['onSurface'], 'end', 600))
    y = dy0 + 144
    for lab, opts, act in [('איפה', ['כל הספרייה', 'הספרים הפתוחים', 'מדף נבחר…'], 0),
                           ('איך', ['מדויק', 'קרוב', 'חכם'], 0),
                           ('תקופה', ['הכול', 'חז"ל', 'ראשונים', 'אחרונים'], 0)]:
        s.add(text(dx1 - 22, y + 19, lab, 13, C['onSurfaceVariant'], 'end', 700))
        segmented(s, dx1 - 90, y, opts, act, h=30, pad=11, size=12)
        y += 48
    s.add(text(dx1 - 22, y + 19, 'מרחק בין המילים', 13, C['onSurfaceVariant'], 'end', 700))
    s.add(line(dx0 + 140, y + 14, dx1 - 160, y + 14, C['outlineVariant'], 4, 'stroke-linecap="round"'))
    s.add(line(dx1 - 260, y + 14, dx1 - 160, y + 14, C['primary'], 4, 'stroke-linecap="round"'))
    s.add(f'<circle cx="{dx1-260}" cy="{y+14}" r="8" fill="{C["primary"]}"/>')
    y += 56
    s.add(text(dx1 - 22, y + 4, 'חיפושים אחרונים', 11.5, C['primary'], 'end', 700))
    for j, q in enumerate(['עמוד השחר', 'מאימתי קורין']):
        s.add(icon('history', dx1 - 30, y + 26 + j * 26, C['onSurfaceVariant'], 0.6))
        s.add(text(dx1 - 46, y + 31 + j * 26, q, 13, C['onSurface'], 'end'))
    s.add(rect(dx0 + 20, dy0 + dh - 54, 140, 36, C['primary'], r=8))
    s.add(text(dx0 + 90, dy0 + dh - 31, 'חיפוש', 14, '#FFFFFF', 'middle', 700))
    s.add(rect(dx0 + 170, dy0 + dh - 54, 110, 36, C['secondaryContainer'], r=8))
    s.add(text(dx0 + 225, dy0 + dh - 31, 'ביטול', 14, C['onSurface'], 'middle', 600))
    m.note(s, 1, dx0 - 16, dy0 + 26)
    m.note(s, 2, CX1 - 40, TOP + 300)
    m.note(s, 3, dx0 - 16, dy0 + 200)
    m.note(s, 4, dx0 + 300, dy0 + dh - 36)
    legend(s, [
        ('חלון ייעודי לחיפוש', ['נפתח מ"חיפוש בכל הספרים"', 'שבראש האוצר, או Ctrl+Shift+F.']),
        ('האוצר מאחור, מובהר', ['לא מסיח את הדעת, ולא נעלם.', 'ההקשר נשאר לנגד העיניים.']),
        ('יישוב הדעת', ['איפה, איך, תקופה ומרחק,', 'הכול במקום אחד לפני החיפוש.']),
        ('התוצאה עוברת לשולחן', ['"חיפוש" מניח את הרשימה', 'בשולחן החיפוש, ושם נשמרת.']),
    ])
    return s


def m_find3():
    s = frame('איתור: על גבי האוצר, ויודע את מקומו', 'מקלידים מראה מקום. השורה המסומנת מראה את הנתיב שלה, והמדף שלה מודגש בעדינות באוצר שמאחור')
    chrome(s, ['ברכות ב.', 'רש"י'], -1, RAIL_NEW, 'ספרייה', desk='הדף היומי', switch='')
    fy, ty, gy = otzar_header(s, ['אוצר הספרים'], typed_find='מסילת ישרים ג')
    px0, pw = CX0 + 20, 232
    _grid(s, gy, px0 + pw + 18, sel=None, glow='מחשבה ומוסר')
    preview_shelf(s, px0, pw, gy, 380, 'מחשבה ומוסר', ['ספרי אמונה, מחשבה ומוסר.'],
                  [('בתוך המדף', [('reading', 'מסילת ישרים'), ('reading', 'חובות הלבבות'), ('more', 'ועוד')])])
    fx1, fw = CX1 - 24, 470
    fx0 = fx1 - fw
    s.add(f'<g filter="url(#sh)">{rect(fx0, fy + 48, fw, 236, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    yy = fy + 66
    def head(t):
        nonlocal yy
        s.add(text(fx1 - 16, yy, t, 11.5, C['primary'], 'end', 700))
        yy += 10
    def item(t, sub, ic, sel=False):
        nonlocal yy
        if sel:
            s.add(rect(fx0 + 8, yy, fw - 16, 42, C['secondaryContainer'], r=8))
        s.add(icon(ic, fx1 - 26, yy + 21, C['primary'] if sel else C['onSurfaceVariant'], 0.75))
        s.add(text(fx1 - 46, yy + 18, t, 13.5, C['onSurface'], 'end', 700 if sel else 500))
        s.add(text(fx1 - 46, yy + 35, sub, 11, C['primary'] if sel else C['onSurfaceVariant'], 'end', 600 if sel else 400))
        yy += 46
    head('מראי מקום')
    item('מסילת ישרים, פרק ג', 'אוצר הספרים > מחשבה ומוסר > מסילת ישרים', 'reading', True)
    item('מסילת ישרים, פרק יג', 'אוצר הספרים > מחשבה ומוסר > מסילת ישרים', 'reading')
    yy += 6
    head('נפתחו לאחרונה')
    item('מסילת ישרים, פרק א', 'אתמול', 'history')
    s.add(line(fx0 + 12, yy + 2, fx1 - 12, yy + 2, C['outlineVariant']))
    s.add(text(fx1 - 18, yy + 24, 'חפש "מסילת ישרים ג" בכל הספרים', 12.5, C['primary'], 'end', 600))
    s.add(text(fx0 + 18, yy + 24, 'איתור מתקדם…', 12.5, C['primary'], 'start', 600))
    tw = (CX1 - 20 - (px0 + pw + 18) - 36) / 4
    m.note(s, 1, fx0 - 16, fy + 21)
    m.note(s, 2, fx0 - 16, fy + 100)
    m.note(s, 3, CX1 - 20 - tw - 14, gy + 2 * 134 + 30)
    m.note(s, 4, px0 + pw + 4, gy + 60)
    legend(s, [
        ('האיתור על גבי האוצר', ['השורה בראש מסך הספרייה.', 'מכל מקום Ctrl+O מביא לכאן.']),
        ('השורה יודעת את מקומה', ['מתחת לכל מראה מקום הנתיב', 'המלא שלו בספרייה.']),
        ('המדף שלה, כסימן מים', ['שטיפה חמה וקלושה סביב', 'המדף שהמקום שייך לו.', 'מורגשת באינטואיציה בלבד.']),
        ('התצוגה המקדימה עוקבת', ['מראה את המדף המסומן,', 'כדי שההקשר לא יאבד.']),
    ])
    return s


# ---------- 9. מפרשים וקישורים: המשך הכרך ----------
def m_commentary_pages():
    s = frame('מפרשים וקישורים: הספר שלם בין שתי ידיים', 'מימין הניווט, כמו הכריכה. משמאל המפרשים, כמו קצה הדפים. העיצוב רומז, ואינו מסביר')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, '', desk='הדף היומי', switch='עיון')
    PX = CX0 + 270          # גבול חלונית המפרשים (משמאל)
    NX0 = CX1 - 170         # גבול חלונית הניווט (מימין)
    m.reader_toolbar(s, PX, NX0)
    # שורת האחיזה בספר היסודי: סימון עדין
    first = TOP + 42 + 44 + 28
    hy = first
    s.add(rect(PX + 18, hy - 18, NX0 - PX - 36, 26, C['secondaryContainer'], r=6, extra='fill-opacity="0.6"'))
    book_text(s, NX0 - 25, TOP + 42 + 44, NX0 - PX - 50, lines=14, size=14, first_title='ברכות ב.')
    # קישור בתוך הטקסט
    ly = first + 26.6 * 5
    s.add(f'<line x1="{PX+90}" y1="{ly+4}" x2="{PX+180}" y2="{ly+4}" stroke="{C["primary"]}" stroke-opacity="0.6" stroke-width="1"/>')
    # חלונית הניווט מימין. בגבול הימני: רמז לכריכת הספר, כמעט בלתי נראה
    s.add(rect(NX0, TOP, CX1 - NX0, WY + WH - TOP, C['high'], r=0))
    s.add(line(NX0, TOP, NX0, WY + WH, C['outlineVariant']))
    s.add(f'<rect x="{CX1-5}" y="{TOP}" width="5" height="{WY+WH-TOP}" fill="{C["primary"]}" fill-opacity="0.05"/>')
    for i, dx in enumerate((7, 9.5)):
        s.add(f'<line x1="{CX1-dx}" y1="{TOP+4}" x2="{CX1-dx}" y2="{WY+WH-4}" stroke="{C["primary"]}" stroke-opacity="0.12" stroke-width="0.8"/>')
    toc = [(0, 'פרק א', False), (1, 'דף ב.', True), (1, 'דף ב:', False), (1, 'דף ג.', False), (1, 'דף ג:', False),
           (1, 'דף ד.', False), (0, 'פרק ב', False), (0, 'פרק ג', False), (0, 'פרק ד', False)]
    ty_ = TOP + 30
    for lvl, lab, sel in toc:
        xr_ = CX1 - 22 - lvl * 14
        if sel:
            s.add(rect(NX0 + 8, ty_ - 17, CX1 - NX0 - 22, 26, C['secondaryContainer'], r=6))
        s.add(text(xr_, ty_, lab, 13, C['onSurface'], 'end', 700 if sel or lvl == 0 else 400))
        ty_ += 30
    # חלונית המפרשים משמאל. בגבול השמאלי: קווים דקיקים ובהירים, כקצה הדפים
    s.add(rect(CX0, TOP, PX - CX0, WY + WH - TOP, C['card'], r=0))
    s.add(line(PX, TOP, PX, WY + WH, C['outlineVariant']))
    for i in range(4):
        s.add(f'<line x1="{CX0+2.5+i*2}" y1="{TOP+3+i*2}" x2="{CX0+2.5+i*2}" y2="{WY+WH-3-i*2}" '
              f'stroke="{C["onSurfaceVariant"]}" stroke-opacity="0.1" stroke-width="0.7"/>')
    xr = PX - 18
    s.add(icon('close', CX0 + 26, TOP + 26, C['onSurfaceVariant'], 0.55))
    segmented(s, xr, TOP + 12, ['רי"ף', 'רא"ש', 'מאירי', 'מהרש"א', 'עוד'], 0, h=28, pad=8, size=12)
    y = TOP + 70
    for head, lines_ in [('רי"ף, ברכות א.', ['מאימתי קורין את שמע בערבין משעה', 'שהכהנים נכנסין לאכול בתרומתן עד', 'סוף האשמורה הראשונה דברי ר"א']),
                         ('רא"ש, פרק א, סימן א', ['מאימתי קורין את שמע בערבין. ופירש', 'רש"י ואנן היכי קרינן מבעוד יום',
                                                   'ואין אנו ממתינין לצאת הכוכבים'])]:
        s.add(text(xr, y, head, 13, C['primary'], 'end', 700))
        y += 26
        for l in lines_:
            s.add(text(xr, y, l, 15, C['onSurface'], 'end', 400, RASHI))
            y += 26
        y += 18
    m.note(s, 1, NX0 - 12, hy - 5)
    m.note(s, 2, CX0 + 18, WY + WH - 40)
    m.note(s, 3, CX1 - 26, WY + WH - 40)
    m.note(s, 4, PX + 70, ly)
    legend(s, [
        ('הספר היסודי נשאר פתוח', ['במקום שבו אוחזים. השורה', 'מסומנת בעדינות, והדף לא זז.']),
        ('קצה הדפים, משמאל', ['קווים דקיקים ובהירים בגבול', 'החיצוני של חלונית המפרשים.', 'בלי כותרת שמסבירה אותם.']),
        ('הכריכה, מימין', ['רמז קלוש בגבול הימני של', 'חלונית הניווט והכותרות.']),
        ('קישורים באותו עיקרון', ['קישור נפתח באותה חלונית', 'משמאל. הספר נשאר במקומו.']),
    ])
    return s


ALL = [('00-today', m.m_today), ('01-overview', m2.m_overview), ('02-library-home', m_library_home),
       ('03-shelf-focus', m_shelf_focus), ('04-work-author', m_work_author), ('05-find-row', m_find3),
       ('06-search-window', m_search_window), ('07-library-panel', m2.m_library_panel),
       ('08-reading-desk', m.m_reading), ('09-commentary-pages', m_commentary_pages),
       ('10-search-desk', m.m_search), ('11-settings-window', m.m_settings)]

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
