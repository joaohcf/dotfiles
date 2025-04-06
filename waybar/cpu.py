#!/usr/bin/env python3
import json
import os
import time

TEMP_PATH = "/sys/class/hwmon/hwmon2/temp1_input"

def read_int_from_file(path):
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except Exception:
        return None

def read_cpu_times():
    with open("/proc/stat", "r") as f:
        line = f.readline()
    cpu_data = list(map(int, line.split()[1:8]))  # Pega mais campos para melhor precisão
    total = sum(cpu_data)
    idle = cpu_data[3]
    return total, idle

def get_cpu_usage():
    total1, idle1 = read_cpu_times()
    time.sleep(0.1)  # espera 100ms
    total2, idle2 = read_cpu_times()

    total_diff = total2 - total1
    idle_diff = idle2 - idle1

    usage = round(100 * (1 - idle_diff / total_diff))
    return usage

def main():
    temp_raw = read_int_from_file(TEMP_PATH)
    usage = get_cpu_usage()

    if temp_raw is not None:
        temp = temp_raw / 1000
    else:
        temp = None

    if temp is not None:
        status_class = "normal"
        if temp > 80 or usage > 80:
            status_class = "critical"
        return {
            "class": status_class,
            "text": f" {usage}%  {int(temp)}°C"
        }
    else:
        return {
            "text": "CPU: N/A",
            "tooltip": "Error retrieving CPU data.",
            "class": "critical"
        }

if __name__ == "__main__":
    output = main()
    print(json.dumps(output))