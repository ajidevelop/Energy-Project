import pymysql.cursors
import python_console.User.email_verification as ev
from argon2 import exceptions as e
from argon2 import PasswordHasher
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

ph = PasswordHasher()

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'toyin'
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    verified = db.Column(db.String(1), nullable=False)
    user_since = db.Column(db.TIMESTAMP, default=datetime.datetime.today(), nullable=False)

    @staticmethod
    def new_user(u, p, email):
        _new_user(u, p, email)

    @staticmethod
    def returning_user(u, p, email=False):
        return _returning_user(u, p, email)

    @classmethod
    def find_user(cls, u, email=False):
        if email:
            return cls.query.filter_by(email=email).first().uid
        else:
            return cls.query.filter_by(username=u).first().uid

    @classmethod
    def find_email(cls, u, email=False):
        if email:
            return cls.query.filter_by(email=email).first().email
        else:
            return cls.query.filter_by(username=u).first().email

    @staticmethod
    def verify_password(result, p):
        try:
            ph.verify(result['password'], p)
            return True
        except e.VerifyMismatchError:
            return False

    @staticmethod
    def check_verification(u, email=False):
        return _check_verification(u, email)

    @staticmethod
    def email_verified(email):
        return _email_verified(email)

    @staticmethod
    def change_password(email, p):
        return _change_password(email, p)


class Verification(db.Model):
    __tablename__ = 'verification'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    token = db.Column(db.String(30), unique=True, nullable=False)
    ts_create = db.Column(db.TIMESTAMP, default=datetime.datetime.today(), nullable=False)

    @classmethod
    def check_verification_token(cls, token):
        return _check_verification_token(token)

    @staticmethod
    def resend_verification(email):
        return _resend_verification_email(email)


def connectdb():
    # Connect to the database
    connection = pymysql.connect(host='GOSHEN-SPECTRE',
                                 port=3306,
                                 user='python',
                                 password='pyth0n_@ccess',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection


def _new_user(u, p, email):
    connection = connectdb()
    p = ph.hash(p)
    ev.verify_email(email)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`username`, `password`, `email`, `verified`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (u, p, email, 'N'))
            token = ev.send_verification_email(email)
            sql = "INSERT INTO `verification` (`uid`, `email`, `token`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (Users.find_user(u), email, token))
            print("Verification code sent to your email.")
    finally:
        connection.close()


def _returning_user(u, p, email=False):
    connection = connectdb()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            if email:
                sql = "SELECT `uid`, `username`, `password` FROM `users` WHERE `email`=%s"
            else:
                sql = "SELECT `uid`, `username`, `password` FROM `users` WHERE `username`=%s"
            cursor.execute(sql, u)
            result = cursor.fetchone()
            if Users.verify_password(result, p) is False:
                return False
    except TypeError:
        return False
    else:
        try:
            return result['username'].title()
        except TypeError:
            return False
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


def _email_verified(email):
    connection = connectdb()
    cursor = connection.cursor()
    sql = "UPDATE `users` SET `verified`='Y' WHERE `email`=%s"
    result = cursor.execute(sql, email)
    try:
        if result == 1:
            sql = "DELETE FROM `db`.`verification` WHERE `email`=%s;"
            cursor.execute(sql, email)
            return True
        elif result == 0:
            return False
    finally:
        connection.close()


def _change_password(email, p):
    connection = connectdb()
    cursor = connection.cursor()
    sql = "UPDATE `password` FROM `users` WHERE `email`=%s"
    result = cursor.execute(sql, (p, email))
    try:
        if result == 1:
            return True
        elif result == 0:
            return False
    finally:
        connection.close()


if __name__ == '__main__':
    testUser = Users()
    print(testUser.find_user('fola@email.com', True))