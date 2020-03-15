from flask import Flask
import json
import os

app = Flask(__name__)

WEBAPP = os.path.dirname(os.path.abspath(__file__))
uri = json.load(open(os.path.join(WEBAPP, 'configs/logins.json')))

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = 'unicode'
if app.config['DEBUG']:
    app.config['SQLALCHEMY_DATABASE_URI'] = uri['admin_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = uri['public_uri']
