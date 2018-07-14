import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql+pymysql://python:pyth0n_@ccess@GOSHEN-SPECTRE:3307/db")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    users = db.execute("SELECT * FROM users").fetchall()
    print(users)
    return render_template('index.html', users=users)

@app.route("/book", methods=['POST'])
def book():
    name = request.form.get('name')
    try:
        uid = int(request.form.get('user'))
    except ValueError:
        print("error")

    if db.execute()

index()
