import scene
import mapdata
import subprocess
import os

if __name__ == "__main__":
    subprocess.run(f"cd {os.getcwd()} && pip install -r requirements.txt", shell=True)
    scenes = scene.Scenes()

    scenes.set_scene(scene.Scene(mapdata.map_1, "平原", {
        10: "例"
    }))
    scenes.set_scene(scene.Scene(mapdata.map_2, "例", {
        10: "平原"
    }))
    scenes.start()
