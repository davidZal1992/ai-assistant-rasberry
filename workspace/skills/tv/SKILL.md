---
name: tv
description: Control the LG TV / טלוויזיה / TV. Use when user asks to control the television, change channels, adjust volume, open apps, or turn TV on/off.
---

# LG TV (טלוויזיה)

Script: `python3 /home/david/.picoclaw/workspace/tv.py <args>`

## Commands
| Action | Command |
|--------|---------|
| Turn on | `tv.py on` |
| Turn off | `tv.py off` |
| Status | `tv.py status` |
| Volume (0–100) | `tv.py volume 20` |
| Volume up/down | `tv.py volume up` / `tv.py volume down` |
| Mute | `tv.py mute` |
| Channel number | `tv.py channel 12` |
| Channel up/down | `tv.py channel up` / `tv.py channel down` |
| Open app | `tv.py app netflix\|youtube\|spotify\|prime\|livetv` |
| Key press | `tv.py key back\|home` |

## Examples
"עבור לערוץ 12":
`python3 /home/david/.picoclaw/workspace/tv.py channel 12`

"פתח נטפליקס":
`python3 /home/david/.picoclaw/workspace/tv.py app netflix`

## CRITICAL RULES
- NEVER use key presses for channels — ALWAYS use `tv.py channel N`
- Always use full path: `/home/david/.picoclaw/workspace/`
- **If the command fails or returns an error → report it immediately in one sentence. Do NOT read the script, do NOT run status, do NOT ping the TV. Just say "הטלוויזיה לא מגיבה — כנראה כבויה לגמרי"**
- The TV disconnects from network when fully off — this is normal. Report it and stop.
