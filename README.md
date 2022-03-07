# IoT RPG  
icon2022の作品  
## 仕様書  
### 解像度  
- 画面の解像度
1280*720  
- マップの1マス
32*32  
- プレイヤー
30*30  
- モンスターの絵
120*120  
  
### マップエディタの使用方法  
- sで保存(maps/〇〇.jsonに保存される)  
- ホイールクリックしながらドラッグでマップ移動  
- パレットの画像を左クリックするとその画像を使用することができる  
- 左クリック長押しでSW / 3からSWの範囲でマウスをドラッグするとマップにブロックを書くことができる  
#### config.pyについて  
- MAP_IS_LOAD  
TrueかFalseで操作するTrueの場合は、MAP_NAMEのファイルを読み込み予め表示してくれる  
- MAP_NAME  
マップの名前・移動先に使われるやつ  
- MAP_WIDTH  
マップのブロック単位の横幅
- MAP_HEIGHT  
マップのブロック単位の縦幅
- MAP_BG_ID  
MAP_IS_LOADがFalseの場合に初期でマップ全体に置かれるブロックID  
※-1であれば、ブロックID 0で埋められる
- MAP_CONF  
遷移先やモンスターの出現率等を操作できる  
※モンスターをオブジェクトとして渡すことはできなさそうなので、後々実装

### IoT要素  
- 天気・時間～ゲーム内データを変更  
- ネットワークのトラフィック量に応じてゲーム内データを変更  
  
### 魔法案  
- ロコモア: HP30前後回復  
- ロコモラ: HP80前後回復
- ロコモラー: HP60前後全体回復
- モデルナ: あらゆる状態異常・マイナス効果を治すが1ターン攻撃力半減  
- ファイザー: あらゆる状態異常・マイナス効果を治すが1ターン動けない  
- パブロン: 毒を直す  
- タミフル: 毒・猛毒を直す  
- ザバス: 攻撃力アップ  
- ユンケル: 魔力アップ  
- バファリン: 防御力アップ  
- イオメロン: 魔法防御アップ
- セサミン: 会心率アップ  
- ボラギ: 攻撃小、魔*1  
- ボラギノ: 攻撃中、魔*1.4  
- ボラギノル: 攻撃大、魔*1.8  
- ボラギノール: 攻撃特大、魔*2.5  
- ワザップ: 攻撃小
- イザップ: 攻撃中
- ラザップ: 攻撃大
- ライザップ: 攻撃特大
  
### 特技
- 命の母  
  
### アイテム  
- 0101: やくそう: 1人のhpを30回復  
- 0102: すごいやくそう: 1人のhpを60回復  
- 0103: やばいやくそう: 1人のhpを120回復
  
### 武器
- トライデント明美  
- トライデント暁美  

### 防具

### プレイヤーステータス  
Player(mapimgdata.load_img("imgs/character/sensi_f.png", -1), "戦士", 50, 20, 13, 5, 4, 3, 10, 8, 0 ,0, 0, [0], [0 for _ in range(7)], 50, 20, 260, 416)  
Player(mapimgdata.load_img("imgs/character/mahoutsukai_f.png", -1), "魔法使い", 35, 30, 5, 15, 5, 15, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 35, 30),  
Player(mapimgdata.load_img("imgs/character/souryo_f.png", -1), "僧侶", 50, 25, 9, 9, 13, 13, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 50, 25),  
Player(mapimgdata.load_img("imgs/character/butouka_f.png", -1), "武闘家", 45, 2, 16, 2, 7, 6, 16, 8, 0, 0, 0, [0], [0 for _ in range(7)], 45, 2),  
