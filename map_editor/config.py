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
MAP_NAME = "洞窟_BF2_南側"
MAP_WIDTH = 12
MAP_HEIGHT = 12
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 3
MAP_CONF = {
    104: ["北の島", 160, 96],
    105: ["洞窟_BF2_北側", 160, 96],
    "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}