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
MAP_IS_LOAD=True
MAP_NAME="初期の島"
MAP_WIDTH=32
MAP_HEIGHT=32
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 1
MAP_CONF = {
    100: ["南の島", 160, 64],
    101: ["洞窟_01", 0, 0],
    103: ["モノル", 0, 0],
    "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}