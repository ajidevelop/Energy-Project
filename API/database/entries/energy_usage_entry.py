__author__ = 'DanielAjisafe'
import API.database.database_connect as dc
from API.database.database_connect import db
import API.User.login as login
import datetime
import API.utilities.exceptions as e

# TODO - ADD WAY TO CHECK IF DATE ENTERED IS VALID - FOR LOOP IF FIRST TWO DIGITS ARE LESS THAN 31


class DayUsage(db.Model):
    __tablename__ = 'day_usage'
    day_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    d_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    @staticmethod
    def new_day_entry(date, d_usage, uid):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%y')
        find = len(__class__.query.filter_by(uid=uid, date=date).all())
        print(find)
        if find == 1:
            return e.DayExist
        cursor = dc.connectdb().cursor()
        sql = 'INSERT INTO `day_usage` (`date`, `d_usage`, `uid`) VALUES (%s, %s, %s)'
        cursor.execute(sql, (date, d_usage, uid))
        dc.connectdb().close()

    @classmethod
    def view_all_daily_usage(cls, uid):
        find = cls.query.filter(cls.uid == uid).order_by(__class__.date).all()
        position = {}
        test = {}
        for dates in range(len(find)):
            position[find[dates].date] = find[dates].d_usage
            test[dates] = find[dates]

        return test

    @classmethod
    def delete_day_entry(cls, dates, uid):
        cursor = dc.connectdb().cursor()
        for date in dates:
            sql = 'DELETE FROM `db`.`day_usage` WHERE (`date`=%s AND `uid`=%s)'
            cursor.execute(sql, (date, uid))
        dc.connectdb().close()

    def edit_day_entry(self):
        pass

    # def view_day_usage(self, day=None, month=None, year=None):


def new_week_entry(date_range, w_usage_input):
    connection = dc.connectdb()
    cursor = connection.cursor()
    w_usage = "INSERT INTO `week_usage` (`date_range`, `w_usage`, `uid`) VALUES (%s, %s, %s)"
    cursor.execute(w_usage, (f'{date_range}', w_usage_input, login.user_class))
    connection.close()


if __name__ == '__main__':
    new_user = DayUsage()
    new_user.new_day_entry('2015-10-12', 14, 64)

    for pos in range(len(new_user.view_all_daily_usage(64))):
        print(f'You used {new_user.view_all_daily_usage(64)[pos].d_usage} on {new_user.view_all_daily_usage(64)[pos].date}')
