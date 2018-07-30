import datetime

day = datetime.datetime.strptime('2017-06-15', '%Y-%m-%d').strftime('%d')
print(day)