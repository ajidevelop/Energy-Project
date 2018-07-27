from API.User.login import check_user, create_user as cu
import API.User.login as lo
import API.utilities.exceptions as e
import API.utilities.strings as s
from API.database.database_connect import Users as dcU, Verification as dcV
from . import app as ac
# from webapp.app_config import app as ac
from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from login

app = ac

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))

# Login Route


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
        log = check_user(username, password)
        if lo.check_if_email(username):
            lo.uid = dcU.find_user(username, email=True)
        else:
            lo.uid = dcU.find_user(username)
        lo.user_logged_in = True
        return render_template('index.html', text=log, loggedin=lo.user_logged_in)
    except e.WrongPassword:
        return render_template('index.html', wrong_credentials=True, showlogin=True, text=s.w_credentials)
    except e.NeedVerificationCode:
        return render_template('index.html', verification=True, showlogin=True)
    except TypeError:
        return render_template('index.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    token = request.form.get('token')
    if dcV.check_verification_token(token):
        user = dcU.email_verified(False, token)
        lo.user_logged_in = True
        return render_template('index.html', tmp_message=True, text=f'Welcome {user}', loggedin=lo.user_logged_in)
    else:
        return render_template('index.html', w_verification=True, text='Incorrect Verification Code')


@app.route('/verify/resend', methods=['POST'])
def resend():
    email = request.form.get('email-code')
    try:
        dcV.resend_verification(email)
        return render_template('index.html', tmp_message=True, text='Email sent')
    except e.NoEmail:
        return render_template('index.html', n_system=True, text='Please enter a valid email in our system or create a new account')


@app.route('/create', methods=['POST'])
def create_user():
    username = request.form.get('username-new')
    password = request.form.get('password-new')
    password_retype = request.form.get('password-retype')
    email = request.form.get('email')
    email_retype = request.form.get('email-retype')
    fName = request.form.get('fName')
    lName = request.form.get('lName')
    if password != password_retype:
        return render_template('index.html', p_match=True, taken=True)
    elif email != email_retype:
        return render_template('index.html', e_match=True, taken=True)
    try:
        cu(username, password, email, fName, lName)
    except e.TakenField as error:
        if str(error) == f'The username "{username}" is already taken':
            return render_template('index.html', u_taken=True, taken=True, text=f'The username "{username}" is already taken')
        elif str(error) == f'The email "{email}" is already taken':
            return render_template('index.html', e_taken=True, taken=True, text=f'The email "{email}" is already taken')
    except e.InvalidEmail:
        return render_template('index.html', i_email=True, taken=True, text='Please enter a valid email')
    else:
        return render_template('index.html', tmp_message=True, text='Verification Code sent to your email')


# Energy Usage Route

@app.route('/show-energy-usage', methods=['POST', 'GET'])
def show_energy_usage():
    print(request.method)


if __name__ == '__main__':
    app.run()
