#!/usr/bin/env python3
import sys
import tinytuya

DEVICE_ID = "bf70c8d565b5d4f7b04zes"
ACCESS_ID = "fkn8ptfcpe9ycydjxscc"
ACCESS_SECRET = "400eb062d33a4a5ba22542e75e11331e"

cloud = tinytuya.Cloud(
    apiRegion="eu",
    apiKey=ACCESS_ID,
    apiSecret=ACCESS_SECRET
)

command = sys.argv[1] if len(sys.argv) > 1 else "status"

if command == "on":
    result = cloud.sendcommand(DEVICE_ID, {"commands": [{"code": "switch_1", "value": True}]})
    print(f"Boiler turned ON: {result}")
elif command == "off":
    result = cloud.sendcommand(DEVICE_ID, {"commands": [{"code": "switch_1", "value": False}]})
    print(f"Boiler turned OFF: {result}")
elif command == "status":
    result = cloud.getstatus(DEVICE_ID)
    print(f"Boiler status: {result}")
else:
    print(f"Unknown command: {command}. Use: on, off, status")
