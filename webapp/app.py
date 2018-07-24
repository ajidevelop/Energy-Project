from API.User.login import check_user, create_user as cu
import API.User.login as lo
import API.utilities.exceptions as e
from API.database.database_connect import Users as dcU, Verification as dcV
from . import app as ac

from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = ac

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))

question = "Would you like to create a new account"
w_credentials = "Wrong Username/Password"


@app.route("/")
def index():
    if lo.user_logged_in is False:
        return redirect(url_for('login'))
    else:
        print(lo.user_logged_in)
        pass  # set logged in functionality
        return render_template('entry_page.html')


@app.route("/<string:rero>")
def reroute(rero):
    if lo.user_logged_in is False:
        return redirect(url_for('login'))
    else:
        pass  # set logged in functionality
        return render_template('entry_page.html')


@app.route('/logout', methods=['POST'])
def logout():
    lo.user_logged_in = False
    return render_template('index.html', text='Logged Out')


@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        lop = request.form.get('username')
        print(lop)
        log = check_user(username, password)
        print(log)
        return render_template('index.html', text=log, loggedin=True)
    except e.WrongPassword:
        return render_template('index.html', wrong_credentials=True, showlogin=True)
    except e.NeedVerificationCode:
        return render_template('index.html', verification=True, showlogin=True)
    except TypeError:
        return render_template('index.html')


@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    return render_template('new_user.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    token = request.form.get('token')
    if dcV.check_verification_token(token):
        user = dcU.email_verified(False, token)
        lo.user_logged_in = True
        return render_template('index.html', text=f'Welcome {user}', loggedin=True)
    else:
        return render_template('index.html', text='Incorrect Verification Code')


@app.route('/verify/resend_request', methods=['POST', 'GET'])
def resend_request():
    return render_template('email.html')


@app.route('/verify/resend', methods=['POST'])
def resend():
    email = request.form.get('email')
    try:
        dcV.resend_verification(email)
        return render_template('index.html', text='Email sent')
    except e.NoEmail:
        return render_template('email.html', text='Email not in system')


@app.route('/create', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        cu(username, password, email)
    except e.TakenField as error:
        if str(error) == f'The username "{username}" is already taken':
            return render_template('new_user.html', text=error)
        elif str(error) == f'The email "{email}" is already taken':
            return render_template('new_user.html', text=error)
    except e.InvalidEmail:
        return render_template('new_user.html', text='Please enter a valid email')
    else:
        return render_template('index.html', text='Verification Code sent to your email')


if __name__ == '__main__':
    ac.app.run()
