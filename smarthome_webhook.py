#!/usr/bin/env python3
"""Webhook - receives Siri commands, forwards to PicoClaw bot via Telegram."""
import json, urllib.request, asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient

API_ID      = 39040426
API_HASH    = "6e6ab2a82b7401ab1513729593a86b1d"
SESSION     = "/home/david/smarthome_session"
BOT_USERNAME = "zaltsman_assistant_bot"

BOT_TOKEN = "8616021483:AAHHslNjxDayDVfoXcGbYsvStAdoa3_D1Bo"
CHAT_ID   = "303984494"

def send_telegram(text):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
    req  = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")

async def forward_to_picoclaw(text):
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        await client.send_message(BOT_USERNAME, text)
        print(f"[FORWARDED] {text}")

def handle(text):
    print(f"[CMD] {text}")
    try:
        asyncio.run(forward_to_picoclaw(text))
        # PicoClaw will reply directly in Telegram — no need to send separately
    except Exception as e:
        print(f"[ERROR] {e}")
        send_telegram(f"שגיאה בשליחת הפקודה: {e}")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length).decode()
        try:
            text = json.loads(body).get("text", "").strip()
        except:
            text = body.strip()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

        if text:
            handle(text)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Smart Home Webhook - PicoClaw bridge")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8899), Handler)
    print("Webhook running on port 8899 - forwarding to PicoClaw via Telegram")
    server.serve_forever()