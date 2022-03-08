import pygame

def bgmplay(name:str, volume = 0.2, times = -1):
    pygame.mixer.music.load("bgm/"+name+".mp3")     # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(times)