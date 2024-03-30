### 目標
前回は、主人公のステータス表示したものの、本来であれば、バトル画面で表示すべきでした。
今回は、主人公が敵とぶつかったらバトル画面へ遷移することを作る

### 敵との衝突処理で必要な要件の整理
* 衝突の判定
PlayerとEnemyはともにWidgetで定義しているので、Widgetが衝突する場合、kivyでは、 <font color="SpringGreen"><b>collide_widget</b></font>が用意されている。これはwidget同士がぶつかる判定をしてくれる
* バトル画面は以下のように簡単なポップアップ画面を用意
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/00d68ed8-c833-3836-1bce-d3590f361655.png)

### 重要ポイント
* Enemyはアニメーションで動くため、動いているEnemyを追跡する必要がある、そのため、
1. 衝突判定メソッドはEnemyクラスに実装する
1. playerをEnemyクラスに持ってゆく

衝突判定メソッドは以下の通り
```py
def check_collision(self, widget, progress, test):
    # ここでEnemyの位置を更新し、Playerとの衝突をチェックする
    self.x = self.pos[0]  # Enemyのx座標を更新
    self.y = self.pos[1]  # Enemyのy座標を更新
    if self.parent is not None and self.parent.player is not None:
        player = self.parent.player
        if self.collide_widget(player):
            self.parent.show_battle_popup()
```
以下メソッドは、3つの引数が必要のようで、widget、progressとtestは使わないが、とりあえず、持たせておかないと引数が足りないエラーが出ているため
```py
def check_collision(self, widget, progress, test):
```
アニメーション表示メソッドには、 <font color="SpringGreen"><b>衝突メソッドをbind</b></font>しておく
```py
def randomize_animation(self):
        # 3種類の敵のGIF画像パスをリストで定義
        enemy_gifs = [
            './enemy_image/enemy_01.gif',
            './enemy_image/enemy_02.gif',
            './enemy_image/enemy_03.gif'
            ]
        random_gif = random.choice(enemy_gifs)  # ランダムに1つのGIF画像を選択
        self.source = random_gif  # 選択されたGIF画像を敵の画像として設定
        self.pos = (random.randint(50, 900), random.randint(50, 300))  # ランダムな位置に敵を配置
        self.anim = Animation(
            pos=(random.randint(50, 900),
                 random.randint(50, 300)),
            duration=5)  # ランダムな位置に移動するアニメーションを作成
        self.anim.bind(on_complete=lambda *args: self.randomize_animation())
        self.anim.start(self)
        # 衝突メソッドをbind
        self.anim.bind(on_progress=self.check_collision)
```
* ポップアップクラスは以下
```py
class BattleScreen(Popup):
    def __init__(self, **kwargs):
        super(BattleScreen, self).__init__(**kwargs)
        # ポップアップ内のコンテンツを作成
        content = Button(text='Attack!', size_hint=(None, None), size=(200, 200))
        content.bind(on_press=self.dismiss)  # ボタンが押されたときにポップアップを閉じる
        self.title = 'Battle Screen'
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.auto_dismiss = False  # ポップアップを自動的に閉じないように設定
        self.add_widget(content)  # ポップアップにコンテンツを追加
```
親クラスの参照（筆者は初めて使う）
```py
player = self.parent.player
```
この行は、Enemyクラス内でPlayerオブジェクトにアクセスするために使用されています。
具体的には、EnemyクラスはRPGAppクラス（またはそのサブクラス）の子ウィジェットとして配置されており、RPGAppクラス内にplayerという名前の属性が存在します。そのため、self.parentはEnemyの親ウィジェットであるRPGAppを指し、self.parent.playerはRPGApp内のplayer属性にアクセスします。
この行の目的は、EnemyオブジェクトがPlayerオブジェクトと衝突した場合に、RPGAppクラス内のshow_battle_popup()メソッドを呼び出すために、Playerオブジェクトにアクセスすることです。

* <font color="SpringGreen"><b>EnemyクラスはRPGAppクラス内でインスタンス宣言している</font>
* <font color="SpringGreen"><b>self.parentを使うと親クラスへのアクセスができること
* <font color="SpringGreen"><b>親クラスのメソッドが使用できるということ

### Kivyでinspectorを調べる
```terminal
# 以下のコマンドを実行
python <test_module> -m inspector

# Ctrl+Eでデバッグモードになる
```

### 感想
今回は、結果から簡単そうに見えるかもしれないが、アニメーションの追記判定に気が付くまで、試行錯誤していました。また、popupクラスを呼び出すにはトリガーが必要であること。
