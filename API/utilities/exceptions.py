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



