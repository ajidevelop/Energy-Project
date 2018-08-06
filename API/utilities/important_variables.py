__author__ = 'DanielAjisafe'


class Average(dict):

    def __init__(self, *args, **kwargs):
        super(Average, self).__init__(*args, *kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Average, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delattr__(item)

    def __delitem__(self, key):
        super(Average, self).__delitem__(key)
        del self.__dict__[key]

class UserAverage(Average):

    def __init__(self):
        super(UserAverage, self).__init__()

