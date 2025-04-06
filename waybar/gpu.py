#!/usr/bin/env python3
import json
import os

TEMP_PATH = "/sys/class/hwmon/hwmon1/temp1_input"
USAGE_PATH = "/sys/class/hwmon/hwmon1/device/gpu_busy_percent"

def read_int_from_file(path):
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except Exception:
        return None

def main():
    temp_raw = read_int_from_file(TEMP_PATH)
    usage = read_int_from_file(USAGE_PATH)

    if temp_raw is not None:
        temp = temp_raw / 1000
    else:
        temp = None

    if temp is not None and usage is not None:
        status_class = "normal"
        if temp > 80 or usage > 80:
            status_class = "critical"
        return {
            "class": "normal",
            "text": f"GPU {usage}%  {int(temp)}°C"
        }
    else:
        return {
            "text": "GPU: N/A",
            "tooltip": "Error retrieving GPU data.",
            "class": "critical"
        }

if __name__ == "__main__":
    output = main()
    print(json.dumps(output))