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
    for map_ary in maps:
        with open(f"maps/{map_ary}.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            scenes.set_scene(scene.Scene(
                Layer(
                    map.Map(json_data["map_main"]),
                    map.Map(json_data["map_everything"])    if "map_everything" in json_data else None,
                    map.Map(json_data["map_npcs"])          if "map_npcs" in json_data else None
                ),
                json_data["name"],
                json_data["conf"],
                json_data["events"] if "events" in json_data else {}
            ))
    scenes.start()