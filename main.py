import subprocess
import os
subprocess.run(f"cd {os.getcwd()} && pip install -r requirements.txt", shell=True)

import scene
import mapdata
import monsterdata

if __name__ == "__main__":
    scenes = scene.Scenes("RPG GAME")

    # 遷移先 マップの名称, プレイヤーX, プレイヤーY
    scenes.set_scene(scene.Scene(mapdata.map_1, "平原", {
        10: ["例", 128, 416],
        11: ["洞窟", 64, 416],
        "monster_info": {
            "kinds": [monsterdata.suraimu,monsterdata.goburin],
            "min": 1,
            "max": 4,
        }
    }))
    scenes.set_scene(scene.Scene(mapdata.map_2, "例", {
        10: ["平原", 160, 64]
    }))
    scenes.set_scene(scene.Scene(mapdata.map_3, "洞窟", {
        11: ["平原", 352, 32]
    }))
    scenes.start()