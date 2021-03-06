from API.User.login import check_user, create_user as cu
import API.User.login as lo
import API.utilities.exceptions as e
import API.utilities.strings as s
from API.database.database_connect import Users as dcU, Verification as dcV
# from . import app as ac
from webapp.app_config import app as ac
from flask import render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from API.database.entries.energy_usage_entry import DayUsage, WeekUsage, MonthUsage, RandomDateRangeUsage
import datetime

app = ac

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db = scoped_session(sessionmaker(bind=engine))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Login Route


@login_manager.user_loader
def load_user(user_id):
    return dcU.query.get(int(user_id))


@app.route("/")
def index():
    return render_template('index.html', loggedin=current_user.is_active)


@app.route("/<string:rero>")
def reroute(rero):
    return render_template('index.html', loggedin=current_user.is_active)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return render_template('index.html', text='Logged Out')


@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        log = check_user(username, password)
        if lo.check_if_email(username):
            lo.user_class = dcU.returning_user(username, password, True)
        else:
            lo.user_class = dcU.returning_user(username, password, False)
        if request.form.get('remember') == 'on':
            login_user(lo.user_class, remember=True, duration=timedelta(days=3))
        else:
            login_user(lo.user_class)
        return render_template('index.html', text=log, loggedin=current_user.is_active)
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
        return render_template('index.html', tmp_message=True, text=f'Welcome {user}', loggedin=current_user.is_active)
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
@login_required
def show_energy_usage():
    view = DayUsage.view_all_daily_usage(current_user.uid)
    average = DayUsage.average_usage()
    week_view = WeekUsage.view_weekly_usage(current_user.uid)
    week_average = WeekUsage.average_usage()
    month_view = MonthUsage.view_monthly_usage(current_user.uid)
    month_average = MonthUsage.average_usage()
    entries = request.form.get('entries')
    if entries is None:
        entries = 'all'
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')
    if start_date is None or end_date is None:
        start_date = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%m/%d/%y')
        end_date = datetime.datetime.today().strftime('%m/%d/%y')
        return render_template('show_usage.html', average_dates=average, dates=view, week_average=week_average, week_dates=week_view,
                               loggedin=current_user.is_active, entries=entries, start_date=start_date, end_date=end_date, month_dates=month_view,
                               month_average=month_average)
    specific_view = DayUsage.view_specifc_day_usage(start_date, current_user.uid, end_date)
    specific_average_view = DayUsage.average_usage(start_date=start_date, end_date=end_date)
    specific_week_view = WeekUsage.view_specific_weekly_usage(start_date, end_date, current_user.uid)
    specific_average_week_view = WeekUsage.average_usage(start_date, end_date)
    specific_month_view = MonthUsage.view_specific_monthly_usage(start_date, end_date, current_user.uid)
    specific_average_monthly_view = MonthUsage.average_usage(start_date, end_date)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%y')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%y')
    return render_template('show_usage.html', dates=specific_view, average_dates=specific_average_view, week_average=specific_average_week_view,
                           week_dates=specific_week_view, loggedin=current_user.is_active, entries=entries, d_entries=len(specific_average_view),
                           w_entries=len(specific_average_week_view), m_enties=len(specific_average_monthly_view), start_date=start_date, end_date=end_date,
                           month_dates=specific_month_view, month_average=specific_average_monthly_view)


@app.route('/energy-usage-input', methods=['POST', 'GET'])
@login_required
def energy_usage_input():
    try:
        usage = request.form.get('usage')
        usage_type = request.form.get('usage-type')
        date = request.form.get('date')
        DayUsage.new_day_entry(date, usage, current_user.uid)
        return redirect('/show-energy-usage')
    except TypeError:
        return render_template('entry_page.html', loggedin=current_user.is_active)
    # if usage_type == 'day':
    #     try:
    #         DayUsage.new_day_entry()


@app.route('/show-energy-usage/delete', methods=['POST'])
@login_required
def delete_entries():
    child_box = request.form.getlist('child-box')
    DayUsage.delete_day_entry(child_box, current_user.uid)
    return redirect('/show-energy-usage')


@app.route('/show-energy-usage/update', methods=['POST'])
@login_required
def update_table():
    dates = request.form.getlist('date-box')
    d_usage = request.form.getlist('d_usage')
    DayUsage.edit_day_entry(dates, d_usage, current_user.uid)
    return redirect('/show-energy-usage')


if __name__ == '__main__':
    app.run()
