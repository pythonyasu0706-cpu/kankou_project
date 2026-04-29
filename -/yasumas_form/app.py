from flask import Flask, render_template,request
from flask_wtf import FlaskForm

# インスタンス生成
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'

# ルーティング
from forms import UserInfoForm

# ユーザー情報：入力
@app.route('/',methods=['GET','POST'])
def show_enter():
    #フォームの作成
    form = UserInfoForm(request.form)
    #POST
    if request.method == "POST" and form.validate():
        return render_template('result.html', form=form)
    #POST以外と「form.validate()がfalse」
    return render_template('enter2.html',form=form)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/")
def index():
    return render_template("index.html")

# 実行
if __name__ == '__main__':
    app.run(debug=True)
