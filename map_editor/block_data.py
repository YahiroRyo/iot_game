from block import Block

BLOCKS = [
    Block("水", "water", 1),
    Block("壁", "wall", 2),
    Block("石", "rock", 3),
    Block("草", "grass", 4),
    Block("土道", "offroad", 5),
    Block("レンガ", "blockroad", 6),
    Block("砂", "sand", 7),
    Block("ワープ", "warp", 100),
    Block("洞窟", "cave", 101),
    Block("村", "village", 102),
    Block("町", "castle", 103),
    Block("階段上り", "stairs_up", 104),
    Block("階段下り", "stairs_down", 105),
]

def get_block_index_from_id(id: int):
    for (idx, block) in enumerate(BLOCKS):
        if block.id == id:
            return idx