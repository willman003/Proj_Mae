from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, IntegerField, StringField, PasswordField

class Form_mua_hang(FlaskForm):
    so_luong = IntegerField('Nhập số lượng')
    submit = SubmitField('Thêm vào giỏ hàng')

class Form_dang_nhap(FlaskForm):
    ten_dang_nhap = StringField('Tên đăng nhập', validators=[ValueRequired()])
    password = PasswordField('Mật khẩu')
    submit = SubmitField('Đăng nhập')