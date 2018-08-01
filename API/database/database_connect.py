import pymysql.cursors
import API.User.email_verification as ev
from argon2 import exceptions as e
import API.utilities.exceptions as mye
from argon2 import PasswordHasher
ph = PasswordHasher()

# Flask Support
from flask_sqlalchemy import SQLAlchemy
import datetime
import webapp.app_config as ac
from flask_login import UserMixin

db = SQLAlchemy(ac.app)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    verified = db.Column(db.String(1), nullable=False)
    user_since = db.Column(db.TIMESTAMP, default=datetime.datetime.today(), nullable=False)

    def get_id(self):
        return self.uid

    @staticmethod
    def new_user(u, p, email, fName, lName):
        _new_user(u, p, email, fName, lName)

    @classmethod
    def returning_user(cls, u, p, email=False):
        if email:
            find = cls.query.filter_by(email=u).first()
        else:
            find = cls.query.filter_by(username=u).first()
        try:
            if Users.verify_password(find, p) is False:
                return False
        except AttributeError:
            return False
        return find

    @classmethod
    def find_user(cls, u, email=False):
        if email:
            return cls.query.filter_by(email=u).first().uid
        else:
            return cls.query.filter_by(username=u).first().uid

    @classmethod
    def find_email(cls, u, email=False):
        if email:
            return cls.query.filter_by(email=u).first().email
        else:
            return cls.query.filter_by(username=u).first().email

    @staticmethod
    def verify_password(result, p):
        try:
            ph.verify(result.password, p)
            return True
        except e.VerifyMismatchError:
            return False

    @staticmethod
    def check_verification(u, email=False):
        return _check_verification(u, email)

    @classmethod
    def email_verified(cls, e_mail, token=None):
        e_mail, email = _email_verified(e_mail, token)
        if e_mail:
            return cls.query.filter_by(email=email).first().username

    @staticmethod
    def change_password(email, p):
        return _change_password(email, p)

    @classmethod
    def check_if_loggedin(cls, uid):
        return cls.query.filter_by(uid=uid).logged_in

    @staticmethod
    def logoff(uid):
        _logoff(uid)


class Verification(db.Model):
    __tablename__ = 'verification'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    token = db.Column(db.String(30), unique=True, nullable=False)
    ts_create = db.Column(db.TIMESTAMP, default=datetime.datetime.today(), nullable=False)

    @staticmethod
    def check_verification_token(token):
        return _check_verification_token(token)

    @staticmethod
    def resend_verification(email):
        try:
            Users.find_email(email, True)
            return _resend_verification_email(email)
        except AttributeError:
            raise mye.NoEmail


def connectdb():
    # Connect to the database
    connection = pymysql.connect(host='GOSHEN-SPECTRE',
                                 port=3307,
                                 user='python',
                                 password='pyth0n_@ccess',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection


def _new_user(u, p, email, fName, lName):
    connection = connectdb()
    p = ph.hash(p)
    ev.verify_email(email)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`username`, `password`, `email`, `fName`, `lName`, `verified`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (u, p, email, fName, lName, 'N'))
            token = ev.send_verification_email(email)
            sql = "INSERT INTO `verification` (`uid`, `email`, `token`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (Users.find_user(u), email, token))
            print("Verification code sent to your email.")
    finally:
        connection.close()


def _check_verification(u, email=False):
    connection = connectdb()
    cursor = connection.cursor()
    result = Users.find_email(u, email)
    sql = "SELECT `verified` FROM `users` WHERE `email`=%s"
    cursor.execute(sql, result)
    result = cursor.fetchone()['verified']
    try:
        if result == 'N':
            return False
        elif result == 'Y':
            return True
    finally:
        connection.close()


def _check_verification_token(token):
    connection = connectdb()
    cursor = connection.cursor()
    sql = "SELECT `token` FROM `verification` WHERE `token`=%s"
    cursor.execute(sql, token)
    try:
        cursor.fetchone()['token']
    except TypeError:
        return False
    else:
        return True
    finally:
        connection.close()


def _resend_verification_email(email):
    connection = connectdb()
    cursor = connection.cursor()
    token = ev.send_verification_email(email)
    sql = "UPDATE `verification` SET `token`=%s WHERE `email`=%s"
    cursor.execute(sql, (token, email))
    connection.close()


def _email_verified(email, token=None):
    connection = connectdb()
    cursor = connection.cursor()
    if token is not None:
        sql1 = "SELECT `email` FROM `verification` WHERE `token`=%s"
        cursor.execute(sql1, token)
        email = cursor.fetchone()['email']
        sql = "UPDATE `users` SET `verified`='Y' WHERE `email`=%s"
        result = cursor.execute(sql, email)
    else:
        sql = "UPDATE `users` SET `verified`='Y' WHERE `email`=%s"
        result = cursor.execute(sql, email)
    try:
        if result == 1:
            sql = "DELETE FROM `db`.`verification` WHERE `email`=%s"
            cursor.execute(sql, email)
            return True, email
        elif result == 0:
            return False
    finally:
        connection.close()


def _change_password(email, p):
    connection = connectdb()
    cursor = connection.cursor()
    sql = "UPDATE `users` SET `password`=%s WHERE `email`=%s"
    result = cursor.execute(sql, (p, email))
    try:
        if result == 1:
            return True
        elif result == 0:
            return False
    finally:
        connection.close()


def _logoff(uid):
    connection = connectdb()
    cursor = connection.cursor()
    sql = "DELETE FROM `db`.`user_logged_in` WHERE `uid`=%s"
    cursor.execute(sql, uid)


if __name__ == '__main__':
    testUser = Users()
    verify = Verification()
    print(testUser.returning_user('test', 'test'))
