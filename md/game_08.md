# 8. 敵の生成と動きの改善
### 目標

敵が倒されたら、また別の敵が湧くという、無限ループがRPGゲームのセオリーです。
筆者は、本日で実現する

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/2529ac03-1b99-16c1-6185-86fbae523d04.png)

### やること
* 敵の数は常に同じ
* 敵が倒されたら、別の敵が現れる

### 重要ポイント 
<font color="SpringGreen"><b> *** EventDispatcher ***</font>
理解しないといつまでもErrorの無限ループとなります。
ChatGPTに聞いてもやはり解決に至らなかった。
```text
もし上記の修正でも問題が解決しない場合は、
EventDispatcherの使用方法についての詳細なドキュメントを確認するか、
KivyのコミュニティフォーラムやStack Overflowなどで質問することをお勧めします。
```
筆者は調べて下記の先輩方が参考になりました。

https://qiita.com/gotta_dive_into_python/items/df8325cc1575800d3a99

EventDispatcherとは何ぞや？
→ 簡単に言うとなんらかの動作にリスナーをつける
（Javascriptで言うボタンリスナーと同じです）

なんでこれが必要？
1. 敵が倒されたことをキャッチしたい
2. キャッチしたら、別の敵を生成する
2. 1と2の無限キャッチループ

まずは、イベントを登録（イベント名は[on_]始まり）
kivyはEventDispatcherが用意されている
```py
from kivy.event import EventDispatcher
def __init__(self, **kwargs):
    super(EntryEnemy, self).__init__(**kwargs)
    # 敵が倒されるイベントを登録しておく
    self.register_event_type('on_enemy_defeated')
```
コールバック関数登録しておく（処理はprint文だけ、不要だったらpass）
```py
def on_enemy_defeated(self):
    print('敵が倒された')
    pass
```
敵を倒したら、RPGMapから削除する
削除後にdispatchイベントを発生させる（発火トリガー）
```py
def remove_enemy(self):
    # 敵を管理しているウィジェットから敵を削除する処理を実装
    if self.parent is not None:
        self.parent.remove_widget(self)
        # 敵が倒されたことを通知
        self.dispatch('on_enemy_defeated')
```

バインド（イベントは関数を関連付ける）
1. 初期マップで敵生成時
```py
def place_enemy(self):
    self.enemies = []  # Enemyインスタンスを格納するリスト
    for i in range(3): 
        enemy = EntryEnemy(pos=(100 * (i + 1), 150))
        
        # 敵が倒されたときに再生成するためのリスナーを追加
        enemy.bind(on_enemy_defeated=self.respawn_enemy)
        self.enemies.append(enemy)
        self.add_widget(enemy)
```

２．敵をもう一度生成したら、これにもバインドしておく
```py
# 敵再配置
def respawn_enemy(self, instance):
    # 敵が倒されたときに新しい敵を生成して配置する
    enemy = EntryEnemy(pos=(100 * (len(self.enemies) +  1),  150))
    # 敵が倒されたときに新しい敵を生成して配置する
    enemy.bind(on_enemy_defeated=self.respawn_enemy)
    self.enemies.append(enemy)
    self.add_widget(enemy)
```

### 感想
今回はまた新しいことを勉強した。一つの技術を知るだけではなく、ゲームに生かせることに非常に意味があると思いました。
以下はgithubからソースコードを取得できるので、そのまま、動かせると思います。

https://github.com/akeyi2018/RPG_Game
