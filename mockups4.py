# -*- coding: utf-8 -*-
"""גרסה 4: לפי הפוסט המעודכן. שולחנות זה מאחורי זה, וארון הכלים. מריצים: python -I mockups4.py <out_dir>"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mockups as m  # noqa
import mockups2 as m2  # noqa
import mockups3 as m3  # noqa
from kit import *  # noqa
from mockups import (W, H, WX, WY, WW, WH, RX, TOP, CX0, CX1, frame, legend, RAIL_NEW)
from mockups2 import chrome, N

m.DESK_X0 = m.DESK_X0 + 66     # רשימת השולחנות נפתחת מתחת לשם השולחן, שזז שמאלה מפני "אודות"
SEARCH_TINT = '#F5EEE1'


# ---------- 12. שני השולחנות, זה מאחורי זה ----------
def m_desks_stacked():
    s = frame('עיון וחיפוש: שני שולחנות, זה מאחורי זה', 'אפשרות לבחירה: שולחן החיפוש מונח מאחורי שולחן העיון, וקצהו מציץ. נגיעה בקצה מקדימה אותו')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, '', desk='הדף היומי', switch='עיון')
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, C['panel'], r=0))
    off = 26
    # השולחן שמאחור: חיפוש, בגוון מעט שונה. מציץ מלמעלה ומשמאל
    bx0, by0, bx1, by1 = CX0 + 10, TOP + 10, CX1 - off - 4, WY + WH - off - 6
    s.add(f'<g filter="url(#sh)">{rect(bx0, by0, bx1 - bx0, by1 - by0, SEARCH_TINT, r=8, stroke=C["outlineVariant"])}</g>')
    s.add(icon('search', bx0 + 14, by0 + 14, C['onSurfaceVariant'], 0.6))
    for j in range(5):
        s.add(f'<line x1="{bx0+8}" y1="{by0+60+j*70}" x2="{bx0+off-6}" y2="{by0+60+j*70}" stroke="{C["onSurfaceVariant"]}" stroke-opacity="0.18"/>')
    # השולחן שלפנים: עיון
    fx0, fy0, fx1, fy1 = CX0 + 10 + off, TOP + 10 + off, CX1 - 4, WY + WH - 6
    s.add(f'<g filter="url(#sh)">{rect(fx0, fy0, fx1 - fx0, fy1 - fy0, C["surface"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(rect(fx0, fy0, fx1 - fx0, 40, C['high'], r=8))
    s.add(text((fx0 + fx1) / 2, fy0 + 26, 'ברכות ב.', 14, C['onSurface'], 'middle', 600))
    book_text(s, (fx0 + fx1) / 2 + 250, fy0 + 84, 500, lines=12, size=16, first_title='ברכות ב.')
    m.note(s, 1, fx1 - 30, fy0 + 70)
    m.note(s, 2, bx0 + 13, by0 + 40)
    m.note(s, 3, (bx0 + bx1) / 2, by0 + 13)
    m.note(s, 4, m.SW_R - 60, N)
    legend(s, [
        ('שולחן העיון, לפנים', ['מלוא הדעת בלימוד. השולחן', 'נקי, בלי מה שמושך את העין.']),
        ('שולחן החיפוש, מאחור', ['קצהו מציץ, בגוון מעט שונה.', 'בלי כיתוב: הגוון והקצה', 'מספיקים כדי להרגיש אותו.']),
        ('נגיעה בקצה', ['מקדימה את שולחן החיפוש,', 'והעיון עובר מאחוריו.']),
        ('המתג נשאר בראש החלון', ['הערימה היא אפשרות לבחירה.', 'מי שמתבלבל ממנה, נשאר עם', 'המתג לבדו.']),
    ])
    return s


# ---------- 13. ארון הכלים ----------
def m_tools_cabinet():
    s = frame('כלים: ארון בעל דלתות ותאים', 'מימין הכלים המובנים. הטור השמאלי כולו לתוספים, בתאים לפי סוגיהם, כמו בחנות התוספים')
    chrome(s, ['ברכות ב.', 'רש"י'], 0, RAIL_NEW, 'כלים', desk='הדף היומי', switch='עיון')
    y = m.reader_toolbar(s, CX0, CX1)
    m.book(s, CX0, CX1, y)
    s.add(rect(CX0, TOP, CX1 - CX0, WY + WH - TOP, '#FFFFFF', r=0, extra='fill-opacity="0.62"'))
    dx0, dy0, dw, dh = CX0 + 30, TOP + 26, 840, 560
    dx1 = dx0 + dw
    s.add(f'<g filter="url(#sh)">{rect(dx0, dy0, dw, dh, C["high"], r=8, stroke=C["outlineVariant"])}</g>')
    s.add(text(dx1 - 22, dy0 + 32, 'כלים', 17, C['onSurface'], 'end', 700))
    s.add(icon('close', dx0 + 24, dy0 + 26, C['onSurfaceVariant'], 0.7))

    def cell(x, yy, cw, ch, title, items, row_h=30, size=13):
        s.add(rect(x, yy, cw, ch, C['card'], r=8, stroke=C['outlineVariant']))
        # קו הדלתות: רמז קלוש לשני כנפי הארון, כסימן מים
        s.add(f'<line x1="{x+cw/2}" y1="{yy+8}" x2="{x+cw/2}" y2="{yy+ch-8}" stroke="{C["primary"]}" stroke-opacity="0.06"/>')
        s.add(text(x + cw - 14, yy + 24, title, 12.5, C['primary'], 'end', 700))
        for j, (ic, lab) in enumerate(items):
            s.add(icon(ic, x + cw - 22, yy + 46 + j * row_h, C['onSurfaceVariant'], 0.62))
            s.add(text(x + cw - 38, yy + 51 + j * row_h, lab, size, C['onSurface'], 'end'))

    # הכלים המובנים: מימין, שני טורים
    built = [
        ('כלי עבודה', [('notes', 'הערות אישיות'), ('bookmark', 'מרקר')]),
        ('יומנים', [('calendar', 'לוח שנה'), ('history', 'שמור וזכור')]),
        ('מידות וחשבונות', [('tools', 'מדות ושיעורים'), ('tools', 'גימטריה')]),
        ('מילונים', [('library', 'מילון ארמי־עברי'), ('library', 'ראשי תיבות'), ('library', 'ביוגרפיות')]),
        ('קריאה בתורה', [('reading', 'תיקון קוראים')]),
        ('ניהול הכלים', [('pin', 'הצמדה לעמודה'), ('settings', 'הסתרת כלים')]),
    ]
    top = dy0 + 52
    bw_total = 470
    gap = 12
    cw = (bw_total - gap) / 2
    ch = (dh - 52 - 16 - 2 * gap) / 3
    for i, (t, items) in enumerate(built):
        r_, c_ = divmod(i, 2)
        cell(dx1 - 16 - (c_ + 1) * cw - c_ * gap, top + r_ * (ch + gap), cw, ch, t, items)
    # הטור השמאלי: התוספים, בתאים לפי סוגי החנות
    px0 = dx0 + 16
    pw = dx1 - 16 - bw_total - 18 - px0
    ph = dh - 52 - 16
    s.add(rect(px0, top, pw, ph, C['card'], r=8, stroke=C['outlineVariant']))
    s.add(text(px0 + pw - 14, top + 24, 'תוספים', 13.5, C['primary'], 'end', 700))
    s.add(text(px0 + 14, top + 24, 'לחנות', 12, C['primary'], 'start', 600))
    cats = [('כלי לימוד', ['על הדף', 'לשקוד', 'מקשר מקורות']),
            ('קריאה משופרת', ['שני טורים']),
            ('איורי עזר ללימוד', ['המחשות משניות']),
            ('כלי קודש', ['קידוש החודש', 'בית המקדש']),
            ('היסטוריה יהודית', ['השמועה ממקורה']),
            ('תפילה', ['סידורון']),
            ('עזרים', ['מעשר כספים'])]
    yy = top + 44
    for k, (cname, plugs) in enumerate(cats):
        if k:
            s.add(f'<line x1="{px0+12}" y1="{yy-10}" x2="{px0+pw-12}" y2="{yy-10}" stroke="{C["outlineVariant"]}" stroke-opacity="0.7"/>')
        s.add(text(px0 + pw - 14, yy + 6, cname, 11.5, C['onSurfaceVariant'], 'end', 700))
        line_txt = ' · '.join(plugs)
        s.add(icon('plugin', px0 + pw - 22, yy + 25, C['primary'], 0.55))
        s.add(text(px0 + pw - 36, yy + 30, line_txt, 12.5, C['onSurface'], 'end'))
        yy += 64
    m.note(s, 1, dx1 + 14, top + 40)
    m.note(s, 2, px0 - 14, top + 140)
    m.note(s, 3, px0 + 66, top + 20)
    m.note(s, 4, CX1 - 30, WY + WH - 40)
    legend(s, [
        ('הכלים המובנים, מימין', ['תא לכל סוג: כלי עבודה, יומנים,', 'מידות, מילונים, קריאה בתורה.']),
        ('הטור השמאלי: התוספים', ['מקום חשוב בארון. מחולק', 'לתאים לפי סוגי החנות: כלי', 'לימוד, קריאה משופרת ועוד.']),
        ('לחנות', ['מעבר לחנות התוספים, באותה', 'חלוקה בדיוק.']),
        ('מעל המקום, ומאחור מובהר', ['הארון נפתח ונסגר. השולחן', 'נשאר במקומו.']),
    ])
    return s


ALL = m3.ALL + [('12-desks-stacked', m_desks_stacked), ('13-tools-cabinet', m_tools_cabinet)]

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
