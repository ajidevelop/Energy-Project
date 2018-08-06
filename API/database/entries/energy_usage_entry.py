__author__ = 'DanielAjisafe'
import API.database.database_connect as dc
from API.database.database_connect import db
import datetime
import API.utilities.exceptions as e
from API.utilities.important_variables import Average


class DayUsage(db.Model):
    __tablename__ = 'day_usage'
    day_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(2), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(2), nullable=False)
    d_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @staticmethod
    def new_day_entry(date, d_usage, uid):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%y')
        day = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d')
        month = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m')
        year = datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y')
        find = len(__class__.query.filter_by(uid=uid, date=date).all())
        if find == 1:
            return e.DayExist
        cursor = dc.connectdb().cursor()
        sql = 'INSERT INTO `day_usage` (`date`, `day`, `month`, `year`, `d_usage`, `uid`) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (date, day, month, year, d_usage, uid))
        dc.connectdb().close()

    @classmethod
    def view_all_daily_usage(cls, uid):
        find = cls.query.filter(cls.uid == uid).order_by(__class__.year, __class__.month, __class__.day).all()
        test = {}
        for dates in range(len(find)):
            test[dates] = find[dates]
        return test

    @classmethod
    def delete_day_entry(cls, dates, uid):
        cursor = dc.connectdb().cursor()
        for date in dates:
            sql = 'DELETE FROM `db`.`day_usage` WHERE (`date`=%s AND `uid`=%s)'
            cursor.execute(sql, (date, uid))
        dc.connectdb().close()

    @classmethod
    def edit_day_entry(cls, date, usage, uid):
        cursor = dc.connectdb().cursor()
        sql = 'UPDATE `day_usage` SET `d_usage`=%s WHERE (`date`=%s AND `uid`=%s)'
        cursor.execute(sql, (usage, date, uid))
        dc.connectdb().close()

    @classmethod
    def average_usage(cls, date=None, month=None, year=None):
        average_properties = Average({'usage': 0})
        if date is not None:
            dates = cls.query.filter_by(date=date).order_by(cls.year, cls.month, cls.day).all()
            average_properties['day'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d'))
            average_properties['month'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m'))
            average_properties['year'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y'))
            average_properties['date'] = datetime.date(average_properties.year, average_properties.month, average_properties.day)
        elif month is not None:
            dates = cls.query.filter_by(month=month, year=year).order_by(cls.year, cls.month, cls.day).all()
        elif year is not None:
            dates = cls.query.filter_by(year=year).order_by(cls.year, cls.month, cls.day).all()
        else:
            dates = cls.query.order_by(cls.year, cls.month, cls.day).all()
            average = []
            for item in range(len(dates)):
                average.append(cls.average_usage(date=dates[item].date))
            return average

        for item in range(len(dates)):
            average_properties['usage'] += dates[item].d_usage

        average_properties['usage'] /= len(dates)
        return average_properties

    @classmethod
    def date_range(cls, start_date, end_date):
        date_range = cls.query.filter


class WeekUsage(db.Model):
    __tablename__ = 'week_usage'
    week_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    w_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @classmethod
    def new_week_entry(cls, start_date, end_date, w_usage_input, uid):
        find = cls.query.filter_by(start_date=start_date, end_date=end_date, uid=uid).first()
        print(find)


class RandomDateRangeUsage(db.Model):
    __tablename__ = 'random_date_range_usage'
    rid = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    r_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @classmethod
    def new_entry(cls, start_date, end_date, usage, uid):
        random_range = end_date - start_date
        if random_range.days < 7:
            average_usage = usage / random_range.days
            dates = []
            for days in range(random_range.days):
                dates.append(start_date)
                start_date = datetime.timedelta(days=1) + start_date
            for day in range(random_range.days):
                DayUsage.new_day_entry(str(dates[day]), average_usage, uid)


if __name__ == '__main__':
    new_user = RandomDateRangeUsage
    # new_user.new_day_entry('2017-10-12', 14, 64)
    test = DayUsage
    print(test.average_usage())

    print(new_user.new_entry(datetime.date(2018, 6, 2), datetime.date(2018, 6, 5), 20, 64))
    # for pos in range(len(new_user.view_all_daily_usage(64))):
    #     print(f'You used {new_user.view_all_daily_usage(64)[pos].d_usage} on {new_user.view_all_daily_usage(64)[pos].year}')
