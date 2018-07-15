__author__ = 'DanielAjisafe'

day = input("Day: ")
try:
    use = int(day)
except TypeError:
    usage = input("Please type a number")
    raise
month = input('Month: ')
year = input('Year: ')
usage = input('Usage: ')

