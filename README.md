# AI Assistant - Raspberry Pi Smart Home

A smart home AI assistant running on Raspberry Pi, powered by [PicoClaw](https://github.com/sipeed/picoclaw) — an ultra-lightweight personal AI agent written in Go.

## Overview

This project controls physical smart home devices via Telegram using PicoClaw as the AI backbone. It supports multiple agents (Home Assistant, AI News Weekly) and a rich set of skills.

## Controlled Devices

| # | Device | Protocol | Script |
|---|--------|----------|--------|
| 1 | מזגן סלון (Tadiran Mini Central AC) | Tuya Cloud | `smarthome.py ac` |
| 2 | מזגן חדר ילדים (Gree) | Gree Local UDP | `room_ac.py ילדים` |
| 3 | מזגן חדר שינה (Gree) | Gree Local UDP | `room_ac.py שינה` |
| 4 | בוילר (Water Heater) | Tuya Cloud | `smarthome.py boiler` |
| 5 | טלוויזיה (LG WebOS TV) | WebOS WebSocket | `tv.py` |

## Architecture

```
Telegram → PicoClaw (Go agent) → Python scripts → Devices
                ↓
         Skills / Memory / Cron
```

### Agents

- **Home Assistant** (`workspace-home/`) — Controls smart home devices, responds in Hebrew/English
- **AI News Weekly** (`workspace-news/`) — Automated weekly AI news digest via Telegram

### Skills

| Skill | Description |
|-------|-------------|
| `ac-salon` | Tadiran AC control via Tuya |
| `ac-rooms` | Gree room ACs control |
| `boiler` | Water heater control via Tuya |
| `tv` | LG WebOS TV control |
| `hardware` | I2C/SPI peripheral control for Sipeed boards |
| `weather` | Weather information |
| `tmux` | Tmux session management |
| `summarize` | Text summarization |
| `github` | GitHub integration |
| `skill-creator` | Create new skills |
| `tuya-boiler` | Direct Tuya boiler control |

## Setup

1. Install PicoClaw on your Raspberry Pi
2. Copy `picoclaw-config/config.example.json` to `~/.picoclaw/config.json` and fill in your API keys
3. Copy workspace files to `~/.picoclaw/workspace/`
4. Install Python dependencies: `pip install tinytuya aiowebostv greeclimate telethon`
5. Run PicoClaw: `picoclaw`

## Scripts

- `workspace/smarthome.py` — Controls Tuya devices (AC + boiler)
- `workspace/room_ac.py` — Controls Gree room ACs via local network
- `workspace/tv.py` — Controls LG WebOS TV over WiFi
- `scripts/smarthome_webhook.py` — Siri webhook → PicoClaw bridge
- `scripts/telethon_login.py` — Telegram login helper
- `scripts/tv_pair.py` — One-time LG TV pairing

## File Structure

```
├── workspace/                  # Main PicoClaw workspace
│   ├── SOUL.md                # Agent personality & behavior
│   ├── AGENT.md               # Agent instructions
│   ├── IDENTITY.md            # Agent identity
│   ├── USER.md                # User profile
│   ├── smarthome.py           # Tuya device controller
│   ├── room_ac.py             # Gree AC controller
│   ├── tv.py                  # LG TV controller
│   ├── skills/                # PicoClaw skills
│   └── memory/                # Agent memory
├── workspace-home/            # Home agent workspace
├── workspace-news/            # News agent workspace
├── scripts/                   # Standalone utility scripts
├── picoclaw-config/           # Config examples
├── config.py                  # Legacy config
└── .env.example               # Environment variables template
```
