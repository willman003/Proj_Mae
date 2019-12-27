from flask import Flask
# from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SECRET_KEY'] = "Impossible to guess"

#---CONFIG-----
app.config['DATABASE_FILE'] = 'du_lieu/ql_mae.db?check_same_thread=False'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

# db = SQLAlchemy(app)


import Mae.xu_ly.Xu_ly_Model
import Mae.app_Web_ban_hang
import Mae.app_Quan_ly
import Mae.app_admin