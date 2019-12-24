from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, IntegerField

class Form_mua_hang(FlaskForm):
    so_luong = IntegerField('Nhập số lượng')
    submit = SubmitField('Thêm vào giỏ hàng')