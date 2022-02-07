import subprocess
import os
subprocess.run(f"cd {os.getcwd()} && pip install -r requirements.txt", shell=True)

import scene
import mapdata
import monsterdata
from layer import Layer

if __name__ == "__main__":
    scenes = scene.Scenes("RPG GAME","imgs/titleicon.png")

    # 遷移先 マップの名称, プレイヤーX, プレイヤーY
    scenes.set_scene(scene.Scene(
        Layer(mapdata.map_1, None, None),
        "平原",
        {
            100: ["例", 128, 416],
            101: ["洞窟", 96, 416],
            "monster_info": {
                "kinds": [monsterdata.suraimu,monsterdata.goburin],
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
            "monster_info": {
                "kinds": [monsterdata.suraimu,monsterdata.goburin],
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
                "kinds": [monsterdata.suraimu,monsterdata.goburin],
                "min": 3,
                "max": 6,
            }
        }
    ))
    scenes.start()