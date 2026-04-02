---
name: boiler
description: Control the boiler / water heater / דוד מים / דוד / בוילר. Use when user asks about hot water or the boiler.
---

# Boiler / Water Heater (בוילר / דוד מים)

Script: `python3 /home/david/.picoclaw/workspace/smarthome.py boiler <args>`

"דוד", "בוילר", "דוד מים" — all the same device.

## Commands
| Action | Command |
|--------|---------|
| Turn on | `smarthome.py boiler on` |
| Turn off | `smarthome.py boiler off` |
| Status | `smarthome.py boiler status` |
| Timer (minutes) | `smarthome.py boiler timer 40` |

## Examples
"הדלק דוד":
`python3 /home/david/.picoclaw/workspace/smarthome.py boiler on`

"הדלק דוד 35 דקות":
`python3 /home/david/.picoclaw/workspace/smarthome.py boiler timer 35`

## Rules
- Always use full path: `/home/david/.picoclaw/workspace/`
