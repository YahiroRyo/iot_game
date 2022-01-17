from tkinter import SW
import scene

class Map:
    # マップデータ
    map = []
    row, col = 0, 0  # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 32                      # 1マスの大きさ[px]
    
    def __init__(self, map: list) -> None:
        self.map = map
        self.row = len(map)
        self.col = len(map[0])

    # マップの描画
    def draw(self, screen):
        x_set=scene.SW/2-self.col*self.msize/2
        y_set=scene.SH/2-self.row*self.msize/2
        print(x_set)
        print(y_set)
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]],
                            (j*self.msize+x_set, i*self.msize+y_set))
