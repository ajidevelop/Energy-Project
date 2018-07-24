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
            token_entry = input('Verification code (If you have no code or need a new one type n): ')
            while token_entry == 'n' or not dcV.check_verification_token(token_entry):
                token_entry = input('Incorrect verification code (If None type n): ')
            if dcV.check_verification_token(token_entry):
                dcU.email_verified(dcU.find_email(u, check_if_email(u)))
                print(f'Welcome {cu}')
            else:
                entry = input('You much verify your email to use the program. Would you like to resend verification email? (y/n)')
                while entry not in {'y', 'n'}:
                    entry = input('Enter "y" for yes, "n" for no please: ')
                if entry == 'y':
                    dcV.resend_verification_email(dcU.find_email(u, check_if_email(u)))
                    print('Sent')
                elif entry == 'n':
                    sys.exit()
    elif cu is False:
        raise e.WrongPassword
    return int(dcU.find_user(u, check_if_email(u)))


def create_user(u, p, email, fName, lName):
    try:
        for letter in u:
            for symbol in ("!@#$%^&*()=?/><:;{[]}|"):
                if symbol == letter:
                    raise error.IntegrityError
        dcU.new_user(u, p, email, fName, lName)
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


user_logged_in = False
