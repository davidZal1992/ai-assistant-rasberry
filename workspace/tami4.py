#!/usr/bin/env python3
"""Tami4 Edge Water Dispenser Controller."""
import sys
import json
import re
import os
import time
import requests

TOKEN_FILE = "/home/david/.picoclaw/workspace/tami4_token.json"
BASE_AUTH = "https://authentication-prod.strauss-group.com"
BASE_API = "https://swelcustomers.strauss-water.com"
API_KEY = "96787682-rrzh-0995-v9sz-cfdad9ac7072"
DEVICE_ID = "50230711505"
PSN = "50230711505"

# Drink IDs from device config
DRINKS = {
    "coffee":    {"id": "762e1eaf-46fd-4b40-a37e-9c3cc42c669c", "name": "קפה",        "vol": "251ml"},
    "קפה":       {"id": "762e1eaf-46fd-4b40-a37e-9c3cc42c669c", "name": "קפה",        "vol": "251ml"},
    "bottle":    {"id": "fb9519ee-994d-4655-8717-6ff26b2af98e", "name": "בקבוק",      "vol": "306ml"},
    "בקבוק":     {"id": "fb9519ee-994d-4655-8717-6ff26b2af98e", "name": "בקבוק",      "vol": "306ml"},
    "cold":      {"id": "56ea8ab2-d7fd-410a-9f4c-892c3eecf52f", "name": "ליטר וחצי",  "vol": "1234ml"},
    "ליטר":      {"id": "56ea8ab2-d7fd-410a-9f4c-892c3eecf52f", "name": "ליטר וחצי",  "vol": "1234ml"},
    "קנקן-קר":  {"id": "56ea8ab2-d7fd-410a-9f4c-892c3eecf52f", "name": "ליטר וחצי",  "vol": "1234ml"},
    "teapot":    {"id": "1070d1c2-ee5c-45bf-88ce-dcd2e76f7d14", "name": "קנקן חם",    "vol": "1205ml"},
    "קנקן":      {"id": "1070d1c2-ee5c-45bf-88ce-dcd2e76f7d14", "name": "קנקן חם",    "vol": "1205ml"},
    "קנקן-חם":  {"id": "1070d1c2-ee5c-45bf-88ce-dcd2e76f7d14", "name": "קנקן חם",    "vol": "1205ml"},
    "hot":       {"id": "1070d1c2-ee5c-45bf-88ce-dcd2e76f7d14", "name": "קנקן חם",    "vol": "1205ml"},
}

def load_tokens():
    """Load saved tokens. Returns dict with refresh_token, access_token, expires_at."""
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_tokens(data):
    """Save tokens — NEVER saves null values over existing ones."""
    existing = load_tokens()
    # Only update fields that have actual values
    for key in ["refresh_token", "access_token", "expires_at"]:
        if key in data and data[key] is not None:
            existing[key] = data[key]
    with open(TOKEN_FILE, "w") as f:
        json.dump(existing, f, indent=2)

def get_access_token():
    """Get a valid access token, refreshing if needed."""
    tokens = load_tokens()
    
    # Check if we have a cached access token that's still valid
    access_token = tokens.get("access_token")
    expires_at = tokens.get("expires_at", 0)
    if access_token and time.time() < expires_at - 60:  # 60s buffer
        return access_token
    
    # Need to refresh
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("ERROR: No refresh token. Run: python3 /tmp/tami4_auth2.py to re-authenticate")
        return None
    
    r = requests.post(f"{BASE_AUTH}/api/v1/auth/token/refresh",
        headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
        json={"refreshToken": refresh_token},
        timeout=10)
    
    if r.status_code != 200:
        print(f"Auth refresh failed: {r.status_code} {r.text}")
        print("Token may have expired. Run: python3 /tmp/tami4_auth2.py to re-authenticate")
        return None
    
    data = r.json()
    new_access = data.get("accessToken")
    new_refresh = data.get("refreshToken")
    
    # Save tokens — only update what we got back
    save_data = {"access_token": new_access}
    if new_access:
        # Access tokens typically last 24h, cache for 23h
        save_data["expires_at"] = time.time() + 82800
    if new_refresh:
        save_data["refresh_token"] = new_refresh
    save_tokens(save_data)
    
    return new_access

def api_headers():
    token = get_access_token()
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

# ── Commands ───────────────────────────────────────────────

def tami_boil():
    """Start boiling water."""
    headers = api_headers()
    if not headers: return
    r = requests.post(f"{BASE_API}/api/v1/device/{DEVICE_ID}/startBoiling", headers=headers, timeout=10)
    if r.status_code == 200:
        print("Tami4: BOILING WATER 🔥")
    elif r.status_code == 502:
        print("Tami4: כבר מרתיח מים")
    else:
        print(f"Tami4: Error {r.status_code} - {r.text}")

def tami_drink(drink_key):
    """Prepare a drink."""
    drink_key_lower = drink_key.lower()
    if drink_key_lower not in DRINKS:
        print(f"משקה לא מוכר: {drink_key}")
        print("משקאות זמינים: coffee/קפה, bottle/בקבוק, cold/ליטר, teapot/קנקן-חם")
        return
    drink = DRINKS[drink_key_lower]
    headers = api_headers()
    if not headers: return
    r = requests.post(f"{BASE_API}/api/v1/device/{DEVICE_ID}/prepareDrink/{drink['id']}", headers=headers, timeout=10)
    if r.status_code == 200:
        print(f"Tami4: PREPARING {drink['name']} ({drink['vol']}) ☕")
    else:
        print(f"Tami4: Error {r.status_code} - {r.text}")

def tami_status():
    """Get device status."""
    headers = api_headers()
    if not headers: return
    r = requests.get(f"{BASE_API}/api/v3/customer/mainPage/{PSN}", headers=headers, timeout=10)
    if r.status_code != 200:
        print(f"Tami4: Error {r.status_code}")
        return
    data = r.json()
    device = data.get("device", {})
    dynamic = data.get("dynamicData", {})
    connected = "מחובר ✅" if dynamic.get("connected") else "מנותק ❌"
    
    print(f"Tami4 Edge: {connected}")
    print(f"  firmware: {device.get('deviceFirmware', '?')}")
    
    filt = dynamic.get("filterInfo", {})
    if filt:
        liters = filt.get("milliLittersPassed", 0) / 1000
        print(f"  filter: {liters:.1f}L passed")
        replacement = filt.get("upcomingReplacement")
        if replacement:
            from datetime import datetime
            dt = datetime.fromtimestamp(replacement / 1000)
            print(f"  filter replacement: {dt.strftime('%Y-%m-%d')}")
    
    uv = dynamic.get("uvInfo", {})
    if uv:
        replacement = uv.get("upcomingReplacement")
        if replacement:
            from datetime import datetime
            dt = datetime.fromtimestamp(replacement / 1000)
            print(f"  UV replacement: {dt.strftime('%Y-%m-%d')}")
    
    drinks = data.get("drinks", [])
    if drinks:
        print("  drinks:")
        for d in drinks:
            vol = d.get("settings", {}).get("volume", "?")
            print(f"    - {d['name']} ({vol}ml)")

def tami_drinks():
    """List available drinks."""
    headers = api_headers()
    if not headers: return
    r = requests.get(f"{BASE_API}/api/v3/customer/mainPage/{PSN}", headers=headers, timeout=10)
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return
    drinks = r.json().get("drinks", [])
    print("משקאות זמינים:")
    for d in drinks:
        vol = d.get("settings", {}).get("volume", "?")
        print(f"  ☕ {d['name']} — {vol}ml")

# ── CLI Router ─────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: tami4.py <command> [value]")
        print("  boil              — start boiling water")
        print("  drink <name>      — prepare a drink (coffee/bottle/cold/teapot)")
        print("  status            — device status & water quality")
        print("  drinks            — list available drinks")
        return

    cmd = args[0].lower()
    val = args[1] if len(args) > 1 else None

    if cmd in ("boil", "רתיחה", "הרתח", "חם"):
        tami_boil()
    elif cmd in ("drink", "משקה", "הכן") and val:
        tami_drink(val)
    elif cmd in ("coffee", "קפה"):
        tami_drink("coffee")
    elif cmd in ("bottle", "בקבוק"):
        tami_drink("bottle")
    elif cmd in ("teapot", "קנקן", "קנקן-חם"):
        tami_drink("teapot")
    elif cmd in ("cold", "ליטר", "קנקן-קר"):
        tami_drink("cold")
    elif cmd in ("status", "סטטוס", "מצב"):
        tami_status()
    elif cmd in ("drinks", "משקאות"):
        tami_drinks()
    else:
        print(f"פקודה לא מוכרת: {cmd}")

if __name__ == "__main__":
    main()
