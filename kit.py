# -*- coding: utf-8 -*-
"""ערכת ציור להדמיות אוצריא (SVG). ימין לשמאל, ערכת ברירת המחדל "חום זהבהב" בבהיר.
הצבעים קירוב של ערכת Material 3 שנגזרת מהזרע 0xFF2C1B02, לפי התפקידים במסמך מערכת העיצוב."""
import os
from xml.sax.saxutils import escape

# הגופנים בתיקייה fonts שליד הסקריפטים (הועתקו מתיקיית fonts במאגר אוצריא)
FONT_URL = 'file:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts').replace(os.sep, '/')

C = dict(
    # "דבש וחלב": הצעה לערכת "חום זהב" בשמנת, חול, בז' וזהב, בלי ורוד ובלי כתום.
    # בסוגריים: הערך של היום, כפי שנדגם מצילומי המסך במאגר (docs/screenshots).
    surface='#FFFBF3',          # רקע קריאה: חלב־שמנת (היום #FFF8F4, נוטה לוורוד)
    panel='#F6EFE3',            # רקע לוח: חול בהיר
    high='#F1E8D8',             # סרגל עליון, עמודת ניווט וחלונית ניווט: חול (היום #F3E6DA)
    highest='#E6DAC4',          # שדה, כותרת דיאלוג: בז' (היום #E5D5C2)
    card='#FFFBF3',             # כרטיס
    primary='#805610',          # חום זהב (כמו היום)
    onPrimary='#FFFFFF',
    primaryContainer='#EFE2C3', # שמנת־זהב (היום #FBDEBC, אפרסק)
    secondaryContainer='#EFE2C3',  # שורה נבחרת: שמנת־זהב (היום #FBDEBC)
    onSurface='#201B13',
    onSurfaceVariant='#4F4539',
    outlineVariant='#D8CCB5',   # קו: בז' (היום #D3C4B4)
    scrim='rgba(32,27,19,0.16)',
    shadow='rgba(32,27,19,0.16)',
    note='#2F5D9A',             # צבע ההערות על ההדמיה (לא חלק מהממשק)
    noteBg='#E7EEF8',
    gold='#B08A3E',
)
FONT = "'Segoe UI','Noto Sans Hebrew',Arial,sans-serif"
RASHI = "'NotoRashiHebrew','David',serif"
SERIF = "'FrankRuhlCLM','Frank Ruhl Libre','David',serif"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.parts = w, h, []
        self.title = title

    def add(self, s):
        self.parts.append(s)
        return self

    def render(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" font-family="{FONT}" direction="rtl">'
                f'<title>{escape(self.title)}</title>'
                '<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
                f'<feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="{C["shadow"]}"/></filter>'
                '<style>@font-face{font-family:FrankRuhlCLM;font-weight:400;src:url(' + FONT_URL + '/FrankRuehlCLM-Medium.ttf)}@font-face{font-family:FrankRuhlCLM;font-weight:700;src:url(' + FONT_URL + '/FrankRuehlCLM-Bold.ttf)}@font-face{font-family:NotoRashiHebrew;src:url(' + FONT_URL + '/NotoRashiHebrew-VariableFont_wght.ttf)}</style>'
                '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{C["note"]}"/></marker></defs>')
        return head + ''.join(self.parts) + '</svg>'


# ---------- יסודות ----------
def rect(x, y, w, h, fill, r=8, stroke=None, sw=1, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} {extra}/>'


def text(x, y, s, size=13, fill=None, anchor='end', weight=400, family=None, extra=''):
    fill = fill or C['onSurface']
    fam = f' font-family="{family}"' if family else ''
    # השורש ב-direction=rtl: 'start' הוא הקצה הימני. כאן 'end' פירושו "מיושר לימין ב-x".
    anchor = {'end': 'start', 'start': 'end'}.get(anchor, anchor)
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{fam} {extra}>{escape(s)}</text>')


def line(x1, y1, x2, y2, stroke, sw=1, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


# ---------- אייקונים (קווים פשוטים, 20x20, ממורכזים ב-cx,cy) ----------
def icon(name, cx, cy, color=None, s=1.0):
    c = color or C['onSurfaceVariant']
    k = f'transform="translate({cx-10*s},{cy-10*s}) scale({s})" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    p = {
        'library': '<path d="M3 3v14M7 3v14M11 4l4 13M3 17h14"/>',
        'reading': '<path d="M2 4c3-1 6-1 8 1v12c-2-2-5-2-8-1zM18 4c-3-1-6-1-8 1v12c2-2 5-2 8-1z"/>',
        'search': '<circle cx="8.5" cy="8.5" r="5.5"/><path d="M13 13l5 5"/>',
        'find': '<circle cx="10" cy="10" r="7"/><circle cx="10" cy="10" r="2.5"/><path d="M10 1v3M10 16v3M1 10h3M16 10h3"/>',
        'tools': '<rect x="3" y="3" width="5.5" height="5.5" rx="1.5"/><rect x="11.5" y="3" width="5.5" height="5.5" rx="1.5"/><rect x="3" y="11.5" width="5.5" height="5.5" rx="1.5"/><rect x="11.5" y="11.5" width="5.5" height="5.5" rx="1.5"/>',
        'bookmark': '<path d="M5 2h10v16l-5-4-5 4z"/>',
        'history': '<circle cx="10" cy="10" r="7.5"/><path d="M10 5v5l3 2"/>',
        'settings': '<circle cx="10" cy="10" r="3"/><path d="M10 1.5v3M10 15.5v3M1.5 10h3M15.5 10h3M4 4l2.1 2.1M13.9 13.9L16 16M4 16l2.1-2.1M13.9 6.1L16 4"/>',
        'calendar': '<rect x="2.5" y="4" width="15" height="13" rx="2"/><path d="M2.5 8h15M6.5 2v4M13.5 2v4"/>',
        'notes': '<path d="M4 2h9l3 3v13H4z"/><path d="M7 8h6M7 11h6M7 14h4"/>',
        'plugin': '<path d="M8 2h4v3h3v4h-2a2 2 0 0 0 0 4h2v4H5v-4h2a2 2 0 0 0 0-4H5V5h3z"/>',
        'desk': '<rect x="2" y="5" width="16" height="10" rx="2"/><path d="M2 9h16"/>',
        'chev': '<path d="M6 8l4 4 4-4"/>',
        'close': '<path d="M5 5l10 10M15 5L5 15"/>',
        'pin': '<path d="M7 2h6l-1 5 3 3H5l3-3zM10 10v8"/>',
        'list': '<path d="M3 5h14M3 10h14M3 15h14"/>',
        'info': '<circle cx="10" cy="10" r="7.5"/><path d="M10 9v5M10 6v.5"/>',
        'heart': '<path d="M10 17s-7-4.3-7-9a4 4 0 0 1 7-2.5A4 4 0 0 1 17 8c0 4.7-7 9-7 9z"/>',
        'report': '<path d="M4 18V3M4 3h11l-2 4 2 4H4"/>',
        'back': '<path d="M8 4l6 6-6 6"/>',
        'more': '<circle cx="4" cy="10" r="1"/><circle cx="10" cy="10" r="1"/><circle cx="16" cy="10" r="1"/>',
        'filter': '<path d="M3 4h14l-5.5 7v5l-3 1.5V11z"/>',
        'save': '<path d="M4 3h10l3 3v11H4z"/><path d="M7 3v5h6V3M7 17v-5h7v5"/>',
    }[name]
    return f'<g {k}>{p}</g>'


# ---------- רכיבי מעטפת ----------
def window(svg, w, h, x=0, y=0):
    svg.add(rect(x, y, w, h, C['surface'], r=10, stroke=C['outlineVariant']))


def titlebar(svg, x, y, w, tabs=None, active=0, h=40, center=None, right_label='אוצריא'):
    """שורת הכותרת: שם התוכנה בצד ימין, כרטיסיות באמצע, כפתורי חלון משמאל."""
    svg.add(f'<path d="M{x+10} {y} H{x+w-10} a10 10 0 0 1 10 10 V{y+h} H{x} V{y+10} a10 10 0 0 1 10 -10z" fill="{C["high"]}"/>')
    # כפתורי חלון בסגנון Windows, משמאל
    for i, g in enumerate(['×', '□', '—']):
        svg.add(text(x + 22 + i * 36, y + 26, g, 14, C['onSurfaceVariant'], 'middle'))
    svg.add(text(x + w - 16, y + 26, right_label, 13, C['onSurfaceVariant'], 'end', 600))
    if center:
        svg.add(center)
    xs = x + w - 96
    if tabs:
        for i, t in enumerate(tabs):
            label, kind = (t if isinstance(t, tuple) else (t, 'book'))
            tw = min(150, 30 + len(label) * 7)
            bx = xs - tw
            if i == active:
                svg.add(f'<path d="M{bx} {y+h} V{y+12} a6 6 0 0 1 6 -6 H{bx+tw-6} a6 6 0 0 1 6 6 V{y+h}z" fill="{C["surface"]}"/>')
            svg.add(icon('search' if kind == 'search' else 'reading', bx + tw - 16, y + 24,
                         C['primary'] if i == active else C['onSurfaceVariant'], 0.7))
            svg.add(text(bx + tw - 30, y + 28, label, 12, C['onSurface'], 'end', 600 if i == active else 400))
            svg.add(icon('close', bx + 12, y + 24, C['onSurfaceVariant'], 0.45))
            xs = bx - 4
    return y + h


def rail(svg, x, y, h, items, active=None, bottom=(), w=76, highlight=None):
    """עמודת הניווט בצד ימין. items: [(icon, label)]"""
    svg.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C["high"]}"/>')
    svg.add(line(x, y, x, y + h, C['outlineVariant']))
    cy = y + 18
    for ic, label in items:
        is_act = (label == active)
        if is_act:
            svg.add(rect(x + 12, cy - 4, w - 24, 34, C['secondaryContainer'], r=8))
        svg.add(icon(ic, x + w / 2, cy + 13, C['primary'] if is_act else C['onSurfaceVariant']))
        svg.add(text(x + w / 2, cy + 46, label, 11, C['onSurface'], 'middle', 600 if is_act else 400))
        if highlight and label in highlight:
            svg.add(rect(x + 5, cy - 8, w - 10, 64, 'none', r=10, stroke=C['note'], sw=2, extra='stroke-dasharray="5 4"'))
        cy += 64
    by = y + h - 64 * len(bottom) - 6
    if bottom:
        svg.add(line(x + 16, by - 6, x + w - 16, by - 6, C['outlineVariant']))
    for ic, label in bottom:
        is_act = (label == active)
        if is_act:
            svg.add(rect(x + 12, by + 10, w - 24, 34, C['secondaryContainer'], r=8))
        svg.add(icon(ic, x + w / 2, by + 27, C['primary'] if is_act else C['onSurfaceVariant']))
        svg.add(text(x + w / 2, by + 60, label, 11, C['onSurface'], 'middle', 600 if is_act else 400))
        if highlight and label in highlight:
            svg.add(rect(x + 5, by + 4, w - 10, 64, 'none', r=10, stroke=C['note'], sw=2, extra='stroke-dasharray="5 4"'))
        by += 64


def segmented(svg, x_right, y, options, active, h=30, pad=16, size=12.5):
    """בורר מקטעים, מצויר מימין לשמאל. מחזיר את הקצה השמאלי."""
    widths = [pad * 2 + len(o) * 7.2 for o in options]
    total = sum(widths)
    x0 = x_right - total
    svg.add(rect(x0, y, total, h, C['card'], r=8, stroke=C['outlineVariant']))
    xr = x_right
    for i, (o, ww) in enumerate(zip(options, widths)):
        bx = xr - ww
        if i == active:
            svg.add(rect(bx + 2, y + 2, ww - 4, h - 4, C['secondaryContainer'], r=6))
        svg.add(text(bx + ww / 2, y + h / 2 + 4.5, o, size, C['onSurface'], 'middle', 700 if i == active else 400))
        if i < len(options) - 1:
            svg.add(line(bx, y + 6, bx, y + h - 6, C['outlineVariant']))
        xr = bx
    return x0


def toggle(svg, x, y, on=True):
    svg.add(rect(x, y, 36, 20, C['primary'] if on else C['outlineVariant'], r=10))
    cx = x + 10 if on else x + 26
    svg.add(f'<circle cx="{cx}" cy="{y+10}" r="7" fill="#FFFFFF"/>')


def book_text(svg, x_right, y, width, lines=12, size=17, lh=1.9, first_title=None):
    """עמודת טקסט של ספר בגופן ספר."""
    sample = [
        'מתני׳ מאימתי קורין את שמע בערבין משעה שהכהנים',
        'נכנסים לאכול בתרומתן עד סוף האשמורה הראשונה דברי',
        'רבי אליעזר וחכמים אומרים עד חצות רבן גמליאל אומר',
        'עד שיעלה עמוד השחר. מעשה ובאו בניו מבית המשתה',
        'אמרו לו לא קרינו את שמע אמר להם אם לא עלה עמוד',
        'השחר חייבין אתם לקרות ולא זו בלבד אמרו אלא כל מה',
        'שאמרו חכמים עד חצות מצותן עד שיעלה עמוד השחר',
        'הקטר חלבים ואברים מצותן עד שיעלה עמוד השחר וכל',
        'הנאכלים ליום אחד מצותן עד שיעלה עמוד השחר אם כן',
        'למה אמרו חכמים עד חצות כדי להרחיק אדם מן העבירה:',
        'גמ׳ תנא היכא קאי דקתני מאימתי ותו מאי שנא דתני',
        'בערבין ברישא לתני דשחרין ברישא תנא אקרא קאי',
    ]
    yy = y
    if first_title:
        svg.add(text(x_right, yy, first_title, size + 3, C['onSurface'], 'end', 700, SERIF))
        yy += size * 2
    for i in range(lines):
        s = sample[i % len(sample)]
        svg.add(f'<text x="{x_right}" y="{yy}" font-size="{size}" fill="{C["onSurface"]}" text-anchor="start" '
                f'font-family="{SERIF}" textLength="{width}" lengthAdjust="spacingAndGlyphs">{escape(s)}</text>')
        yy += size * lh
    return yy


def note(svg, n, x, y, label=None, to=None, anchor='end', wrap=None):
    """הערת הדמיה ממוספרת: עיגול כחול ותווית. to=(x,y) מצייר חץ."""
    if to:
        svg.add(f'<path d="M{x} {y} L{to[0]} {to[1]}" stroke="{C["note"]}" stroke-width="1.6" fill="none" marker-end="url(#ar)"/>')
    svg.add(f'<circle cx="{x}" cy="{y}" r="12" fill="{C["note"]}"/>')
    svg.add(text(x, y + 4.5, str(n), 13, '#FFFFFF', 'middle', 700))
    if label:
        lines = label if isinstance(label, list) else [label]
        lx = x - 20 if anchor == 'end' else x + 20
        for i, l in enumerate(lines):
            svg.add(text(lx, y + 5 + i * 17, l, 13, C['note'], anchor, 700 if i == 0 else 400))


def caption_bar(svg, w, y, title, sub):
    svg.add(text(w - 24, y, title, 20, C['onSurface'], 'end', 700, SERIF))
    svg.add(text(w - 24, y + 24, sub, 13.5, C['onSurfaceVariant'], 'end'))
