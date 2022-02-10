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
MAP_NAME="テスト"
MAP_WIDTH=64
MAP_HEIGHT=64
MAP_MSIZE = 32
# -1だと0埋めされる
MAP_BG_ID = 4
MAP_CONF = {
    100: ["平原", 160, 64],
    101: ["洞窟", 0, 0],
    "monster_info": {
        "kinds": ["goburin", "suraimu"],
        "min": 4,
        "max": 8,
    }
}