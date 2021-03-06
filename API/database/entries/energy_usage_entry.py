__author__ = 'DanielAjisafe'
import API.database.database_connect as dc
from API.database.database_connect import db
import datetime
from dateutil import relativedelta
from calendar import monthrange
import API.utilities.exceptions as e
from API.utilities.important_variables import Average
from sqlalchemy import and_
import pandas as pd


class DayUsage(db.Model):
    __tablename__ = 'day_usage'
    did = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(2), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(2), nullable=False)
    d_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    @staticmethod
    def new_day_entry(date, d_usage, uid):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%y')
        day = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d')
        month = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m')
        year = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y')
        find = pd.read_sql_table('day_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='did')
        f = len(find[(find['uid'] == uid) & (find['date'] == date)])
        if f == 1:
            return e.DayExist
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'INSERT INTO `day_usage` (`date`, `day`, `month`, `year`, `d_usage`, `uid`) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (date, day, month, year, d_usage, uid))

    @classmethod
    def view_all_daily_usage(cls, uid):
        find = pd.read_sql_table('day_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='did')
        find.sort_values(['year', 'month', 'day'], inplace=True)
        f = find[(find['uid'] == uid)]
        days = {}
        for dates in range(len(f)):
            days[dates] = DatatoClass(f, dates)
        cls.create_week_usage(uid)
        cls.create_monthly_usage(uid)
        return days

    @classmethod
    def view_specifc_day_usage(cls, start_date, uid, end_date=None):
        s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%y')
        if end_date is not None:
            e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            days = e_date - s_date
            days = days.days
        else:
            days = 1
        dates = {}
        for i in range(days):
            find = cls.query.filter_by(uid=uid, date=start_date).first()
            dates[i] = find
            start_date = (datetime.datetime.strptime(start_date, '%m/%d/%y') + datetime.timedelta(days=1)).strftime('%m/%d/%y')
        return dates

    # Under Development
    @classmethod
    def delete_day_entry(cls, dates, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        for date in dates:
            try:
                day_number = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d'))
                date1 = datetime.datetime.strptime(date, '%m/%d/%y')
                date2 = date1 - datetime.timedelta(days=day_number)
                month, year = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m')), int(datetime.datetime.strptime(date,
                                                                                                                '%m/%d/%y').strftime('%y'))
                month_find = MonthUsage.query.filter_by(month=month, year=year, uid=uid).first()
                week_find = WeekUsage.query.filter_by(week_start_date=date2, uid=uid).first()
                finder = cls.query.filter_by(date=date, uid=uid).first()
                w_usage = week_find.w_usage - finder.d_usage
                m_usage = month_find.m_usage - finder.d_usage
                sql = 'UPDATE `week_usage` SET `w_usage`=%s WHERE (`week_start_date`=%s AND `uid`=%s)'
                cursor.execute(sql, (w_usage, date2, uid))
                sql = 'UPDATE `month_usage` SET `m_usage`=%s WHERE (`month`=%s AND `year`=%s AND `uid`=%s)'
                cursor.execute(sql, (m_usage, month, year, uid))
            except AttributeError:
                pass
            finally:
                sql = 'DELETE FROM `db`.`day_usage` WHERE (`date`=%s AND `uid`=%s)'
                cursor.execute(sql, (date, uid))
        connection.close()

    @classmethod
    def edit_day_entry(cls, date, usage, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        try:
            day_number = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%w'))
            date1 = datetime.datetime.strptime(date, '%m/%d/%y')
            date2 = date1 - datetime.timedelta(days=day_number)
            find = WeekUsage.query.filter_by(week_start_date=date2, uid=uid).first()
            finder = cls.query.filter_by(date=date, uid=uid).first()
            w_usage = find.w_usage - finder.d_usage + usage
            sql = 'UPDATE `week_usage` SET `w_usage`=%s WHERE (`week_start_date`=%s AND `uid`=%s)'
            cursor.execute(sql, (w_usage, date2, uid))
        except AttributeError:
            pass
        finally:
            sql = 'UPDATE `day_usage` SET `d_usage`=%s WHERE (`date`=%s AND `uid`=%s)'
            cursor.execute(sql, (usage, date, uid))
        connection.close()

    @classmethod
    def average_usage(cls, date=None, start_date=None, end_date=None):
        average_properties = Average({'usage': 0})
        if date is not None:
            dates = cls.query.filter_by(date=date).order_by(cls.year, cls.month, cls.day).all()
            average_properties['day'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d'))
            average_properties['month'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m'))
            average_properties['year'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y'))
            average_properties['date'] = datetime.date(average_properties.year, average_properties.month, average_properties.day)
        else:
            dates = pd.read_sql_table('day_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='did')
            dates.sort_values(['year', 'month', 'day'], inplace=True)
            if start_date is not None:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%y')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%y')
                dates = dates[(dates['date'] >= start_date) & (dates['date'] <= end_date)]
                # dates = cls.query.filter(and_(cls.date >= start_date, cls.date <= end_date)).order_by(cls.year, cls.month, cls.day).all()
            else:
                pass
                # dates = cls.query.order_by(cls.year, cls.month, cls.day).all()
            average = []
            averages = []
            for item in range(len(dates)):
                average.append(cls.average_usage(dates['date'].iloc[item]))
            for i in average:
                if i not in averages:
                    averages.append(i)
            return averages

        for item in range(len(dates)):
            average_properties['usage'] += dates[item].d_usage

        average_properties['usage'] /= len(dates)
        return average_properties

    @classmethod
    def create_week_usage(cls, uid):
        dates = cls.query.filter_by(uid=uid).order_by(cls.year, cls.month, cls.day).all()
        w_usage = 0
        for position, item in enumerate(dates):
            weekday = int(datetime.datetime.strptime(item.date, '%m/%d/%y').strftime('%w'))
            if weekday == 0:
                try:
                    week = []
                    for i in range(len(dates[position: position + 7])):
                        if i == 0:
                            week.append(dates[position])
                            w_usage += week[i].d_usage
                            continue
                        days = datetime.datetime.strptime(dates[position + i].date, '%m/%d/%y') \
                        - datetime.datetime.strptime(dates[position + i - 1].date, '%m/%d/%y')
                        if days.days == 1:
                            week.append(dates[position + i])
                            w_usage += week[i].d_usage
                        else:
                            w_usage = 0
                            break
                except AttributeError:
                    pass
                else:
                    if len(week) == 7:
                        WeekUsage.new_week_entry(datetime.datetime.strptime(week[0].date, '%m/%d/%y').strftime('%Y-%m-%d'), w_usage, uid)
                        w_usage = 0

    @classmethod
    def create_monthly_usage(cls, uid):
        dates = cls.query.filter_by(uid=uid).order_by(cls.year, cls.month, cls.day).all()
        m_usage = 0
        for position, item in enumerate(dates):
            month_number = int(datetime.datetime.strptime(item.date, '%m/%d/%y').strftime('%m'))
            number_of_days = 0
            try:
                if int(datetime.datetime.strptime(dates[position + number_of_days].date, '%m/%d/%y').strftime('%d')) == 1:
                    number_of_days += 1
                    while int(datetime.datetime.strptime(dates[position + number_of_days].date, '%m/%d/%y').strftime('%m')) == month_number:
                        number_of_days += 1
                else:
                    continue
                if number_of_days == monthrange(item.year, month_number)[1]:
                    print(monthrange(item.year, month_number)[1], number_of_days)
                    pass
                else:
                    continue
            except IndexError:
                number_of_days = 0
                for i in range(len(dates[position: position + monthrange(item.year, month_number)[1]])):
                    number_of_days += 1
            try:
                month = []
                for i in range(len(dates[position: position + number_of_days])):
                    if i == 0:
                        month.append(dates[position])
                        m_usage += month[i].d_usage
                        continue
                    months = datetime.datetime.strptime(dates[position + i].date, '%m/%d/%y') \
                             - datetime.datetime.strptime(dates[position + i - 1].date, '%m/%d/%y')
                    if months.days == 1:
                        month.append(dates[position + i])
                        m_usage += month[i].d_usage
                    else:
                        m_usage = 0
                        break
            except AttributeError:
                pass
            else:
                if len(month) == monthrange(item.year, month_number)[1]:
                    MonthUsage.new_month_entry(datetime.date(month[0].year, month[0].month, month[0].day), m_usage, uid)
                    m_usage = 0
                else:
                    m_usage = 0


class DatatoClass:
    def __init__(self, df, position, type='day'):
        self.data = df
        self.uid = df['uid'].iloc[position]
        self.cost = df['cost'].iloc[position]
        if type == 'week':
            self.week_start_date = df['week_start_date'].iloc[position]
            self.week_start_year = df['week_start_year'].iloc[position]
            self.week_start_month = df['week_start_month'].iloc[position]
            self.week_start_day = df['week_start_day'].iloc[position]
            self.w_usage = df['w_usage'].iloc[position]
        else:
            self.date = df['date'].iloc[position]
            self.year = df['year'].iloc[position]
            self.month = df['month'].iloc[position]
            self.day = df['day'].iloc[position]
            if type == 'day':
                self.d_usage = df['d_usage'].iloc[position]
            elif type == 'month':
                self.m_usage = df['m_usage'].iloc[position]
                self.month = datetime.datetime.strptime(self.month, '%b').strftime('%m')


class WeekUsage(db.Model):
    __tablename__ = 'week_usage'
    wid = db.Column(db.Integer, primary_key=True)
    week_start_date = db.Column(db.Date, nullable=False)
    week_start_year = db.Column(db.Integer, nullable=False)
    week_start_month = db.Column(db.Integer, nullable=False)
    week_start_day = db.Column(db.Integer, nullable=False)
    w_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0)

    @classmethod
    def new_week_entry(cls, week_start_date, w_usage_input, uid):
        try:
            datetime.datetime.strptime(week_start_date, '%Y-%m-%d')
        except TypeError:
            pass
        find = len(cls.query.filter_by(week_start_date=week_start_date, uid=uid).all())
        day = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%d')
        month = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%m')
        year = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%Y')
        if find == 1:
            return e.DayExist
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'INSERT INTO `week_usage` (`week_start_date`, `week_start_day`, `week_start_month`, `week_start_year`, `w_usage`, `uid`) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (week_start_date, day, month, year, w_usage_input, uid))
        connection.close()

    @classmethod
    def average_usage(cls, week_start_date=None, week_end_date=None):
        average_properties = Average({'usage': 0})
        if week_end_date is not None or week_start_date is None:
            if week_end_date is not None:
                week_start_date = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%m/%d/%y')
                isitsunday = int(datetime.datetime.strptime(week_start_date, '%m/%d/%y').strftime('%w'))
                while isitsunday != 0:
                    week_start_date = (datetime.datetime.strptime(week_start_date, '%m/%d/%y') - datetime.timedelta(days=1)).strftime(
                        '%m/%d/%y')
                    isitsunday = int(datetime.datetime.strptime(week_start_date, '%m/%d/%y').strftime('%w'))
                week_end_date = datetime.datetime.strptime(week_end_date, '%Y-%m-%d').strftime('%m/%d/%y')
                isitsunday = int(datetime.datetime.strptime(week_end_date, '%m/%d/%y').strftime('%w'))
                while isitsunday != 0:
                    week_end_date = (datetime.datetime.strptime(week_end_date, '%m/%d/%y') + datetime.timedelta(days=1)).strftime(
                        '%m/%d/%y')
                    isitsunday = int(datetime.datetime.strptime(week_end_date, '%m/%d/%y').strftime('%w'))
                week_start_date = datetime.datetime.strptime(week_start_date, '%m/%d/%y')
                week_end_date = datetime.datetime.strptime(week_end_date, '%m/%d/%y')
                dates = cls.query.filter(and_(cls.week_start_date >= week_start_date, cls.week_start_date <= week_end_date)).order_by(
                    cls.week_start_year, cls.week_start_month, cls.week_start_day).all()
                print(dates)
            else:
                dates = cls.query.order_by(cls.week_start_year, cls.week_start_month, cls.week_start_day).all()
            average = []
            averages = []
            for item in range(len(dates)):
                average.append(cls.average_usage(week_start_date=str(dates[item].week_start_date)))
            for i in average:
                if i not in averages:
                    averages.append(i)
            return averages
        else:
            dates = cls.query.filter_by(week_start_date=week_start_date).order_by(cls.week_start_date).all()
            average_properties['week_start_day'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%d'))
            average_properties['week_start_month'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%m'))
            average_properties['week_start_year'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%Y'))
            average_properties['week_start_date'] = datetime.date(average_properties.week_start_year, average_properties.week_start_month,
                                                                  average_properties.week_start_day)

        for item in range(len(dates)):
            average_properties['usage'] += dates[item].w_usage

        average_properties['usage'] /= len(dates)
        return average_properties

    @classmethod
    def view_weekly_usage(cls, uid):
        find = pd.read_sql_table('week_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='wid')
        find.sort_values(['week_start_year', 'week_start_month', 'week_start_day'], inplace=True)
        f = find[(find['uid'] == uid)]
        days = {}
        for dates in range(len(f)):
            days[dates] = DatatoClass(f, dates, type='week')
        return days

    @classmethod
    def view_specific_weekly_usage(cls, start_date, end_date, uid):
        s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%y')
        isitsunday = int(datetime.datetime.strptime(start_date, '%m/%d/%y').strftime('%w'))
        while isitsunday != 0:
            start_date = (datetime.datetime.strptime(start_date, '%m/%d/%y') - datetime.timedelta(days=1)).strftime('%m/%d/%y')
            isitsunday = int(datetime.datetime.strptime(start_date, '%m/%d/%y').strftime('%w'))
            s_date = datetime.datetime.strptime(start_date, '%m/%d/%y')
        e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%y')
        isitsunday = int(datetime.datetime.strptime(end_date, '%m/%d/%y').strftime('%w'))
        while isitsunday != 0:
            end_date = (datetime.datetime.strptime(end_date, '%m/%d/%y') + datetime.timedelta(days=1)).strftime('%m/%d/%y')
            isitsunday = int(datetime.datetime.strptime(end_date, '%m/%d/%y').strftime('%w'))
            e_date = datetime.datetime.strptime(end_date, '%m/%d/%y')
        weeks = e_date - s_date
        weeks = weeks.days // 7
        dates = {}
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%y')
        for i in range(weeks):
            find = cls.query.filter_by(uid=uid, week_start_date=start_date).first()
            dates[i] = find
            start_date = start_date + datetime.timedelta(days=7)
        return dates

    # Under Development
    @classmethod
    def delete_usage(cls, week_date, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'DELETE FROM `db`.`week_usage` WHERE `uid`=%s'
        cursor.execute(sql, uid)
        connection.close()


class MonthUsage(db.Model):
    __tablename__ = 'month_usage'
    mid = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(3), nullable=False)
    day = db.Column(db.Integer, nullable=False, default=1)
    m_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    @classmethod
    def new_month_entry(cls, month_start_date, m_usage_input, uid):
        try:
            month = month_start_date.strftime('%b')
            year = month_start_date.strftime('%Y')
        except TypeError:
            month = datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%B')
            year = datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%Y')
        find = len(cls.query.filter_by(date=month_start_date, uid=uid).all())
        if find == 1:
            return e.DayExist
        if cls.isitthefirst(month_start_date.strftime('%Y-%m-%d')) is not None:
            connection = dc.connectdb()
            cursor = connection.cursor()
            sql = 'INSERT INTO `month_usage` (`date`, `month`, `year`, `m_usage`, `uid`) ' \
                  'VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (month_start_date, month, year, m_usage_input, uid))
            connection.close()

    @classmethod
    def average_usage(cls, month_start_date=None, month_end_date=None):
        average_properties = Average({'usage': 0})
        if month_end_date is not None or month_start_date is None:
            dates = pd.read_sql_table('month_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='mid')
            dates.sort_values(['date'], inplace=True)
            if month_end_date is not None:
                month_start_date, month_end_date = cls.isitthefirst(month_start_date, month_end_date)
                dates = dates[(dates['date'] >= month_start_date) & (dates['date'] <= month_end_date)]
            average = []
            averages = []
            for item in range(len(dates)):
                average.append(cls.average_usage(dates['date'].iloc[item].strftime('%Y-%m-%d')))
            for i in average:
                if i not in averages:
                    averages.append(i)
            return averages
        else:
            dates = cls.query.filter_by(date=month_start_date).order_by(cls.month, cls.year).all()
            average_properties['day'] = int(datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%d'))
            average_properties['month'] = int(datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%m'))
            average_properties['year'] = int(datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%Y'))
            average_properties['date'] = datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%B %Y')

        for item in range(len(dates)):
            average_properties['usage'] += dates[item].m_usage

        average_properties['usage'] /= len(dates)
        return average_properties

    @classmethod
    def view_monthly_usage(cls, uid):
        find = pd.read_sql_table('month_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='mid')
        find.sort_values(['date'], inplace=True)
        f = find[(find['uid'] == uid)]
        days = {}
        for dates in range(len(f)):
            days[dates] = DatatoClass(f, dates, 'month')
        return days

    @classmethod
    def view_specific_monthly_usage(cls, start_date, end_date, uid):
        start_date, end_date = cls.isitthefirst(start_date, end_date)
        s_date_list = [int(datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y')), int(datetime.datetime.strptime(start_date,
                        '%Y-%m-%d').strftime('%m')), int(datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%d'))]
        e_date_list = [int(datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y')), int(datetime.datetime.strptime(end_date,
                        '%Y-%m-%d').strftime('%m')), int(datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%d'))]
        months = 0
        while s_date_list[0] != e_date_list[0] and s_date_list[1] != e_date_list[1]:
            s_date_list[1] += 1
            if s_date_list[1] >= 13:
                s_date_list[0] += 1
                s_date_list[1] = 1
            months += 1
        dates = {}
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(months):
            find = cls.query.filter_by(uid=uid, date=start_date).first()
            dates[i] = find
            start_date = start_date + relativedelta(months=1)
        return dates

    # Under Development
    @classmethod
    def delete_usage(cls, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'DELETE FROM `db`.`month_usage` WHERE `uid`=%s'
        cursor.execute(sql, uid)
        connection.close()

    @classmethod
    def isitthefirst(cls, month_start_date, month_end_date=None, special_date=False):
        month_start_date = datetime.datetime.strptime(month_start_date, '%Y-%m-%d').strftime('%m/%d/%y')
        isitfirst = int(datetime.datetime.strptime(month_start_date, '%m/%d/%y').strftime('%d'))
        s_date = datetime.datetime.strptime(month_start_date, '%m/%d/%y')
        while isitfirst != 1:
            month_start_date = (datetime.datetime.strptime(month_start_date, '%m/%d/%y') - datetime.timedelta(days=1)).strftime(
                '%m/%d/%y')
            isitfirst = int(datetime.datetime.strptime(month_start_date, '%m/%d/%y').strftime('%d'))
            s_date = datetime.datetime.strptime(month_start_date, '%m/%d/%y')
        if month_end_date is not None:
            month_end_date = datetime.datetime.strptime(month_end_date, '%Y-%m-%d').strftime('%m/%d/%y')
            isitfirst = int(datetime.datetime.strptime(month_end_date, '%m/%d/%y').strftime('%d'))
            e_date = datetime.datetime.strptime(month_end_date, '%m/%d/%y')
            while isitfirst != 1:
                month_end_date = (datetime.datetime.strptime(month_end_date, '%m/%d/%y') + datetime.timedelta(days=1)).strftime(
                    '%m/%d/%y')
                isitfirst = int(datetime.datetime.strptime(month_end_date, '%m/%d/%y').strftime('%d'))
                e_date = datetime.datetime.strptime(month_end_date, '%m/%d/%y')
            month_start_date = datetime.datetime.strptime(month_start_date, '%m/%d/%y').strftime('%Y-%m-%d')
            month_end_date = datetime.datetime.strptime(month_end_date, '%m/%d/%y').strftime('%Y-%m-%d')
            if special_date is not False:
                return month_start_date, month_end_date, s_date, e_date
            else:
                return month_start_date, month_end_date
        else:
            month_start_date = datetime.datetime.strptime(month_start_date, '%m/%d/%y').strftime('%B')
            return month_start_date


class RandomDateRangeUsage(db.Model):
    __tablename__ = 'random_date_range_usage'
    rid = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    r_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @classmethod
    def new_entry(cls, start_date, end_date, usage, uid):
        start_date_datetime = datetime.datetime.strptime(start_date, '%m/%d/%y')
        end_date_datetime = datetime.datetime.strptime(end_date, '%m/%d/%y')
        random_range = end_date_datetime - start_date_datetime
        average_usage = usage / random_range.days
        dates = []
        if random_range.days < 7:
            for days in range(random_range.days):
                dates.append(start_date_datetime.strftime('%Y-%m-%d'))
                start_date_datetime = datetime.timedelta(days=1) + start_date_datetime
            for day in range(random_range.days):
                DayUsage.new_day_entry(str(dates[day]), average_usage, uid)
        if 7 <= random_range.days < 30:
            for days in range(random_range.days):
                dates.append(start_date_datetime.strftime('%Y-%m-%d'))
                start_date_datetime = datetime.timedelta(days=1) + start_date_datetime
            for position, date in enumerate(dates):
                weekday = int(datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%w'))
                if weekday == 0:
                    try:
                        if len(dates[position:]) < 7:
                            week = []
                            for i in dates[position:]:
                                week.append(i)
                        else:
                            week = []
                            for i in range(len(dates[position: position + 7])):
                                week.append(dates[position + i])
                    except AttributeError:
                        pass
                    else:
                        if len(week) == 7:
                            WeekUsage.new_week_entry(week[0], average_usage, uid)
                        else:
                            for dates in week:
                                DayUsage.new_day_entry(dates, average_usage, uid)


if __name__ == '__main__':
    dc.db.create_all()
