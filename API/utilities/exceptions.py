class DayExist(Exception):

    def __init__(self, arguments):
        super().__init__("Day Already Exists")
        self.arguments = arguments


class NeedVerificationCode(Exception):
    def __init__(self):
        super().__init__()


class WrongPassword(Exception):
    def __init__(self):
        super().__init__()


class NoEmail(Exception):
    def __init__(self):
        super().__init__()


class TakenField(Exception):
    def __init__(self, args, field):
        super().__init__(f'The {field} "{args}" is already taken')


class InvalidEmail(Exception):
    def __init__(self, args):
        super().__init__(f'The email "{args}" is invalid')
