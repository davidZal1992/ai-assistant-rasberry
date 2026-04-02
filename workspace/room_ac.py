#!/usr/bin/env python3
"""Room AC controller - Gree/EWPE Smart (חדר ילדים + חדר שינה)."""
import asyncio, json, sys

KEY_FILE = "/home/david/.picoclaw/workspace/room_ac_keys.json"

MODE_MAP = {
    "auto": 0, "cool": 1, "cold": 1, "heat": 4, "hot": 4,
    "dry": 2, "wet": 2, "fan": 3, "wind": 3,
    "קר": 1, "חם": 4, "קריר": 1, "אוטו": 0,
}
FAN_MAP  = {
    "auto": 0, "low": 1, "נמוך": 1,
    "medium": 2, "middle": 2, "בינוני": 2,
    "high": 3, "גבוה": 3,
}
MODES_STR = {0:"auto", 1:"cool", 2:"dry", 3:"fan", 4:"heat"}
FANS_STR  = {0:"auto", 1:"low",  2:"medium", 3:"high"}

def load_keys():
    with open(KEY_FILE) as f:
        return json.load(f)

async def get_device(d):
    from greeclimate.device import Device
    from greeclimate.discovery import DeviceInfo
    from greeclimate.cipher import CipherV1
    info = DeviceInfo(d["ip"], d["port"], d["mac"], d["name"])
    dev = Device(info)
    await dev.bind(key=d["key"], cipher=CipherV1())
    dev._transport, _ = await dev._loop.create_datagram_endpoint(
        lambda: dev, remote_addr=(d["ip"], d["port"])
    )
    await dev.update_state()
    await asyncio.wait_for(dev._valid_state.wait(), timeout=5)
    return dev

async def _run(room_key, action):
    rooms = load_keys()
    if room_key == "all":
        devs = [(await get_device(rooms[k]), rooms[k]["name"]) for k in rooms]
        await asyncio.gather(*[action(dev, name) for dev, name in devs])
    elif room_key in rooms:
        dev = await get_device(rooms[room_key])
        await action(dev, rooms[room_key]["name"])
    else:
        print(f"Unknown room: {room_key}. Use: ילדים / שינה / all")

def run(room_key, action):
    asyncio.run(_run(room_key, action))

# ── Commands ────────────────────────────────────────────────

def ac_on(room):
    async def _a(dev, name):
        dev.power = True
        await dev.push_state_update()
        print(f"{name}: ON")
    run(room, _a)

def ac_off(room):
    async def _a(dev, name):
        dev.power = False
        await dev.push_state_update()
        print(f"{name}: OFF")
    run(room, _a)

def ac_temp(room, temp):
    temp = int(temp)
    if not 16 <= temp <= 32:
        print("temp must be 16-32"); return
    async def _a(dev, name):
        dev.target_temperature = temp
        await dev.push_state_update()
        print(f"{name}: TEMP {temp}C")
    run(room, _a)

def ac_mode(room, mode):
    m = MODE_MAP.get(mode.lower())
    if m is None:
        print(f"Unknown mode: {mode}. Use: auto/cool/heat/dry/fan"); return
    async def _a(dev, name):
        dev.mode = m
        await dev.push_state_update()
        print(f"{name}: MODE {mode}")
    run(room, _a)

def ac_fan(room, speed):
    s = FAN_MAP.get(speed.lower())
    if s is None:
        print(f"Unknown fan speed: {speed}. Use: auto/low/medium/high"); return
    async def _a(dev, name):
        dev.fan_speed = s
        await dev.push_state_update()
        print(f"{name}: FAN {speed}")
    run(room, _a)

def ac_status(room):
    async def _a(dev, name):
        state = "ON" if dev.power else "OFF"
        print(f"{name}: {state}  temp={dev.target_temperature}C  mode={MODES_STR.get(dev.mode,'?')}  fan={FANS_STR.get(dev.fan_speed,'?')}")
    run(room, _a)

# ── CLI ─────────────────────────────────────────────────────

ROOM_ALIASES = {
    "ילדים": "ילדים", "kids": "ילדים",
    "שינה": "שינה", "bedroom": "שינה",
    "all": "all", "הכל": "all",
}

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: room_ac.py <room> <cmd> [value]")
        print("  room: ילדים / שינה / all")
        print("  cmd:  on / off / status / temp N / mode M / fan S")
        return

    room = ROOM_ALIASES.get(args[0], args[0])
    cmd  = args[1].lower()
    val  = args[2] if len(args) > 2 else None

    if   cmd == "on":            ac_on(room)
    elif cmd == "off":           ac_off(room)
    elif cmd == "status":        ac_status(room)
    elif cmd == "temp" and val:  ac_temp(room, val)
    elif cmd == "mode" and val:  ac_mode(room, val)
    elif cmd == "fan"  and val:  ac_fan(room, val)
    else: print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
