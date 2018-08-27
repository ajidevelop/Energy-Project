import pandas as pd
from API.database.database_connect import db

start_date, end_date = '1/11/12', '1/12/12'
d = pd.read_sql_table('day_usage', db.app.config['SQLALCHEMY_DATABASE_URI'], index_col='did')
f = d[(d['uid'] == 52) & (d['day'] == 31)]
dates = d[(d['date'] >= start_date) & (d['date'] <= end_date)]
print(d['year'].iloc[0])
