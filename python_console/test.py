def test(**kwargs):
    print(kwargs)


def hello(**kwargs):
    for key, value in kwargs.items():
        test(value)


hello(people=123)
