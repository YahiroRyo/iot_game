from block import Block

BLOCKS = [
    Block("透明", "None", 0),
    Block("水", "water", 1),
    Block("壁", "wall", 2),
    Block("石", "rock", 3),
    Block("草", "grass", 4),
    Block("土道", "offroad", 5),
    Block("レンガ", "blockroad", 6),
    Block("砂", "sand", 7),
    Block("濃い草", "deep_grass", 8),
    Block("水", "water_none", 9),
    Block("明るい草道01", "light_grass_road_01", 20),
    Block("明るい草道02", "light_grass_road_02", 21),
    Block("明るい草01", "light_grass_01", 22),
    Block("明るい草02", "light_grass_02", 24),
    Block("明るい草03", "light_grass_03", 25),
    Block("明るい木01", "light_grass_tree_01", 26),
    Block("明るい木02", "light_grass_tree_02", 27),
    Block("ワープ", "warp", 100),
    Block("洞窟", "cave", 101),
    Block("村", "village", 102),
    Block("町", "castle", 103),
    Block("階段上り", "stairs_up", 104),
    Block("階段下り", "stairs_down", 105),
    Block("塔", "tower", 106),
]

def get_block_index_from_id(id: int):
    for (idx, block) in enumerate(BLOCKS):
        if block.id == id:
            return idx
    return -1