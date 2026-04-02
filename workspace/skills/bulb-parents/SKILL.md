---
name: bulb-parents
description: שליטה בנורה חכמה בחדר הורים — הדלקה, כיבוי, בהירות, צבע, טמפרטורת צבע, סצנות, טיימר
metadata: {"nanobot":{"emoji":"💡"}}
---

# נורה חכמה — חדר הורים 💡

שליטה בנורה החכמה (Smart Life) בחדר ההורים.

## פקודות

כל הפקודות מריצות את הסקריפט דרך exec. **אסור להשתמש ב-echo.**

### הדלקה / כיבוי
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים on
python3 /home/david/.picoclaw/workspace/bulbs.py הורים off
python3 /home/david/.picoclaw/workspace/bulbs.py הורים status
```

### בהירות (1-100)
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים brightness 50
python3 /home/david/.picoclaw/workspace/bulbs.py הורים brightness 100
python3 /home/david/.picoclaw/workspace/bulbs.py הורים brightness 10
```

### טמפרטורת צבע (חם/קריר)
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים temp warm      # אור חם (נר/שקיעה)
python3 /home/david/.picoclaw/workspace/bulbs.py הורים temp cool      # אור קריר (אור יום)
python3 /home/david/.picoclaw/workspace/bulbs.py הורים temp natural   # ניטרלי
python3 /home/david/.picoclaw/workspace/bulbs.py הורים temp 70        # 0=קריר, 100=חם
```

### צבעים 🎨
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color red       # אדום
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color blue      # כחול
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color green     # ירוק
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color yellow    # צהוב
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color purple    # סגול
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color pink      # ורוד
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color orange    # כתום
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color cyan      # תכלת
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color white     # לבן
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color warm      # חם
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color cool      # קריר
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color lavender  # לבנדר
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color coral     # אלמוג
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color mint      # מנטה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color gold      # זהב
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color turquoise # טורקיז
```

גם בעברית:
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color אדום
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color כחול
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color ירוק
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color סגול
python3 /home/david/.picoclaw/workspace/bulbs.py הורים color ורוד
```

### HSV מדויק (גוון 0-360, רוויה 0-100, בהירות 0-100)
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים hsv 180 80 70
```

### סצנות / תאורה 🎭
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene night     # אור לילה — עמום וחם
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene reading   # קריאה — בהיר וניטרלי
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene relax     # רגיעה — בינוני וחם
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene party     # מסיבה — צבעים מתחלפים
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene romance   # רומנטי — ורוד/סגול עמום
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene focus     # ריכוז — בהיר וקריר
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene energy    # אנרגיה — מקסימום אור קריר
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene sleep     # שינה — מאוד עמום וחם
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene rainbow   # קשת — כל הצבעים
```

גם בעברית:
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene לילה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene קריאה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene רגיעה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene מסיבה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene רומנטי
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene ריכוז
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene שינה
python3 /home/david/.picoclaw/workspace/bulbs.py הורים scene קשת
```

### טיימר כיבוי אוטומטי (דקות)
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים timer 30     # כבה אחרי 30 דקות
python3 /home/david/.picoclaw/workspace/bulbs.py הורים timer 60     # כבה אחרי שעה
```

### קיצורים — הדלקה עם הגדרה
```
python3 /home/david/.picoclaw/workspace/bulbs.py הורים on red       # הדלק באדום
python3 /home/david/.picoclaw/workspace/bulbs.py הורים on 30        # הדלק ב-30% בהירות
python3 /home/david/.picoclaw/workspace/bulbs.py הורים on warm      # הדלק באור חם
```

## דוגמאות לבקשות בעברית ומה להריץ

| בקשה | פקודה |
|------|-------|
| "תדליק את הנורה בחדר הורים" | `bulbs.py הורים on` |
| "תכבה אור בחדר שינה" | `bulbs.py הורים off` |
| "תשים אור עמום בחדר" | `bulbs.py הורים brightness 15` |
| "תשנה את הנורה לסגול" | `bulbs.py הורים color סגול` |
| "אור לילה בחדר שינה" | `bulbs.py הורים scene לילה` |
| "תשים אור חם" | `bulbs.py הורים temp warm` |
| "תכבה את הנורה אחרי חצי שעה" | `bulbs.py הורים on && bulbs.py הורים timer 30` |
| "תשים רומנטי" | `bulbs.py הורים scene רומנטי` |
| "אור מלא" | `bulbs.py הורים brightness 100` |
| "תשים ורוד" | `bulbs.py הורים color ורוד` |

## כללים

1. פקודה ברורה → exec מיידי. לא לקרוא קבצים. לא לחקור.
2. **אסור** לדמות פקודה עם echo — תמיד להריץ את הסקריפט האמיתי.
3. אחרי כל exec, לדווח את הפלט האמיתי.
4. "נורה" בלי ציון חדר → לשאול: חדר ילדים או חדר הורים?
5. "חדר שינה" = חדר הורים (אותו מכשיר).
