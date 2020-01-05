from Mae import app

from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import flask_admin as admin

from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy import exc
from flask_sqlalchemy import Pagination

from flask_sqlalchemy import BaseQuery

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
        return super(MyAdminIndexView, self).render('admin/index.html')

class admin_view(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_export = False

class san_pham_view(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_export = False
    page_size = 10
    column_list = ('ma_san_pham','ten_san_pham','ma_loai', 'gia_ban','gia_nhap', 'so_luong_ton', 'hinh_anh')
    column_labels ={
        'ma_san_pham':'Mã sản phẩm',
        'ten_san_pham':'Tên sản phẩm',
        'ma_loai':'Mã loại',
        'gia_ban':'Giá bán',
        'gia_nhap':'Giá nhập',
        'so_luong_ton': 'Số lượng tồn'
        ,'hinh_anh':'Hình ảnh'
    }



@app.route('/cong-ty',methods=['GET','POST'])
def admin():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    dia_chi_frame = ''
    if request.form.get('Th_Ma_so'):
        man_hinh = request.form.get('Th_Ma_so')
        if man_hinh == "QL_Don_hang":
            dia_chi_frame = "/QL-don-hang"
        elif man_hinh == "QL_Kho":
            dia_chi_frame = "/QL-kho"
        elif man_hinh == "QL_Doanh_thu":
            dia_chi_frame = "/Ql-doanh-thu"
        elif man_hinh == "Admin":
            dia_chi_frame = "/admin"
        

    return render_template('Quan_ly/MH_Chinh.html', dia_chi_frame = dia_chi_frame)

@app.route('/QL-don-hang', methods = ['GET','POST'])
def ql_don_hang():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    today = datetime.now()
    ngay_hom_nay = today.date()
    hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ngay_tao_hoa_don == ngay_hom_nay).all()
    tieu_de = 'Đơn hàng ngày hôm nay'
    dia_chi = ''
    if request.form.get('Th_hoa_don'):
        dieu_khien = request.form.get('Th_hoa_don')
        if dieu_khien == 'All':
            dia_chi = '/QL-don-hang/all/1'
        elif dieu_khien == 'TimKiem':
            dia_chi = '/QL-don-hang/ma-hoa-don'
        elif dieu_khien == 'TheoNgay':
            dia_chi ='/QL-don-hang/theo-ngay/1'
    return render_template('Quan_ly/MH_QL_don_hang.html', hoa_don = hoa_don, tieu_de = tieu_de, dia_chi = dia_chi)

@app.route('/QL-don-hang/all/<int:page>', methods=['GET'])
def ql_don_hang_all(page=1):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    query = BaseQuery(Hoa_don, dbSession)
    page_filter = query.paginate(page,10,False)
    
    tieu_de = 'Tất cả đơn hàng'
    return render_template('Quan_ly/QL_don_hang/QL_don_hang_all.html',page_filter = page_filter, tieu_de = tieu_de)

@app.route('/QL-don-hang/ma-hoa-don', methods=['GET','POST'])
def ql_don_hang_ma_hd():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_QL_don_hang()
    hoa_don = []
    tieu_de = ''
    if form.validate():
        ma_hd = form.ma_hoa_don_tim_kiem.data
        hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ma_hoa_don == ma_hd).all()
        if len(hoa_don)==0:
            tieu_de = "Không tìm thấy mã hóa đơn"
        else:
            tieu_de = "Đơn hàng số " + str(ma_hd)

    return render_template('Quan_ly/QL_don_hang/QL_don_hang_theo_ma_hd.html', form = form, hoa_don = hoa_don,  tieu_de = tieu_de)

@app.route('/QL-don-hang/theo-ngay/<int:page>', methods=['GET','POST'])
def ql_don_hang_theo_ngay(page):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_QL_don_hang()
    tieu_de = 'Đơn hàng ngày hôm nay'
    today = datetime.now()
    # hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ngay_tao_hoa_don == today.date()).all()

    query = BaseQuery(Hoa_don, dbSession)
    page_filter = query.filter(Hoa_don.ngay_tao_hoa_don == today.date()).paginate(page,5,False)
    

    if request.method == 'POST':
        ngay_tim_kiem = form.ngay_tim_kiem.data
        # hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ngay_tao_hoa_don == ngay_tim_kiem).all()
        query = BaseQuery(Hoa_don, dbSession)
        page_filter = query.filter(Hoa_don.ngay_tao_hoa_don == ngay_tim_kiem).paginate(page,5,False)
        if page_filter.total==0:
            tieu_de = "Không tìm thấy hóa đơn"

        else:
            tieu_de = "Đơn hàng của ngày " + str(ngay_tim_kiem.day) + " tháng " +str(ngay_tim_kiem.month)+ " năm " +str(ngay_tim_kiem.year)
    
    
    return render_template('Quan_ly/QL_don_hang/QL_don_hang_theo_ngay.html', page_filter = page_filter,form = form, tieu_de = tieu_de)

@app.route("/QL-don-hang/hoa-don/hd_<int:ma_hd>", methods = ['GET','POST'])
def xem_hoa_don(ma_hd):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    
    hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ma_hoa_don == ma_hd).first()
    don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == ma_hd).all()
    khach_hang = dbSession.query(Khach_hang).filter(Khach_hang.ma_khach_hang == hoa_don.ma_khach_hang).first()
    lst_temp = []
    for item in don_hang:
        san_pham = {}
        san_pham['ma_sp'] = item.ma_san_pham
        san_pham['ten_sp'] = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item.ma_san_pham).first()
        san_pham['don_gia'] = int(item.don_gia.split(',')[0])*1000
        lst_temp.append(san_pham)
    tong_tien = "{:,}".format(int(hoa_don.tong_tien))
    return render_template('Quan_ly/QL_don_hang/QL_don_hang_chi_tiet.html', hoa_don = hoa_don, don_hang = don_hang, khach_hang = khach_hang, lst_temp =lst_temp, tong_tien = tong_tien)

@app.route("/QL-kho", methods = ['GET','POST'])
def ql_kho():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    dia_chi = ''
    if request.method == 'POST':
        dieu_khien = request.form.get('Th_kho_hang')
        if dieu_khien == 'Import':
            dia_chi = '/QL-kho/nhap-hang'
        elif dieu_khien == 'SoLuongTon':
            dia_chi = '/QL-kho/ton-kho'
       
    return render_template('Quan_ly/QL_kho_hang/MH_QL_kho_hang.html', dia_chi = dia_chi)

@app.route('/QL-kho/nhap-hang',methods=['GET','POST'])
def ql_kho_nhap():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_tim_kiem()
    san_pham= []
    if request.method == 'POST':
        tim_kiem = form.noi_dung.data
        if tim_kiem.isdigit():
            san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == tim_kiem).all()
        else:
            chuoi_truy_van = '%'+tim_kiem.upper()+'%'
            san_pham = dbSession.query(San_pham).filter(San_pham.ten_san_pham.like(chuoi_truy_van)).all()

    return render_template('Quan_ly/QL_kho_hang/Nhap_hang.html', form=form, san_pham = san_pham)

@app.route('/QL-kho/ton-kho',methods = ['GET','POST'])
def ql_kho_so_luong():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_tim_kiem()
    san_pham= []
    if request.method == 'POST':
        tim_kiem = form.noi_dung.data
        if tim_kiem.isdigit():
            san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == tim_kiem).all()
        else:
            chuoi_truy_van = '%'+tim_kiem.upper()+'%'
            san_pham = dbSession.query(San_pham).filter(San_pham.ten_san_pham.like(chuoi_truy_van)).all()
    # san_pham = dbSession.query(San_pham).all()
    # for item in san_pham:
    #     item.so_luong_ton += 10
    #     dbSession.add(item)
    #     dbSession.commit()
    return render_template('Quan_ly/QL_kho_hang/Ton_kho.html', form=form, san_pham = san_pham)

@app.route('/QL-kho/nhap/sp_<int:ma_sp>', methods= ['GET','POST'])
def nhap_san_pham(ma_sp):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_nhap_hang()
    san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == ma_sp).first()
    chuoi_thong_bao = ''
    if request.method == 'POST':
        so_luong_nhap = form.so_luong_nhap.data
        san_pham.so_luong_ton += so_luong_nhap
        dbSession.add(san_pham)
        dbSession.commit()
        chuoi_thong_bao = "Đã thêm " + str(so_luong_nhap) + " "+ san_pham.ten_san_pham + " vào kho hàng"
    return render_template('Quan_ly/QL_kho_hang/Chi_tiet_nhap_hang.html', chuoi_thong_bao = chuoi_thong_bao, form = form, san_pham = san_pham)


init_login()
admin = Admin(app, name = "Admin", index_view=MyAdminIndexView(name="Admin"), template_mode='bootstrap3')
admin.add_view(admin_view(Loai_san_pham, dbSession, 'Loại sản phẩm'))
admin.add_view(san_pham_view(San_pham, dbSession, 'Sản phẩm'))
admin.add_view(ModelView(Dot_khuyen_mai, dbSession, 'Đợt khuyến mãi'))
admin.add_view(ModelView(San_pham_khuyen_mai, dbSession, 'Sản phẩm khuyến mãi'))
admin.add_view(admin_view(Loai_nguoi_dung, dbSession, 'Loại người dùng'))
admin.add_view(admin_view(Nguoi_dung, dbSession, 'Người dùng'))
