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
MAP_NAME = "神殿_01_F3"
MAP_WIDTH = 9
MAP_HEIGHT = 9
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 2
MAP_CONF = {
    105: ["神殿_01_F2", 480, 384],
        "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}