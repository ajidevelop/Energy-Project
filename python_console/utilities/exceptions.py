class DayExist(Exception):

    def __init__(self, arguments):
        super().__init__("Day Already Exists")
        self.arguments = arguments
