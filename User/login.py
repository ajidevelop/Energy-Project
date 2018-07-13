__author__ = 'DanielAjisafe'

from database.database_connect import Users as dcU
from database.database_connect import Verification as dcV
import User.email_verification as ev
import pymysql.err as error
import sys
from argon2 import PasswordHasher
ph = PasswordHasher()

user = input('Username or Email: ')
password = input('Password (Forgot Password? Press F): ')


def check_if_email(u):
    for let in u:
        if let == '@':
            return True
        else:
            return False


def check_user(u, p):
    if p == 'F':
        email = input('Email: ')
        reset_password(email)
        u = input('Username or Email: ')
        p = input('Password: ')
        check_user(u, p)
    else:
        cu = dcU.returning_user(u, p, check_if_email(u))
        if cu is not False:
            if dcU.check_verification(u, check_if_email(u)):
                print(f'Welcome back {cu}')
            else:
                token_entry = input('Verification code (If you have no code or need a new one type n): ')
                while token_entry not in ('n', dcV.check_verification_token(token_entry)):
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
            print('Wrong username/password')
            new_user = input('Create new User? y/n (q to leave) ')
            while new_user not in {'q', 'y', 'n'}:
                new_user = input('Enter "y" for yes, "n" for no, or "q" for quit please: ')
            if new_user == 'y':
                u, p = create_user()
                check_user(u, p)
            elif new_user == 'n':
                u = input('Username or Email: ')
                p = input('Password (Forgot Password? Press F): ')
                check_user(u, p)
            elif new_user == 'q':
                sys.exit()
        return int(dcU.find_user(u, check_if_email(u)))


def create_user():
    u = input('Username: ')
    p = input('Password: ')
    email = input('Email: ')
    try:
        dcU.new_user(u, p, email)
    except error.IntegrityError as e:
        if str(e) == str((1062, f"Duplicate entry '{u}' for key 'username'")):
            print("Username is taken")
            create_user()
        if str(e) == str((1062, f"Duplicate entry '{email}' for key 'email'")):
            print("Email is taken")
            create_user()
    except ValueError:
        print("Invalid Email")
        create_user()
    else:
        return u, p


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


uid = check_user(user, password)
