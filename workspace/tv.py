#!/usr/bin/env python3
"""LG TV controller - part of smarthome suite."""
import asyncio
import json
import sys
import subprocess

TV_IP = "192.168.31.200"
KEY_FILE     = "/home/david/.picoclaw/workspace/tv_key.json"
CELLCOM_HDMI = "com.webos.app.hdmi1"  # Cellcom TV box is on HDMI 1

def load_key():
    try:
        with open(KEY_FILE) as f:
            return json.load(f).get("client_key")
    except:
        return None

async def _run(action):
    from aiowebostv import WebOsClient
    key = load_key()
    client = WebOsClient(TV_IP, client_key=key)
    connected = False
    try:
        await asyncio.wait_for(client.connect(), timeout=2)
        connected = True
        result = await action(client)
        return result
    finally:
        if connected:
            await client.disconnect()

def run(action):
    return asyncio.run(_run(action))

def run_safe(action, off_msg="TV already off or unreachable"):
    """Like run() but returns None instead of crashing if TV is unreachable."""
    try:
        return run(action)
    except Exception:
        if off_msg is not None:
            print(off_msg)
        return None

# ── Commands ───────────────────────────────────────────────

def tv_on():
    """Turn TV on via Wake-on-LAN."""
    import subprocess
    # Get TV MAC first
    try:
        with open(KEY_FILE) as f:
            d = json.load(f)
        mac = d.get("mac")
        if mac:
            subprocess.run(["wakeonlan", mac], capture_output=True)
            print("TV ON (WoL sent)")
            return
    except: pass
    # Fallback: try WebSocket power on (works if TV in standby)
    async def _on(c):
        await c.turn_on()
    try:
        run(_on)
        print("TV ON")
    except:
        print("TV ON signal sent (TV may need WoL - see setup)")

def tv_off():
    async def _off(c):
        await c.power_off()
    result = run_safe(_off, None)
    if result is None:
        print("TV OFF (already off or unreachable)")
    else:
        print("TV OFF")

def tv_volume(val):
    val = int(val)
    async def _vol(c):
        await c.set_volume(val)
    run(_vol)
    print("VOLUME " + str(val))

def tv_volume_up():
    async def _up(c):
        await c.volume_up()
    run(_up)
    print("VOLUME UP")

def tv_volume_down():
    async def _down(c):
        await c.volume_down()
    run(_down)
    print("VOLUME DOWN")

def tv_mute():
    async def _mute(c):
        vol = await c.get_volume()
        muted = vol.get("muted", False) if isinstance(vol, dict) else False
        await c.set_mute(not muted)
        return not muted
    result = run(_mute)
    print("MUTE ON" if result else "MUTE OFF")

def tv_app(app_name):
    APP_MAP = {
        "netflix":    "netflix",
        "youtube":    "youtube.leanback.v4",
        "spotify":    "spotify-beehive",
        "prime":      "amazon",
        "primevideo": "amazon",
        "disney":     "disneyplus",
        "apple":      "com.apple.tv",
        "hdmi1":      "com.webos.app.hdmi1",
        "hdmi2":      "com.webos.app.hdmi2",
        "hdmi3":      "com.webos.app.hdmi3",
        "hdmi4":      "com.webos.app.hdmi4",
        "live":       "com.webos.app.livetv",
        "livetv":     "com.webos.app.livetv",
        # Cellcom TV aliases — all map to HDMI 1
        "cellcom":    "com.webos.app.hdmi1",
        "cellcom-tv": "com.webos.app.hdmi1",
        "סלקום":      "com.webos.app.hdmi1",
        "cable":      "com.webos.app.hdmi1",
    }
    app_id = APP_MAP.get(app_name.lower(), app_name)
    async def _app(c):
        await c.launch_app(app_id)
    run(_app)
    print("LAUNCHED " + app_name)

async def _ensure_cellcom(c):
    """Switch to HDMI 1 (Cellcom) if not already there."""
    current = await c.get_current_app()
    if current != CELLCOM_HDMI:
        await c.launch_app(CELLCOM_HDMI)
        await asyncio.sleep(2)

def tv_channel_up():
    async def _ch(c):
        await _ensure_cellcom(c)
        await c.button("CHANNELUP")
    run(_ch)
    print("CHANNEL UP (Cellcom)")

def tv_channel_down():
    async def _ch(c):
        await _ensure_cellcom(c)
        await c.button("CHANNELDOWN")
    run(_ch)
    print("CHANNEL DOWN (Cellcom)")

def tv_channel(num):
    """Switch to Cellcom (HDMI 1) and dial channel number digit by digit."""
    async def _ch(c):
        await _ensure_cellcom(c)
        for digit in str(num):
            await c.button(digit)
            await asyncio.sleep(0.4)
    run(_ch)
    print("CHANNEL " + str(num) + " (Cellcom)")

def tv_input(src):
    INPUT_MAP = {
        "hdmi1": "com.webos.app.hdmi1",
        "hdmi2": "com.webos.app.hdmi2",
        "hdmi3": "com.webos.app.hdmi3",
        "hdmi4": "com.webos.app.hdmi4",
    }
    app_id = INPUT_MAP.get(src.lower(), "com.webos.app.hdmi1")
    async def _inp(c):
        await c.launch_app(app_id)
    run(_inp)
    print("INPUT " + src)

def tv_status():
    async def _status(c):
        vol   = await c.get_volume()
        power = await c.get_power_state()
        app   = await c.get_current_app()
        return vol, power, app
    try:
        vol, power, app = run(_status)
        state = power.get("state", "?") if isinstance(power, dict) else str(power)
        print("TV status: " + state)
        print("  volume: " + str(vol))
        print("  app: " + str(app))
    except Exception as e:
        print("TV status: OFF or unreachable (" + str(e) + ")")

def tv_key(key_name):
    """Send a remote control button."""
    KEY_MAP = {
        "back":     "BACK",
        "home":     "HOME",
        "ok":       "ENTER",
        "up":       "UP",
        "down":     "DOWN",
        "left":     "LEFT",
        "right":    "RIGHT",
        "play":     "PLAY",
        "pause":    "PAUSE",
        "stop":     "STOP",
        "forward":  "FASTFORWARD",
        "rewind":   "REWIND",
    }
    button = KEY_MAP.get(key_name.lower(), key_name.upper())
    async def _key(c):
        await c.button(button)
    run(_key)
    print("KEY " + button)

# ── CLI Router ─────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: tv.py <command> [value]")
        print("  on/off/status")
        print("  volume <0-100> / up / down / mute")
        print("  app <netflix|youtube|spotify|hdmi1|hdmi2|livetv>")
        print("  channel up / down / <number>")
        print("  key <back|home|ok|play|pause|up|down>")
        return

    cmd = args[0].lower()
    val = args[1] if len(args) > 1 else None

    if cmd == "on":           tv_on()
    elif cmd == "off":        tv_off()
    elif cmd == "status":     tv_status()
    elif cmd == "mute":       tv_mute()
    elif cmd == "volume":
        if val in ("up", "העלה"):   tv_volume_up()
        elif val in ("down", "הנמך"): tv_volume_down()
        elif val:                     tv_volume(val)
        else: print("volume needs a value: up / down / 0-100")
    elif cmd in ("up", "העלה"):    tv_volume_up()
    elif cmd in ("down", "הנמך"):  tv_volume_down()
    elif cmd == "app" and val:    tv_app(val)
    elif cmd == "channel":
        if val in ("up", "למעלה"):    tv_channel_up()
        elif val in ("down", "למטה"): tv_channel_down()
        elif val:                      tv_channel(val)
        else: print("channel needs: up / down / <number>")
    elif cmd in ("channel+", "ch+"):  tv_channel_up()
    elif cmd in ("channel-", "ch-"):  tv_channel_down()
    elif cmd == "input" and val:  tv_input(val)
    elif cmd == "key" and val:    tv_key(val)
    else: print("unknown tv command: " + cmd)

if __name__ == "__main__":
    main()