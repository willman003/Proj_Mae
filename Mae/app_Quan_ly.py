from Mae import app
from flask import Flask, render_template

@app.route('/cong-ty',methods=['GET','POST'])
def dang_nhap():
    return render_template('Quan_ly/MH_Dang_nhap.html')

@app.route('/cong-ty/admin',methods=['GET','POST'])
def admin():
    return render_template('Quan_ly/MH_Chinh.html')