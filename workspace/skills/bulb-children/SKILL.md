---
name: bulb-children
description: שליטה בנורה חכמה בחדר ילדים — הדלקה, כיבוי, בהירות, צבע, טמפרטורת צבע, סצנות, טיימר
metadata: {"nanobot":{"emoji":"💡"}}
---

# נורה חכמה — חדר ילדים 💡

שליטה בנורה החכמה (Smart Life) בחדר הילדים.

## פקודות

כל הפקודות מריצות את הסקריפט דרך exec. **אסור להשתמש ב-echo.**

### הדלקה / כיבוי
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים on
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים off
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים status
```

### בהירות (1-100)
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים brightness 50
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים brightness 100
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים brightness 10
```

### טמפרטורת צבע (חם/קריר)
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים temp warm      # אור חם (נר/שקיעה)
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים temp cool      # אור קריר (אור יום)
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים temp natural   # ניטרלי
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים temp 70        # 0=קריר, 100=חם
```

### צבעים 🎨
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color red       # אדום
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color blue      # כחול
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color green     # ירוק
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color yellow    # צהוב
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color purple    # סגול
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color pink      # ורוד
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color orange    # כתום
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color cyan      # תכלת
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color white     # לבן
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color warm      # חם
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color cool      # קריר
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color lavender  # לבנדר
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color coral     # אלמוג
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color mint      # מנטה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color gold      # זהב
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color turquoise # טורקיז
```

גם בעברית:
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color אדום
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color כחול
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color ירוק
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color סגול
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים color ורוד
```

### HSV מדויק (גוון 0-360, רוויה 0-100, בהירות 0-100)
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים hsv 180 80 70
```

### סצנות / תאורה 🎭
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene night     # אור לילה — עמום וחם
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene reading   # קריאה — בהיר וניטרלי
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene relax     # רגיעה — בינוני וחם
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene party     # מסיבה — צבעים מתחלפים
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene romance   # רומנטי — ורוד/סגול עמום
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene focus     # ריכוז — בהיר וקריר
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene energy    # אנרגיה — מקסימום אור קריר
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene sleep     # שינה — מאוד עמום וחם
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene rainbow   # קשת — כל הצבעים
```

גם בעברית:
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene לילה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene קריאה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene רגיעה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene מסיבה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene רומנטי
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene ריכוז
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene שינה
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene קשת
```

### טיימר כיבוי אוטומטי (דקות)
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים timer 30     # כבה אחרי 30 דקות
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים timer 60     # כבה אחרי שעה
```

### קיצורים — הדלקה עם הגדרה
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים on red       # הדלק באדום
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים on 30        # הדלק ב-30% בהירות
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים on warm      # הדלק באור חם
```

## דוגמאות לבקשות בעברית ומה להריץ

| בקשה | פקודה |
|------|-------|
| "תדליק את הנורה בחדר ילדים" | `bulbs.py ילדים on` |
| "תכבה אור בחדר ילדים" | `bulbs.py ילדים off` |
| "תשים אור חלש בחדר ילדים" | `bulbs.py ילדים brightness 20` |
| "תשנה את הנורה לכחול" | `bulbs.py ילדים color כחול` |
| "תשים אור לילה" | `bulbs.py ילדים scene לילה` |
| "תשים אור חם בחדר ילדים" | `bulbs.py ילדים temp warm` |
| "תכבה את הנורה בחדר ילדים אחרי 20 דקות" | `bulbs.py ילדים on && bulbs.py ילדים timer 20` |
| "תשים מסיבה" | `bulbs.py ילדים scene מסיבה` |
| "בהירות מלאה" | `bulbs.py ילדים brightness 100` |
| "תשים צבע ורוד" | `bulbs.py ילדים color ורוד` |
| "תשים אור שינה לתינוק" | `bulbs.py ילדים scene baby` |
| "אור לילה טוב" | `bulbs.py ילדים scene לילה-טוב` |
| "תשים אור לתינוק ל-30 דקות" | `bulbs.py ילדים scene baby && bulbs.py ילדים timer 30` |



### אור שינה לתינוק (Baby Sleep Light) 👶
אור אדום-כתום עמום מאוד — לא מדכא מלטונין, עוזר לתינוק להירדם.
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene baby
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene תינוק
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene לילה-טוב
```

עם טיימר כיבוי אוטומטי:
```
python3 /home/david/.picoclaw/workspace/bulbs.py ילדים scene baby && python3 /home/david/.picoclaw/workspace/bulbs.py ילדים timer 30
```

## כללים

1. פקודה ברורה → exec מיידי. לא לקרוא קבצים. לא לחקור.
2. **אסור** לדמות פקודה עם echo — תמיד להריץ את הסקריפט האמיתי.
3. אחרי כל exec, לדווח את הפלט האמיתי.
4. "נורה" בלי ציון חדר → לשאול: חדר ילדים או חדר הורים?
