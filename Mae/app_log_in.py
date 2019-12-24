from Mae import app

from Mae.xu_ly.Xu_ly_Form import *

from flask import render_template

@app.route('/dang-nhap', methods = ['GET', 'POST'])
def log_in():
    form_dang_nhap = Form_dang_nhap()
    return render_template('Quan_ly/MH_Dang_nhap.html', form_dang_nhap = form_dang_nhap)