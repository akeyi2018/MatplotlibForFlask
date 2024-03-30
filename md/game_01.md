### 背景
RPGゲームはRPGツクールなどがあり、だれでも簡単に作れる時代だが、筆者は昔からPygameを使ってゲーム画面まで作りましたが、一度は挫折した。
久しぶりにゲーム作成をググってみたら、昔かなり嫌がっていたkivyが出てきた。しかも、簡単にゲームが作れるとのことで、早速PongBallを作ったが、今回は再度、RPGゲームの作成に挑戦する。

### 目標
RPGフィールドマップの表示とPlayerを動かすまで

### 前提
1. Pythonの基礎文法を理解している
1. クラスメソッドを理解している
1. kivyインストール済
1. 仮想環境構築済

### 早速ChatGPTに質問

筆者が設定した前提
1. kivyを使ってRPGのフィールドマップを作成したい
1. キーボードを使ってPlayerを動かしたい
1. Playerの画像をGif画像である
1. RPGMapは、１と0の数字で構成されています。１は障害物で、0は通行可能で、0と１をそれぞれ別々の画像に置き換えて表示する
1. Mapデータは以下に示す
```py
map_data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
```
### ChatGPT結果
```py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window

# プレイヤーキャラクタークラス
class Player(Image):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self, rpg_map):
        # self.pos = Vector(*self.velocity) + self.pos
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y

        # 移動先が障害物でないかチェック
        if not rpg_map.is_obstacle(new_x, new_y):
            self.pos = Vector(*self.velocity) + self.pos

# RPGマップクラス
class RPGMap(Widget):
    def __init__(self, **kwargs):
        super(RPGMap, self).__init__(**kwargs)
        # self.size = (15, 15)  # マップのサイズを設定
        self.tile_size = 50 # タイルのサイズを設定
        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.tile_images = {
            0: 'floor_brick.png',  # 0に対応する画像のパス
            1: 'floor_carpet.png'  # 1に対応する画像のパス
        }

        self.update_map()

    def update_map(self):
        self.clear_widgets()  # 既存のタイルをすべて削除

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                tile_image_path = self.tile_images.get(tile)
                if tile_image_path:
                    tile_image = Image(source=tile_image_path)
                    tile_image.size = (self.tile_size, self.tile_size)
                    tile_image.pos = (x * self.tile_size, (len(self.map_data) - 1 - y) * self.tile_size)
                    self.add_widget(tile_image)

    def is_obstacle(self, x, y):
        # マップ上の座標をマップデータ上のインデックスに変換
        map_x = int(x / self.width * len(self.map_data[0]))
        map_y = int(y / self.height * len(self.map_data))

        # マップデータの範囲内にあることを確認
        if 0 <= map_y < len(self.map_data) and 0 <= map_x < len(self.map_data[0]):
            # マップデータ上で座標が障害物であるかをチェック
            return self.map_data[map_y][map_x] == 1
        else:
            # マップデータの範囲外にある場合は障害物と見なす
            return True

# メインの画面
class RPGApp(Widget):
    def __init__(self, **kwargs):
        super(RPGApp, self).__init__(**kwargs)

        self.rpg_map = RPGMap()
        self.add_widget(self.rpg_map)
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyboard.bind(on_key_up=self._on_keyboard_up)

        self.player = Player(source='player_image.gif')
        self.player.size = (50, 50)
        self.player.pos = (50, 50)
        self.add_widget(self.player)

    def on_touch_down(self, touch):
        self.player.velocity = Vector(touch.x - self.player.center_x, touch.y - self.player.center_y)

    def on_touch_up(self, touch):
        self.player.velocity = Vector(0, 0)

    def update(self, dt):
        self.player.move(self.rpg_map)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]  # キーボードイベントのキーを取得
        if key == 'w':
            self.player.velocity_y = 5
        elif key == 's':
            self.player.velocity_y = -5
        elif key == 'a':
            self.player.velocity_x = -5
        elif key == 'd':
            self.player.velocity_x = 5
    
    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard.unbind(on_key_up=self._on_keyboard_up)
        self.keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'w' or keycode[1] == 's':
            self.player.velocity_y = 0
        elif keycode[1] == 'a' or keycode[1] == 'd':
            self.player.velocity_x = 0

class RPGGame(App):
    def build(self):
        game = RPGApp()
        Clock.schedule_interval(game.update, 1.0 / 30.0)
        return game

if __name__ == '__main__':
    RPGGame().run()
```
### ゲーム画面

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/645c1ba1-f925-e6ef-7e2b-f951f3e442d5.png)

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/77a13d25-d4c6-0676-09fe-4aa1fcb23cac.png)
とりあえず、キャラクターを動かすことができるようになった。

### 次回予告
障害物検知して、壁の内側のみ動かせるようにしたい。
