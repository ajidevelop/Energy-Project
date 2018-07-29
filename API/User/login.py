__author__ = 'DanielAjisafe'

from API.database.database_connect import Users as dcU
from API.database.database_connect import Verification as dcV
import API.User.email_verification as ev
import pymysql.err as error
import sys
from argon2 import PasswordHasher
ph = PasswordHasher()
import API.utilities.exceptions as e


def check_if_email(u):
    for let in u:
        if let == '@':
            return True
        else:
            return False


def check_user(u, p):
    cu = dcU.returning_user(u, p, check_if_email(u))
    if cu is not False:
        if dcU.check_verification(u, check_if_email(u)):
            return f'Welcome back {cu}'
        else:
            raise e.NeedVerificationCode()
    elif cu is False:
        raise e.WrongPassword
    return int(dcU.find_user(u, check_if_email(u)))


def create_user(u, p, email, fName, lName):
    try:
        for letter in u:
            for symbol in ("!@#$%^&*()=?/><:;{[]}|"):
                if symbol == letter:
                    raise error.IntegrityError
        dcU.new_user(u, p, email, fName.capitalize(), lName.capitalize())
    except error.IntegrityError as exception:
        if str(exception) == str((1062, f"Duplicate entry '{u}' for key 'username'")):
            raise e.TakenField(u, 'username')
        if str(exception) == str((1062, f"Duplicate entry '{email}' for key 'email'")):
            raise e.TakenField(email, 'email')
    except ValueError:
        raise e.InvalidEmail(email)


def reset_password(email):
    ev.send_verification_email(email)
    print("Verification Code Sent.")
    token = input("Verification Code (press q to quit): ")
    while dcV.check_verification_token(token) is False or token == 'q':
        print("Invalid Verification Code")
        input("Verification code (press q to quit): ")
    new_pass = input("New Password: ")
    new_pass_verify = input("Re-enter new password: ")
    while new_pass != new_pass_verify:
        print("Passwords do not match. Try Again.")
        new_pass = input("New Password: ")
        new_pass_verify = input("Re-enter new password: ")
    if dcU.change_password(email, new_pass):
        print("Password Reset")
    else:
        print('Error')
        sys.exit()


user_class = None
user_logged_in = False
