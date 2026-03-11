#!/usr/bin/env python3
"""Webhook - receives Siri commands, forwards to PicoClaw bot via Telegram."""
import json, urllib.request, asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from telethon import TelegramClient

from config import API_ID, API_HASH, SESSION, BOT_TOKEN, CHAT_ID, BOT_USERNAME


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
        except (json.JSONDecodeError, ValueError):
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


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each request in a separate thread."""


if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", 8899), Handler)
    print("Webhook running on port 8899 - forwarding to PicoClaw via Telegram")
    server.serve_forever()
