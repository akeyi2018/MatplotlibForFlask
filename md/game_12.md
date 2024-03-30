# RPGMapの再整備
### 目標ゴール
Mapの端っこになった場合、イベント発火に備えているための布石
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/f919dba5-fdc9-43d6-8c02-0ba2857ba455.png)

衝突問題がある（このように画像の中にいるのにもかかわらず、衝突判定してくれいない）
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/d39ae4dd-2a40-f343-2480-ea13c2dde680.png)

### 変更の整理
---
Before：
Imageを使ってMapを作成、衝突判定などのバグが存在していた。
Imageもwidgetであるが、これを使わず、Playerの座標とMap座標を使用して判定をしていた。
作りが分かりにくいし、デバッグもしにくい構造になっていた。

---
After:ButtonImageへ変更
変更のメリットは、ImageButtonとPlayerの衝突判定を行い、ImageButtonにtextを付与しているので、どのMapタイプなのか、即時に判断ができて、座標による判定が不要
但し、冒頭の画像のように、衝突判定のバグは存在している、これはすぐに解決できそうにない問題である。

### 重要ポイント
* 衝突判定の変更
* Map作成widgetの変更
* キャラクターが移動する時の向きにgifを付加
* posとvelocityの違いが判明
---

ButtonBehaviorとImageを組み合わせる、画像ボタンが作れる
```py
class ImageButton(ButtonBehavior, Image):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
  
    def on_press(self):  
        print ('pressed', self.text)
```

ImageButton生成部分
```py
def update_map(self):
    self.clear_widgets()  # 既存のタイルをすべて削除

    for y, row in enumerate(self.map_data):
        for x, tile in enumerate(row):
            tile_image_path = self.tile_images.get(tile)
            if tile_image_path:
                # ImageButton生成
                tile_image = ImageButton(text=f'{tile}',source=tile_image_path)
                tile_image.size = (self.tile_size, self.tile_size)
                tile_image.pos = (x * self.tile_size, (len(self.map_data) - 1 - y) * self.tile_size)
                self.add_widget(tile_image)
```
衝突判定本体（めっちゃ簡単になった）ただしバグは存在する
```py
def is_valid_move(self):
    move_list = ['0','1']
    stop_list = ['2']
    player = self.parent.player
    for img_bt in self.children:
        if img_bt.collide_widget(player):
            if img_bt.text in move_list:
                return True
            elif img_bt.text in stop_list:
                return False
            else:
                return False
```

キャラクターの向き画像を付加
event_keyを付加し、衝突判定で使う
```py
def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    key = keycode[1]  # キーボードイベントのキーを取得
    if key == 'up':
        self.player.source = './player_image/back.gif'
        self.player.event_key = key
        self.player.velocity_y = 2
    elif key == 'down':
        self.player.source = './player_image/front.gif'
        self.player.event_key = key
        self.player.velocity_y = -2
    elif key == 'left':
        self.player.source = './player_image/left.gif'
        self.player.event_key = key
        self.player.velocity_x = -2
    elif key == 'right':
        self.player.source = './player_image/right.gif'
        self.player.event_key = key
        self.player.velocity_x = 2
```
衝突判定コール側
こちらはバグ対策でいろいろ長くなってしまった。
Mapから外に出れないようにしたり、壁にぶつかった場合、元に戻す工夫はしている
```py
def move(self, rpg_map):
    # Map範囲
    max_y = 400
    min_y = 0
    max_x = 950
    min_x = 0        
    # 次に移動する位置
    new_pos = Vector(*self.velocity) + self.pos
    
    # # 移動先が障害物でないかチェック
    if rpg_map.is_valid_move():
        if new_pos[0] < min_x:
            new_pos[0] = min_x
        if new_pos[0] > max_x:
            new_pos[0] = max_x
        # Mapから出れないようにする（Y座標はマイナスに対して補正）
        if new_pos[1] < min_y:
            new_pos[1] = min_y
        if new_pos[1] > max_y:
            new_pos[1] = max_y
    #     # 障害物でない場合→新しい位置にPlayerを移動する
        self.pos = new_pos
    else:
        if self.event_key == 'right':
            self.pos[0] =  self.pos[0] - 5
        if self.event_key == 'down':
            self.pos[1] =  self.pos[1] + 5

        if self.event_key == 'up':
            self.pos[1] =  self.pos[1] - 5
        if self.event_key == 'left':
            self.pos[0] =  self.pos[0] + 5

```
### 感想
Button同士でも衝突判定が微妙という記事もあったので、機会があったらもう少し深堀する予定

https://qiita.com/gotta_dive_into_python/items/abe433ae3b716d4fb8a7


https://github.com/kivy/kivy/issues/7226
