#!/usr/bin/env python3
"""One-time LG TV pairing - run once, saves client key for future use."""
import asyncio
import json
from aiowebostv import WebOsClient

TV_IP    = "192.168.31.207"
KEY_FILE = "/home/david/.picoclaw/workspace/tv_key.json"

async def pair():
    print(f"Connecting to LG TV at {TV_IP}...")
    print(">>> A prompt will appear on your TV — click ALLOW <<<")

    client = WebOsClient(TV_IP)
    await client.connect()

    key = client.client_key
    print(f"\nPairing successful! Client key: {key}")

    with open(KEY_FILE, "w") as f:
        json.dump({"ip": TV_IP, "client_key": key}, f)
    print(f"Key saved to {KEY_FILE}")

    # Quick test
    info = await client.get_software_info()
    print(f"TV model: {info.get('model_name', 'unknown')}")
    print(f"WebOS version: {info.get('major_ver', '?')}.{info.get('minor_ver', '?')}")

    await client.disconnect()

asyncio.run(pair())
