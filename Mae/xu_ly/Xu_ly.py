from Mae import app

from datetime import datetime

from flask_mail import Mail, Message

from flask import render_template



import re



#---Loại bỏ tag HTML
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)


def tao_chuoi_ngay(ngay_sinh):
    chuoi_ngay_sinh = ngay_sinh.split("/")
    ngay = int(chuoi_ngay_sinh[0])
    thang = int(chuoi_ngay_sinh[1])
    nam = int(chuoi_ngay_sinh[2])
    ket_qua = datetime(nam,thang,ngay)
    return ket_qua

mail = Mail(app)
def gui_email(ma_hoa_don, hoa_don, customer, don_hang):
    msg = Message('[Xác nhận đơn hàng #%d]'%ma_hoa_don, sender = 'willman0031@gmail.com', recipients = ['truongnguyenhoangtan@gmail.com'])
    noi_dung_mail = render_template('Web/Mail.html', ma_hoa_don=ma_hoa_don, hoa_don=hoa_don, customer=customer, don_hang=don_hang)
    mail.body = noi_dung_mail
    msg.html = mail.body
    mail.send(msg)
    return 





