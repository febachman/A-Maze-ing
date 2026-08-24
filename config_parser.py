#!/usr/bin/env python3

def read_config(filepath):
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            key, value = line.split("=")

            if key == "WIDTH":
                config[key] = int(value)
            elif key == "HEIGHT":
                config[key] = int(value)
            elif key == "ENTRY" or key == "EXIT":
                x, y = value.split(",")
                config[key] = (int(x), int(y))
            elif key == "PERFECT":
                config[key] = (value == "True")
            else:
                config[key] = value
    req_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT"]
    for req in req_keys:
        if req not in config:
            print("Error: Missing key", req)
            exit(1)
    return config
