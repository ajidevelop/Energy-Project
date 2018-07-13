__author__ = 'DanielAjisafe'

# Flask Support
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    verified = db.Column(db.String(1))
    user_since = db.Column(db.TIMESTAMP, default=datetime.datetime.today())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.verified = 'N'


new_user = User('test', 'test', 'test')
dbs = db.session(autocommit=True)
dbs.add(new_user)
users = User.query.all()
print(users[0].username)

# if __name__ == '__test__':
#     app.run()
