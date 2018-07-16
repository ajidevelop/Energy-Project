from API.User.login import check_user, create_user as cu
import API.utilities.exceptions as e
from API.database.database_connect import Users as dcU, Verification as dcV
import webapp.app_config as ac

from flask import render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = ac.app

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))

question = "Would you like to create a new account"
w_credentials = "Wrong Username/Password"


@app.route("/")
def index():
    return render_template('web/index.html', loggedin=False)


@app.route('/logout', methods=['POST'])
def logout():
    return render_template('web/index.html', text='Logged Out', loggedin=False)


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        log = check_user(username, password)
        return render_template('web/index.html', text=log, loggedin=True)
    except e.WrongPassword:
        return render_template('web/index.html', text=w_credentials)
    except e.NeedVerificationCode:
        return render_template('web/verification.html')


@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    return render_template('web/new_user.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    token = request.form.get('token')
    if dcV.check_verification_token(token):
        user = dcU.email_verified(False, token)
        return render_template('web/index.html', text=f'Welcome {user}', loggedin=True)
    else:
        return render_template('web/verification.html', text='Incorrect Verification Code')


@app.route('/resend_request', methods=['POST', 'GET'])
def resend_request():
    return render_template('web/email.html')


@app.route('/resend', methods=['POST'])
def resend():
    email = request.form.get('email')
    try:
        dcV.resend_verification(email)
        return render_template('web/index.html', text='Email sent', loggedin=False)
    except e.NoEmail:
        return render_template('web/email.html', text='Email not in system')


@app.route('/create', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        cu(username, password, email)
    except e.TakenField as error:
        if str(error) == f'The username "{username}" is already taken':
            return render_template('web/new_user.html', text=error)
        elif str(error) == f'The email "{email}" is already taken':
            return render_template('web/new_user.html', text=error)
    except e.InvalidEmail:
        return render_template('web/new_user.html', text='Please enter a valid email')
    else:
        return render_template('web/index.html', text='Verification Code sent to your email', loggedin=False)


if __name__ == '__main__':
    ac.app.run()
