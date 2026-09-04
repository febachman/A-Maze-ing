#!/usr/bin/env python3

import typing


def read_config(filepath: str) -> typing.Dict[str, typing.Any]:
    """Read and parse the maze configuration file."""
    config: typing.Dict[str, typing.Any] = {}

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)

            if key == "WIDTH":
                config[key] = int(value)
            elif key == "HEIGHT":
                config[key] = int(value)
            elif key == "ENTRY" or key == "EXIT":
                x, y = value.split(",")
                config[key] = (int(x), int(y))
            elif key == "PERFECT":
                if value not in ("True", "False"):
                    raise ValueError(
                        "PERFECT must be either True or False."
                    )
                config[key] = value == "True"
            elif key == "SEED":
                config[key] = int(value)
            else:
                config[key] = value

    req_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for req in req_keys:
        if req not in config:
            raise ValueError(f"Missing required key {req}")

    return config
