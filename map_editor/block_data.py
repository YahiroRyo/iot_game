import os
from block import Block

FILTER = [
    "character",
    "monsters",
    "titleicon.png",
]

files = os.listdir("../imgs")
for filter in FILTER:
    files.remove(filter)
    
BLOCKS = [Block("透明", "None", 0)]
for file in files:
    names = file.split("_")
    BLOCKS.append(Block("", file, int(names[0])))

def get_block_index_from_id(id: int):
    for (idx, block) in enumerate(BLOCKS):
        if block.id == id:
            return idx
    return -1