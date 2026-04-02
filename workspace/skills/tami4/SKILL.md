---
name: tami4
description: שליטה בבר המים Tami4 Edge — הרתחה, הכנת משקאות, סטטוס פילטר ו-UV
metadata: {"nanobot":{"emoji":"💧"}}
---

# Tami4 Edge — בר מים חכם 💧

שליטה בבר המים Tami4 Edge.

## פקודות

כל הפקודות מריצות את הסקריפט דרך exec. **אסור להשתמש ב-echo.**

### הרתחת מים
```
python3 /home/david/.picoclaw/workspace/tami4.py boil
```

### הכנת משקה
```
python3 /home/david/.picoclaw/workspace/tami4.py coffee          # קפה (251ml)
python3 /home/david/.picoclaw/workspace/tami4.py bottle          # בקבוק (306ml)
python3 /home/david/.picoclaw/workspace/tami4.py cold            # ליטר וחצי (1234ml)
python3 /home/david/.picoclaw/workspace/tami4.py teapot          # קנקן חם (1205ml)
```

גם בעברית:
```
python3 /home/david/.picoclaw/workspace/tami4.py קפה
python3 /home/david/.picoclaw/workspace/tami4.py בקבוק
python3 /home/david/.picoclaw/workspace/tami4.py ליטר
python3 /home/david/.picoclaw/workspace/tami4.py קנקן
python3 /home/david/.picoclaw/workspace/tami4.py water          # כוס מים קר (260ml)
python3 /home/david/.picoclaw/workspace/tami4.py כוס            # כוס מים קר (260ml)
python3 /home/david/.picoclaw/workspace/tami4.py מים            # כוס מים קר (260ml)
```

או עם פקודת drink:
```
python3 /home/david/.picoclaw/workspace/tami4.py drink coffee
python3 /home/david/.picoclaw/workspace/tami4.py drink קפה
python3 /home/david/.picoclaw/workspace/tami4.py drink bottle
python3 /home/david/.picoclaw/workspace/tami4.py drink teapot
```

### סטטוס ומידע
```
python3 /home/david/.picoclaw/workspace/tami4.py status          # סטטוס מכשיר, פילטר, UV
python3 /home/david/.picoclaw/workspace/tami4.py drinks          # רשימת משקאות
```

## משקאות זמינים

| שם | פקודה | נפח |
|----|-------|------|
| קפה | `coffee` / `קפה` | 251ml |
| בקבוק | `bottle` / `בקבוק` | 306ml |
| ליטר וחצי (קנקן קר) | `cold` / `ליטר` / `קנקן-קר` | 1234ml |
| קנקן חם | `teapot` / `קנקן` / `קנקן-חם` / `hot` | 1205ml |
| כוס מים קר | `water` / `cup` / `כוס` / `מים` / `מים-קרים` | 260ml |

## דוגמאות לבקשות בעברית ומה להריץ

| בקשה | פקודה |
|------|-------|
| "תרתיח מים" | `tami4.py boil` |
| "הרתח לי מים" | `tami4.py boil` |
| "תכין לי קפה" | `tami4.py coffee` |
| "תמלא בקבוק" | `tami4.py bottle` |
| "תכין קנקן חם" | `tami4.py teapot` |
| "מלא קנקן קר" | `tami4.py cold` |
| "מה מצב הפילטר?" | `tami4.py status` |
| "מתי צריך להחליף UV?" | `tami4.py status` |
| "מה המשקאות שיש?" | `tami4.py drinks` |
| "מים חמים" | `tami4.py boil` |
| "כוס מים קרים" | `tami4.py water` |
| "תמלא כוס מים" | `tami4.py cup` |
| "מים קרים" | `tami4.py מים` |

## כללים

1. פקודה ברורה → exec מיידי. לא לקרוא קבצים. לא לחקור.
2. **אסור** לדמות פקודה עם echo — תמיד להריץ את הסקריפט האמיתי.
3. אחרי כל exec, לדווח את הפלט האמיתי.
4. "מים" סתם → שאול: הרתחה או משקה מסוים?
5. "תכין" ללא ציון משקה → שאול: קפה / בקבוק / קנקן חם / ליטר וחצי?
