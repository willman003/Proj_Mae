from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()

# from Mae import app, db



#------CLASS cho Web bán hàng------#

class Loai_san_pham(Base):
    __tablename__ = 'loai_san_pham'
    ma_loai = Column(Integer, nullable = False, primary_key = True)
    ten_loai = Column(String(50), nullable = False)
    mo_ta = Column(Text)
    
    def __str__(self):
        return self.ten_loai

class San_pham(Base):
    __tablename__ = 'san_pham'
    ma_san_pham = Column(Integer, nullable = False, primary_key = True)
    ten_san_pham = Column(String(100), nullable = False)
    ma_loai = Column(Integer, ForeignKey('loai_san_pham.ma_loai'))
    gia_ban = Column(Integer, nullable = False, default = 0)
    gia_nhap = Column(Integer, nullable = False)
    so_luong_ton = Column(Integer, nullable = False, default = 0)
    don_vi_tinh = Column(String(20), nullable = False, default = 'Cái')
    hinh_anh = Column(String(100), nullable = False)
    id_sendo = Column(Integer)
    sku_sendo = Column(String(100))
    thuoc_tinh = Column(String(200))
    mo_ta_tom_tat = Column(Text)
    mo_ta_chi_tiet = Column(Text)
    loai_san_pham = relationship(Loai_san_pham, backref='san_pham')
    def __str__(self):
        return self.ten_san_pham

class Loai_nguoi_dung(Base):
    __tablename__ = 'loai_nguoi_dung'
    ma_loai_nguoi_dung = Column(Integer, nullable = False, primary_key = True)
    ten_loai_nguoi_dung = Column(String(100), nullable = False)
    def __str__(self):
        return self.ten_loai_nguoi_dung


class Nguoi_dung(Base):
    __tablename__ = 'nguoi_dung'
    ma_nguoi_dung = Column(Integer, nullable = False, primary_key = True)
    ma_loai_nguoi_dung = Column(Integer, ForeignKey('loai_nguoi_dung.ma_loai_nguoi_dung'))
    ho_ten = Column(String(100), nullable = False)
    email = Column(String(120), nullable = False)
    ten_dang_nhap = Column(String(64), nullable = False)
    mat_khau_hash = Column(String(128), nullable = False)
    ngay_dang_ky = Column(Date)
    lan_dang_nhap_cuoi = Column(DateTime)
    dang_hoat_dong = Column(Integer, nullable = False, default = 0)
    loai_nguoi_dung = relationship(Loai_nguoi_dung,backref='nguoi_dung')

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.ma_nguoi_dung

    def __unicode__(self):
        return self.ho_ten

class Khach_hang(Base):
    __tablename__ = 'khach_hang'
    ma_khach_hang = Column(Integer, nullable = False, primary_key = True)
    ma_nguoi_dung = Column(Integer, ForeignKey('nguoi_dung.ma_nguoi_dung'))
    ten_khach_hang = Column(String(100), nullable = False)
    gioi_tinh = Column(String(1), nullable = False)
    ngay_sinh = Column(Date, nullable = False)
    dia_chi = Column(String(200), nullable = False)
    dien_thoai = Column(String(20), nullable = False)
    nguoi_dung = relationship(Nguoi_dung, backref = 'khach_hang')
    def __str__(self):
        return self.ten_khach_hang

class Hoa_don(Base):
    __tablename__ = 'hoa_don'
    ma_hoa_don = Column(Integer, nullable = False, primary_key = True)
    ngay_tao_hoa_don = Column(Date, nullable = False)
    ma_khach_hang = Column(Integer, ForeignKey('khach_hang.ma_khach_hang'))
    tong_tien = Column(Float, nullable = False)
    dia_chi_giao_hang = Column(String(200), nullable = False)
    so_dien_thoai_nguoi_nhan = Column(String(50), nullable = False)
    khach_hang = relationship(Khach_hang, backref = 'hoa_don')
    def get_id(self):
        return self.ma_hoa_don

class Don_hang(Base):
    __tablename__ = 'don_hang'
    so_thu_tu = Column(Integer, nullable =False, primary_key = True)
    ma_hoa_don = Column(Integer, ForeignKey('hoa_don.ma_hoa_don'))
    ma_san_pham = Column(Integer, ForeignKey('san_pham.ma_san_pham'))
    so_luong = Column(Integer, nullable = False)
    don_gia = Column(Integer, ForeignKey('san_pham.gia_ban'))
    hoa_don = relationship(Hoa_don, backref = 'don_hang', foreign_keys=[ma_hoa_don])
    san_pham = relationship(San_pham, backref = 'don_hang', foreign_keys=[ma_san_pham])
    
    def get_id(self):
        return self.ma_hoa_don

class Loai_bai_viet(Base):
    __tablename__ = 'loai_bai_viet'
    ma_loai_bai_viet = Column(Integer, nullable = False, primary_key = True)
    ten_loai_bai_viet = Column(String(200), nullable = False)
    mo_ta = Column(String(200))
    def __str__(self):
        return self.ten_loai_bai_viet

class Bai_viet(Base):
    __tablename__ = 'bai_viet'
    ma_bai_viet = Column(Integer, nullable = False, primary_key = True)
    ma_loai_bai_viet = Column(Integer, ForeignKey('loai_bai_viet.ma_loai_bai_viet'))
    tieu_de = Column(String(200), nullable = False)
    noi_dung_tom_tat = Column(Text)
    noi_dung_chi_tiet = Column(Text, nullable = False)
    hinh_anh_bai_viet = Column(String(100))
    ngay_tao_bai_viet = Column(DateTime, nullable = False)
    nguon_tham_khao = Column(String(200))
    loai_bai_viet = relationship(Loai_bai_viet, backref = 'bai_viet')
    def __str__(self):
        return self.tieu_de


# class User(db.Model):
#     	__tablename__='user'
# 	id = db.Column(db.Integer, primary_key=True)
# 	first_name = db.Column(db.String(100), nullable = False)
# 	last_name = db.Column(db.String(100), nullable = False)
# 	ma_loai_nguoi_dung = db.Column(db.Integer, db.ForeignKey('bs_loai_nguoi_dung.ma_loai_nguoi_dung')) 
# 	loai_nguoi_dung = db.relationship(bs_loai_nguoi_dung, backref=db.backref('user', lazy=True))
# 	login = db.Column(db.String(80), unique=True, nullable = False)
# 	email = db.Column(db.String(120))
# 	password = db.Column(db.String(64), nullable = False)

# 	@property
# 	def is_authenticated(self):
# 		return True

# 	@property
# 	def is_active(self):
# 		return True

# 	@property
# 	def is_anonymous(self):
# 		return False

# 	def get_id(self):
# 		return self.id

# 	# Required for administrative interface
# 	def __unicode__(self):
# 		return self.last_name


#----------CLASS cho Quản lý Store--------#
class Dot_khuyen_mai(Base):
    __tablename__ = 'dot_khuyen_mai'
    ma_dot_khuyen_mai = Column(Integer, nullable = False, primary_key = True)
    ten_dot_khuyen_mai = Column(String(200), nullable = False)
    noi_dung_dot_khuyen_mai = Column(Text, nullable = False)
    ngay_bat_dau = Column(Date, nullable = False)
    ngay_ket_thuc = Column(Date, nullable = False)
    hinh_dot_khuyen_mai = Column(String(100), nullable = False)
    def __str__(self):
        return self.ten_dot_khuyen_mai 

class San_pham_khuyen_mai(Base):
    __tablename__ = 'san_pham_khuyen_mai'
    so_thu_tu = Column(Integer, nullable=False, primary_key=True)
    ma_dot_khuyen_mai = Column(Integer, ForeignKey('dot_khuyen_mai.ma_dot_khuyen_mai')) 
    ma_san_pham = Column(Integer, ForeignKey('san_pham.ma_san_pham'))
    ma_loai = Column(Integer, ForeignKey('loai_san_pham.ma_loai'))
    gia_khuyen_mai = Column(Float, nullable = False)
    hinh_anh = Column(String(100), nullable = False)
    khuyen_mai = relationship(San_pham, backref = 'san_pham_khuyen_mai')
    code_khuyen_mai = relationship(Dot_khuyen_mai, backref = "code_khuyen_mai")
    def __str__(self):
        return self.ma_san_pham

engine = create_engine('sqlite:///Mae/du_lieu/ql_mae.db?check_same_thread=False')
Base.metadata.create_all(engine)

print('Done!')

