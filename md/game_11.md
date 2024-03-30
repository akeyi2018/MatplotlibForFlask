# 戦闘画面その２

### ゴール

戦闘中：
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/6566c980-1d1d-b2d7-ca2d-b8604a2f408e.png)
戦闘終了：
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/52e6fc22-b35c-216c-d833-87993ad6f475.png)

だんだんドラクエっぽくなってきた

### ポイント整理
* 戦闘メッセージ表示の調整（背景）
* 「＜モンスター名＞が現れました」の追加
* 戦闘中の場合、戦闘終了ボタンを非表示（敵を倒したら、表示する）
* 敵にHPデータを付加（裏で付加しているので、Playerは見えない）
* ダメージ減算処理（単純な固定値ダメージ）
* 敵登録処理の追加（裏方）
* 敵のプロパティの追加（名前、HP、MP、STR、IMG）

戦闘メッセージ部分の調整
```YML
Label:
    id: battle_message
    font_size:  25
    text_size: self.size
    size_hint_y: 0.3
    height:  5 * self.font_size
    valign: 'top'
    pos_hint: {'top':  0.4, 'x': 0.1}  #  親ウィジェットの上端に寄せる
    pos:  0,  10  #  親ウィジェットの左上から20ピクセル下に配置
    canvas.before:
        Color:
            rgba:  0,  0,  0,  1
        Rectangle:
            pos: (0,80)
            size: (self.width, self.height)
        Color:
            rgba:  1,  1,  1,  1  # Red color for the line
        Line:
            width: 2
            points: [(2,  540), (self.width -  590,  540)]
        Line:
            width: 2
            points: [(2,  660), (self.width -  590,  660)] 
        Line:
            width: 2
            points: [(2,  660), (2,  540)] 
        Line:
            width: 2
            points: [(self.width -  590,  660), (self.width -  590,  540)]

```
敵登録クラスの作成（jsonファイルで管理）
```py
class Config():
    
    def __init__(self, info_id, **kwargs) -> None:
        self.info_id = info_id 
        # 敵情報を管理するJson
        self.enemy_info = os.path.join(os.getcwd(),'enemy_settings', f'enemy_info{self.info_id}.json')

        self.name = kwargs.get('name', '未登録')  # 'name'
        self.HP = kwargs.get('HP', 0)  # HP
        self.MP = kwargs.get('MP', 0)  # MP
        self.str = kwargs.get('STR',0)  # 強さ
        self.image = kwargs.get('IMG', 'enemy_0000.png') # image

    def registe_json(self):
        json_data = {'name': self.name,
                     'HP': self.HP,
                     'MP': self.MP,
                     'STR': self.str,
                     'IMG': self.image}

        with open(self.enemy_info, 'w', encoding='cp932') as json_file:
                json.dump(json_data, json_file, indent=4)
```
敵登場の処理
```py
def on_open(self):
    # 敵の名前
    self.ids.battle_message.text = f'{self.enemy_status["name"]}が現れました \n'
    for source in self.images:
        inner_layout = BoxLayout(
            orientation='vertical', height=150)
        
        image = Image(source=source)
        inner_layout.add_widget(image)

        self.ids.content.add_widget(inner_layout)
```
物理攻撃の処理
```py
def physical_attack(self):
        # ここに物理攻撃時の処理を記述します。
        attack_str = 8
        if len(self.ids.content.children) > 0:
            self.enemy_status['HP'] -= attack_str
            if self.enemy_status['HP'] > 0:
                new_message = f'{self.enemy_status["name"]}に{attack_str}のダメージを与えました \n'
                self.reconstruct_battle_message(new_message)
            else:
                # 戦闘終了処理
                self.finish_battle() 
```
戦闘終了処理
```py
def finish_battle(self):

        # モンスターを倒したメッセージ表示
        new_message = f'{self.enemy_status["name"]}を倒しました \n'
        self.reconstruct_battle_message(new_message)

        # モンスターが存在する場合
        if len(self.ids.content.children) > 0:
            # モンスターを削除
            self.ids.content.remove_widget(self.ids.content.children[0])
```
### 感想
戦闘画面はだいぶ充実してきた。
次回は戦闘効果アニメーションをつける予定
MAPの課題点が残っていますが、少しずつLevelアップしていきます。
