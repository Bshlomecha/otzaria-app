# הדמיות "בית המדרש"

הקוד שמפיק את ההדמיות למסמך היסוד `docs/design-system/APP_STRUCTURE.md`, שבבקשת המיזוג https://github.com/Otzaria/otzaria/pull/6015 . זה ענף עזר, לא לקוד התוכנה.

## הקבצים

- `kit.py`: צבעי "דבש וחלב", גופנים, אייקונים ורכיבי מעטפת.
- `mockups.py` עד `mockups4.py`: כל קובץ מרחיב את קודמו, ו־`mockups4.py` מפיק את כל ארבע עשרה ההדמיות.
- `render.sh`: הופך כל SVG בתיקייה ל־PNG, בעזרת Edge במצב headless, ברוחב 1320 על 800.
- `fonts/`: FrankRuhlCLM ו־NotoRashiHebrew, מתיקיית `fonts` במאגר אוצריא.
- `HANDOFF.md`: מסמך המסירה, להדבקה בשיחה חדשה.
- `post50303-snapshot.md`: פוסט היסוד כפי שהיה ב־25.11.2026, להשוואה עם גרסה חדשה.

## הרצה (Git Bash ב־Windows)

```
python -I mockups4.py out
bash render.sh "$PWD/out"
```

התמונות נוצרות בתיקייה `out`. מעתיקים אותן ל־`docs/design-system/app-structure/` בענף `docs/app-structure-beit-midrash`.

כדאי לשמור את התיקייה בנתיב בלי עברית. Edge טוען את הגופנים דרך כתובת `file:///`, ונתיב בעברית עלול להכשיל אותה.

## המתווה המפושט (v2, 27.11)

לפי פוסט 50637: שלושה מצבים למסך הראשי — ספרייה · עיון · חקירה. ההדמיות בתיקייה `v2/`, ב־HTML ו־CSS, ומצולמות ב־Edge headless ברוחב 1440 על 900.

- `v2/build.py`: כותב את הדפים. `v2/style.css`: הצבעים, הגופנים והרכיבים. `v2/logo.png`: הלוגו מ־`assets/icon/icon_256.png` במאגר אוצריא.
- `fonts/DrugulinCLM-Bold.ttf`: לכותרות, כבתוספים.

```
python -I v2/build.py /c/tmp/v2/out
bash v2/render.sh /c/tmp/v2/out
```

התמונות נכנסות ל־`docs/design-system/app-structure/v2/` בענף המסמך. ההדמיות הישנות (`mockups*.py`) נשארות כמות שהן.
