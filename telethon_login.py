#!/usr/bin/env python3
"""Two-phase Telethon login - reads OTP from /tmp/tg_code.txt"""
import asyncio, os, sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import API_ID, API_HASH, SESSION, PHONE

CODE_FILE = "/tmp/tg_code.txt"


async def wait_for_file(path, timeout=180):
    """Poll until a file exists and has content. Returns content or None on timeout."""
    for _ in range(timeout):
        if os.path.exists(path):
            content = open(path).read().strip()
            if content:
                return content
        await asyncio.sleep(1)
    return None


async def main():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    try:
        await client.connect()

        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"Already logged in as: {me.first_name} (@{me.username})")
            return

        print(f"Sending code to {PHONE}...")
        await client.send_code_request(PHONE)
        print("CODE SENT to your Telegram app.")
        print(f"Write the code to: {CODE_FILE}")
        print("Waiting for code file...")

        code = await wait_for_file(CODE_FILE)
        if not code:
            print("Timeout waiting for code.")
            sys.exit(1)

        try:
            await client.sign_in(PHONE, code)
        except SessionPasswordNeededError:
            print("2FA enabled - password needed. Write password to /tmp/tg_code.txt")
            os.remove(CODE_FILE)
            pw = await wait_for_file(CODE_FILE)
            if not pw:
                print("Timeout waiting for 2FA password.")
                sys.exit(1)
            await client.sign_in(password=pw)

        me = await client.get_me()
        print(f"Login successful! Logged in as: {me.first_name} (@{me.username})")
        print(f"Session saved to: {SESSION}.session")
        if os.path.exists(CODE_FILE):
            os.remove(CODE_FILE)
    finally:
        await client.disconnect()


asyncio.run(main())
