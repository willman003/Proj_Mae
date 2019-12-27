from Mae import app

from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, IntegerField, StringField, PasswordField
from wtforms import form, fields, validators

import flask_login as login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker

from Mae.xu_ly.Xu_ly_Model import *
from Mae.xu_ly.Xu_ly import *

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
    gioi_tinh = fields.RadioField('Giới tính:', choices=[('M','Nam'),('F','Nữ')])
    ngay_sinh = fields.StringField('Ngày sinh:', [validators.required()])
    dia_chi = fields.StringField('Địa chỉ:', [validators.required()])
    dien_thoai = fields.StringField('Số điện thoại', [validators.required()])
    
    def validate_ten_dang_nhap(self, ten_dang_nhap):
        if dbSession.query(Nguoi_dung).filter_by(ten_dang_nhap = self.ten_dang_nhap.data).count() > 0:
            raise validators.ValidationError('Tên đăng nhập đã được sử dụng!')
    
    

    def tao_khach_hang(self):
        user = dbSession.query(Nguoi_dung).filter_by(ten_dang_nhap = self.ten_dang_nhap.data).first()
        customer = Khach_hang()
        customer.ma_nguoi_dung = user.ma_nguoi_dung
        customer.ten_khach_hang = self.ho_ten.data
        customer.gioi_tinh = self.gioi_tinh.data
        customer.ngay_sinh = tao_chuoi_ngay(self.ngay_sinh.data)        
        customer.dia_chi = self.dia_chi.data
        customer.dien_thoai = self.dien_thoai.data
        dbSession.add(customer)
        dbSession.commit()
        return

def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# Create user loader function
	@login_manager.user_loader
	def load_user(user_id):
		return dbSession.query(Nguoi_dung).get(user_id)




    