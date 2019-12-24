from Mae import app

from Mae.xu_ly.Xu_ly_Model import *
from Mae.xu_ly.Xu_ly import *
from Mae.xu_ly.Xu_ly_Form import *

from flask import Flask, render_template, Markup, session
from sqlalchemy.orm import sessionmaker

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
db_session = DBSession()

@app.route('/',methods=['GET','POST'])
def index():
       
    danh_sach_category = db_session.query(Loai_san_pham).all()
    
    return render_template('Web/index.html', danh_sach_category = danh_sach_category)

@app.route('/cau-chuyen-cua-mae')
def story():
    return render_template('Web/Story.html')

@app.route('/mae-beauty-blog', methods=['GET','POST'])
def beauty_blog():
    return render_template('Web/Beauty_blog.html')

@app.route('/loai_<int:id>',methods=['GET','POST'])
def san_pham(id):
    danh_sach_category = db_session.query(Loai_san_pham).all()
    loai = db_session.query(Loai_san_pham).filter(Loai_san_pham.ma_loai == id).one()
    danh_sach_san_pham = db_session.query(San_pham).filter(San_pham.ma_loai == id).all()
   
    return render_template('Web/Loai_san_pham.html', loai = loai, danh_sach_san_pham = danh_sach_san_pham, id = id, danh_sach_category = danh_sach_category)

@app.route('/chi-tiet/sp_<int:ma_sp>',methods = ['GET','POST'])
def chi_tiet_san_pham(ma_sp):
    form_mua_hang = Form_mua_hang()

    danh_sach_category = db_session.query(Loai_san_pham).all()
    san_pham = db_session.query(San_pham).filter(San_pham.ma_san_pham == ma_sp).one()
    mo_ta_dai = Markup(san_pham.mo_ta_chi_tiet.split('——————————')[0])
    
    chuoi_bo_tag_html = remove_tags(san_pham.mo_ta_chi_tiet)
    chuoi_temp_1 = chuoi_bo_tag_html.split('❖')
    thong_bao = ''
    
    if len(chuoi_temp_1) >1:
        chi_tiet = {}
        chi_tiet['xuat_xu'] = chuoi_temp_1[1]
        chi_tiet['dung_tich'] = chuoi_temp_1[2]
    else:
        chi_tiet = ''
                
    return render_template('Web/Chi_tiet_san_pham.html', form_mua_hang = form_mua_hang, mo_ta_dai = mo_ta_dai, chi_tiet = chi_tiet, san_pham = san_pham, danh_sach_category = danh_sach_category)

