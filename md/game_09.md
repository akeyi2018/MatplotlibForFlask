# 敵の生成と動きの改善その２

### 問題点

1. 現在、筆者のプログラムには、敵とPlayerが遭遇した場合、遭遇した敵のみアニメーションが止まる仕組みになっている。そのため、ランダムに敵を配置した場合、戦闘画面表示中に敵とPlayerが遭遇してしまうので、そのまま発火されるため、戦闘中に敵が勝手に入れ替えられてしまいます
1. 敵のwidgetを削除にするには、remove_widgetを使うが、widgetと結びつけているアニメーションを完全にStopすることはできていない(unbindしても効かない）
1. 敵の名前はハードコードで適当につけている、これを修正したい

### やることリスト
1. 問題点１の解決策
→敵の初期位置をMapの中央に配置し、上下に繰り返し、ランダムな距離を巡回する
→敵とPlayerが遭遇した場合、戦闘画面へ切り替わる
→敵を倒した10秒後に、マップにランダムな敵を生成する
1. 問題点２の解決策
→根本的な解決策は現在持ち合わせていないため、戦闘画面へ切り替わた後、その間に近くに敵と遭遇しないようにする
1. 上記の問題点3の解決策
→新たにEnemy管理クラスを作成、ランダムな敵を生成し、名前とgifパスを返却する

### 重要ポイント
敵を管理するクラス
```py
import random, os

class Enemy():
    def __init__(self) -> None:
        self.root_path = './enemy_image'

    def generate_random_enemy(self):
        enemy_name_list = ['goblin',
                           'wizard',
                           'Snake Woman'
                          ]
        enemy_gifs = [
            'enemy_01.gif',
            'enemy_02.gif',
            'enemy_03.gif'
            ]
        choice = random.choice(enemy_gifs)
        index = enemy_gifs.index(choice)
        image_path = os.path.join(os.getcwd(), self.root_path, choice)
        return enemy_name_list[index], image_path
```
敵が上下移動するメソッド
二つのアニメーションを作成し、それを結ぶと上下に一回だけ移動する
Playerとの遭遇関数をbindしておく必要がある
アニメーション終わったら場合、on_animation_completeをbindしておく
この二つのメソッドで、無限に敵のアニメーションが動く
```py
def move_enemy_animation_fix(self):
    random_val = random.randint(-150, 150)
    anim_up = Animation(pos=(self.x, self.y + random_val), duration=self.move_animation_time)
    #  ウィジェットの初期位置から下に移動するアニメーションを作成
    anim_down = Animation(pos=(self.x, self.y), duration=self.move_animation_time)

    #  アニメーションを連鎖させ、最後に最初のアニメーションに戻るように設定
    self.anim = anim_up + anim_down
    # self.repeat = True
    self.anim.bind(on_complete=self.on_animation_complete)
    #  アニメーションを開始
    self.anim.start(self)
    self.anim.bind(on_progress=self.check_collision)
```
バインドされたアニメーション終了メソッド
注意点：そのまま再開ではなく、戦闘画面が開いているかの判定を入れている
```py
def on_animation_complete(self, animation, instance):
    if self.pop_up_flag != 1:
        print("Animation completed:", datetime.now(), self.id)
        self.move_enemy_animation_fix()
```
戦闘画面へ切り替わるメソッド
self.pop_up_flag = 1で戦闘画面フラグを付与
```py
def show_battle_popup(self):

    self.pop_up_flag = 1
    # アニメーションを停止する
    self.anim.stop(self)
    # self.anim.stop_all(self.parent)
    # 敵衝突をアンバインドする
    self.anim.unbind(on_progress=self.check_collision)
    self.anim.unbind(on_animation_complete=self.move_enemy_animation_fix)

    # ポップアップウィンドウを作成
    battle_screen = BattleScreen(self)
    battle_screen.open()
    
    battle_screen.bind(on_dismiss=self.resume_animation)
```
敵を削除後、10秒後、`on_enemy_defeated'を発火させる
```py
def remove_enemy(self):
    # 敵を管理しているウィジェットから敵を削除する処理を実装
    if self.parent is not None:
        self.parent.remove_widget(self)
        # 敵が倒されたことを通知
        Clock.schedule_once(lambda dt: self.dispatch('on_enemy_defeated'), 10)
```
敵を配置する関数（名前とGIF画像をクラスに渡して生成する）
```py
def place_enemy_fix(self):
    self.enemies = []  # Enemyインスタンスを格納するリスト
    for i in range(self.enemys_num):
        # 敵のGIF
        enemy_name, random_gif = Enemy().generate_random_enemy()
        enemy = EntryEnemy(pos=(100 * (i + 2)*1, 200),
                           source=random_gif,
                           enemy_name=enemy_name)
        # 新しい敵が生成されたらバインドする
        enemy.bind(on_enemy_defeated= lambda instance: self.respawn_enemy(enemy))
        enemy.move_enemy_animation_fix()
        self.enemies.append(enemy)
        
        enemy.dispatch('on_enemy_generated')
        self.add_widget(enemy)
```
敵を再配置する関数
```py
# 敵再配置（敵が倒されたときに新しい敵を生成して配置する）
def respawn_enemy(self, instance): 
    enemy_name, random_gif = Enemy().generate_random_enemy() 
    # 敵が倒されたときに新しい敵を生成して配置する
    enemy = EntryEnemy(pos=(self.player.x - 80,  200),
                       source=random_gif,
                       enemy_name=enemy_name)

    # 敵が生成されたときにバインドする
    enemy.bind(on_enemy_generated=self.generate_enemy)
    # 新しい敵が生成されたらバインドする
    enemy.bind(on_enemy_defeated= lambda instance: self.respawn_enemy(enemy))
    enemy.move_enemy_animation_fix()
    # 新しい敵を生成して配置する
    self.enemies.append(enemy)
    enemy.dispatch('on_enemy_generated')
    self.add_widget(enemy)
```
bindで新規に覚えた事
lambda関数を使うと引数を渡せるようで「enemy」インスタンスを渡している
```py
enemy.bind(on_enemy_defeated= lambda instance: self.respawn_enemy(enemy))
```

### 感想
筆者は、ほぼ一日、アニメーション問題に取りかかってしまいました。
* 一つ、複数の敵が同時に動いているため、widghtの切り分けと識別について、よく調べないとわからなかった。
* widgetとanimationの関係についてもう少し深堀しないとだめかも

* 今後として、Mapにバグは存在していたので、Playerというwidgetが持っている座標とRPGMapの床との関係
* dispatcherが早すぎて、関数を何回もコールしてしまう問題がある

https://github.com/akeyi2018/RPG_Game
