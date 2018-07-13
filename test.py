__author__ = 'DanielAjisafe'

# Flask Support
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import database.database_connect as dc
from argon2 import PasswordHasher
ph = PasswordHasher()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Verification:

    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    token = db.Column(db.String(30), unique=True)
    ts_create = db.Column(db.TIMESTAMP, default=datetime.datetime.today())

    def __init__(self, uid):
        self.token = ''
        self.email = ''
        self.uid = uid


class Users(db.Model):

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    verified = db.Column(db.String(1))
    user_since = db.Column(db.TIMESTAMP, default=datetime.datetime.today())

    def __init__(self):
        self.email = ''
        self.username = ''
        self.password = ''
        self.verified = ''

    @staticmethod
    def new_user(u, p, email):
        dc.new_user(u, p, email)


new_user = Users()
new_user.new_user('test12', 'test', 'a2@email.com')
dbs = db.session(autocommit=True)
dbs.add(new_user)
users = Users.query.all()
print(users[0].username)

# if __name__ == '__test__':
#     app.run()
