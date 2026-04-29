# app.py
from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
# forms.pyをimport
from forms import UserInfoForm
# ================
# インスタンス生成
# ================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'

# ================
# ルーティング
# ================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spots")
def spots():
    return render_template("spots.html")

@app.route("/spots/<name>")
def spot_detail(name):
    return f"{name}の詳細" 
    # 上はテスト用本番は下を使用
    # return render_template("spot_detail.html", name=name)

@app.route("/foods")
def foods():
    return render_template("foods.html")

@app.route("/foods/<name>")
def food_detail(name):
    return f"{name}の詳細" 
    # 上はテスト用本番は下を使用
    # return render_template("spot_detail.html", name=name)

@app.route("/course")
def course():
    return render_template("course.html")

@app.route("/map")
def map_course():
    return render_template("partials/map_course.html")

@app.route("/access")
def access():
    return render_template("access.html")

# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     return render_template("contact.html")

# お問い合わせ
# 入力ページ
@app.route('/contact', methods=['GET','POST'])
def contact():
    form = UserInfoForm()

    if form.validate_on_submit():
        return render_template('contact/confirm.html', form=form)

    return render_template('contact/contact.html', form=form)

# 確認 → 完了
@app.route('/contact/result', methods=['POST'])
def result():
    form = UserInfoForm()

    if form.validate_on_submit():
        return render_template('contact/result.html', form=form)

    return redirect(url_for('contact'))


# プライバシー
@app.route("/privacy")
def privacy():
    return render_template("contact/privacy.html")

# @app.route("/")
# def index():
#     return render_template("index.html")

# ================
# 実行
# ================
if __name__ == '__main__':
    app.run(debug=True)