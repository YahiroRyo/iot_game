import subprocess
import os
subprocess.run(f"cd {os.getcwd()} && pip install -r requirements.txt", shell=True)

import scene
import mapdata
import config
import json
import map
from layer import Layer

if __name__ == "__main__":
    scenes = scene.Scenes("RPG GAME","imgs/titleicon.png")
    maps = config.MAPS

    # 遷移先 マップの名称, プレイヤーX, プレイヤーY
    scenes.set_scene(scene.Scene(
        Layer(mapdata.map_1, None, None),
        "平原",
        {
            100: ["例", 128, 416],
            101: ["洞窟", 96, 416],
            "monster_info": {
                "kinds": ["suraimu", "goburin"],
                "min": 1,
                "max": 4,
            }
        }
    ))
    scenes.set_scene(scene.Scene(
        Layer(mapdata.map_2, None, None),
        "例",
        {
            100: ["平原", 160, 64],
            101: ["テスト", 0, 0],
            "monster_info": {
                "kinds": ["suraimu", "goburin"],
                "min": 4,
                "max": 8,
            }
        }
    ))
    scenes.set_scene(scene.Scene(
        Layer(mapdata.map_3, None, None),
        "洞窟",
        {
            101: ["平原", 351, 32],
            "monster_info": {
                "kinds": ["suraimu", "goburin"],
                "min": 3,
                "max": 6,
            }
        }
    ))
    
    for map_ary in maps:
        with open(f"maps/{map_ary}.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            scenes.set_scene(scene.Scene(
                Layer(map.Map(json_data["map"]), None, None),
                json_data["name"],
                json_data["conf"]
            ))
    scenes.start()