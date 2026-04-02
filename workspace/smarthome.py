#!/usr/bin/env python3
"""Smart Home Controller - Controls all Tuya devices at home."""
import sys
import time
import tinytuya

# ── Device Config ──────────────────────────────────────────
TUYA_API_KEY    = "fkn8ptfcpe9ycydjxscc"
TUYA_API_SECRET = "400eb062d33a4a5ba22542e75e11331e"
TUYA_REGION     = "eu"

DEVICES = {
    "ac": {
        "name": "מזגן (תדיראן מיני מרכזי)",
        "id":   "bf0253c0c6cfc68b3axws2",
        "key":  "Q!)/=UnczJ]0A/=_",
        "ip":   "192.168.31.230",
        "ver":  "3.3",
    },
    "boiler": {
        "name": "בוילר (Boiler Switch)",
        "id":   "bf70c8d565b5d4f7b04zes",
        "key":  "P8#JW{.8cb]c68c@",
        "ip":   "192.168.31.151",
        "ver":  "3.4",
    },
}

_cloud = None

def get_cloud():
    global _cloud
    if _cloud is None:
        _cloud = tinytuya.Cloud(apiRegion=TUYA_REGION, apiKey=TUYA_API_KEY, apiSecret=TUYA_API_SECRET)
    return _cloud

def cloud_send(device_key, commands):
    return get_cloud().sendcommand(DEVICES[device_key]["id"], {"commands": commands})

def cloud_status(device_key):
    return get_cloud().getstatus(DEVICES[device_key]["id"])

def parse_minutes(val):
    try:
        return int(val)
    except:
        print("יש להזין מספר דקות, למשל: timer 40")
        return None

# ── AC Commands ────────────────────────────────────────────
def ac_on():
    # Send switch together with current mode+temp — some AC WiFi modules require combined command
    result = cloud_status("ac")
    dps = {s["code"]: s["value"] for s in result.get("result", [])}
    commands = [{"code": "switch", "value": True}]
    if dps.get("mode"):
        commands.append({"code": "mode", "value": dps["mode"]})
    if dps.get("temp_set"):
        commands.append({"code": "temp_set", "value": dps["temp_set"]})
    cloud_send("ac", commands)
    print("AC ON")

def ac_off():
    cloud_send("ac", [{"code": "switch", "value": False}])
    print("AC OFF")

def ac_temp(temp):
    temp = int(temp)
    if not 16 <= temp <= 32:
        print("temp must be 16-32"); return
    cloud_send("ac", [{"code": "temp_set", "value": temp}])
    # Wait for Tuya cloud cache to update then read back actual value
    time.sleep(4)
    result = cloud_status("ac")
    actual = next((s["value"] for s in result.get("result", []) if s["code"] == "temp_set"), temp)
    print("TEMP SET " + str(actual) + "C")

def ac_mode(mode):
    valid = ["auto", "cold", "hot", "wet", "wind", "eco"]
    mode_map = {"cool": "cold", "cooling": "cold", "heat": "hot", "heating": "hot",
                "fan": "wind", "dry": "wet", "dehumidify": "wet"}
    mode = mode_map.get(mode.lower(), mode.lower())
    if mode not in valid:
        print("invalid mode: " + str(valid)); return
    cloud_send("ac", [{"code": "mode", "value": mode}])
    print("MODE " + mode)

def ac_fan(speed):
    valid = ["auto", "low", "middle", "high"]
    speed_map = {"medium": "middle", "strong": "high", "quiet": "low", "slow": "low"}
    speed = speed_map.get(speed.lower(), speed.lower())
    if speed not in valid:
        print("invalid fan speed: " + str(valid)); return
    cloud_send("ac", [{"code": "fan_speed_enum", "value": speed}])
    print("FAN " + speed)

def ac_status():
    result = cloud_status("ac")
    dps = {s["code"]: s["value"] for s in result.get("result", [])}
    on_off = "ON" if dps.get("switch") else "OFF"
    temp_c = dps.get("temp_current", 0) / 10 if dps.get("temp_current") is not None else "N/A"
    print("AC status: " + on_off)
    print("  current temp: " + str(temp_c) + "C")
    print("  set temp: " + str(dps.get("temp_set", "N/A")) + "C")
    print("  mode: " + str(dps.get("mode", "N/A")))
    print("  fan: " + str(dps.get("fan_speed_enum", "N/A")))

# ── Boiler Commands ────────────────────────────────────────
def boiler_on():
    cloud_send("boiler", [{"code": "switch_1", "value": True}])
    print("BOILER ON")

def boiler_off():
    cloud_send("boiler", [{"code": "switch_1", "value": False}])
    print("BOILER OFF")

def boiler_timer(minutes):
    mins = parse_minutes(minutes)
    if mins is None: return
    secs = mins * 60
    cloud_send("boiler", [{"code": "switch_1", "value": True}, {"code": "countdown_1", "value": secs}])
    print("BOILER TIMER " + str(mins) + " min")

def boiler_status():
    result = cloud_status("boiler")
    dps = {s["code"]: s["value"] for s in result.get("result", [])}
    on_off = "ON" if dps.get("switch_1") else "OFF"
    power = (dps.get("cur_power", 0) or 0) / 10
    countdown = dps.get("countdown_1", 0)
    print("BOILER status: " + on_off + ", power: " + str(power) + "W")
    if countdown and countdown > 0:
        print("  timer: " + str(countdown // 60) + " min remaining")

# ── CLI Router ─────────────────────────────────────────────
MODE_ALIASES = {
    "heat": "hot", "heating": "hot",
    "cool": "cold", "cooling": "cold",
    "fan": "wind", "dry": "wet"
}

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: smarthome.py <device> <command> [value]")
        print("  ac on/off/status/temp N/mode M/fan S")
        print("  ac on hot 27  (shorthand: on + mode + temp)")
        print("  boiler on/off/status/timer N")
        print("  boiler on 35  (shorthand: on with timer)")
        return

    device = args[0].lower()
    cmd    = args[1].lower() if len(args) > 1 else ""
    val    = args[2] if len(args) > 2 else None
    extra  = args[3:]

    if device == "ac":
        if cmd == "on":
            ac_on()
            # Shorthand: ac on [mode] [temp]
            if val:
                norm = MODE_ALIASES.get(val.lower(), val.lower())
                if norm in ["hot", "cold", "auto", "eco", "wet", "wind"]:
                    ac_mode(norm)
                    if extra:
                        try: ac_temp(int(extra[0]))
                        except: pass
                else:
                    try: ac_temp(int(val))
                    except: pass
        elif cmd == "off":    ac_off()
        elif cmd == "status": ac_status()
        elif cmd == "temp" and val:  ac_temp(val)
        elif cmd == "mode" and val:  ac_mode(val)
        elif cmd == "fan"  and val:  ac_fan(val)
        else: print("unknown ac command: " + cmd)

    elif device in ("boiler", "heater", "dod"):
        if cmd == "on":
            # Shorthand: boiler on 35 = timer 35
            if val:
                try: boiler_timer(int(val))
                except: boiler_on()
            else: boiler_on()
        elif cmd == "off":    boiler_off()
        elif cmd == "status": boiler_status()
        elif cmd == "timer" and val: boiler_timer(val)
        else: print("unknown boiler command: " + cmd)

    elif device == "all" and cmd == "status":
        ac_status()
        print()
        boiler_status()
    else:
        print("unknown device: " + device)

if __name__ == "__main__":
    main()
