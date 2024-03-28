### 本記事の背景
Javascript入門は多くの情報と解説があるが、Jinja2と組合わせで使う場合やグラフ描画用ライブライであるchatjs+Jinja2で使う場合の紹介記事は少ない。筆者は、ある程度Javascriptの基礎文法を習得している人向けにJinja2との組み合わせで注意すべき点や引数の渡し方について焦点を合わせている。
※Jinja2については、以下の記事参照

https://qiita.com/akeyi2018/items/2557911351493aff87a8

jinja2とJavaScriptの組み合わせの事例（chat.jsのData部分にjinja2の構文が書ける）は、以下の記事でも紹介している

https://qiita.com/akeyi2018/items/ba806a89ca852157a591

### 本記事の対象者

- JavaScriptの基礎文法を理解している
- chatjsとはなにかを理解している
- Flaskの基礎を取得している
- HTML/CSSのタグを理解している
- Python基礎文法を理解している
- Webの基本的な仕組みを理解している（localhost,portとはなにかが分かる程度）
※上記で未収得の場合は下記の関連情報を先に参照し、習得、理解してください。

#### 関連情報
- [JavaScript超入門](https://qiita.com/rukukun/items/39bd94377b4b2021e684)（var/let/const解説付)
- [とほほJavascript入門](https://www.tohoho-web.com/js/index.htm)（必要に応じて逆引き）
- [とほほchatjs入門](https://www.tohoho-web.com/ex/chartjs.html)
- [chatjs公式](https://www.chartjs.org/docs/latest/)(chatjsはバージョンによって若干変更されているので、必要に応じて公式ページ参照）
- [chatjs日本語](https://misc.0o0o.org/chartjs-doc-ja/)
- [Flask構築手順](https://qiita.com/akeyi2018/items/0005cebf81c7909db84d)

### HTML内にJavaScriptを記述する場合

- 引き渡しでうまくいかない場合→「tojson」でデータ変換を行う
```html
{{ user_list|tojson }}
```
- 辞書型は「tojson」を付けないで、そのまま引き渡す
```html
datasets: [{
              label: {{ data_label|tojson }},
              data: {{ member_gender.male }},
              stack: 'stack-1',
              }
```

#### HTMLではなく、別途にJavaScriptを記述する場合
- 引き渡しデータをHTML側で用意しておく（グローバル変数）
```html
<script>
    const data = {{user_in | tojson}};
    const user_name = '{{ user_name }}';
</script>
```
- jsの参照設定
```html
<script src="{{url_for('static', filename='post.js')}}"></script>
```
- 呼び出し部分の実装
```html
<button type="button" class="btn btn-primary" onclick="post_data()">データPOST</button>
```

- JavaScript本体(post.js)の実装
```javascript
function post_data() {
  let checkbox = document.getElementById("checked_");
  if (checkbox.checked){
    let res = JSON.stringify(
      data,
      );
    $.ajax(
      {
        type: 'POST',
        url: '/set_user_data',
        data: res,
        contentType: 'application/json',
        success: function(){
          window.location.href = '/payment/' + user_name;
        }
      });
  }else{
    alert('同意にチェックを入れて下さい。')
  }
}
```
上記の例は、
①バックエンドからuser_nameをHTMLへ引き渡す。
②HTML内でグローバル変数の「user_name」を定義する
③post.jsへ引き渡す。
④post.jsでユーザ登録処理を行う
⑤登録処理結果が成功した場合、支払いのページを表示し、urlに「user_name」を引き渡す

バックエンド側で、決済ページに「user_name」を引数で受け取る
```py
@app.route('/payment/<name>')
def payment(name):
    cls = User()
    user = cls.get_user(name)
    user_email = user['email']
    user_kana = user['kana_name']
    return render_template('payment.html', 
        checkout_public_key=stripe_keys['publishable_key'],
        user_kana = user_kana,
        user_email = user_email)
```
        
