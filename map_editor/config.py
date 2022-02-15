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
MAP_NAME = "塔_1_F3"
MAP_WIDTH = 17
MAP_HEIGHT = 17
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 2
MAP_CONF = {
    105: ["塔_1_F2", 32, 128],
    "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}