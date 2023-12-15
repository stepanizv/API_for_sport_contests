from app import app, USERS, CONTESTS
from flask import render_template


@app.route("/")
def index():
    return render_template('index.html', USERS=USERS, CONTESTS=CONTESTS)
