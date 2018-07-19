# __author__ = 'DanielAjisafe'
#
# # Flask Support
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import datetime
# from python_console.database.database_connect import Users as dcU
# from argon2 import PasswordHasher
# ph = PasswordHasher()
#
# app = Flask(__name__)
# app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
#
#
# class Verification:
#
#     uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True, nullable=False)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     token = db.Column(db.String(30), unique=True)
#     ts_create = db.Column(db.TIMESTAMP, default=datetime.datetime.today())
#
#     def __init__(self, uid):
#         self.token = ''
#         self.email = ''
#         self.uid = uid
#
#
# class Users(db.Model):
#
#     uid = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     verified = db.Column(db.String(1))
#     user_since = db.Column(db.TIMESTAMP, default=datetime.datetime.today())
#
#     def __init__(self):
#         self.email = ''
#         self.username = ''
#         self.password = ''
#         self.verified = ''
#
#     @staticmethod
#     def new_user(u, p, email):
#         dcU.new_user(u, p, email)
#
#
# print(datetime.date(2001, 12, 22))
#
# users = Users.query.all()
# print(users[0])
#
# # if __name__ == '__test__':
# #     app.run()


import webapp.app_config as ac
from flask import redirect, url_for

app = ac.app

@app.route('/')
def inde():
    return redirect(url_for('login'))

@app.route('/<string:rero>')
def index(rero):
    return redirect(url_for('login'))


@app.route('/log')
def login():
    return 'Hello World'


app.run()