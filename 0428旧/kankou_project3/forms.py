# forms.py
from wtforms import Form
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,IntegerField,PasswordField,DateField,
    RadioField,SelectField,BooleanField,TextAreaField,
    EmailField,SubmitField
)
from wtforms.validators import DataRequired,Optional
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

# #使用するvalidatorをインポート
# リスト5.14で「ValidationError」を追加
from wtforms.validators import (
    DataRequired,EqualTo,Length,NumberRange,Email,ValidationError
)

def phone_check(form, field):
    value = field.data.replace('-', '')

    if not value.isdigit():
        raise ValidationError('数字のみ入力してください')

    if len(value) not in (10, 11):
        raise ValidationError('電話番号は10桁または11桁です')
    
import re

def zipcode_check(form, field):
    if not re.match(r'^\d{3}-?\d{4}$', field.data):
        raise ValidationError('郵便番号の形式が正しくありません')

def fullwidth_check(form, field):
    if not re.match(r'^[^\x01-\x7E\xA1-\xDF]+$', field.data):
        raise ValidationError('全角で入力してください')
    
def kana_check(form, field):
    if not re.match(r'^[ァ-ヶー]+$', field.data):
        raise ValidationError('カタカナで入力してください')

#Formクラス
#ユーザー情報クラス
class UserInfoForm(FlaskForm):
    #カタログ:チェックボックス

    # カタログ（複数選択）
    catalog = SelectMultipleField(
        '資料請求',
        choices=[
            ('map', '観光イラストマップ'),
            ('guide', '総合ガイドブック')
        ],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    #メッセージ:複数行テキスト
    note = TextAreaField('お問い合わせ内容（500字以内） ',  validators=[Optional(),Length(max=500, message='500文字以内で入力してください')])
    #名前:文字入力
    name = StringField(
    'お名前（全角）',
    validators=[
        DataRequired('名前（全角）は必須入力です'),
        fullwidth_check
    ],
                    render_kw={"placeholder":"(例)山田太郎"}    
    )

    kana = StringField(
        'お名前（フリガナ）',
        validators=[
            DataRequired('名前（カナ）は必須入力です'),
            kana_check
        ],
                    render_kw={"placeholder":"(例)ヤマダタロウ"}
    )
    #郵便番号
    zipcode = StringField(
        '郵便番号',
        validators=[
            DataRequired('郵便番号は入力必須です'),
            zipcode_check
        ]
    )
    #出身地域:セレクトボックス
    PREFECTURES = [
        ('', '都道府県'),
        ('北海道', '北海道'),
        ('青森県', '青森県'),
        ('岩手県', '岩手県'),
        ('宮城県', '宮城県'),
        ('秋田県', '秋田県'),
        ('山形県', '山形県'),
        ('福島県', '福島県'),
        ('茨城県', '茨城県'),
        ('栃木県', '栃木県'),
        ('群馬県', '群馬県'),
        ('埼玉県', '埼玉県'),
        ('千葉県', '千葉県'),
        ('東京都', '東京都'),
        ('神奈川県', '神奈川県'),
        ('新潟県', '新潟県'),
        ('富山県', '富山県'),
        ('石川県', '石川県'),
        ('福井県', '福井県'),
        ('山梨県', '山梨県'),
        ('長野県', '長野県'),
        ('岐阜県', '岐阜県'),
        ('静岡県', '静岡県'),
        ('愛知県', '愛知県'),
        ('三重県', '三重県'),
        ('滋賀県', '滋賀県'),
        ('京都府', '京都府'),
        ('大阪府', '大阪府'),
        ('兵庫県', '兵庫県'),
        ('奈良県', '奈良県'),
        ('和歌山県', '和歌山県'),
        ('鳥取県', '鳥取県'),
        ('島根県', '島根県'),
        ('岡山県', '岡山県'),
        ('広島県', '広島県'),
        ('山口県', '山口県'),
        ('徳島県', '徳島県'),
        ('香川県', '香川県'),
        ('愛媛県', '愛媛県'),
        ('高知県', '高知県'),
        ('福岡県', '福岡県'),
        ('佐賀県', '佐賀県'),
        ('長崎県', '長崎県'),
        ('熊本県', '熊本県'),
        ('大分県', '大分県'),
        ('宮崎県', '宮崎県'),
        ('鹿児島県', '鹿児島県'),
        ('沖縄県', '沖縄県'),
    ]
    area = SelectField('都道府県: ', choices=PREFECTURES,  validators=[DataRequired('都道府県を選択してください')])
#:複数行テキスト
    address = TextAreaField('住所', validators=[DataRequired('住所は入力必須です')])
    #パスワード：パスワード入力
    password = PasswordField('パスワード: ',validators=[Length(1, 10 ,'パスワードの長さは1文字以上10文字以内です'),
                                                DataRequired('パスワードは入力必須です'),
                                                EqualTo('confirm_password','パスワードが一致しません')])
    #確認用:パスワード入力
    confirm_password = PasswordField('パスワード確認: ',validators=[DataRequired('入力必須です')])
    #Email:メールアドレス入力
    email = EmailField('メールアドレス:',validators=[DataRequired('メールアドレスは入力必須です'),Email('メールアドレスのフォーマットではありません')])
    #電話番号
    tel = StringField(
        '電話番号',
        validators=[
            Optional(),
            phone_check
        ]
    )

    agree = BooleanField(
        'プライバシーポリシーに同意する',
        validators=[DataRequired(message='同意が必要です')]
    )
    #ボタン
    submit = SubmitField('送信')

    #  ▼▼▼ リスト5.14で追加 ▼▼▼ 
    # カスタムバリデータ
    # 英数字と記号が含まれているかチェックする
    def validate_password(self, password):
        if not(any(c.isalpha() for c in password.data)and \
            any(c.isdigit()for c in password.data)and \
                any(c in '!@#$%^&*()'for c in password.data)):
            raise ValidationError('パスワードには【英数字と記号:!@#$%^&*()】を含める必要があります')
    #  ▲▲▲ リスト5.14で追加 ▲▲▲ 