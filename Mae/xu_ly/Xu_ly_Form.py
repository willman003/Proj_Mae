from Mae import app

from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, IntegerField, StringField, PasswordField
from wtforms import form, fields, validators

import flask_login as login

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import sessionmaker

from Mae.xu_ly.Xu_ly_Model import *

Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
dbSession = DBsession()

class Form_mua_hang(FlaskForm):
    so_luong = IntegerField('Nhập số lượng')
    submit = SubmitField('Thêm vào giỏ hàng')

class Form_dang_nhap(FlaskForm):
    ten_dang_nhap = fields.StringField('Tên đăng nhập', [validators.required()])
    password = fields.PasswordField('Mật khẩu', [validators.required()])

    def validate_ten_dang_nhap(self, ten_dang_nhap):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Tên đăng nhập không tồn tại!')
        if not check_password_hash(user.mat_khau_hash, self.password.data):
            raise validators.ValidationError('Mật khẩu không hợp lệ!')
    
    def get_user(self):
        return dbSession.query(Nguoi_dung).filter_by(ten_dang_nhap = self.ten_dang_nhap.data).first()

class Form_dang_ky(FlaskForm):
    ho_ten = fields.StringField('Họ tên:', [validators.required()])
    email = fields.StringField('Email:', [validators.required()])
    ten_dang_nhap = fields.StringField('Tên đăng nhập:', [validators.required()])
    mat_khau = fields.PasswordField('Mật khẩu:',[validators.required()])
    
    def validate_ten_dang_nhap(self, field):
        if dbSession.query(Nguoi_dung).filter_by(ten_dang_nhap = self.ten_dang_nhap.data).count() > 0:
            raise validators.ValidationError('Tên đăng nhập đã được sử dụng!')

def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# Create user loader function
	@login_manager.user_loader
	def load_user(user_id):
		return dbSession.query(Nguoi_dung).get(user_id)




    