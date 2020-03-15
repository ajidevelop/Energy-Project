__author__ = 'DanielAjisafe'
import python_console.database.database_connect as dc
from python_console.database.database_connect import db
import python_console.User.login as login
import datetime
import python_console.utilities.exceptions as e
import sys

# TODO - ADD WAY TO CHECK IF DATE ENTERED IS VALID - FOR LOOP IF FIRST TWO DIGITS ARE LESS THAN 31


class DayUsage(db.Model):
    __tablename__ = 'day_usage'
    day_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    d_usage = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.ForeignKey('users.uid'), nullable=False)

    def new_day_entry(self, day, month, year, d_usage):
        find = len(__class__.query.filter(__class__.uid == login.uid, __class__.date == datetime.date(year, month, day)).all())
        try:
            if find == 1:
                raise e.DayExist
            else:
                try:
                    self.date = datetime.date(year, month, day)
                except TypeError:  # one of the variables is not a number
                    return False
        except e.DayExist:
                user = input("Would you like to edit the entry? (Y/N): ")
                while user not in {'Y', 'N'}:
                    user = input('Enter "Y" for yes, "N" for no please: ')
                if user == "N":
                    sys.exit()
                if user == 'Y':
                    __class__.edit_day_entry(self)
        self.d_usage = d_usage
        self.uid = login.uid

    @classmethod
    def view_all_daily_usage(cls):
        find = cls.query.filter(cls.uid == login.uid).order_by(__class__.date).all()
        position = {}
        for dates in range(len(find)):
            position[find[dates].date] = find[dates].d_usage
            print(position)
        return position

    def edit_day_entry(self):
        pass

    # def view_day_usage(self, day=None, month=None, year=None):


def new_week_entry(date_range, w_usage_input):
    connection = dc.connectdb()
    cursor = connection.cursor()
    w_usage = "INSERT INTO `week_usage` (`date_range`, `w_usage`, `uid`) VALUES (%s, %s, %s)"
    cursor.execute(w_usage, (f'{date_range}', w_usage_input, login.uid))
    connection.close()


new_user = DayUsage()
new_user.new_day_entry(11, 10, 2014, 12)
print(new_user.view_all_daily_usage())
