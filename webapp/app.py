from API.User.login import check_user
import API.utilities.exceptions as e
from API.database.database_connect import Users, Verification as dcU

from flask import render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import app_config as ac

app = ac.app

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))

question = "Would you like to create a new account"
w_credentials = "Wrong Username/Password"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        log = check_user(username, password)
        return render_template('web/index.html', text=log)
    except e.WrongPassword:
        return render_template('web/index.html', text=w_credentials)
    except e.NeedVerificationCode:
        return render_template('web/verification.html')


@app.route('/new_user', methods=['POST'])
def new_user():
    login.check_user()


@app.route('/verify', methods=['POST'])
def verify():

    token = request.form.get('token')
    dcU.check_verification_token(token)
    return render_template('web/index.html', text='Verified')


if __name__ == '__main__':
    ac.app.run()
