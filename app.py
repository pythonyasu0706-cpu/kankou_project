# app.py
from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
# forms.pyをimport
from forms import UserInfoForm
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from db import get_db_connection
import os

# Flozen-Flask
# from flask_frozen import Freezer
# ================
# インスタンス生成
# ================
app = Flask(__name__)
# flozen-flask
# freezer = Freezer(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['API_KEY'] = os.environ.get('API_KEY')

# ================
# ルーティング
# ================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spots")
def spots():

    spots = [
        {
            "title": "大濠公園",
            "text": "福岡市中央区にある大きな池を中心とした公園。散歩やランニングコースとして人気があり、自然を感じながらゆったり過ごすことができます。",
            "image": "spot/ohorikouen.jpg",
            "alt": "大濠公園1",
            "lat": 33.58650763843376,
            "lon": 130.3765841848311,
            "weather_id": "ohori-weather"
        },
        {
            "title": "福岡タワー",
            "text": "選び抜かれた新鮮な牛もつと、甘みを増した野菜が共演する滋味深い味わい。素材の旨みが溶け出した秘伝のスープが、二人の心と身体を芯から温めてくれます。",
            "image": "spot/momochihama.jpg",
            "alt": "福岡タワー1",
            "lat": 33.593644949724855,
            "lon": 130.35168524200876,
            "weather_id": "fukuokatower-weather"
        },
        {
            "title": "太宰府天満宮",
            "text": "学問の神様・菅原道真を祀る神社。受験シーズンには多くの参拝客が訪れ、周辺では名物の梅ヶ枝餅も楽しめます。",
            "image": "spot/dazaifutenmangu.jpg",
            "alt": "太宰府天満宮1",
            "lat": 33.52178626549702,
            "lon": 130.5348432124952,
            "weather_id": "dazaifu-weather"

        }
    ]

    spots_gallery = [
        {"image": "spot/dontaku.jpg", "alt": "スポット2"},
        {"image": "spot/jazz.jpg", "alt": "スポット3"},
        {"image": "spot/kushdajinjya.jpg", "alt": "スポット4"},
        {"image": "spot/maidurukouen.jpg", "alt": "スポット5"},
        {"image": "spot/marineworld.jpg", "alt": "スポット6"},
        {"image": "spot/nakasu.jpg", "alt": "スポット7"},
        {"image": "spot/nemophila.jpg", "alt": "スポット8"},
        {"image": "spot/nishinakasu.jpg", "alt": "スポット9"},
        {"image": "spot/tenjinNishikouoen.jpg", "alt": "スポット10"}
    ]

    return render_template(
        "spots.html", 
        spots=spots,
        # API_KEY=os.environ.get("API_KEY"),
        gallery=spots_gallery,
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "スポット"}
        ]
    )

@app.route("/spots/<name>")
def spot_detail(name):
    return f"{name}の詳細" 
    # 上はテスト用本番は下を使用
    # return render_template("spot_detail.html", name=name)

@app.route("/foods")
def foods():
    foods = [
        {
            "title": "博多ラーメン",
            "text": "丹念に炊き上げた豚骨スープは、見た目以上にクリーミーで奥深い味わい。博多ならではの「替え玉」で、最後の一口まで自分流の楽しみ方を。",
            "image": "food/ramen01.jpg",
            "alt": "ラーメン1"
        },
        {
            "title": "もつ鍋",
            "text": "選び抜かれた新鮮な牛もつと、甘みを増した野菜が共演する滋味深い味わい。素材の旨みが溶け出した秘伝のスープが、二人の心と身体を芯から温めてくれます。",
            "image": "food/motsunabe01.jpg",
            "alt": "もつ鍋"
        },
        {
            "title": "明太子",
            "text": "弾けるような粒立ちと、奥深い旨みのあとにくる心地よい刺激。炊き立ての白米にはもちろん、お酒の肴としても愛され続ける福岡が誇る至福の逸品。",
            "image": "food/mentai01.jpg",
            "alt": "明太子"
        }
    ]

    foods_gallery = [
        {"image": "food/ramen02.jpg", "alt": "グルメ2"},
        {"image": "food/ramen03.jpg", "alt": "グルメ3"},
        {"image": "food/ramen5000yen.jpg", "alt": "グルメ4"},
        {"image": "food/motsunabe02.jpg", "alt": "グルメ5"},
        {"image": "food/motsunabe03.jpg", "alt": "グルメ6"},
        {"image": "food/motsunabe04.jpg", "alt": "グルメ7"},
        {"image": "food/mentai02.jpg", "alt": "グルメ8"},
        {"image": "food/mentai03.jpg", "alt": "グルメ9"},
        {"image": "food/mentai04.jpg", "alt": "グルメ10"}
    ]

    return render_template(
        "foods.html", 
        foods=foods, 
        gallery=foods_gallery,
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "グルメ"}
        ]
    )

@app.route("/foods/<name>")
def food_detail(name):
    return f"{name}の詳細" 
    # 上はテスト用本番は下を使用
    # return render_template("spot_detail.html", name=name)

@app.route("/course")
def course():
    return render_template("" \
    "course.html",
    breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "モデルコース"}
        ]
    )

@app.route("/course/detail")
def course_detail():
    return render_template(
        "course_detail.html",
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "モデルコース", "url": url_for("course")},
            {"label": "コースの詳細"}
        ]
    )

@app.route("/access")
def access():
    return render_template(
        "access.html",
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "アクセス"}
        ]
    )

# お問い合わせ
# 入力ページ
@app.route('/contact', methods=['GET','POST'])
def contact():
    form = UserInfoForm()


    if form.validate_on_submit():
        return render_template('contact/confirm.html', form=form)


    return render_template(
        'contact/contact.html',
        form=form,
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "お問い合わせフォーム"}
        ]
    )


# 確認
@app.route('/contact/confirm', methods=['POST'])
def confirm():
    form = UserInfoForm()
    if not form.validate_on_submit():
        return redirect(url_for('contact'))


    return render_template('contact/confirm.html', form=form)


# メール送信
@app.route('/contact/send', methods=['POST'])
def send():
    form = UserInfoForm()


    if not form.validate_on_submit():
        return redirect(url_for('contact'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacts (name, email, tel, address, title, note, catalog)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        form.name.data,
        form.email.data,
        form.tel.data,
        form.address.data,
        form.title.data,
        form.note.data,
        ','.join(form.catalog.data) if form.catalog.data else None
    ))

    conn.commit()
    conn.close()


    # 管理者宛
    msg = MIMEText(f"""
-------------------------
資料請求: {', '.join(form.catalog.data) if form.catalog.data else 'なし'}
件名: {form.title.data}
お名前: {form.name.data}
メール: {form.email.data}
電話番号: {form.tel.data}
住所: {form.address.data}
お問い合わせ内容:
{form.note.data}
-------------------------
""")
    msg['Subject'] = 'お問い合わせ受信'
    msg['From'] = os.environ.get("EMAIL_USER")
    msg['To'] = 's10ak025@gmail.com'


    # 自動返信
    reply = MIMEText(f"""
{form.name.data} 様


このたびは福岡観光協会のお問い合わせフォームより
お問い合わせいただきありがとうございます。


以下の内容で受け付けました。


-------------------------
資料請求: {', '.join(form.catalog.data) if form.catalog.data else 'なし'}
件名: {form.title.data}
お問い合わせ内容:
{form.note.data}
-------------------------


内容を確認のうえ、担当者より順次ご返信させていただきます。
なお、内容によってはご返信まで数日いただく場合がございます。




あらかじめご了承くださいますようお願い申し上げます。




────────────────────
福岡観光協会
お問い合わせ窓口（自動返信メール）
────────────────────
""")


    reply['Subject'] = '【福岡観光協会】お問い合わせ受付完了'
    reply['From'] = os.environ.get("EMAIL_USER")
    reply['To'] = form.email.data


    try:
        email_user = os.environ.get("EMAIL_USER")
        email_pass = os.environ.get("EMAIL_PASS")


        if not email_user or not email_pass:
            return "メール設定が不足しています"


        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as smtp:
            smtp.ehlo()      # サーバーに挨拶
            smtp.starttls()  # 通信の暗号化（必須）
            smtp.ehlo()      # 暗号化後にもう一度挨拶
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            smtp.send_message(reply)


    except Exception as e:
        print(f"Mail Error: {e}")
        # 本来はここでユーザーにエラーを表示するなどの処理
        return "メール送信に失敗しました。設定を確認してください。"


    return redirect(url_for('result'))


# 完了
@app.route('/contact/result')
def result():
    return render_template('contact/result.html')


# プライバシー
@app.route("/privacy")
def privacy():
    return render_template(
        "contact/privacy.html",
        breadcrumb_items=[
            {"label": "Home", "url": url_for("index")},
            {"label": "お問い合わせフォーム", "url": url_for("contact")},
            {"label": "プライバシーポリシー"}
        ]
    )

# データ保存
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    contacts = cursor.fetchall()

    conn.close()
    return render_template("admin.html", contacts=contacts)

# データ削除
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    conn.commit()

    conn.close()
    return redirect(url_for("admin"))

# ================
# 実行
# ================
if __name__ == '__main__':
    # freezer.freeze()
    # with app.app_context():
    #     from init_db import create_table
    #     create_table()
    # app.run(debug=True, port=5001)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
