from Mae import app

from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, session, flash

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import flask_admin as admin

from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy import exc,asc,desc
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
        elif dieu_khien == 'TheoTrangThai':
            dia_chi = '/QL-don-hang/theo-trang-thai/page_1'
        
    return render_template('Quan_ly/MH_QL_don_hang.html', hoa_don = hoa_don, tieu_de = tieu_de, dia_chi = dia_chi)

@app.route('/QL-don-hang/all/<int:page>', methods=['GET'])
def ql_don_hang_all(page=1):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    query = BaseQuery(Hoa_don, dbSession)
    page_filter = query.order_by(desc(Hoa_don.ngay_tao_hoa_don)).paginate(page,10,False)
    
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
    ngay_tim_kiem = today.date()
        
    if session.get('ngay_tim_kiem'):
        temp_1 = datetime.strptime(session['ngay_tim_kiem'],"%a, %d %b %Y %H:%M:%S %Z")
        ngay_tim_kiem = temp_1.date()
    if form.validate_on_submit():
        ngay_tim_kiem = form.ngay_tim_kiem.data
        
        session['ngay_tim_kiem'] = ngay_tim_kiem
       
        page = 1
    
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
    form = Form_huy_don_hang()
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
    thoi_diem_huy = ''
    li_do_huy = ''
    if hoa_don.trang_thai == 2:
        ghi_chu = hoa_don.ghi_chu
        chuoi_xu_ly_1 = ghi_chu.split("|")
        chuoi_xu_ly_2 = chuoi_xu_ly_1[1]
        chuoi_xu_ly = chuoi_xu_ly_2.split(',')
        thoi_diem_huy = chuoi_xu_ly[1]
        li_do_huy = chuoi_xu_ly[2]
    return render_template('Quan_ly/QL_don_hang/QL_don_hang_chi_tiet.html', thoi_diem_huy = thoi_diem_huy, li_do_huy = li_do_huy, form = form, hoa_don = hoa_don, don_hang = don_hang, khach_hang = khach_hang, lst_temp =lst_temp, tong_tien = tong_tien)

@app.route("/QL-don-hang/theo-trang-thai/page_<int:id>",methods=['GET','POST'])
def xem_hd_theo_trang_thai(id):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_lua_chon()
    query = BaseQuery(Hoa_don, dbSession)
    trang_thai = 0
    
    if session.get('trang_thai'):
        trang_thai = session['trang_thai']
    
    if form.validate_on_submit():
        trang_thai = int(form.lua_chon.data)
        session['trang_thai'] = trang_thai
        id = 1
    if trang_thai == 0:
        tieu_de = 'Chưa thanh toán'
    elif trang_thai == 1:
        tieu_de = 'Đã thanh toán'
    elif trang_thai == 2:
        tieu_de = 'Huỷ'
    page_filter = query.filter(Hoa_don.trang_thai == trang_thai).paginate(id,5,False)
    
    return render_template('Quan_ly/QL_don_hang/QL_don_hang_theo_trang_thai.html', tieu_de = tieu_de, page_filter = page_filter, form=form)

@app.route('/QL-don-hang/thanh-toan/hd_<int:ma_hd>', methods=['GET','POST'])
def thanh_toan(ma_hd):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    today = datetime.now()
    hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ma_hoa_don == ma_hd).first()
    hoa_don.trang_thai = 1
    hoa_don.ghi_chu += "| [ĐÃ THANH TOÁN], " + today.strftime("%d-%m-%Y %H:%M:%S")
    dbSession.add(hoa_don)
    dbSession.commit()
    return redirect(url_for('xem_hoa_don',ma_hd = ma_hd))

@app.route('/QL-don-hang/huy/bill_<int:ma_hd>', methods = ['GET','POST'])
def huy_hoa_don(ma_hd):
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    form = Form_huy_don_hang()
    if form.validate_on_submit():
        today = datetime.now()
        hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ma_hoa_don == ma_hd).first()
        hoa_don.trang_thai = 2
        if hoa_don.ghi_chu == None:
            hoa_don.ghi_chu = "| [HỦY], " +today.strftime("%d-%m-%Y %H:%M:%S") + " , " + form.li_do.data
        else:
            hoa_don.ghi_chu += "| [HỦY], " +today.strftime("%d-%m-%Y %H:%M:%S") + " , " + form.li_do.data

        dbSession.add(hoa_don)
        dbSession.commit()
    return redirect(url_for('xem_hoa_don',ma_hd = ma_hd))

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


@app.route('/Ql-doanh-thu',methods=['GET','POST'])
def xem_doanh_thu():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    dia_chi = ''
    if request.method == 'POST':
        dieu_khien = request.form.get('Th_doanh_thu')
        if dieu_khien == 'All':
            dia_chi = '/Ql-doanh-thu/all'
        elif dieu_khien == 'TheoThang':
            dia_chi = '/Ql-doanh-thu/theo-thang'
        elif dieu_khien == 'TheoNgay':
            dia_chi = '/Ql-doanh-thu/theo-ngay'
        elif dieu_khien == 'TheoSanPham':
            dia_chi = '/Ql-doanh-thu/theo-san-pham'
        
    return render_template('Quan_ly/QL_doanh_thu/MH_QL_doanh_thu.html', dia_chi = dia_chi)

@app.route('/Ql-doanh-thu/all', methods = ['GET'])
def xem_doanh_thu_all():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    danh_sach_cac_ngay = []
    hoa_don = dbSession.query(Hoa_don).all()
    for item in hoa_don:
        dict_temp = {}
        dict_temp['ngay_tao_hoa_don'] = item.ngay_tao_hoa_don.strftime("%d-%m-%Y")
        if dict_temp not in danh_sach_cac_ngay:
            danh_sach_cac_ngay.append(dict_temp)
    
    tong_loi_nhuan = 0
    danh_sach_hoa_don = []
    for item in hoa_don:
        if item.trang_thai == 1:
            dict_temp = {}
            don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == item.ma_hoa_don).all()
            loi_nhuan_1_hoa_don = 0
            for item_1 in don_hang:
                san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item_1.ma_san_pham).first()
                loi_nhuan_1_hoa_don += san_pham.gia_ban*item_1.so_luong
                # loi_nhuan_1_hoa_don += (san_pham.gia_ban - san_pham.gia_nhap)*item_1.so_luong
            dict_temp['ngay_tao_hoa_don'] = item.ngay_tao_hoa_don.strftime("%d-%m-%Y")
            dict_temp['loi_nhuan'] = loi_nhuan_1_hoa_don
            danh_sach_hoa_don.append(dict_temp)
    
    for ngay in danh_sach_cac_ngay:
        loi_nhuan_theo_ngay = 0
        for bill in danh_sach_hoa_don:
            if bill['ngay_tao_hoa_don'] == ngay['ngay_tao_hoa_don']:
                loi_nhuan_theo_ngay += bill['loi_nhuan']
        ngay['tong_loi_nhuan'] = loi_nhuan_theo_ngay
    # print(danh_sach_cac_ngay)
        
    return render_template('Quan_ly/QL_doanh_thu/Doanh_thu_all.html', danh_sach_cac_ngay = danh_sach_cac_ngay)

@app.route("/Ql-doanh-thu/theo-thang", methods=['GET','POST'])
def doanh_thu_thang():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    danh_sach_cac_thang = []
    hoa_don = dbSession.query(Hoa_don).all()
    for item in hoa_don:
        dict_temp = {}
        dict_temp['thang'] = item.ngay_tao_hoa_don.strftime("%m-%Y")
        if dict_temp not in danh_sach_cac_thang:
            danh_sach_cac_thang.append(dict_temp)
    
    tong_loi_nhuan = 0
    danh_sach_hoa_don = []
    for item in hoa_don:
        if item.trang_thai == 1:
            dict_temp = {}
            don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == item.ma_hoa_don).all()
            loi_nhuan_1_hoa_don = 0
            for item_1 in don_hang:
                san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item_1.ma_san_pham).first()
                loi_nhuan_1_hoa_don += san_pham.gia_ban*item_1.so_luong
                # loi_nhuan_1_hoa_don += (san_pham.gia_ban - san_pham.gia_nhap)*item_1.so_luong
            dict_temp['thang'] = item.ngay_tao_hoa_don.strftime("%m-%Y")
            dict_temp['loi_nhuan'] = loi_nhuan_1_hoa_don
            danh_sach_hoa_don.append(dict_temp)
    
    for ngay in danh_sach_cac_thang:
        loi_nhuan_theo_thang = 0
        for bill in danh_sach_hoa_don:
            if bill['thang'] == ngay['thang']:
                loi_nhuan_theo_thang += bill['loi_nhuan']
        ngay['tong_loi_nhuan'] = loi_nhuan_theo_thang
    return render_template('Quan_ly/QL_doanh_thu/Doanh_thu_theo_thang.html', danh_sach_cac_thang = danh_sach_cac_thang)

@app.route("/Ql-doanh-thu/theo-ngay", methods=['GET','POST'])
def doanh_thu_ngay():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    today = datetime.now()
    ds_hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ngay_tao_hoa_don == today.date()).all()
    dict_sp_trong_ngay = {}
    tong_doanh_thu = 0
    for hoa_don in ds_hoa_don:
        tong_doanh_thu += int(hoa_don.tong_tien)
        don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == hoa_don.ma_hoa_don).all()
        for san_pham in don_hang:
            if san_pham.ma_san_pham not in dict_sp_trong_ngay:
                dict_sp_trong_ngay[san_pham.ma_san_pham] = san_pham.so_luong
            else:
                dict_sp_trong_ngay[san_pham.ma_san_pham] += san_pham.so_luong
    lst_sp_trong_ngay = []
    for item in dict_sp_trong_ngay:
        san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item).first()
        dict_temp = {}
        dict_temp['ma_sp'] = item
        dict_temp['ten_sp'] = san_pham.ten_san_pham
        dict_temp['so_luong'] = dict_sp_trong_ngay[item]
        dict_temp['gia_ban'] = san_pham.gia_ban
        lst_sp_trong_ngay.append(dict_temp)
    ngay = "Ngày " + str(today.day) + " Tháng " + str(today.month) + " năm " + str(today.year)
    return render_template('Quan_ly/QL_doanh_thu/Doanh_thu_theo_ngay.html', ngay = ngay, tong_doanh_thu = tong_doanh_thu, lst_sp_trong_ngay  = lst_sp_trong_ngay)

@app.route('/Ql-doanh-thu/theo-san-pham', methods = ['GET','POST'])
def xem_doanh_thu_sp():
    if not current_user.is_authenticated or current_user.ma_loai_nguoi_dung != 1:
        return redirect(url_for('dang_nhap', next=request.url))
    ds_hoa_don = dbSession.query(Hoa_don).all()
    dict_sp_trong_ngay = {}
    tong_doanh_thu = 0
    for hoa_don in ds_hoa_don:
        tong_doanh_thu += int(hoa_don.tong_tien)
        don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == hoa_don.ma_hoa_don).all()
        for san_pham in don_hang:
            if san_pham.ma_san_pham not in dict_sp_trong_ngay:
                dict_sp_trong_ngay[san_pham.ma_san_pham] = san_pham.so_luong
            else:
                dict_sp_trong_ngay[san_pham.ma_san_pham] += san_pham.so_luong
    lst_sp_trong_ngay = []
    for item in dict_sp_trong_ngay:
        san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item).first()
        dict_temp = {}
        dict_temp['ma_sp'] = item
        dict_temp['ten_sp'] = san_pham.ten_san_pham
        dict_temp['so_luong'] = dict_sp_trong_ngay[item]
        dict_temp['gia_ban'] = san_pham.gia_ban
        lst_sp_trong_ngay.append(dict_temp)
       
    return render_template('Quan_ly/QL_doanh_thu/Doanh_thu_theo_san_pham.html', lst_sp_trong_ngay = lst_sp_trong_ngay)

init_login()
admin = Admin(app, name = "Admin", index_view=MyAdminIndexView(name="Admin"), template_mode='bootstrap3')
admin.add_view(admin_view(Loai_san_pham, dbSession, 'Loại sản phẩm'))
admin.add_view(san_pham_view(San_pham, dbSession, 'Sản phẩm'))
admin.add_view(ModelView(Dot_khuyen_mai, dbSession, 'Đợt khuyến mãi'))
admin.add_view(ModelView(San_pham_khuyen_mai, dbSession, 'Sản phẩm khuyến mãi'))
admin.add_view(ModelView(Hoa_don, dbSession, 'Hóa đơn'))
admin.add_view(admin_view(Loai_nguoi_dung, dbSession, 'Loại người dùng'))
admin.add_view(admin_view(Nguoi_dung, dbSession, 'Người dùng'))
