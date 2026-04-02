#!/usr/bin/env python3
"""Smart Bulb Controller - Controls Tuya/Smart Life RGB bulbs (children room + parents room)."""
import sys
import json
import tinytuya

# ── Device Config ──────────────────────────────────────────
TUYA_API_KEY    = "fkn8ptfcpe9ycydjxscc"
TUYA_API_SECRET = "400eb062d33a4a5ba22542e75e11331e"
TUYA_REGION     = "eu"

# TODO: Update these device IDs and local keys after renewing Tuya Cloud plan
# Device IDs found via network scan:
#   192.168.31.160 = bf329bcc5fa941704bp17h (v3.5)
#   192.168.31.148 = bfe79bdf3b20826fa86zcu (v3.5)
# Assign which is children vs parents after identifying them

DEVICES = {
    "parents": {
        "name": "נורה חדר הורים",
        "id":   "bf329bcc5fa941704bp17h",
        "ip":   "192.168.31.160",
        "ver":  "3.5",
    },
    "children": {
        "name": "נורה חדר ילדים",
        "id":   "bfe79bdf3b20826fa86zcu",
        "ip":   "192.168.31.148",
        "ver":  "3.5",
    },
}

# ── Color Presets (HSV: hue 0-360, saturation 0-1000, value/brightness 0-1000) ──
COLORS = {
    # Basic colors
    "red":     {"h": 0,   "s": 1000, "v": 1000},
    "אדום":    {"h": 0,   "s": 1000, "v": 1000},
    "orange":  {"h": 30,  "s": 1000, "v": 1000},
    "כתום":    {"h": 30,  "s": 1000, "v": 1000},
    "yellow":  {"h": 60,  "s": 1000, "v": 1000},
    "צהוב":    {"h": 60,  "s": 1000, "v": 1000},
    "green":   {"h": 120, "s": 1000, "v": 1000},
    "ירוק":    {"h": 120, "s": 1000, "v": 1000},
    "cyan":    {"h": 180, "s": 1000, "v": 1000},
    "תכלת":   {"h": 180, "s": 1000, "v": 1000},
    "blue":    {"h": 240, "s": 1000, "v": 1000},
    "כחול":    {"h": 240, "s": 1000, "v": 1000},
    "purple":  {"h": 270, "s": 1000, "v": 1000},
    "סגול":    {"h": 270, "s": 1000, "v": 1000},
    "pink":    {"h": 330, "s": 800,  "v": 1000},
    "ורוד":    {"h": 330, "s": 800,  "v": 1000},
    "white":   {"h": 0,   "s": 0,    "v": 1000},
    "לבן":     {"h": 0,   "s": 0,    "v": 1000},
    # Mood colors
    "warm":       {"h": 30,  "s": 600, "v": 800},
    "חם":         {"h": 30,  "s": 600, "v": 800},
    "cool":       {"h": 210, "s": 400, "v": 900},
    "קריר":       {"h": 210, "s": 400, "v": 900},
    "lavender":   {"h": 270, "s": 400, "v": 800},
    "לבנדר":      {"h": 270, "s": 400, "v": 800},
    "coral":      {"h": 16,  "s": 800, "v": 1000},
    "אלמוג":      {"h": 16,  "s": 800, "v": 1000},
    "mint":       {"h": 150, "s": 600, "v": 900},
    "מנטה":       {"h": 150, "s": 600, "v": 900},
    "gold":       {"h": 45,  "s": 900, "v": 1000},
    "זהב":        {"h": 45,  "s": 900, "v": 1000},
    "turquoise":  {"h": 170, "s": 800, "v": 900},
    "טורקיז":     {"h": 170, "s": 800, "v": 900},
}

# ── Scene Presets ──────────────────────────────────────────
# scene_data format: "AABBCCDDEEFFGGHHaabbccdd" where:
#   AA=scene number, BB=change mode (00=static, 01=jump, 02=gradient)
#   CC=speed, then groups of HHHHSSSSBBBB (HSV values)
SCENES = {
    "night":      "night_light",
    "לילה":       "night_light",
    "nightlight": "night_light",
    "אור-לילה":  "night_light",
    "reading":    "reading",
    "קריאה":      "reading",
    "relax":      "relax",
    "רגוע":       "relax",
    "רגיעה":      "relax",
    "party":      "party",
    "מסיבה":      "party",
    "romance":    "romance",
    "רומנטיקה":   "romance",
    "רומנטי":     "romance",
    "focus":      "focus",
    "ריכוז":      "focus",
    "energy":     "energy",
    "אנרגיה":     "energy",
    "sleep":      "sleep",
    "שינה":       "sleep",
    "rainbow":    "rainbow",
    "קשת":        "rainbow",
}

# Scene implementations (scene_data_v2 format)
SCENE_DATA = {
    "night_light": {"brightness": 50,  "temp": 1000, "mode": "white"},
    "reading":     {"brightness": 900, "temp": 500,  "mode": "white"},
    "relax":       {"brightness": 400, "temp": 800,  "mode": "white"},
    "party":       {"brightness": 1000, "mode": "colour", "colors": [
        {"h": 0, "s": 1000, "v": 1000}, {"h": 120, "s": 1000, "v": 1000},
        {"h": 240, "s": 1000, "v": 1000}, {"h": 60, "s": 1000, "v": 1000},
    ]},
    "romance":     {"brightness": 300, "mode": "colour", "colors": [
        {"h": 330, "s": 700, "v": 600}, {"h": 0, "s": 800, "v": 500},
        {"h": 270, "s": 500, "v": 400},
    ]},
    "focus":       {"brightness": 1000, "temp": 200, "mode": "white"},
    "energy":      {"brightness": 1000, "temp": 0,   "mode": "white"},
    "sleep":       {"brightness": 30,   "temp": 1000, "mode": "white"},
    "rainbow":     {"brightness": 1000, "mode": "colour", "colors": [
        {"h": 0, "s": 1000, "v": 1000}, {"h": 60, "s": 1000, "v": 1000},
        {"h": 120, "s": 1000, "v": 1000}, {"h": 180, "s": 1000, "v": 1000},
        {"h": 240, "s": 1000, "v": 1000}, {"h": 300, "s": 1000, "v": 1000},
    ]},
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

def resolve_room(room_arg):
    """Resolve room aliases to device key."""
    aliases = {
        "ילדים": "children", "children": "children", "kids": "children",
        "חדר-ילדים": "children", "ילד": "children",
        "הורים": "parents", "parents": "parents", "parent": "parents",
        "חדר-הורים": "parents", "שינה": "parents", "bedroom": "parents",
        "חדר-שינה": "parents", "master": "parents",
        "all": "all", "הכל": "all", "כל": "all", "שני": "all", "שתי": "all",
    }
    return aliases.get(room_arg.lower(), room_arg.lower())

def get_targets(room_key):
    """Return list of device keys to act on."""
    if room_key == "all":
        return ["children", "parents"]
    if room_key in DEVICES:
        return [room_key]
    print(f"חדר לא מוכר: {room_key}. השתמש ב: ילדים / הורים / all")
    return []

# ── Commands ───────────────────────────────────────────────

def bulb_on(room):
    for key in get_targets(room):
        cloud_send(key, [{"code": "switch_led", "value": True}])
        print(f"{DEVICES[key]['name']}: ON ✅")

def bulb_off(room):
    for key in get_targets(room):
        cloud_send(key, [{"code": "switch_led", "value": False}])
        print(f"{DEVICES[key]['name']}: OFF ✅")

def bulb_brightness(room, level):
    """Set brightness 1-100 (mapped to 10-1000). Preserves current color/mode."""
    level = int(level)
    if not 1 <= level <= 100:
        print("בהירות חייבת להיות בין 1 ל-100"); return
    value = max(10, level * 10)
    for key in get_targets(room):
        # Check current mode to preserve color if in colour mode
        try:
            result = cloud_status(key)
            dps = {s["code"]: s["value"] for s in result.get("result", [])}
            current_mode = dps.get("work_mode", "white")
        except:
            current_mode = "white"
        
        if current_mode == "colour":
            # In colour mode, adjust brightness via HSV value
            try:
                import json as _json
                colour = dps.get("colour_data_v2", "")
                if isinstance(colour, str) and colour:
                    hsv = _json.loads(colour)
                else:
                    hsv = colour if isinstance(colour, dict) else {"h": 0, "s": 1000, "v": 1000}
                hsv["v"] = value
                cloud_send(key, [
                    {"code": "switch_led", "value": True},
                    {"code": "work_mode", "value": "colour"},
                    {"code": "colour_data_v2", "value": hsv},
                ])
            except:
                cloud_send(key, [
                    {"code": "switch_led", "value": True},
                    {"code": "bright_value_v2", "value": value},
                ])
        else:
            cloud_send(key, [
                {"code": "switch_led", "value": True},
                {"code": "bright_value_v2", "value": value},
            ])
        print(f"{DEVICES[key]['name']}: BRIGHTNESS {level}%")

def bulb_temp(room, temp):
    """Set color temperature: warm (0) to cool (100), or keywords."""
    temp_map = {
        "warm": 100, "חם": 100, "חמים": 100,
        "neutral": 50, "ניטרלי": 50, "טבעי": 50, "natural": 50,
        "cool": 0, "קריר": 0, "קרירה": 0, "קר": 0,
        "daylight": 0, "אור-יום": 0,
        "candle": 100, "נר": 100,
    }
    if temp.lower() in temp_map:
        pct = temp_map[temp.lower()]
    else:
        pct = int(temp)
    if not 0 <= pct <= 100:
        print("טמפרטורת צבע: 0 (קריר) עד 100 (חם)"); return
    value = pct * 10  # 0-1000
    for key in get_targets(room):
        cloud_send(key, [
            {"code": "switch_led", "value": True},
            {"code": "work_mode", "value": "white"},
            {"code": "temp_value_v2", "value": value},
        ])
        label = "חם 🔥" if pct > 60 else "קריר ❄️" if pct < 40 else "ניטרלי"
        print(f"{DEVICES[key]['name']}: TEMP {pct}% ({label})")

def bulb_color(room, color_name, brightness=None):
    """Set color by name or HSV, with optional brightness (1-100)."""
    color_name_lower = color_name.lower()
    if color_name_lower in COLORS:
        hsv = dict(COLORS[color_name_lower])  # copy to avoid mutating preset
    else:
        print(f"צבע לא מוכר: {color_name}")
        print("צבעים זמינים: " + ", ".join(
            k for k in COLORS if not any(c in k for c in "אבגדהוזחטיכלמנסעפצקרשת")))
        print("בעברית: " + ", ".join(
            k for k in COLORS if any(c in k for c in "אבגדהוזחטיכלמנסעפצקרשת")))
        return

    if brightness is not None:
        hsv["v"] = max(10, int(brightness) * 10)

    for key in get_targets(room):
        cloud_send(key, [
            {"code": "switch_led", "value": True},
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data_v2", "value": hsv},
        ])
        brt_str = f" ({brightness}%)" if brightness else ""
        print(f"{DEVICES[key]['name']}: COLOR {color_name}{brt_str} 🎨")

def bulb_hsv(room, h, s, v):
    """Set exact HSV color: h=0-360, s=0-100, v=0-100."""
    h, s, v = int(h), int(s), int(v)
    hsv = {"h": h, "s": s * 10, "v": v * 10}
    for key in get_targets(room):
        cloud_send(key, [
            {"code": "switch_led", "value": True},
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data_v2", "value": hsv},
        ])
        print(f"{DEVICES[key]['name']}: HSV h={h} s={s} v={v}")

def bulb_mode(room, mode):
    """Set work mode: white / colour / scene / music."""
    valid = ["white", "colour", "scene", "music"]
    mode_map = {"לבן": "white", "צבע": "colour", "סצנה": "scene", "מוזיקה": "music",
                "color": "colour", "rgb": "colour"}
    mode = mode_map.get(mode.lower(), mode.lower())
    if mode not in valid:
        print(f"מצבים: white / colour / scene / music"); return
    for key in get_targets(room):
        cloud_send(key, [{"code": "work_mode", "value": mode}])
        print(f"{DEVICES[key]['name']}: MODE {mode}")

def bulb_scene(room, scene_name):
    """Apply a scene preset."""
    scene_name_lower = scene_name.lower()
    scene_key = SCENES.get(scene_name_lower)
    if not scene_key:
        print(f"סצנה לא מוכרת: {scene_name}")
        print("סצנות זמינות: " + ", ".join(
            k for k in SCENES if not any(c in k for c in "אבגדהוזחטיכלמנסעפצקרשת")))
        print("בעברית: " + ", ".join(
            k for k in SCENES if any(c in k for c in "אבגדהוזחטיכלמנסעפצקרשת")))
        return

    scene = SCENE_DATA[scene_key]
    for key in get_targets(room):
        commands = [{"code": "switch_led", "value": True}]
        if scene["mode"] == "white":
            commands.append({"code": "work_mode", "value": "white"})
            commands.append({"code": "bright_value_v2", "value": scene["brightness"]})
            if "temp" in scene:
                commands.append({"code": "temp_value_v2", "value": scene["temp"]})
        elif scene["mode"] == "colour":
            # Set first color; for multi-color scenes use scene mode
            commands.append({"code": "work_mode", "value": "colour"})
            commands.append({"code": "colour_data_v2", "value": scene["colors"][0]})
            commands.append({"code": "bright_value_v2", "value": scene["brightness"]})
        cloud_send(key, commands)
        print(f"{DEVICES[key]['name']}: SCENE {scene_name} 🎭")

def bulb_timer(room, minutes):
    """Set auto-off timer in minutes."""
    try:
        mins = int(minutes)
    except ValueError:
        print("יש להזין מספר דקות"); return
    if not 1 <= mins <= 1440:
        print("טיימר: 1-1440 דקות (24 שעות)"); return
    secs = mins * 60
    for key in get_targets(room):
        cloud_send(key, [{"code": "countdown_1", "value": secs}])
        print(f"{DEVICES[key]['name']}: TIMER {mins} min ⏱️")

def bulb_status(room):
    """Get bulb status."""
    for key in get_targets(room):
        result = cloud_status(key)
        dps = {s["code"]: s["value"] for s in result.get("result", [])}
        on_off = "ON ✅" if dps.get("switch_led") else "OFF ⬛"
        mode = dps.get("work_mode", "?")
        bright = dps.get("bright_value_v2", "?")
        if isinstance(bright, int):
            bright = f"{bright // 10}%"
        temp = dps.get("temp_value_v2", "?")
        colour = dps.get("colour_data_v2", "")
        countdown = dps.get("countdown_1", 0)

        print(f"{DEVICES[key]['name']}: {on_off}")
        print(f"  mode: {mode}")
        print(f"  brightness: {bright}")
        if mode == "white":
            print(f"  color temp: {temp}")
        elif mode == "colour" and colour:
            print(f"  color: {colour}")
        if countdown and countdown > 0:
            print(f"  timer: {countdown // 60} min remaining")

# ── CLI Router ─────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: bulbs.py <room> <command> [value]")
        print("  room:  ילדים / הורים / all")
        print("  commands:")
        print("    on / off / status")
        print("    brightness <1-100>")
        print("    temp <0-100|warm|cool|natural>")
        print("    color <red|blue|green|pink|...>")
        print("    hsv <h> <s> <v>")
        print("    mode <white|colour|scene|music>")
        print("    scene <night|reading|relax|party|romance|focus|sleep|rainbow>")
        print("    timer <minutes>")
        return

    room = resolve_room(args[0])
    cmd  = args[1].lower()
    val  = args[2] if len(args) > 2 else None
    extra = args[3:]

    if cmd in ("on", "הדלק", "הדלקי"):
        bulb_on(room)
        # Shorthand: on red / on 50 / on warm
        if val:
            if val.lower() in COLORS:
                bulb_color(room, val)
            elif val.lower() in SCENES or val.lower() in [v for v in SCENES.values()]:
                bulb_scene(room, val)
            else:
                try:
                    bulb_brightness(room, int(val))
                except ValueError:
                    bulb_temp(room, val)
    elif cmd in ("off", "כבה", "כבי"):
        bulb_off(room)
    elif cmd in ("status", "סטטוס", "מצב"):
        bulb_status(room)
    elif cmd in ("brightness", "בהירות", "עוצמה", "dim") and val:
        bulb_brightness(room, val)
    elif cmd in ("temp", "temperature", "טמפרטורה", "חום-צבע"):
        if val:
            bulb_temp(room, val)
        else:
            print("temp needs a value: 0-100, warm, cool, natural")
    elif cmd in ("color", "colour", "צבע") and val:
        bulb_color(room, val)
    elif cmd == "hsv" and val and len(extra) >= 2:
        bulb_hsv(room, val, extra[0], extra[1])
    elif cmd in ("mode", "מצב-עבודה") and val:
        bulb_mode(room, val)
    elif cmd in ("scene", "סצנה", "תאורה") and val:
        bulb_scene(room, val)
    elif cmd in ("timer", "טיימר", "כיבוי-אוטומטי") and val:
        bulb_timer(room, val)
    # Direct color/scene shortcuts (no "color" keyword needed)
    elif cmd in COLORS:
        bulb_color(room, cmd)
    elif cmd in SCENES:
        bulb_scene(room, cmd)
    else:
        print(f"פקודה לא מוכרת: {cmd}")

if __name__ == "__main__":
    main()
