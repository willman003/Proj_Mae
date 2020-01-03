from Mae import app

from flask import render_template, redirect, url_for, session

from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin import helpers, expose

from sqlalchemy.orm import sessionmaker

from Mae.xu_ly.Xu_ly_Form import *
from Mae.xu_ly.Xu_ly_Model import *

init_login()

@app.route('/dang-nhap', methods = ['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form_dang_nhap = Form_dang_nhap()
    if form_dang_nhap.validate_on_submit():
        form_dang_nhap.validate_ten_dang_nhap(form_dang_nhap.ten_dang_nhap.data)
        user = form_dang_nhap.get_user()
        login_user(user)
        return redirect(url_for('index'))
        
    return render_template('Quan_ly/MH_Dang_nhap.html', form_dang_nhap = form_dang_nhap)

@app.route('/dang-xuat',methods = ['GET','POST'])
def log_out():
    session.clear()
    login.logout_user()
    return redirect(url_for('index'))

@app.route('/dang-ky', methods = ['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Form_dang_ky()
    
    if form.validate_on_submit():
        form.validate_ten_dang_nhap(form.ten_dang_nhap.data)
        user = Nguoi_dung()
        form.populate_obj(user)
        user.ho_ten = form.ho_ten.data
        user.ten_dang_nhap = form.ten_dang_nhap.data
        user.email = form.email.data
        user.mat_khau_hash = generate_password_hash(form.mat_khau.data)
        user.ma_loai_nguoi_dung = 2
        dbSession.add(user)
        dbSession.commit()
        form.tao_khach_hang()
        login.login_user(user)
        return redirect(url_for('index'))
    
    return render_template('Quan_ly/MH_Dang_ky.html',form = form)

###-----app quản lý
@app.route('/cong-ty/dang-nhap',methods=['GET','POST'])
def dang_nhap():
    form_dang_nhap = Form_dang_nhap()
    if form_dang_nhap.validate_on_submit():
        form_dang_nhap.validate_ten_dang_nhap(form_dang_nhap.ten_dang_nhap.data)
        user = form_dang_nhap.get_user()
        login_user(user)
        return redirect(url_for('admin'))
    return render_template('Quan_ly/MH_Dang_nhap.html', form_dang_nhap = form_dang_nhap)

@app.route('/cong-ty/dang-xuat',methods =['GET','POST'])
def dang_xuat():
    session.clear()
    login.logout_user()
    return redirect(url_for('dang_nhap'))