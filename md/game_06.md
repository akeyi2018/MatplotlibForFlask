
### 目標
下記のバトル画面を作成

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/576081/04f9c88a-cf10-a5b5-51e1-ab76f6618cf8.png)

### 要件整理
* 異なる敵の名前と画像
* 戦闘メッセージ
* 物理攻撃、魔法攻撃、逃げるボタンを配置

※物理攻撃、魔法攻撃、逃げるの処理実装は後回し

### kvファイルの使用
* kvファイルを使うためには、kvルールを知る必要がある
```yml
<PopupD>:
    title: root.title
    size_hint: None, None
    size: 800, 750  # Popupウィンドウのサイズを設定

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: content
            orientation: 'horizontal'
        Label:
            text: 'Hero Attack goblin take 10 damages. \n goblin attack hero take 5 damages.'
            font_size: 30
           
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None  # 垂直方向のサイズを固定する
            height: 50
            Button:
                text: 'Physical Attack'
                font_size: 30 
                
            Button:
                text: 'Magical Attack'
                font_size: 30 
                
            Button:
                text: 'escape ...'
                font_size: 30 
                on_release: root.dismiss()  # Popupを閉じる
```
### 重要ポイント
* ListPropertyの使用
→これを使うとList型の変数を渡せるようになる

```py
labels = ListProperty()
images = ListProperty()
```
メインからポップアップ画面（バトル画面）へ渡す側は以下
Enemyの画像と名前をリストで渡す

```py
class MainDisp(Widget):

    def __init__(self, **kwargs):
        super(MainDisp, self).__init__(**kwargs)

    def on_release(self):
        image_paths = [
            './enemy_image/enemy_01.gif',
            './enemy_image/enemy_02.gif',
            './enemy_image/enemy_03.gif'
            ]
        enemy_name_list = ['goblin',
                           'wizard',
                           'Snake Woman'
                        ]
        self.popup = PopupD('battle screen', enemy_name_list, image_paths)
        self.popup.open()
```
バトル画面側
```py
class PopupD(Popup):
    labels = ListProperty()
    images = ListProperty()

    def __init__(self, title, labels, images, **kwargs):
        super(PopupD, self).__init__(**kwargs)
        self.title = title
        self.labels = labels
        self.images = images

    def on_open(self):
        for text, source in zip(self.labels, self.images):
            inner_layout = BoxLayout(orientation='vertical')
            
            label = Label(text=text)
            inner_layout.add_widget(label)
            
            image = Image(source=source)
            inner_layout.add_widget(image)
            self.ids.content.add_widget(inner_layout)
```

このように入れ子構造を構築できて、kvファイル側は、下記のようにすごく簡単になる
```py
inner_layout = BoxLayout(orientation='vertical')

label = Label(text=text)
inner_layout.add_widget(label)

image = Image(source=source)
inner_layout.add_widget(image)
self.ids.content.add_widget(inner_layout)
```
「id: content」がプログラム側が作成したレイアウトID（すでに入れ子になっている）

```yml
BoxLayout:
    id: content
    orientation: 'horizontal'
```
### 感想
kvファイルには時間がかかりました。
※ちなみにバトル画面にはEnemyは少し大きくなってます。

次回は戦闘シーンでメッセージ処理する予定

