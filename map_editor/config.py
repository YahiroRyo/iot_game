from re import T


SW = 1280
SH = 720

ML = 1
MM = 2
MR = 3
MUP = 4
MDOWN = 4

FPS=60

# ////////////////////////////////////////////////
#
# マップ系
#
# ////////////////////////////////////////////////
MAP_IS_LOAD = True
MAP_NAME = "北の島"
MAP_WIDTH = 32
MAP_HEIGHT = 32
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 1
MAP_CONF = {
    100: ["港の島", 160, 96],
    101: ["洞窟_BF1_北側", 0, 32],
    "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}