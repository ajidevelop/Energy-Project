from webapp.app_config import app

app = app

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["CACHE_TYPE"] = "null"
