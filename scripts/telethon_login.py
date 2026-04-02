#!/usr/bin/env python3
"""Two-phase Telethon login - reads OTP from /tmp/tg_code.txt"""
import asyncio, os, sys, time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID   = 39040426
API_HASH = "6e6ab2a82b7401ab1513729593a86b1d"
SESSION  = "/home/david/smarthome_session"
PHONE    = "+972542020184"
CODE_FILE = "/tmp/tg_code.txt"

async def main():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"Already logged in as: {me.first_name} (@{me.username})")
        await client.disconnect()
        return

    print(f"Sending code to {PHONE}...")
    await client.send_code_request(PHONE)
    print("CODE SENT to your Telegram app.")
    print(f"Write the code to: {CODE_FILE}")
    print("Waiting for code file...")

    # Wait up to 3 minutes for the code file
    for _ in range(180):
        if os.path.exists(CODE_FILE):
            with open(CODE_FILE) as f:
                code = f.read().strip()
            if code:
                break
        time.sleep(1)
    else:
        print("Timeout waiting for code.")
        await client.disconnect()
        sys.exit(1)

    try:
        await client.sign_in(PHONE, code)
    except SessionPasswordNeededError:
        print("2FA enabled - password needed. Write password to /tmp/tg_code.txt")
        os.remove(CODE_FILE)
        for _ in range(180):
            if os.path.exists(CODE_FILE):
                with open(CODE_FILE) as f:
                    pw = f.read().strip()
                if pw:
                    break
            time.sleep(1)
        await client.sign_in(password=pw)

    me = await client.get_me()
    print(f"Login successful! Logged in as: {me.first_name} (@{me.username})")
    print(f"Session saved to: {SESSION}.session")
    os.remove(CODE_FILE)
    await client.disconnect()

asyncio.run(main())