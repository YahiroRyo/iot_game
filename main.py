import scene
import mapdata


if __name__ == "__main__":
    scenes = scene.Scenes()

    scenes.set_scene(scene.Scene(mapdata.map_1, "平原", {
        10: 1
    }))
    scenes.set_scene(scene.Scene(mapdata.map_2, "例", {
        10: 0
    }))
    scenes.start()