# -*- coding: utf-8 -*-
"""הדמיות המתווה המפושט (פוסט 50637): שלושה מצבים למסך הראשי — ספרייה · עיון · חקירה.
כותב קובצי HTML לתיקיית היעד; render.sh הופך אותם לתמונות 1440x900.

הרצה (Git Bash):  python -I v2/build.py <out>  &&  bash v2/render.sh <out>
התיקייה <out> צריכה לשבת בנתיב בלי עברית (Edge טוען את הגופנים דרך file:///).
שמות הספרים, המדפים, מניין הספרים במדפים ותוכן העניינים — מן המסד של אוצריא (seforim.db, 27.11.2026).
המספרים בחלון החקירה להמחשה בלבד."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = 'חקירה'   # השם הקצר ל"תוצאות חיפוש" — טרם הוכרע

# ---------------- אייקונים (קו דק, 24x24) ----------------
P = {
    'lib': '<path d="M4.5 4v16M8.5 4v16M12.5 5.2l4.6 14.8M3 20h18"/>',
    'read': '<path d="M3 5.6c3-1.3 6-1.2 9 .9v13c-3-2-6-2.1-9-.9zM21 5.6c-3-1.3-6-1.2-9 .9v13c3-2 6-2.1 9-.9z"/>',
    'probe': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3L20.5 20.5M7.8 9h5.4M7.8 12h3.6"/>',
    'spread': '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M9 4.5v15M15 4.5v15"/>',
    'spread2': '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M12 4.5v15"/>',
    'gear': '<circle cx="12" cy="12" r="2.8"/><path d="M12 3.2l1.4 2.2 2.5-.7.7 2.5 2.2 1.4-1 2.4 1 2.4-2.2 1.4-.7 2.5-2.5-.7L12 20.8l-1.4-2.2-2.5.7-.7-2.5-2.2-1.4 1-2.4-1-2.4 2.2-1.4.7-2.5 2.5.7z"/>',
    'info': '<circle cx="12" cy="12" r="8.8"/><path d="M12 11v5.6M12 7.6v.4"/>',
    'min': '<path d="M6.5 12h11"/>',
    'max': '<rect x="6.5" y="6.5" width="11" height="11" rx="1"/>',
    'close': '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    'x': '<path d="M8 8l8 8M16 8l-8 8"/>',
    'back': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'fwd': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'up': '<path d="M12 19V5.5M6.5 11L12 5.5 17.5 11"/>',
    'home': '<path d="M4 11.2L12 4.5l8 6.7V20H4z"/><path d="M10 20v-5.5h4V20"/>',
    'grid': '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    'list': '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="5" cy="6" r=".8"/><circle cx="5" cy="12" r=".8"/><circle cx="5" cy="18" r=".8"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3L20.5 20.5"/>',
    'target': '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.4"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3"/>',
    'navp': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M15 4v16M17 8h2M17 11h2"/>',
    'commp': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M5 8h2M5 11h2M5 14h2"/>',
    'c2r': '<path d="M5.5 6.5l5.5 5.5-5.5 5.5M12 6.5l5.5 5.5-5.5 5.5"/>',
    'c1r': '<path d="M9 6.5l5.5 5.5L9 17.5"/>',
    'c1l': '<path d="M15 6.5L9.5 12l5.5 5.5"/>',
    'c2l': '<path d="M18.5 6.5L13 12l5.5 5.5M12 6.5L6.5 12l5.5 5.5"/>',
    'cdown': '<path d="M7 10l5 5 5-5"/>',
    'justify': '<path d="M4.5 6.5h15M4.5 10.5h15M4.5 14.5h15M4.5 18.5h15"/>',
    'zin': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3L20.5 20.5M8 10.5h5M10.5 8v5"/>',
    'zout': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3L20.5 20.5M8 10.5h5"/>',
    'bookmark': '<path d="M7 3.8h10v16.4l-5-3.8-5 3.8z"/>',
    'note': '<path d="M5 3.8h9.5l4.5 4.5V20.2H5z"/><path d="M14.5 3.8v4.5H19M8 12h8M8 15.5h6"/>',
    'print': '<path d="M7 9V4h10v5"/><rect x="3.8" y="9" width="16.4" height="7.2" rx="1.6"/><path d="M7 13.5h10V20H7z"/>',
    'more': '<circle cx="6" cy="12" r="1.1" fill="currentColor"/><circle cx="12" cy="12" r="1.1" fill="currentColor"/><circle cx="18" cy="12" r="1.1" fill="currentColor"/>',
    'versions': '<path d="M12 3.5l8.5 4.6L12 12.7 3.5 8.1z"/><path d="M3.5 12.2l8.5 4.6 8.5-4.6M3.5 16.2l8.5 4.6 8.5-4.6"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3A4 4 0 0 0 13 5.3l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    'cal': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 13.5h2M14 13.5h2M8 16.5h2"/>',
    'check': '<circle cx="12" cy="12" r="8.6"/><path d="M8 12.4l2.7 2.7L16 9.8"/>',
    'scroll': '<path d="M6.5 4v16M17.5 4v16"/><path d="M6.5 6h11M6.5 18h11"/><path d="M9.5 9.5h5M9.5 12h5M9.5 14.5h3"/>',
    'plus': '<path d="M12 5.5v13M5.5 12h13"/>',
    'filter': '<path d="M4 5.5h16l-6 7.2v5.3l-4 2v-7.3z"/>',
    'sort': '<path d="M7.5 4.5v15M4.5 16.5l3 3 3-3M13.5 6.5h7M13.5 11h5M13.5 15.5h3"/>',
    'book': '<path d="M6.5 3.8h11.7v16.4H6.5a2 2 0 0 1-2-2V5.8a2 2 0 0 1 2-2z"/><path d="M4.5 17.6a2 2 0 0 1 2-1.8h11.7"/>',
    'folder': '<path d="M3.5 7.2a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8.6a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>',
    'person': '<circle cx="12" cy="8" r="3.8"/><path d="M4.8 20c1.3-3.7 4.3-5.3 7.2-5.3s5.9 1.6 7.2 5.3"/>',
    'desk': '<rect x="3" y="5.5" width="18" height="11" rx="1.8"/><path d="M7 20h10M12 16.5V20"/>',
    'open': '<path d="M14 4h6v6M20 4l-8.5 8.5"/><path d="M18 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6H10"/>',
    'enter': '<path d="M19 6v5.5a2 2 0 0 1-2 2H6"/><path d="M10 9.5l-4 4 4 4"/>',
    'source': '<path d="M5 4h9l5 5v11H5z"/><path d="M14 4v5h5"/><path d="M8.5 14.5l2 2 4-4.5"/>',
    'pin': '<path d="M9 4h6l-1 5.5 3.5 3.5h-11L10 9.5z"/><path d="M12 13v7"/>',
    'history': '<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M4.5 4.5v3.7h3.7M12 8v4.3l3 1.7"/>',
}


def ic(name, cls=''):
    return f'<svg class="i {cls}" viewBox="0 0 24 24">{P[name]}</svg>'


def ib(name, on=False, dim=False, cls='', title=''):
    c = 'ib' + (' on' if on else '') + (' dim' if dim else '') + (' ' + cls if cls else '')
    return f'<span class="{c}" title="{title}">{ic(name)}</span>'


# ---------------- רצועת הכותרת הקבועה ----------------
def strip(mode):
    def seg(key, label, icon):
        return f'<b class="{key}{" on" if mode == key else ""}">{ic(icon)}{label}</b>'
    spread_on = ' on' if mode == 'spread' else ''
    return f'''<header class="strip">
  <div class="brand"><img src="logo.png" alt=""><span>אוצריא</span></div>
  <div class="switch">
    <div class="seg">{seg("lib", "ספרייה", "lib")}{seg("read", "עיון", "read")}{seg("probe", PROBE, "probe")}</div>
    <span class="spread{spread_on}" title="פרישה: כולם במקביל">{ic("spread")}</span>
  </div>
  <div class="strip-end">
    <span class="sbtn" title="הגדרות">{ic("gear")}</span>
    <span class="sbtn" title="אודות">{ic("info")}</span>
    <div class="winctl"><span>{ic("min", "s")}</span><span>{ic("max", "s")}</span><span>{ic("close", "s")}</span></div>
  </div>
</header>'''


def page(mode, body, title, extra=''):
    m = {'lib': 'm-lib', 'read': 'm-read', 'probe': 'm-probe', 'spread': 'm-spread'}[mode]
    return f'''<!doctype html>
<html dir="rtl" lang="he"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="style.css"></head>
<body><div class="app {m}">{strip(mode)}<main class="stage">{body}</main>{extra}</div></body></html>'''


# ---------------- נתונים מן המסד ----------------
SHELVES = [  # (שם, מספר ספרים, מדפי משנה) — seforim.db, 27.11.2026
    ('תנ״ך', 737, 'תורה · נביאים · כתובים · תרגומים · ראשונים · אחרונים'),
    ('תלמוד בבלי', 1890, 'סדר זרעים · סדר מועד · סדר נשים · סדר נזיקין · ראשונים · אחרונים'),
    ('משנה', 930, 'ששת הסדרים · ראשונים · אחרונים · מפרשים'),
    ('תלמוד ירושלמי', 535, 'סדר זרעים · סדר מועד · סדר נשים · סדר נזיקין · מפרשים'),
    ('מדרש', 273, 'אגדה · הלכה'),
    ('הלכה', 2605, 'משנה תורה · טור · שולחן ערוך · ספרי מצוות · ראשונים · אחרונים'),
    ('קבלה', 203, 'זהר · כתבי האר״י · רמ״ק · רמח״ל · ספר יצירה'),
    ('סדר התפילה', 75, 'סידור · ימים נוראים · הגדה · פיוטים · מפרשים'),
    ('מחשבת ישראל', 78, 'מורה נבוכים · ראשונים · אחרונים'),
    ('תוספתא', 94, 'דפוס וילנא · מהדורת ליברמן'),
    ('חסידות', 130, 'ספרי ראשית · חב״ד · ברסלב · איזביצה · ר׳ צדוק הכהן'),
    ('ספרי מוסר', 77, 'ראשונים · אחרונים · מחברי זמננו'),
    ('שו״ת', 524, 'גאונים · ראשונים · אחרונים · מחברי זמננו'),
    ('בית שני', 13, 'ספרים חיצונים · יוסף בן מתתיהו'),
    ('ספרות עזר', 101, 'דקדוק · מילונים · אנציקלופדיות · תולדות עם ישראל'),
    ('לימוד יומי', 5, 'חק לישראל'),
]


def fmt(n):
    return f'{n:,}'


# ---------------- ספרייה ----------------
def lib_row(crumbs, query='', who='חיבור', locator=''):
    cr = ''.join((f'<span class="gt">&gt;</span>' if i else '') + (f'<b>{c}</b>' if i == len(crumbs) - 1 else f'<span>{c}</span>')
                 for i, c in enumerate(crumbs))
    q = f'<span class="val">{query}</span>' if query else '<span class="ph">חיפוש חיבור או מחבר</span>'
    chips = ''.join(f'<i class="{"on" if who == w else ""}">{w}</i>' for w in ('חיבור', 'מחבר'))
    loc = f'<span class="val">{locator}</span>' if locator else '<span class="ph">איתור לפי מראה מקום — ברכות ב. · או״ח רלה א</span>'
    return f'''<div class="row">
  {ib("back", title="אחורה")}{ib("fwd", dim=True, title="קדימה")}{ib("up", title="מדף מעל")}{ib("home", title="אוצר הספרים")}
  <div class="crumbs" style="margin-inline-start:6px">{cr}</div>
  <div class="grow"></div>
  <div class="field{" focus" if query else ""}" style="width:300px">{ic("search", "s")}{q}<span class="grow"></span><div class="chipset">{chips}</div></div>
  <div class="field" style="width:330px">{ic("target", "s")}{loc}</div>
  <div class="sep"></div>
  {ib("grid", on=True, title="משבצות")}{ib("list", title="רשימה")}
</div>'''


def tiles(active):
    out = []
    for name, n, sub in SHELVES:
        out.append(f'<div class="tile{" on" if name == active else ""}"><span class="wm">{ic("lib")}</span>'
                   f'<h3>{name}</h3><div class="n">{fmt(n)} ספרים</div><div class="sub">' + ' '.join(f'<span class="it">{x}</span>' for x in sub.split(' · ')) + '</div></div>')
    return '<div class="shelves">' + ''.join(out) + '</div>'


def screen_library_shelf():
    prev = '''<aside class="preview">
  <div class="kicker">מדף</div>
  <h2>ספרי מוסר</h2>
  <div class="by">77 ספרים · שלושה מדפים</div>
  <p>ספרי תיקון המידות ועבודת ה׳: מ«שערי תשובה» לרבנו יונה ו«אורחות צדיקים», דרך «מסילת ישרים» ו«שני לוחות הברית», ועד ספרי תנועת המוסר.</p>
  <h4>במדף</h4>
  <ul class="toc">
    <li>ראשונים <span>23 ספרים</span></li>
    <li>אחרונים <span>46 ספרים</span></li>
    <li>מחברי זמננו <span>8 ספרים</span></li>
  </ul>
  <h4>נפתחו לאחרונה מן המדף</h4>
  <ul class="toc">
    <li>מסילת ישרים <span>פרק ו</span></li>
    <li>שערי תשובה <span>שער א</span></li>
    <li>אורחות צדיקים <span>שער הגאוה</span></li>
  </ul>
  <div class="actions"><span class="btn pri">''' + ic('folder', 's') + '''פתח את המדף</span><span class="btn ghost">''' + ic('pin', 's') + '''הצמד</span></div>
</aside>'''
    body = lib_row(['אוצר הספרים']) + f'<div class="lib-body">{tiles("ספרי מוסר")}{prev}</div>'
    return page('lib', body, 'ספרייה — מדף נבחר')


MUSAR_ACH = ['מסילת ישרים', 'אורחות צדיקים', 'שערי תשובה', 'חובות הלבבות', 'מנורת המאור', 'תומר דבורה',
             'ספר הישר', 'יסוד התשובה', 'אגרת הרמב״ן', 'כד הקמח', 'מבחר הפנינים', 'ספר היראה']


def screen_library_book():
    # ספרי מוסר > אחרונים, כסדרם במסד (seforim.db)
    books = [('מסילת ישרים', 'רבי משה חיים לוצאטו — הרמח״ל'), ('אגרת הגר״א', 'רבנו אליהו מווילנה — הגר״א'),
             ('אהבת דוד', 'רבי חיים יוסף דוד אזולאי — החיד״א'), ('אהבת ישראל', 'רבי ישראל מאיר הכהן מראדין'),
             ('אור הצפון', 'רבי נתן צבי פינקל'), ('אור ישראל', 'רבי ישראל מסלנט'),
             ('אלפא ביתא', 'רבי צבי הירש מנדבורנא'), ('אמרות טהורות', 'רבי אברהם חיון'),
             ('בית הלוי על מצות הביטחון', 'רבי יוסף דוב הלוי סולובייצ׳יק'), ('ברית אברהם', 'רבי אברהם הלוי הורוויץ'),
             ('דבר בעתו', 'רבי ישראל מאיר הכהן מראדין'), ('חוסן יהושע', 'רבי יהושע העליר'),
             ('יסוד ושורש העבודה', 'רבי אלכסנדר זיסקינד מהוראדנא'), ('מאמר מזכה הרבים', 'רבי יוסף יוזל הורוביץ'),
             ('מאמר תורה אור', 'רבי ישראל מאיר הכהן מראדין'), ('מעלות התורה', 'רבי אברהם אחי הגר״א'),
             ('מרבה תבונה', 'רבי יהושע איזיק שפירא'), ('משלי יעקב', 'רבי יעקב קראנץ'),
             ('ספר החיים', 'רבי חיים ב״ר בצלאל'), ('פלא יועץ', 'רבי אליעזר פאפו'),
             ('קב הישר', 'רבי צבי הירש קאיידנובר'), ('קונטרס שפת תמים', 'רבי ישראל מאיר הכהן מראדין'),
             ('ראשית חכמה', ''), ('שבט מוסר', 'רבי אליהו הכהן האיתמרי'),
             ('שמירת הלשון', 'רבי ישראל מאיר הכהן מראדין'), ('שני לוחות הברית', 'רבי ישעיהו הלוי הורוויץ — השל״ה'),
             ('ראה מעשה', 'רבי רפאל אוחנא'), ('ראש הגבעה', 'רבי פנחס ב״ר יהודה')]
    books = [b for b in books if b[1]]  # רק מה שנמצא במסד
    bl = ''.join(f'<div class="bk{" on" if i == 0 else ""}"><span class="sp"></span><div><b>{t}</b><em>{a}</em></div></div>'
                 for i, (t, a) in enumerate(books))
    main = f'''<div class="booklist"><h5>אחרונים · 46 ספרים</h5><div class="books" style="grid-template-columns:repeat(3,1fr)">{bl}</div></div>'''
    prev = '''<aside class="preview">
  <div class="kicker">ספרי מוסר &gt; אחרונים</div>
  <h2>מסילת ישרים</h2>
  <div class="by">מאת <b>רבי משה חיים לוצאטו</b> — הרמח״ל</div>
  <p class="short">ספר יסוד בדרכי עבודת ה׳ ותיקון המידות, ערוך על סדר המדרגות שבברייתא דרבי פנחס בן יאיר.</p>
  <p>מן הזהירות והזריזות, דרך הנקיות, הפרישות והטהרה, אל החסידות, הענווה ויראת החטא, ועד הקדושה. נדפס לראשונה באמשטרדם, ה׳ת״ק.</p>
  <h4>תוכן הספר</h4>
  <ul class="toc">
    <li>הקדמה <span></span></li>
    <li>פרק א — כלל חובת האדם בעולמו <span></span></li>
    <li>פרקים ב–ה — הזהירות <span></span></li>
    <li>פרקים ו–ט — הזריזות <span></span></li>
    <li>פרקים י–יב — הנקיות <span>ועוד 17 פרקים</span></li>
  </ul>
  <div class="actions"><span class="btn pri">''' + ic('read', 's') + '''פתח לעיון</span><span class="btn sec">''' + ic('person', 's') + '''על המחבר</span><span class="btn ghost">''' + ic('source', 's') + '''מקור</span></div>
</aside>'''
    body = lib_row(['אוצר הספרים', 'ספרי מוסר', 'אחרונים']) + f'<div class="lib-body">{main}{prev}</div>'
    return page('lib', body, 'ספרייה — ספר נבחר')


def screen_library_author():
    groups = [('קבלה &gt; רמח״ל', 31, ['קל״ח פתחי חכמה', 'אדיר במרום', 'דעת תבונות', 'כללי פתחי חכמה ודעת', 'ספר קנאת ה׳ צבאות', 'עשרה אורות']),
              ('מחשבת ישראל &gt; אחרונים &gt; רמחל', 7, ['דרך ה׳', 'מאמר העיקרים', 'ספר ההגיון', 'ספר המליצה', 'לישרים תהילה', 'מגדל־עז']),
              ('ספרי מוסר &gt; אחרונים', 1, ['מסילת ישרים']),
              ('תלמוד בבלי &gt; כללי הש״ס', 1, ['ספר דרך תבונות'])]
    gl = ''
    for path, n, bs in groups:
        items = ''.join(f'<div class="bk{" on" if b == "מסילת ישרים" else ""}"><span class="sp"></span><div><b>{b}</b><em>{path.split(" &gt; ")[0]}</em></div></div>' for b in bs)
        gl += f'<h5>{path} <span style="font-family:var(--ui);font-size:12px;color:var(--muted)">· {n}</span></h5><div class="books" style="margin-bottom:8px">{items}</div>'
    main = f'<div class="booklist">{gl}</div>'
    axis = '''<div class="axis"><div class="ln"></div>
    <div class="er" style="top:2%">תנאים</div><div class="er" style="top:17%">אמוראים</div>
    <div class="er" style="top:31%">גאונים</div><div class="er" style="top:47%">ראשונים</div>
    <div class="er" style="top:66%">אחרונים</div>
    <div class="me" style="top:74%"></div><div class="me-l" style="top:calc(74% - 4px)">הרמח״ל</div>
    <div class="er" style="top:93%">מחברי זמננו</div></div>'''
    prev = f'''<aside class="preview with-axis">
  {axis}
  <div class="kicker">מחבר · 40 חיבורים באוצריא</div>
  <h2>הרמח״ל</h2>
  <div class="by"><b>רבי משה חיים לוצאטו</b></div>
  <dl class="facts"><dt>שנותיו</dt><dd>ה׳תס״ז – ה׳תק״ו</dd><dt>מקומו</dt><dd>פדובה · אמשטרדם · עכו</dd><dt>תקופתו</dt><dd>אחרונים</dd></dl>
  <p>מגדולי המקובלים ומעמודי תורת המוסר. נולד בפדובה שבאיטליה, ישב באמשטרדם, עלה לארץ ישראל ונפטר בעכו.</p>
  <p>חיבוריו בדרכי עבודת ה׳ — «מסילת ישרים», «דרך ה׳», «דעת תבונות» — נעשו מספרי היסוד של בית המדרש.</p>
  <div class="actions"><span class="btn pri">{ic("lib", "s")}כל חיבוריו</span><span class="btn ghost">{ic("source", "s")}מקור</span></div>
</aside>'''
    body = lib_row(['אוצר הספרים', 'חיפוש: רמח״ל'], query='רמח״ל', who='מחבר') + f'<div class="lib-body">{main}{prev}</div>'
    return page('lib', body, 'ספרייה — חיפוש מחבר')


# ---------------- עיון ----------------
MISHNA = ('מאימתי קורין את שמע בערבין. משעה שהכהנים נכנסים לאכול בתרומתן עד סוף האשמורה הראשונה דברי ר׳ אליעזר. '
          'וחכמים אומרים עד חצות. רבן גמליאל אומר עד שיעלה עמוד השחר. מעשה ובאו בניו מבית המשתה אמרו לו לא קרינו את שמע '
          'אמר להם אם לא עלה עמוד השחר חייבין אתם לקרות ולא זו בלבד אמרו אלא כל מה שאמרו חכמים עד חצות מצותן עד שיעלה עמוד השחר '
          'הקטר חלבים ואברים מצותן עד שיעלה עמוד השחר וכל הנאכלים ליום אחד מצותן עד שיעלה עמוד השחר א״כ למה אמרו חכמים עד חצות '
          'כדי להרחיק אדם מן העבירה:')
GEMARA = ('תנא היכא קאי דקתני מאימתי ותו מאי שנא דתני בערבית ברישא לתני דשחרית ברישא תנא אקרא קאי דכתיב '
          '<span class="ref">(דברים ו, ז)</span> בשכבך ובקומך והכי קתני זמן קריאת שמע דשכיבה אימת משעה שהכהנים נכנסין לאכול בתרומתן '
          'ואי בעית אימא יליף מברייתו של עולם דכתיב <span class="ref">(בראשית א, ה)</span> ויהי ערב ויהי בקר יום אחד אי הכי סיפא דקתני '
          'בשחר מברך שתים לפניה ואחת לאחריה ובערב מברך שתים לפניה ושתים לאחריה לתני דערבית ברישא.')
RASHI = ('<b>משעה שהכהנים נכנסים לאכול בתרומתן.</b> כהנים שנטמאו וטבלו והעריב שמשן והגיע עתם לאכול בתרומה:')
TRYH = ('<b>רבן גמליאל אומר עד שיעלה עמוד השחר.</b> בגמרא (ח׳:) אמר רב יהודה אמר שמואל הלכה כר׳ גמליאל, אע״ג דרבנן פליגי עליה '
        'ומצריכי עד חצות לק״ש לחומרא מ״מ הלכה כר״ג ואין צריך להחמיר ולהרחיק מחצות לגבי ק״ש כמו לגבי שאר דברים. '
        'מ״מ צריך למהר לכתחלה מתחלת הלילה, כדאמרינן בריש פרקין שלא יאמר אדם אוכל קמוכו׳:')


def read_tabs(active='ברכות'):
    tabs = [('ברכות, דף ב.', 'ברכות'), ('מסילת ישרים, פרק ו', 'מסילת'), ('משנה ברורה, סימן רלה', 'משנ״ב')]
    t = ''.join(f'<span class="tab{" on" if k == active else ""}">{ic("read", "s")}{lab}<span class="x">{ic("x", "s")}</span></span>'
                for lab, k in tabs)
    return f'''<div class="tabs">{t}<span class="tab add">{ic("plus", "s")}</span><span class="grow"></span>
  <span class="tab" style="height:32px;margin-bottom:4px;border-radius:8px;background:#E9DEC8">{ic("desk", "s")}שולחן: סוגיית קריאת שמע{ic("cdown", "s")}</span></div>'''


def read_bar():
    left_plugins = (f'<span class="ib plug" title="שמור וזכור">{ic("check")}</span>'
                    f'<span class="ib plug" title="לוח השנה">{ic("cal")}</span>'
                    f'<span class="ib plug" title="המקרא כמסורה">{ic("scroll")}</span>')
    return f'''<div class="bar">
  {ib("navp", on=True, title="חלונית ניווט")}
  <div class="sep"></div>
  {ib("c2r", title="הדף הקודם")}{ib("c1r", title="הקטע הקודם")}{ib("justify", title="שורות או רציף")}{ib("c1l", title="הקטע הבא")}{ib("c2l", title="הדף הבא")}
  <div class="sep"></div>
  {ib("zin", title="הגדל")}{ib("zout", title="הקטן")}
  <span class="ib" title="ניקוד וטעמים" style="font-family:var(--book);font-size:19px;font-weight:700">אָ</span>
  {ib("search", title="חיפוש בספר")}{ib("target", title="איתור")}
  <div class="sep"></div>
  {ib("bookmark", title="סימנייה")}{ib("note", title="הערות אישיות")}{ib("versions", title="נוסחאות")}
  <span class="grow"></span>
  <span class="ttl">ברכות · פרק ראשון · דף ב.</span>
  <span class="grow"></span>
  {left_plugins}
  <div class="sep"></div>
  {ib("link", title="קישור ישיר")}{ib("print", title="הדפסה")}{ib("more", title="עוד")}
  <div class="sep"></div>
  {ib("commp", on=True, title="חלונית מפרשים")}
</div>'''


def nav_panel():
    return f'''<aside class="nav">
  <div class="tt"><span class="chipset" style="width:100%"><i class="on" style="flex:1;text-align:center">כותרות</i><i style="flex:1;text-align:center">חיפוש בספר</i></span></div>
  <ul class="tree">
    <li>{ic("cdown", "s")}ברכות</li>
    <li class="l2">{ic("cdown", "s")}פרק ראשון — מאימתי</li>
    <li class="l3 on">דף ב.</li><li class="l3">דף ב:</li><li class="l3">דף ג.</li><li class="l3">דף ג:</li>
    <li class="l3">דף ד.</li><li class="l3">דף ד:</li><li class="l3">דף ה.</li><li class="l3">דף ה:</li>
    <li class="l3">דף ו.</li><li class="l3">דף ו:</li>
    <li class="l2">{ic("c1l", "s")}פרק שני — היה קורא</li>
    <li class="l2">{ic("c1l", "s")}פרק שלישי — מי שמתו</li>
    <li class="l2">{ic("c1l", "s")}פרק רביעי — תפלת השחר</li>
    <li class="l2">{ic("c1l", "s")}פרק חמישי — אין עומדין</li>
  </ul>
</aside>'''


def comm_panel():
    return f'''<aside class="comm">
  <div class="ctabs"><i class="on">על הקטע</i><i>מפרשים</i><i>קישורים</i><i>הערות</i></div>
  <div class="cbody">
    <div class="src">רש״י</div><p class="cb">{RASHI}</p>
    <div class="src">תוספות רבינו יהודה החסיד</div><p class="cb">{TRYH}</p>
  </div>
</aside>'''


def read_text(sel=True):
    return f'''<article class="text">
  <h1>ברכות</h1><h2>פרק ראשון · מאימתי · דף ב.</h2>
  <h3>מתני׳</h3><p class="{"sel" if sel else ""}">{MISHNA}</p>
  <h3>גמ׳</h3><p>{GEMARA}</p>
</article>'''


def screen_reading():
    body = read_tabs() + read_bar() + f'<div class="read-body">{nav_panel()}{read_text()}{comm_panel()}</div>'
    return page('read', body, 'עיון')


# ---------------- חלונות הביצוע ----------------
def screen_find():
    rows = [('ברכות', 'דף ב.', 'תלמוד בבלי &gt; סדר זרעים', 'ספר ומקום', True),
            ('משנה ברכות', 'פרק ב', 'משנה &gt; סדר זרעים', 'ספר ומקום', False),
            ('רש״י על ברכות', 'דף ב.', 'תלמוד בבלי &gt; ראשונים &gt; רש״י', 'מפרש', False),
            ('תוספתא ברכות', 'פרק ב', 'תוספתא &gt; דפוס וילנא', 'ספר ומקום', False),
            ('רי״ף ברכות', 'דף ב.', 'תלמוד בבלי &gt; ראשונים &gt; רי״ף', 'מפרש', False),
            ('מאירי על ברכות', '', 'תלמוד בבלי &gt; ראשונים &gt; מאירי', 'ספר', False)]
    lis = ''.join(f'<li class="{"on" if on else ""}">{ic("book", "s")}<div><b>{t}</b>{(" · <span style=&quot;font-family:var(--book);font-size:16px&quot;>" + w + "</span>") if w else ""}'
                  f'<div class="path">{p}</div></div><span class="tag">{tag}</span></li>' for t, w, p, tag, on in rows)
    lis = lis.replace('&quot;', '"')
    float_ = f'''<div class="scrim"></div>
<div class="float" style="top:118px;left:390px;width:660px">
  <div class="fh">{ic("target", "l")}<h3>איתור</h3><span class="grow"></span>{ib("x")}</div>
  <div class="fb">
    <div class="field focus" style="height:44px;font-size:16px">{ic("target", "s")}<span class="val" style="font-family:var(--book);font-size:19px">ברכות ב</span><span class="grow"></span><span class="pill">ספר + מקום</span></div>
    <ul class="res">{lis}</ul>
  </div>
  <div class="foot">{ic("enter", "s")}פתיחה בעיון<span style="margin-inline-start:14px">↑↓ מעבר בין התוצאות</span><span class="grow"></span>המדף של התוצאה מודגש בספרייה שמאחור</div>
</div>'''
    prev = '''<aside class="preview">
  <div class="kicker">מדף</div>
  <h2>תלמוד בבלי</h2>
  <div class="by">1,890 ספרים · ארבעה עשר מדפים</div>
  <p>התלמוד הבבלי לסדריו, ועמו ספרי הראשונים והאחרונים על הש״ס, כללי הש״ס ומראי המקומות.</p>
  <h4>במדף</h4>
  <ul class="toc">
    <li>סדר זרעים <span>1</span></li><li>סדר מועד <span>11</span></li><li>סדר נשים <span>7</span></li>
    <li>סדר נזיקין <span>8</span></li><li>ראשונים <span>657</span></li><li>אחרונים <span>990</span></li>
  </ul>
</aside>'''
    body = lib_row(['אוצר הספרים']) + f'<div class="lib-body">{tiles("תלמוד בבלי")}{prev}</div>'
    return page('lib', body, 'חלון האיתור', extra=float_)


def screen_search():
    float_ = f'''<div class="scrim"></div>
<div class="float" style="top:108px;left:370px;width:700px">
  <div class="fh">{ic("search", "l")}<h3>חיפוש בספרייה</h3><span class="grow"></span>{ib("x")}</div>
  <div class="fb">
    <div class="field focus" style="height:46px">{ic("search", "s")}<span class="val" style="font-family:var(--book);font-size:20px">עמוד השחר</span><span class="grow"></span></div>
    <div style="display:flex;gap:26px;margin:16px 4px 6px">
      <div style="display:flex;flex-direction:column;gap:9px">
        <div style="font-size:12px;color:var(--muted);font-weight:600">אופן החיפוש</div>
        <span class="opt"><span class="radio on"></span>צירוף מדויק</span>
        <span class="opt"><span class="radio"></span>כל המילים, בקרבה של עד 5 מילים</span>
        <span class="opt"><span class="radio"></span>אחת המילים לפחות</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:9px">
        <div style="font-size:12px;color:var(--muted);font-weight:600">דיוק</div>
        <span class="opt"><span class="chk on"><svg viewBox="0 0 24 24" style="width:12px;height:12px;fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>גם בכתיב מלא וחסר</span>
        <span class="opt"><span class="chk"></span>גם עם אותיות השימוש (ו״ה״ש״ב)</span>
        <span class="opt"><span class="chk on"><svg viewBox="0 0 24 24" style="width:12px;height:12px;fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>גם בראשי תיבות</span>
      </div>
    </div>
    <div style="font-size:12px;color:var(--muted);font-weight:600;margin:14px 4px 8px">היכן</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <span class="pill">{ic("lib", "s")}כל הספרייה</span>
      <span class="pill" style="background:#FFFCF6;border:1px dashed var(--gold)">{ic("plus", "s")}הגבל למדפים</span>
      <span class="pill" style="background:#FFFCF6;border:1px dashed var(--gold)">{ic("plus", "s")}הגבל לספרים</span>
    </div>
  </div>
  <div class="foot"><span>התוצאות ייפתחו בלשונית חדשה במסך ה{PROBE}</span><span class="grow"></span><span class="btn sec" style="height:34px">שמור כחיפוש קבוע</span><span class="btn pri" style="height:34px">{ic("search", "s")}חפש</span></div>
</div>'''
    body = read_tabs() + read_bar() + f'<div class="read-body">{nav_panel()}{read_text(sel=False)}{comm_panel()}</div>'
    return page('read', body, 'חלון החיפוש', extra=float_)


# ---------------- חקירה ----------------
HITS = [
    ('ברכות', 'דף ב.', 'תלמוד בבלי &gt; סדר זרעים',
     '…וחכמים אומרים עד חצות. רבן גמליאל אומר עד שיעלה <mark>עמוד השחר</mark>. מעשה ובאו בניו מבית המשתה אמרו לו לא קרינו את שמע…'),
    ('ברכות', 'דף ב.', 'תלמוד בבלי &gt; סדר זרעים',
     '…אמר להם אם לא עלה <mark>עמוד השחר</mark> חייבין אתם לקרות ולא זו בלבד אמרו אלא כל מה שאמרו חכמים עד חצות מצותן עד שיעלה <mark>עמוד השחר</mark>…'),
    ('משנה ברכות', 'פרק א, משנה א', 'משנה &gt; סדר זרעים',
     '…הקטר חלבים ואברים מצותן עד שיעלה <mark>עמוד השחר</mark> וכל הנאכלים ליום אחד מצותן עד שיעלה <mark>עמוד השחר</mark>…'),
    ('משנה ברכות', 'פרק א, משנה א', 'משנה &gt; סדר זרעים',
     '…רבן גמליאל אומר עד שיעלה <mark>עמוד השחר</mark>. מעשה ובאו בניו מבית המשתה אמרו לו לא קרינו את שמע אמר להם אם לא עלה <mark>עמוד השחר</mark> חייבין אתם לקרות…'),
    ('תוספות רבינו יהודה החסיד על ברכות', 'דף ב.', 'תלמוד בבלי &gt; ראשונים',
     'רבן גמליאל אומר עד שיעלה <mark>עמוד השחר</mark>. בגמרא (ח׳:) אמר רב יהודה אמר שמואל הלכה כר׳ גמליאל…'),
]


def probe_tabs():
    t = ''.join(f'<span class="tab{" on" if i == 0 else ""}">{ic("probe", "s")}{q}<span class="x">{ic("x", "s")}</span></span>'
                 for i, q in enumerate(['עמוד השחר', 'צאת הכוכבים', 'זמן שכיבה']))
    return f'<div class="tabs">{t}<span class="tab add">{ic("plus", "s")}</span></div>'


def facet():
    rows = [('כל הספרייה', 412, 0, True), ('תלמוד בבלי', 168, 1, False), ('סדר זרעים', 41, 2, False), ('ראשונים', 74, 2, False),
            ('משנה', 37, 1, False), ('תלמוד ירושלמי', 29, 1, False), ('הלכה', 121, 1, False), ('שולחן ערוך', 33, 2, False),
            ('אחרונים', 58, 2, False), ('מדרש', 19, 1, False), ('שו״ת', 38, 1, False)]
    lis = ''.join(f'<li class="{"l2" if lv == 1 else "l3" if lv == 2 else ""}{" on" if on else ""}">'
                  f'{ic("folder", "s") if lv < 2 else ""}{n}<span class="cnt">{c}</span></li>' for n, c, lv, on in rows)
    return f'''<aside class="facet"><h6>סינון לפי מדף</h6><ul class="tree">{lis}</ul></aside>'''


def screen_probe():
    hits = ''.join(f'''<div class="hit{" on" if i == 0 else ""}"><div class="hp"><b>{t}</b>{w}<span class="grow"></span>{p}</div><p>{s}</p></div>'''
                   for i, (t, w, p, s) in enumerate(HITS))
    row = f'''<div class="row thin">
  <span style="font-family:var(--head);font-size:18px;color:#3E4228">«עמוד השחר»</span>
  <span class="pill" style="background:#E8E7D3;color:#3E4228">צירוף מדויק</span><span class="pill" style="background:#E8E7D3;color:#3E4228">כל הספרייה</span>
  {ib("search", title="ערוך את החיפוש")}
  <span class="grow"></span>
  <span style="font-size:12.5px;color:var(--muted)">412 תוצאות ב־96 ספרים</span>
  <div class="sep"></div>{ib("sort", title="מיון")}{ib("filter", title="סינון")}{ib("commp", on=True, title="תצוגה מקדימה")}
</div>'''
    ctx = f'''<aside class="ctx">
  <h3>ברכות, דף ב.</h3><div class="path">תלמוד בבלי &gt; סדר זרעים &gt; ברכות &gt; פרק ראשון</div>
  <p class="dim">מאימתי קורין את שמע בערבין. משעה שהכהנים נכנסים לאכול בתרומתן עד סוף האשמורה הראשונה דברי ר׳ אליעזר.</p>
  <p>וחכמים אומרים עד חצות. רבן גמליאל אומר עד שיעלה <mark>עמוד השחר</mark>. מעשה ובאו בניו מבית המשתה אמרו לו לא קרינו את שמע אמר להם אם לא עלה <mark>עמוד השחר</mark> חייבין אתם לקרות…</p>
  <div class="actions" style="position:absolute;bottom:20px;left:24px;right:24px"><span class="btn pri">{ic("read", "s")}פתח לעיון</span><span class="btn sec">{ic("spread2", "s")}פתח לצד החקירה</span></div>
</aside>'''
    body = probe_tabs() + row + f'<div class="probe-body">{facet()}<section class="hits">{hits}</section>{ctx}</div>'
    return page('probe', body, PROBE)


# ---------------- פרישה ----------------
def lib_tree_pane():
    return f'''<section class="pane p-lib">
  <div class="pane-h">{ic("lib", "s")}<span class="pt">ספרייה</span><span class="grow"></span>{ib("search")}</div>
  <div style="padding:8px 10px 0"><div class="field" style="height:32px">{ic("search", "s")}<span class="ph">חיפוש חיבור או מחבר</span></div></div>
  <ul class="ltree">
    <li>{ic("c1l", "s")}תנ״ך</li>
    <li>{ic("cdown", "s")}תלמוד בבלי</li>
    <li class="l2">{ic("cdown", "s")}סדר זרעים</li>
    <li class="l3 on"><span class="bkI">{ic("book", "s")}</span>ברכות</li>
    <li class="l2">{ic("c1l", "s")}סדר מועד</li>
    <li class="l2">{ic("c1l", "s")}סדר נשים</li>
    <li class="l2">{ic("c1l", "s")}סדר נזיקין</li>
    <li class="l2">{ic("cdown", "s")}ראשונים</li>
    <li class="l3"><span class="bkI">{ic("book", "s")}</span>רש״י על ברכות</li>
    <li class="l3"><span class="bkI">{ic("book", "s")}</span>רי״ף ברכות</li>
    <li class="l3"><span class="bkI">{ic("book", "s")}</span>מאירי על ברכות</li>
    <li class="l2">{ic("c1l", "s")}אחרונים</li>
    <li>{ic("c1l", "s")}משנה</li>
    <li>{ic("c1l", "s")}תלמוד ירושלמי</li>
    <li>{ic("c1l", "s")}מדרש</li>
    <li>{ic("c1l", "s")}הלכה</li>
    <li>{ic("c1l", "s")}קבלה</li>
    <li>{ic("c1l", "s")}ספרי מוסר</li>
  </ul>
</section>'''


def read_pane(compact_bar=True):
    bar = f'''<div class="pane-h" style="background:var(--surface)">{ic("read", "s")}<span class="pt">ברכות · דף ב.</span><span class="grow"></span>
  {ib("c2r")}{ib("c1r")}{ib("justify")}{ib("c1l")}{ib("c2l")}<div class="sep"></div>{ib("zin")}{ib("zout")}{ib("commp")}{ib("more")}</div>'''
    return f'''<section class="pane p-read">{bar}
  <article class="text" style="padding:24px 40px">
    <h2 style="margin-bottom:10px">פרק ראשון · מאימתי</h2>
    <h3>מתני׳</h3><p>{MISHNA}</p>
    <h3>גמ׳</h3><p>{GEMARA}</p>
  </article></section>'''


def probe_pane():
    hits = ''.join(f'''<div class="mini-hit{" on" if i == 1 else ""}"><div class="hp"><b>{t}</b> · {w}</div><p>{s}</p></div>'''
                   for i, (t, w, p, s) in enumerate(HITS))
    return f'''<section class="pane p-probe">
  <div class="pane-h">{ic("probe", "s")}<span class="pt">{PROBE}: «עמוד השחר»</span><span class="grow"></span><span style="font-size:12px;color:var(--muted)">412</span>{ib("filter")}</div>
  {hits}
</section>'''


def screen_spread_three():
    body = f'<div class="spread-body">{lib_tree_pane()}{read_pane()}{probe_pane()}</div>'
    return page('spread', body, 'פרישה — שלושתם')


def screen_spread_two():
    body = f'<div class="spread-body">{read_pane()}{probe_pane()}</div>'
    html = page('spread', body, 'פרישה — עיון וחקירה')
    # במתג: פרישה של שניים — ספרייה כבויה
    return html.replace('title="פרישה: כולם במקביל">' + ic('spread'), 'title="פרישה: עיון וחקירה">' + ic('spread2'))


def screen_board():
    return f'''<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8"><title>שלושת המצבים</title>
<link rel="stylesheet" href="style.css"></head><body><div class="board">
<h1>המסך הראשי בשלושה מצבים</h1>
<div class="lead">רצועת הכותרת קבועה; המתג שבמרכזה מחליף את המצב, וההבדל בין המצבים — בגוון המסגרת בלבד.</div>
<div class="trip">
 <figure><img src="04-library-shelf.png"><figcaption>ספרייה<span>הרקע שעומד תמיד: משבצות המדפים, ותצוגה מקדימה משמאל.</span></figcaption></figure>
 <figure><img src="07-reading.png"><figcaption>עיון<span>הספר הפתוח ולשוניות הספרים; ניווט מימין ומפרשים משמאל.</span></figcaption></figure>
 <figure><img src="10-probe.png"><figcaption>{PROBE}<span>תוצאות החיפוש, כמו היום: סינון מימין, תצוגה מקדימה משמאל.</span></figcaption></figure>
</div>
<h2 class="bh2">רצועת הכותרת — אחת לשלושתם</h2>
<div class="crops">
 <div class="crop"><img src="04-library-shelf.png"></div>
 <div class="crop"><img src="07-reading.png"></div>
 <div class="crop"><img src="10-probe.png"></div>
</div></div></body></html>'''


SCREENS = [
    ('02-spread-three', screen_spread_three),
    ('03-spread-two', screen_spread_two),
    ('04-library-shelf', screen_library_shelf),
    ('05-library-book', screen_library_book),
    ('06-library-author', screen_library_author),
    ('07-reading', screen_reading),
    ('08-find-window', screen_find),
    ('09-search-window', screen_search),
    ('10-probe', screen_probe),
]


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else 'out-v2')
    os.makedirs(out, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'style.css'), out)
    shutil.copy(os.path.join(HERE, 'logo.png'), out)
    fonts = os.path.join(os.path.dirname(out), 'fonts')
    if not os.path.isdir(fonts):
        shutil.copytree(os.path.join(HERE, '..', 'fonts'), fonts)
    for name, fn in SCREENS:
        with open(os.path.join(out, name + '.html'), 'w', encoding='utf-8') as f:
            f.write(fn())
    with open(os.path.join(out, '01-three-modes.html'), 'w', encoding='utf-8') as f:
        f.write(screen_board())
    print('נכתבו', len(SCREENS) + 1, 'דפים אל', out)


if __name__ == '__main__':
    main()
