from Mae import app
from Mae.xu_ly.Xu_ly_Model import *

from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/',methods=['GET','POST'])
def index():
    danh_sach_category = session.query(Loai_san_pham).all()
    return render_template('Web/index.html', danh_sach_category = danh_sach_category)

@app.route('/cau-chuyen-cua-mae')
def story():
    return render_template('Web/Story.html')

@app.route('/mae-beauty-blog', methods=['GET','POST'])
def beauty_blog():
    return render_template('Web/Beauty_blog.html')

@app.route('/loai_<int:id>',methods=['GET','POST'])
def san_pham(id):
    danh_sach_category = session.query(Loai_san_pham).all()
    loai = session.query(Loai_san_pham).filter(Loai_san_pham.ma_loai == id).one()
    danh_sach_san_pham = session.query(San_pham).filter(San_pham.ma_loai == id).all()
   
    return render_template('Web/Loai_san_pham.html', loai = loai, danh_sach_category = danh_sach_category, danh_sach_san_pham = danh_sach_san_pham, id = id)

@app.route('/sp_<int:ma_sp>',methods = ['GET','POST'])
def chi_tiet_san_pham(ma_sp):
    return render_template('Web/Chi_tiet_san_pham.html')

