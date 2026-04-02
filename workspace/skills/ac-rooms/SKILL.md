---
name: ac-rooms
description: Control bedroom or kids room AC / מזגן חדר ילדים / מזגן חדר שינה / מזגן גרי. Use when user asks to control a room air conditioner.
---

# Room ACs (מזגני חדרים — Gree)

Script: `python3 /home/david/.picoclaw/workspace/room_ac.py <room> <args>`

Rooms: `ילדים` | `שינה` | `all`

## Commands
| Action | Command |
|--------|---------|
| Turn on | `room_ac.py ילדים on` |
| Turn off | `room_ac.py ילדים off` |
| Set temp | `room_ac.py ילדים temp 23` |
| Set mode | `room_ac.py ילדים mode heat\|cool\|auto\|dry\|fan` |
| Set fan | `room_ac.py ילדים fan low\|medium\|high\|auto` |
| Status | `room_ac.py ילדים status` |
| Turn off all rooms | `room_ac.py all off` |
| Status all rooms | `room_ac.py all status` |

Same commands apply for `שינה`.

## Examples
"הדלק מזגן חדר ילדים קר 22":
`python3 /home/david/.picoclaw/workspace/room_ac.py ילדים on && python3 /home/david/.picoclaw/workspace/room_ac.py ילדים mode cool && python3 /home/david/.picoclaw/workspace/room_ac.py ילדים temp 22`

"כבה את שני מזגני החדרים":
`python3 /home/david/.picoclaw/workspace/room_ac.py all off`

## Rules
- Always use full path: `/home/david/.picoclaw/workspace/`
