import scene

class Map:
    # マップデータ
    map = []
    row, col = 0, 0  # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 32                      # 1マスの大きさ[px]
    x = 0                           # マップ配置始点X
    y = 0                           # マップ配置始点Y
    
    def __init__(self, map: list) -> None:
        self.map = map
        self.row = len(map)
        self.col = len(map[0])
        self.x = scene.SW / 2 - 32
        self.y = scene.SH / 2 - 32


    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(
                    self.imgs[self.map[i][j]],
                    (j * self.msize + self.x, i * self.msize + self.y)
                )
