__author__ = 'DanielAjisafe'
import database.database_connect as dc
from database.database_connect import db
import User.login as login

# TODO - ADD WAY TO CHECK IF DATE ENTERED IS VALID - FOR LOOP IF FIRST TWO DIGITS ARE LESS THAN 31

class day_usage(db.Model):

    day_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255))




def new_day_entry(date, d_usage_input):
    connection = dc.connectdb()
    cursor = connection.cursor()
    d_usage = "INSERT INTO `day_usage` (`date`, `d_usage`, `uid`) VALUES (%s, %s, %s)"
    cursor.execute(d_usage, (f'{date}', d_usage_input, login.uid))
    connection.close()


def new_week_entry(date_range, w_usage_input):
    connection = dc.connectdb()
    cursor = connection.cursor()
    w_usage = "INSERT INTO `week_usage` (`date_range`, `w_usage`, `uid`) VALUES (%s, %s, %s)"
    cursor.execute(w_usage, (f'{date_range}', w_usage_input, login.uid))
    connection.close()

