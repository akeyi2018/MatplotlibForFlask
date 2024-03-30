# 10．戦闘画面

### 目標
今回のゴール画面
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/ba0dd3cf-f51a-8c97-a850-1d3064298599.png)

### やることリスト
* Playerのステータスを画面で表示する
* まほうを選択した時にDropUpメニューが出て、選択したメニューで処理ができること

### 重要ポイント
ステータスを画面の部分は静的な表示にしているので、kvファイルで作成
```YML
BoxLayout:
    orientation: 'vertical'
    size_hint_y: 0.15
    pos_hint: {'top': 0.95, 'x': -0.4}
    
    Label:
        id: player_name 
        text: 'ken'
        font_size: 30
        size:  50,  50
        canvas.before:
            Color:
                rgba:  0,  0,  0,  1  # Red background
            Rectangle:
                pos: (0,530)
                size: (self.width -580, self.height +  115)
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
    Label:
        id: player_hp
        text: 'HP: 100'
        font_size: 30
    Label:
        id: player_mp
        text: 'MP: 10'
        font_size:30
```
まほうメニューでは、解説動画を見つけたので[ここ](https://www.youtube.com/watch?v=Wu7kTFZtM6I&ab_channel=Codemy.com)参照

```YML
Spinner:
    id: spinner_id
    text: 'まほう'
    font_size: 30
    values: ['ホイミ', 'メラ']
    on_text: root.spinner_clicked(spinner_id.text)
```
Python処理側
```py
def spinner_clicked(self,text):
    if text == 'ホイミ':
        self.handle_item1()
    elif text == 'メラ':
        self.handle_item2()
    self.ids.spinner_id.text = 'まほう'

def handle_item1(self):
    # 項目1を選択した場合の処理
    # print("ホイミを唱えました")
    new_message = 'ホイミを唱えました \n'
    self.reconstruct_battle_message(new_message)

def handle_item2(self):
    # 項目2を選択した場合の処理
    print("メラを唱えました")
    new_message = 'メラを唱えました \n'
    self.reconstruct_battle_message(new_message)
```
### 感想
今回はspinnerというのを見つけたので、苦労はしていないが、kivyではdropDownを提供しているので、そちらを選んでいたらハマりそうでした。
次回は、敵にHPを持たせて、HPが0になったら、倒れた判定をして、戦闘画面の終了実装予定
PlayerのHPが0になったら「Game Over」画面を用意する予定

[Github](https://github.com/akeyi2018/RPG_Game)

https://github.com/akeyi2018/RPG_Game
