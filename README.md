# AI Assistant - Raspberry Pi

Smart home AI assistant running on Raspberry Pi.
Integrates with Telegram bot and controls smart home devices via Siri webhooks.

## Components
- **smarthome_webhook.py** - Receives Siri commands, forwards to Telegram bot
- **telethon_login.py** - Telegram client authentication
- **tv_pair.py** - TV pairing/control

## Setup
```bash
pip install telethon
python telethon_login.py
python smarthome_webhook.py
```
