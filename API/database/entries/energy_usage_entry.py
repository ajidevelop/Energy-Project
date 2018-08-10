__author__ = 'DanielAjisafe'
import API.database.database_connect as dc
from API.database.database_connect import db
import datetime
import API.utilities.exceptions as e
from API.utilities.important_variables import Average
import random


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
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'INSERT INTO `day_usage` (`date`, `day`, `month`, `year`, `d_usage`, `uid`) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (date, day, month, year, d_usage, uid))

    @classmethod
    def view_all_daily_usage(cls, uid):
        find = cls.query.filter(cls.uid == uid).order_by(cls.year, cls.month, cls.day).all()
        days = {}
        for dates in range(len(find)):
            days[dates] = find[dates]
        cls.create_week_usage(uid)
        return days

    @classmethod
    def delete_day_entry(cls, dates, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        for date in dates:
            try:
                day_number = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%w'))
                date1 = datetime.datetime.strptime(date, '%m/%d/%y')
                date2 = date1 - datetime.timedelta(days=day_number)
                find = WeekUsage.query.filter_by(week_start_date=date2, uid=uid).first()
                finder = cls.query.filter_by(date=date, uid=uid).first()
                w_usage = find.w_usage - finder.d_usage
                sql = 'UPDATE `week_usage` SET `w_usage`=%s WHERE (`week_start_date`=%s AND `uid`=%s)'
                cursor.execute(sql, (w_usage, date2, uid))
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
    def average_usage(cls, date=None):
        average_properties = Average({'usage': 0})
        if date is not None:
            dates = cls.query.filter_by(date=date).order_by(cls.year, cls.month, cls.day).all()
            average_properties['day'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%d'))
            average_properties['month'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%m'))
            average_properties['year'] = int(datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y'))
            average_properties['date'] = datetime.date(average_properties.year, average_properties.month, average_properties.day)
        else:
            dates = cls.query.order_by(cls.year, cls.month, cls.day).all()
            average = []
            averages = []
            for item in range(len(dates)):
                average.append(cls.average_usage(dates[item].date))
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
            w_usage += item.d_usage
            weekday = int(datetime.datetime.strptime(item.date, '%m/%d/%y').strftime('%w'))
            if weekday == 0:
                try:
                    week = []
                    for i in range(len(dates[position: position + 7])):
                        days = datetime.datetime.strptime(dates[position + i].date, '%m/%d/%y') \
                        - datetime.datetime.strptime(dates[position + i - 1].date, '%m/%d/%y')
                        if i == 0:
                            week.append(dates[position])
                        elif days.days == 1:
                            week.append(dates[position + i])
                        else:
                            break
                except AttributeError:
                    pass
                else:
                    if len(week) == 7:
                        WeekUsage.new_week_entry(datetime.datetime.strptime(week[0].date, '%m/%d/%y').strftime('%Y-%m-%d'), w_usage, uid)
                        w_usage = 0


class WeekUsage(db.Model):
    __tablename__ = 'week_usage'
    week_id = db.Column(db.Integer, primary_key=True)
    week_start_date = db.Column(db.Date, nullable=False)
    week_start_year = db.Column(db.Integer, nullable=False)
    week_start_month = db.Column(db.Integer, nullable=False)
    week_start_day = db.Column(db.Integer, nullable=False)
    w_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @classmethod
    def new_week_entry(cls, week_start_date, w_usage_input, uid):
        find = len(cls.query.filter_by(week_start_date=week_start_date, uid=uid).all())
        day = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%d')
        month = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%m')
        year = datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%Y')
        if find == 1:
            return e.DayExist
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'INSERT INTO `week_usage` (week_start_date, `week_start_day`, `week_start_month`, `week_start_year`, `w_usage`, `uid`) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (week_start_date, day, month, year, w_usage_input, uid))
        connection.close()

    @classmethod
    def average_usage(cls, week_start_date=None):
        average_properties = Average({'usage': 0})
        if week_start_date is not None:
            dates = cls.query.filter_by(week_start_date=week_start_date).order_by(cls.week_start_date).all()
            average_properties['week_start_day'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%d'))
            average_properties['week_start_month'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%m'))
            average_properties['week_start_year'] = int(datetime.datetime.strptime(week_start_date, '%Y-%m-%d').strftime('%Y'))
            average_properties['week_start_date'] = datetime.date(average_properties.week_start_year, average_properties.week_start_month,
                                                                  average_properties.week_start_day)
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

        for item in range(len(dates)):
            average_properties['usage'] += dates[item].w_usage

        average_properties['usage'] /= len(dates)
        return average_properties

    @classmethod
    def view_weekly_usage(cls, uid):
        find = cls.query.filter_by(uid=uid).order_by(cls.week_start_year, cls.week_start_month, cls.week_start_day).all()
        days = {}
        for dates in range(len(find)):
            days[dates] = find[dates]
        return days

    @classmethod
    def delete_usage(cls, uid):
        connection = dc.connectdb()
        cursor = connection.cursor()
        sql = 'DELETE FROM `db`.`week_usage` WHERE `uid`=%s'
        cursor.execute(sql, uid)
        connection.close()


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
    new_user = RandomDateRangeUsage
    test = WeekUsage
    test1 = DayUsage
    test2 = Average
    # test1.new_day_entry('2018-10-30', 35, 64)
    # date = datetime.datetime.strptime('1/1/18', '%m/%d/%y')
    # print(date)
    # for day in range(365):
    #     date = date.strftime('%Y-%m-%d')
    #     test1.new_day_entry(date, random.randrange(10, 50), 52)
    #     date = datetime.datetime.strptime(date, '%Y-%m-%d')
    #     date = date + datetime.timedelta(days=1)
    #     print(date)
    test1.create_week_usage(52)

    # print(test1.average_usage(str(test1.average_usage()[0].date)))
    # print(test.new_week_entry(datetime.date(2018, 6, 2), 70, 64))

    # print(new_user.new_entry('06/02/18', '06/05/18', 20, 64))
    # for pos in range(len(new_user.view_all_daily_usage(64))):
    #     print(f'You used {new_user.view_all_daily_usage(64)[pos].d_usage} on {new_user.view_all_daily_usage(64)[pos].year}')
