import os

INIT_MAP = "モノル_F2"

MAPS = [INIT_MAP]
files = os.listdir("maps")
for file in files:
    if INIT_MAP != file:
        MAPS.append(file.replace('.json', ''))

DEBUG_MAPS = [
    {
        "name": "モノル_F2",
        "to": (260, 416),
    },
    {
        "name": "モノル_F1",
        "to": (480, 864),
    },
    {
        "name": "モノル_BF1",
        "to": (32, 64),
    },
    {
        "name": "初期の島",
        "to": (800, 512),
    },
    {
        "name": "北の島",
        "to": (800, 960),
    },
    {
        "name": "港の島",
        "to": (192, 192),
    },
    {
        "name": "テスト",
        "to": (32, 32),
    },
    {
        "name": "テスト2",
        "to": (120, 120),
    },
]

RAIN_LEN = 500