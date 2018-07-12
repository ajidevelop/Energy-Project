__author__ = "Daniel Ajisafe"

import threading


class EnergyUsage:

    def __init__(self):
        self.day_usage = {}
        self.week_usage = {}
        self.month_usage = {}
        self.total_usage = 0
        thread = threading.Thread(target=self.update_usage())
        thread.daemon = True
        thread.start()

    def __repr__(self):
        return f'{self.day_usage} \n{self.week_usage} \n{self.total_usage}'

    def new_day(self, day_number, kwhpd):
        self.day_usage[f'Day {day_number}'] = kwhpd

    def new_week(self, week_number, kwhpw=None):
        if kwhpw is not None:
            self.week_usage[f'Week {week_number}'] = kwhpw
        else:
            try:
                for num in range(1, 8):
                    self.week_usage[f'Week {week_number}'] += self.day_usage[f'Day {num}']
            except TypeError:
                m = []
                for day in range(1, 8):
                    if type(self.day_usage[f'Day {day}']) == str:
                        m.append(f'Day {day}')
                print(f'You inputted a string instead of an integer on {m}')
            except KeyError:
                print("Not enough days in the week")

    def new_month(self, month_name, kwhpm=None):
        if kwhpm is not None:
            self.month_usage[f'Month {month_name}'] = kwhpm
        else:
            try:
                for num in range(1, 5):
                    self.month_usage[f'Week {month_name}'] += self.week_usage[f'Week {num}']
            except TypeError:
                m = []
                for week in range(1, 5):
                    if type(self.week_usage[f'Week {week}']) == str:
                        m.append(f'Week {week}')
                print(f'You inputted a string instead of an integer on {m}')
            except KeyError:
                print("Not enough days in the week")

    def update_usage(self):
        for num in range(len(self.day_usage)):
            self.total_usage += self.day_usage[f'Day {num + 1}']


class EnergyCost(EnergyUsage):

    def __init__(self):
        super().__init__()
        self.group1to500 = 0
        self.group501to1000 = 0
        self.group1001_plus = 0
        self.total_costs = 0
        self.daily_costs = 0
        self.weekly_costs = 0
        self.monthly_costs = 0

    def costs(self):
        if self.total_usage <= 500:
            self.total_costs = self.total_usage * self.group1to500
        elif 501 >= self.total_usage <= 1000:
            self.total_costs = self.total_usage * self.group501to1000
        elif 1001 >= self.total_usage:
            self.total_costs = self.total_usage * self.group1001_plus


Dan = EnergyUsage()
Dan.new_day(1, '10')
Dan.new_day(2, 10)
Dan.new_day(3, 10)
Dan.new_day(4, 10)
Dan.new_day(5, 10)
Dan.new_day(6, 10)
Dan.new_day(7, 10)
Dan.new_day(1, 10)
Dan.new_week(1)
Dan.update_usage()
print(Dan)
