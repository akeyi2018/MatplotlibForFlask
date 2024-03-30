# 7. バトル画面切り替えと敵の制御

### 本日の目標
Map画面で敵に遭遇して、戦闘画面へ切り替わること
遭遇した敵の画像がそのまま戦闘シーンへ転送

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/9e0d1dd9-c24c-e8be-7148-66adfab3ea0c.png)

### やること整理
* battleクラスを整理
* Playerが敵と遭遇したタイミングでバトル画面へコール
* 敵を倒した想定でMapから敵を削除し、Map画面へ遷移する（アニメーションは再開する）
* 戦闘画面になったらアニメーションを停止する
* 敵を倒したら、Map画面へ遷移する

以下はやらない
* 敵の数の管理
* 敵の名前と画像の紐づけ
* 敵を無限に生成するループはいったん停止
* 戦闘画面に複数の敵はとりあえず、やらない（前回で複数の敵を配置できたので）

### 重要ポイント

* 敵遭遇したら、アニメーションを停止、敵遭遇判定を止める
```py
def show_battle_popup(self):
    # アニメーションを停止する
    self.anim.stop(self)

    # check_collision  メソッドのアニメーションを停止
    self.anim.unbind(on_progress=self.check_collision)
    # ポップアップウィンドウを作成
    battle_screen = BattleScreen(self)
    battle_screen.open()
    # ポップアップ画面が閉じたらアニメーションを再開
    battle_screen.bind(on_dismiss=self.resume_animation)
```
* アニメーションを再開する
```py
def resume_animation(self, instance):
    # self.remove_widget(self)
    self.anim.start(self)
    # self.anim.bind(on_progress=self.check_collision)
```
* Map画面の敵をRemoveするメソッド
```py
def remove_enemy(self):
    # 敵を管理しているウィジェットから敵を削除する処理を実装
    if self.parent is not None:
        self.parent.remove_widget(self)
```

### <font color="SpringGreen"><b>  ★★★ selfの極意 ★★★ </font>
```py
# self: EntryEnemyクラスのインスタンスをBattleScreenクラスへ引き渡す
battle_screen = BattleScreen(self)

# self: 自クラスのインスタンスを引数にして自クラスのメソッドに引き渡す
self.anim.start(self)  

# EntryEnemyクラスの親クラスにアクセスして、自クラスのインスタンスを削除する
self.parent.remove_widget(self)
```
### 感想
筆者は、クラスを扱っていたが、selfを引数として別のクラスへ引き渡すのは、初めての体験
Pythonって難しいねと感じる瞬間でした。（逆にこんなこともできるのか？）と感心してしまう。

