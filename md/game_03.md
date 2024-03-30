### 目標

* モンスターの配置
* モンスターが動く
* モンスターがうようよしている世界を作り出す

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/90063381-474d-0eaf-64d8-d4afa99e0ad1.png)

### 状況整理

* 敵を配置するため、Mapを少し広げた
* 異なる種類の敵を3体
* 動きはランダムに

制限：
* 敵とPlayerがぶつかった時の実装はしない
* 敵を倒したら一定時間にMapから出現しない 

### 重要ポイント
* モンスターが動くには、Animation機能を導入する
* いろんなモンスターを作り出すためには、Enemyクラスを作成（別ファイル）
* モンスター配置メソッド

### モンスタークラス
* モンスターのサイズとアニメーションの設定
```py
def __init__(self, **kwargs):
    super(Enemy, self).__init__(**kwargs)
    self.size = (50,50)
    self.anim = Animation()
    self.randomize_animation()
    self.anim.repeat = True
    self.anim.start(self)
```
* モンスターをランダムにセット
```py
# 3種類の敵のGIF画像パスをリストで定義
enemy_gifs = ['enemy_01.gif', 'enemy_02.gif', 'enemy_03.gif']
random_gif = random.choice(enemy_gifs)  # ランダムに1つのGIF画像を選択
self.source = random_gif  # 選択されたGIF画像を敵の画像として設定
```
* アニメーションの設定（self.randomize_animation()を再帰的に呼び出し）
* durationをいろいろ変えるとモンスターの動きが早かったり、遅かったりするので楽しい
```py
self.anim = Animation(
    pos=(random.randint(50, 900),
    random.randint(50, 300)),
    duration=1)  # ランダムな位置に移動するアニメーションを作成
self.anim.bind(on_complete=lambda *args: self.randomize_animation())
self.anim.start(self)
```
* モンスターの配置
```py
def place_enemy(self):
    self.enemies = []  # Enemyインスタンスを格納するリスト
    for i in range(3): 
        enemy = Enemy(pos=(200 * (i + 1), 150))
        self.enemies.append(enemy)
        self.add_widget(enemy)
```

### 感想
さすがPython様様だと思います。
こんな短いコードでこれだけのことをできてしまうのは、すごい時代になりました。
N88BASCIの時代ではマシン語を一字正確に打ち込んで、やっと動くみたいなことは…

