# -*- coding: utf-8 -*-
"""סדרת האייקונים של סל"ע — ספרייה · לימוד · עיון — ושלושה נלווים: שליפה, איתור, חיפוש.
קו נקי ומעודן (24x24, קו 1.5, קצוות מעוגלים), ברוח הספר הפתוח שבלוגו של אוצריא.
מילוי "var(--ibg)" — רקע מסתיר, כדי שיד או ספר יעמדו לפני מה שמאחוריהם."""

BG = 'fill="var(--ibg, #FFFDF8)"'
DIM = 'stroke-opacity=".45"'


def _open_book(x0, x1, top, bot, mid_top, mid_bot, sag=1.4):
    """ספר פתוח במבט מלפנים, כמו בלוגו: שני דפים שמתעגלים אל השדרה."""
    c = (x0 + x1) / 2
    return (f'M{c} {mid_top}C{c - 2} {mid_top - sag} {x0 + 2.6} {top - .4} {x0} {top}V{bot}'
            f'C{x0 + 2.6} {bot - .7} {c - 2} {bot - .3} {c} {mid_bot}'
            f'C{c + 2} {bot - .3} {x1 - 2.6} {bot - .7} {x1} {bot}V{top}'
            f'C{x1 - 2.6} {top - .4} {c + 2} {mid_top - sag} {c} {mid_top}Z'
            f'M{c} {mid_top}V{mid_bot}')


def _slab(cx, y, w):
    """ספר פתוח שמונח על פניו במבט מלפנים: פני הדפים, ועובי הכרך."""
    return (f'M{cx - w} {y + 1.3}Q{cx - w / 2} {y - .5} {cx} {y + .9}Q{cx + w / 2} {y - .5} {cx + w} {y + 1.3}'
            f'V{y + 2.6}Q{cx + w / 2} {y + 1.4} {cx} {y + 3}Q{cx - w / 2} {y + 1.4} {cx - w} {y + 2.6}Z'
            f'M{cx} {y + .9}V{y + 3}')


# ספרייה — מדף, ועליו ספרים עומדים ואחד נשען
LIB = ('<path d="M2.5 20.5h19"/>'
       '<rect x="3.8" y="6.6" width="3.3" height="13.9" rx=".7"/>'
       '<rect x="7.1" y="4" width="3.5" height="16.5" rx=".7"/>'
       '<path d="M11.2 20.5L14.5 6.2l3.2.8-3 13.5z"/>'
       '<rect x="17.9" y="8.8" width="3.2" height="11.7" rx=".7"/>'
       '<path d="M3.8 9.3h3.3M3.8 17.7h3.3M7.1 6.9h3.5M7.1 17.6h3.5M17.9 11.4h3.2"/>')

# לימוד — ספר פתוח על סטנדר
LIMUD = (f'<path d="{_open_book(4.3, 19.7, 5.6, 13.2, 6.9, 14.4, 1.2)}"/>'
         f'<path {DIM} d="M6.5 8.3h3.4M6.5 10.4h3.4M14.1 8.3h3.4M14.1 10.4h3.4"/>'
         '<path d="M3.2 15.7h17.6M4.8 15.7l2.2 2.9h10l2.2-2.9M12 18.6v2.6M8.4 21.2h7.2"/>')

# עיון — שלושה ספרים פתוחים זה על זה, על שולחן
IYUN = (f'<path {BG} d="{_open_book(3.4, 18.6, 13.4, 16.4, 14.3, 17.3, 1)}"/>'
        f'<path {BG} d="{_open_book(6.4, 20.8, 9.7, 12.7, 10.6, 13.6, 1)}"/>'
        f'<path {BG} d="{_open_book(4.6, 16.6, 6, 9, 6.9, 9.9, 1)}"/>'
        '<path d="M2.4 18.6h19.2M5 18.6v3M19 18.6v3"/>')

# שליפה (תיבת החיפוש שבספרייה) — ספר נשלף מבין ספרי המדף
PULL = ('<path d="M2.5 20.5h19"/>'
        '<rect x="3.8" y="7" width="3.2" height="13.5" rx=".7"/>'
        '<rect x="7" y="5" width="3.4" height="15.5" rx=".7"/>'
        '<rect x="17" y="6.5" width="3.3" height="14" rx=".7"/>'
        f'<path {DIM} stroke-dasharray="1.2 1.6" d="M10.9 20.5V8.5M16.5 20.5V8.5"/>'
        f'<rect {BG} x="11.2" y="2.3" width="3.6" height="13.4" rx=".7" transform="rotate(-13 13 9)"/>'
        '<path d="M11.6 4.9l3.4-.8M13.4 12.6l3.4-.8" />'
        '<path d="M3.8 9.6h3.2M7 7.4h3.4M17 9h3.3"/>')

# איתור — יד מצביעה על שורה בתוך ספר פתוח
_HAND = ('M15.7 21.6l-2-2.8a1 1 0 0 1 1.5-1.3l.8.8V11.2a1.05 1.05 0 0 1 2.1 0v4.3h2.3'
         'a1.4 1.4 0 0 1 1.4 1.4v1.6c0 1.8-1.3 3.1-3.1 3.1z')
FIND = (f'<path d="{_open_book(2.6, 21.4, 4.4, 15, 5.8, 16.4, 1.3)}"/>'
        f'<path {DIM} d="M5 7.6h4.4M5 9.9h4.4M5 12.2h3M14.4 7.6h4.6M14.4 12.2h1.4"/>'
        '<path stroke-width="1.9" d="M14.4 9.9h4.6"/>'
        f'<path {BG} d="{_HAND}"/>')

# חיפוש — ספר פתוח, שורות בהירות, ומילים מסומנות
SRCH = (f'<path d="{_open_book(2.6, 21.4, 4.4, 17, 5.8, 18.6, 1.3)}"/>'
        '<rect x="5.6" y="9.5" width="4.4" height="2.2" rx=".7" fill="currentColor" fill-opacity=".2" stroke="none"/>'
        '<rect x="14.2" y="12.1" width="4.4" height="2.2" rx=".7" fill="currentColor" fill-opacity=".2" stroke="none"/>'
        f'<path {DIM} d="M5 8h4.6M5 13.2h4.6M14.4 8h4.6M14.4 10.6h4.6"/>'
        '<path stroke-width="1.9" d="M6.2 10.6h3.2M14.8 13.2h3.2"/>')

SERIES = {'m_lib': LIB, 'm_limud': LIMUD, 'm_iyun': IYUN, 'pull': PULL, 'find': FIND, 'srch': SRCH}
NAMES = {'m_lib': 'ספרייה', 'm_limud': 'לימוד', 'm_iyun': 'עיון',
         'pull': 'חיפוש חיבור או מחבר', 'find': 'איתור', 'srch': 'חיפוש'}


def sheet():
    """גיליון בדיקה: כל אייקון בשלושה גדלים, בצבע הממשק ובזהב."""
    cells = ''
    for k, body in SERIES.items():
        row = ''.join(f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" style="fill:none;stroke:{c};stroke-width:1.5;'
                      f'stroke-linecap:round;stroke-linejoin:round">{body}</svg>'
                      for s, c in ((20, '#4F4539'), (32, '#4F4539'), (96, '#4F4539'), (96, '#9A7424')))
        cells += f'<div class="c"><div class="r">{row}</div><b>{NAMES[k]}</b></div>'
    return ('<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>'
            'body{margin:0;width:1440px;height:900px;background:#FFFDF8;font-family:Segoe UI;--ibg:#FFFDF8}'
            '.g{display:grid;grid-template-columns:1fr 1fr;gap:22px 40px;padding:30px 40px}'
            '.c{border:1px solid #E4D7BD;border-radius:12px;padding:16px 20px}'
            '.r{display:flex;align-items:flex-end;gap:26px}b{display:block;margin-top:8px;font-size:18px;color:#5A3D0A}'
            f'</style></head><body><div class="g">{cells}</div></body></html>')
