__author__ = 'LobaAjisafe'

from selenium import webdriver, common as se
import time
import pandas as pd
import calendar
from datetime import datetime, timedelta
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def round_time(dt=None, round_to=60 * 60):
    if dt is None:
        dt = datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)


def edit_url(month, year, location=('rosenberg', 'usa')):
    url = f'https://www.timeanddate.com/weather/{location[1]}/{location[0]}/historic?month={month}&year={year}'
    return url


def edit_dataframe(df, y, m, d):
    new_header = [i[1] for i in list(df.columns)]
    df.columns = new_header
    df = df.drop([df.columns[1], df.columns[3], df.columns[5]], axis=1)
    idx = df.iloc[0, 0].index('m') + 1
    df.iloc[0, 0] = df.iloc[0, 0][0:idx]
    df = df.drop(df.tail(1).index)

    df = df.rename(columns={'Time': 'DateTime'})
    for i, row in df.iterrows():
        row[0] = datetime.strptime(row[0], '%I:%M %p')
        df.iloc[i, 0] = str(round_time(datetime(y, m, d, row[0].hour, row[0].minute)))  # format time into datetime
        df.iloc[i, 1] = int(df.iloc[i, 1].split()[0])  # Converts temp to int
        try:  # Converts wind to int
            df.iloc[i, 2] = int(df.iloc[i, 2].split()[0])
        except ValueError:  # if No wind
            df.iloc[i, 2] = 0
        except AttributeError:
            pass
        try:  # Converts humidity to int
            df.iloc[i, 3] = int(df.iloc[i, 3][:-1])
        except TypeError:  # if N/A
            pass
        try:  # Converts barometer to int
            df.iloc[i, 4] = float(df.iloc[i, 4].split()[0])
        except TypeError:  # if N/A
            pass
        try:  # Converts visibility to int
            df.iloc[i, 5] = int(df.iloc[i, 5].split()[0])
        except TypeError:  # if N/A
            pass
    df = df.drop_duplicates(subset='DateTime', keep="first").reset_index(drop=True)

    df = df.astype({
        'Temp': float,
        'Wind': float,
        'Humidity': float,
        'Barometer': float,
        'Visibility': float
    })

    if len(df.index) < 24:
        i = 0
        while len(df.index) < 24:
            if len(df.index) == 23 and datetime.strptime(df.iloc[22, 0], '%Y-%m-%d %H:%M:%S').hour != 0:
                line = pd.DataFrame({
                    'DateTime': str(datetime(y, m, d+1, 0, 0)),
                    'Temp': np.nan,
                    'Wind': np.nan,
                    'Humidity': np.nan,
                    'Barometer': np.nan,
                    'Visibility': np.nan
                }, index=[23])
                df = pd.concat([df.iloc[:i-1], line]).reset_index(drop=True)
                break

            try:
                assert i < len(df.index)
            except AssertionError:
                line = pd.DataFrame({
                    'DateTime': str(datetime(y, m, d, i+1, 0)),
                    'Temp': np.nan,
                    'Wind': np.nan,
                    'Humidity': np.nan,
                    'Barometer': np.nan,
                    'Visibility': np.nan
                }, index=[i])
                df = pd.concat([df.iloc[:len(df.index)], line]).reset_index(drop=True)
                i += 1
                continue

            if datetime.strptime(df.iloc[i, 0], '%Y-%m-%d %H:%M:%S').hour != i + 1:
                line = pd.DataFrame({
                    'DateTime': str(datetime(y, m, d, i+1, 0)),
                    'Temp': np.nan,
                    'Wind': np.nan,
                    'Humidity': np.nan,
                    'Barometer': np.nan,
                    'Visibility': np.nan
                }, index=[i])
                df = pd.concat([df.iloc[:i], line, df.iloc[i:]]).reset_index(drop=True)
            i += 1

    df = df.fillna(df.mean())
    return df


table_id = 'wt-his'
final_df = pd.DataFrame()

browser = webdriver.Chrome()
times = [(11, 2019), (12, 2019), (1, 2020), (2, 2020), (3, 2020)]
for dates in times:
    browser.get(edit_url(dates[0], dates[1]))
    for day in range(0, calendar.monthrange(dates[1], dates[0])[1]):
        browser.execute_script(f'cityssi({day});')
        time.sleep(1)

        historic_table = browser.find_element_by_id(table_id)
        tab = pd.read_html(historic_table.get_attribute('outerHTML'))[0]
        tab = edit_dataframe(tab, dates[1], dates[0], day + 1)

        final_df = final_df.append(tab).reset_index(drop=True)


final_df = final_df.drop_duplicates()
print(final_df)
RNN = os.path.dirname(os.path.abspath(__file__))

final_df.to_csv(RNN + '\\data\\temp_nov-mar.csv')
browser.close()
