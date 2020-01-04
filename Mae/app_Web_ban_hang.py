from Mae import app

from Mae.xu_ly.Xu_ly_Model import *
from Mae.xu_ly.Xu_ly import *
from Mae.xu_ly.Xu_ly_Form import *

from flask import Flask, render_template, Markup, session, redirect, url_for, request, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from flask_login import current_user, login_user

from flask_ckeditor import CKEditor

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
db_session = DBSession()

ckeditor = CKEditor(app)

@app.route('/',methods=['GET','POST'])
def index():
    
    danh_sach_category = db_session.query(Loai_san_pham).all()
    san_pham = db_session.query(San_pham).all()
    lst_temp = []
    for item in san_pham:
        dict_temp = {}
        dict_temp['ma_sp'] = item.ma_san_pham
        dict_temp['gia_ban'] = item.gia_ban
        lst_temp.append(dict_temp)
    return render_template('Web/index.html', lst_temp = lst_temp,san_pham = san_pham, danh_sach_category = danh_sach_category)

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
    
    session['id_category'] = id
   
    return render_template('Web/Loai_san_pham.html', loai = loai, danh_sach_san_pham = danh_sach_san_pham, id = id, danh_sach_category = danh_sach_category)

@app.route('/chi-tiet/sp_<int:ma_sp>',methods = ['GET','POST'])
def chi_tiet_san_pham(ma_sp):
    if session.get('Gio_hang') == None or session['Gio_hang'] == '':
        gio_hang = []
    else:
        gio_hang = session['Gio_hang']
    form_mua_hang = Form_mua_hang()
    form_y_kien = Form_y_kien()
    danh_sach_category = db_session.query(Loai_san_pham).all()
    san_pham = db_session.query(San_pham).filter(San_pham.ma_san_pham == ma_sp).one()
    mo_ta_dai = Markup(san_pham.mo_ta_chi_tiet.split('——————————')[0])
    
    list_y_kien = db_session.query(Y_kien).filter(Y_kien.ma_san_pham == ma_sp).order_by(desc(Y_kien.ngay_tao)).all()
    danh_sach_y_kien = []
    for y_kien in list_y_kien:
        dict_temp={}
        kh = db_session.query(Khach_hang).filter(Khach_hang.ma_nguoi_dung == y_kien.ma_khach_hang).first()
        dict_temp['khach_hang'] = kh.ten_khach_hang
        date_temp = y_kien.ngay_tao.date().strftime('%d-%m-%Y')
        time_temp = y_kien.ngay_tao.time().strftime('%X')
        dict_temp['ngay_tao'] = date_temp + " " + time_temp
        dict_temp['diem_danh_gia'] = y_kien.diem_danh_gia
        dict_temp['noi_dung'] = Markup(y_kien.noi_dung)
        danh_sach_y_kien.append(dict_temp)

    chuoi_bo_tag_html = remove_tags(san_pham.mo_ta_chi_tiet)
    chuoi_temp_1 = chuoi_bo_tag_html.split('❖')
        
    if len(chuoi_temp_1) >1:
        chi_tiet = {}
        chi_tiet['xuat_xu'] = chuoi_temp_1[1]
        chi_tiet['dung_tich'] = chuoi_temp_1[2]
    else:
        chi_tiet = ''
    if form_mua_hang.submit_1.data and form_mua_hang.validate_on_submit():
        for item in gio_hang:
            if item['ma_sp'] == ma_sp:
                item['so_luong'] = form_mua_hang.so_luong.data
                flash('Đã cập nhật ' + item['ten_sp'] + ' vào giỏ hàng')
                break
        else:
            sp_don_hang = {}
            sp_don_hang['ma_sp'] = ma_sp
            sp_don_hang['ten_sp'] = san_pham.ten_san_pham
            sp_don_hang['gia_ban'] = "{:,}".format(san_pham.gia_ban)
            sp_don_hang['so_luong'] = form_mua_hang.so_luong.data
            gio_hang.append(sp_don_hang)
            flash('Đã thêm '+ sp_don_hang['ten_sp'] + ' vào giỏ hàng')
        session['Gio_hang'] = gio_hang
    
    if form_y_kien.submit_2.data and form_y_kien.is_submitted():
        y_kien = Y_kien()
        y_kien.ma_khach_hang = form_y_kien.ma_khach_hang.data
        y_kien.ma_san_pham = ma_sp
        y_kien.tieu_de = form_y_kien.tieu_de.data
        y_kien.diem_danh_gia = form_y_kien.diem_danh_gia.data
        y_kien.noi_dung = form_y_kien.noi_dung.data
        y_kien.ngay_tao = datetime.now()
        db_session.add(y_kien)
        db_session.commit()
        flash('Ý kiến của bạn đã được ghi nhận! Mae cảm ơn bạn!')

    return render_template('Web/Chi_tiet_san_pham.html', danh_sach_y_kien = danh_sach_y_kien, form_y_kien = form_y_kien, form_mua_hang = form_mua_hang, mo_ta_dai = mo_ta_dai, chi_tiet = chi_tiet, san_pham = san_pham, danh_sach_category = danh_sach_category)

@app.route('/xem-gio-hang', methods = ['GET','POST'])
def xem_gio_hang():
    if session.get('Gio_hang') == None:
        session['Gio_hang'] = ''
    form = Form_mua_hang()
    danh_sach_category = db_session.query(Loai_san_pham).all()
    tong_tien = 0
    for item in session['Gio_hang']:
        gia_ban_convert = item['gia_ban'].split(',')
        gia_ban = gia_ban_convert[0]
        tong_tien += (int(gia_ban) * 1000 * int(item['so_luong']))
    
    tong_tien = "{:,}".format(tong_tien)
    
    return render_template('Web/Shopping_Cart.html', form = form, danh_sach_category = danh_sach_category, tong_tien = tong_tien)

@app.route('/xem-gio-hang/xoa/sp_<int:ma_sp>', methods =['GET'])
def xoa_gio_hang(ma_sp):
    gio_hang = session['Gio_hang']
      
    for item in gio_hang:
        if item['ma_sp'] == ma_sp:
            session['Gio_hang'].remove(item)
            break
    session['Gio_hang'] = gio_hang
    
    return redirect(url_for('xem_gio_hang'))

@app.route('/xem-gio-hang/cap-nhat/sp_<int:ma_sp>', methods = ['GET','POST'])
def cap_nhat_gio_hang(ma_sp):
    form = Form_mua_hang()
    gio_hang = session['Gio_hang']
    if form.validate_on_submit():
        for item in gio_hang:
            if item['ma_sp'] == ma_sp:
                item['so_luong'] = form.so_luong.data
                break
    session['Gio_hang'] = gio_hang      
    print(session['Gio_hang'])   
    return redirect(url_for('xem_gio_hang'))

@app.route('/dat-hang', methods = ['GET','POST'])
def dat_hang():
    if not current_user.is_authenticated:
        return redirect(url_for('log_in'))
    customer = dbSession.query(Khach_hang).filter(Khach_hang.ma_nguoi_dung == current_user.ma_nguoi_dung).first()
    danh_sach_category = db_session.query(Loai_san_pham).all()
    form = Form_hoa_don()
    tong_tien = 0
    for item in session['Gio_hang']:
        gia_ban_convert = item['gia_ban'].split(',')
        gia_ban = gia_ban_convert[0]
        tong_tien += (int(gia_ban) * 1000 * int(item['so_luong']))
    
    if form.validate_on_submit():
        print('Success')
        ma_hoa_don = form.tao_hoa_don(customer.ma_khach_hang, tong_tien)
        session['Ma_hoa_don'] = ma_hoa_don
        for item in session['Gio_hang']:
            don_hang = Don_hang()
            don_hang.ma_hoa_don = ma_hoa_don
            don_hang.ma_san_pham = item['ma_sp']
            don_hang.so_luong = item['so_luong']
            don_hang.don_gia = item['gia_ban']
            dbSession.add(don_hang)
            dbSession.commit()
        return redirect(url_for('success'))
        
    
    return render_template('Web/Checkout.html', form = form, customer = customer, tong_tien = tong_tien, danh_sach_category = danh_sach_category)

@app.route('/success',methods=['GET'])
def success():
    if session.get('Ma_hoa_don') == None or not current_user.is_authenticated:
        return redirect(url_for('index'))
    ma_hoa_don = session['Ma_hoa_don']
    hoa_don = dbSession.query(Hoa_don).filter(Hoa_don.ma_hoa_don == ma_hoa_don).first()
    customer = dbSession.query(Khach_hang).filter(Khach_hang.ma_nguoi_dung == current_user.ma_nguoi_dung).first()
    don_hang = dbSession.query(Don_hang).filter(Don_hang.ma_hoa_don == ma_hoa_don).all()
    danh_sach_category = db_session.query(Loai_san_pham).all()
    for item in don_hang:
        san_pham = dbSession.query(San_pham).filter(San_pham.ma_san_pham == item.ma_san_pham).first()
        san_pham.so_luong_ton -= item.so_luong
        dbSession.add(san_pham)
        dbSession.commit()
    gui_email(ma_hoa_don,hoa_don, customer, don_hang)
    
    return render_template('Web/Success.html', danh_sach_category = danh_sach_category)

@app.route('/tiep-tuc', methods =['GET'])
def tiep_tuc():
    session.pop('Gio_hang', None)
    session.pop('Ma_hoa_don', None)
    
    return redirect(url_for('index'))
