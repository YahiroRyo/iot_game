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
MAP_IS_LOAD = False
MAP_NAME = "ジルジノ"
MAP_WIDTH = 32
MAP_HEIGHT = 32
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 4
MAP_CONF = {
    4: ["港の島", 800, 320],
        "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}