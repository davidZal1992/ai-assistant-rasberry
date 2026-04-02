---
name: ac-salon
description: Control the salon AC / central AC / מזגן סלון / מזגן מרכזי / מזגן תדיראן. Use when user asks to control the main living room air conditioner.
---

# Salon AC (מזגן סלון — Tadiran)

Script: `python3 /home/david/.picoclaw/workspace/smarthome.py ac <args>`

## Commands
| Action | Command |
|--------|---------|
| Turn on | `smarthome.py ac on` |
| Turn off | `smarthome.py ac off` |
| Status | `smarthome.py ac status` |
| Set temp (16–32°C) | `smarthome.py ac temp 24` |
| Set mode | `smarthome.py ac mode hot\|cold\|auto\|wet\|wind` |
| Set fan | `smarthome.py ac fan low\|middle\|high\|auto` |

Each setting is a **separate call**, chained with `&&`.

## Examples
"הדלק מזגן סלון חום 27":
`python3 /home/david/.picoclaw/workspace/smarthome.py ac on && python3 /home/david/.picoclaw/workspace/smarthome.py ac mode hot && python3 /home/david/.picoclaw/workspace/smarthome.py ac temp 27`

"קרר את הסלון ל-22":
`python3 /home/david/.picoclaw/workspace/smarthome.py ac on && python3 /home/david/.picoclaw/workspace/smarthome.py ac mode cold && python3 /home/david/.picoclaw/workspace/smarthome.py ac temp 22`

## Rules
- "מזגן" with no room specified → ask: סלון / חדר ילדים / חדר שינה / הכל?
- Always use full path: `/home/david/.picoclaw/workspace/`
