### 目標
* 主人公のステータス画面を作成する

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/52399ea1-6d2f-7641-7b30-2148895e3a9d.png)

### 必要なことの整理（FFっぽいことを）
* 枠線（白）
* 背景（青）
* 文字（白）

### 重要ポイント
* レイアウトが必要であること(FloatLayout)
* 文字はLabelを使用
* 枠線は丸みのある枠線にエレガントがあるので、少し凝りました
 →ChatGPTにKivyを使って円弧を書かせる

FloatLayoutを継承しないと書けない
```py
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label

class PlayerStatusWidget(FloatLayout):
# 略
```

日本語Font指定してあげると文字化けを回避できる
pos_hintを使わないと位置調整がうまくいかなかった
（座標はWindowの大きさを認識しているようなので、理解するのに時間がかかった）

```py
# プレイヤーステータスを表示するラベルを作成し、キャンバス内に配置
font_path = 'NotoSansSC-Regular.ttf'
self.player_name_label = Label(text="エンジニア Y", font_name=font_path,
                            font_size=20, pos_hint={'center_x': 0.9, 'center_y': 8.85},
                            halign='left')
self.job = Label(text="職業: SE", font_name=font_path, font_size=20, 
                      pos_hint={'center_x': 0.8, 'center_y': 8.75},
                            halign='left')
self.hp_label = Label(text="HP: 100", font_name=font_path, font_size=20, 
                      pos_hint={'center_x': 0.8, 'center_y': 8.5},
                            halign='left')
self.mp_label = Label(text="MP: 50", font_name=font_path, font_size=20,
                      pos_hint={'center_x': 0.8, 'center_y': 8.25},
                            halign='left')
self.level_label = Label(text="レベル: 1", font_name=font_path, font_size=20,
                      pos_hint={'center_x': 0.8, 'center_y': 8.0},
                            halign='left')
```

枠の描画については、地道に座標と戦闘してました。

```py
# 枠の描画
with self.canvas:
    Color(1, 1, 1, 1)  # 枠の色を青に設定
    Line(circle=(30 - 10, 890 - 10, 10, -90, 0), width=2)
    # Line(points=[20, 890, 170, 890], width=2) # OK
    Line(circle=(180 - 10, 890 - 10, 10, 90, 0), width=2)
    Line(points=[20, 730, 170, 730], width=2) # OK
    Line(circle=(180 - 10, 750 - 10, 10, 90, 180), width=2)
    Line(points=[180, 880, 180, 740], width=2) # OK
    Line(circle=(30 - 10, 750 - 10, 10, 180, 270), width=2)
    Line(points=[10, 880, 10, 740], width=2) #ok
    Color(0, 0, 1, 1)  # 枠の色を青に設定
    self.rect = Rectangle(size=(165, 150), pos=(14, 735))
    self.rect = Rectangle(size=(150, 10), pos=(20, 885))
```
Labelのデフォルトはcenterで、左揃えは以下を指定すること
```py
self.job.text_size = self.job.size
self.hp_label.text_size = self.hp_label.size
self.mp_label.text_size = self.mp_label.size
self.level_label.text_size = self.level_label.size
```

### 感想
今回は簡単な画面ではあるが、kivyの作法を知らないと結構苦労しました。
これでKivyのLevelは5ぐらいかと思います。
