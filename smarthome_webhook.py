#!/usr/bin/env python3
"""Webhook - receives Siri commands, forwards to PicoClaw bot via Telegram."""
import json, urllib.request, asyncio, uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from telethon import TelegramClient

from config import API_ID, API_HASH, SESSION, BOT_TOKEN, CHAT_ID, BOT_USERNAME
from trace import Trace


def send_telegram(text):
    url  = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
    req  = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print("[TELEGRAM ERROR] {}".format(e))


async def forward_to_picoclaw(text, trace):
    with trace.step("telethon_connect"):
        client = TelegramClient(SESSION, API_ID, API_HASH)
        await client.connect()

    try:
        with trace.step("send_message"):
            await client.send_message(BOT_USERNAME, text)
            print("[FORWARDED] {}".format(text))
    finally:
        with trace.step("telethon_disconnect"):
            await client.disconnect()


def handle(text):
    trace = Trace(request_id=str(uuid.uuid4())[:8])
    print("[CMD] {}".format(text))
    try:
        with trace.step("total_telegram_roundtrip"):
            asyncio.run(forward_to_picoclaw(text, trace))
        trace.finish("ok")
    except Exception as e:
        print("[ERROR] {}".format(e))
        trace.finish("error")
        send_telegram("שגיאה בשליחת הפקודה: {}".format(e))


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
