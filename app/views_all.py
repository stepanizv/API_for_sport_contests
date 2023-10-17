from app import app, USERS, CONTESTS
from flask import Response
from http import HTTPStatus


@app.route("/")
def index():
    # the homepage, where the data of all stored objects is represented
    response = (
        f"<h2>Hello,world!<h2>"
        f"<br>USERS:<br>{'<br>'.join([user.repr() for user in USERS])}<br>"
        f"<br>CONTESTS:<br>{'<br>'.join([contest.repr() for contest in CONTESTS])}"
    )
    return Response(response, HTTPStatus.OK)
