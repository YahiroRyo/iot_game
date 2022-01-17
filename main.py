import subprocess
import os
subprocess.run(f"cd {os.getcwd()} && pip install -r requirements.txt", shell=True)

import scene
import mapdata

if __name__ == "__main__":
    scenes = scene.Scenes()

    # 遷移先 マップの名称, プレイヤーX, プレイヤーY
    scenes.set_scene(scene.Scene(mapdata.map_1, "平原", {
        10: ["例", 0, 0]
    }))
    scenes.set_scene(scene.Scene(mapdata.map_2, "例", {
        10: ["平原", 0, 0]
    }))
    scenes.start()