import pymysql.cursors
import User.email_verification as ev
from argon2 import exceptions as e
from argon2 import PasswordHasher
ph = PasswordHasher()


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


def new_user(u, p, email):
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
            cursor.execute(sql, (find_user(u), email, token))
            print("Verification code sent to your email.")
    finally:
        connection.close()


def returning_user(u, p, email=False):
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
            if verify_password(result, p) is False:
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


def find_user(u, email=False):
    connection = connectdb()
    cursor = connection.cursor()
    if email:
        sql = "SELECT `uid` FROM `users` WHERE `email`=%s"

    else:
        sql = "SELECT `uid` FROM `users` WHERE `username`=%s"
    cursor.execute(sql, u)
    result = cursor.fetchone()
    connection.close()
    return result['uid']


def find_email(u, email=False):
    connection = connectdb()
    cursor = connection.cursor()
    if email:
        sql = "SELECT `email` FROM `users` WHERE `email`=%s"
    else:
        sql = "SELECT `email` FROM `users` WHERE `username`=%s"
    cursor.execute(sql, u)
    result = cursor.fetchone()
    connection.close()
    return result['email']


def verify_password(result, p):
    try:
        ph.verify(result['password'], p)
        return True
    except e.VerifyMismatchError:
        return False


def check_verification(u, email=False):
    result = find_email(u, email)
    if result == 'N':
        return False
    elif result == 'Y':
        return True


def check_verification_token(token):
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


def resend_verification_email(email):
    connection = connectdb()
    cursor = connection.cursor()
    token = ev.send_verification_email(email)
    sql = "UPDATE `verification` SET `token`=%s WHERE `email`=%s"
    cursor.execute(sql, (token, email))
    connection.close()


def email_verified(email):
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


def change_password(email, p):
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
