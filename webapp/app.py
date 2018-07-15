import API.User.login as login

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_folder='webapp')

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('web/index.html')


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    uid = login.check_user(username, password)
    return render_template('web/index.html', success='success')

