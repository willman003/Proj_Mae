from Mae import app

from flask import Flask, render_template, redirect, url_for, request, session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import flask_admin as admin

from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy import exc

from Mae.xu_ly.Xu_ly_Model import *
from Mae.xu_ly.Xu_ly_Form import *

configure_mappers()
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbSession = DBSession()

class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('dang_nhap'))
        return super(MyAdminIndexView, self).render('Quan_ly/manage_master.html')


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
    return redirect(url_for('index'))

@app.route('/cong-ty',methods=['GET','POST'])
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('dang_nhap'))
    dia_chi_frame = ''
    if request.form.get('Th_Ma_so'):
        man_hinh = request.form.get('Th_Ma_so')
        if man_hinh == "QL_Don_hang":
            dia_chi_frame = "/QL-don-hang"
        elif man_hinh == "QL_Kho":
            dia_chi_frame = "QL-kho"
        elif man_hinh == "QL_Doanh_thu":
            dia_chi_frame = "/Ql-doanh-thu"
        elif man_hinh == "Admin":
            dia_chi_frame = "/admin"
        print(dia_chi_frame)

    return render_template('Quan_ly/MH_Chinh.html', dia_chi_frame = dia_chi_frame)

init_login()
admin = Admin(app, name = "Admin", index_view=MyAdminIndexView(name="Admin"), base_template='Quan_ly/manage_master.html', template_mode='bootstrap3')
admin.add_view(ModelView(Loai_san_pham, dbSession))