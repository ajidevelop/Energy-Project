__author__ = 'DanielAjisafe'
import EnergyProject.entries.energy_usage_entry as eue


entry = input("Insert a date and usage and separate with comma: ").split(', ')
try:
    usage = int(entry[1])
except TypeError:
    usage = input("Please type a number")
eue.new_day_entry(entry[0], usage)

