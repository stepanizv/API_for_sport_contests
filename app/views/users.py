from app import app, CONTESTS, USERS, models, funcs
from flask import request, Response, send_file
import json
from http import HTTPStatus


@app.post("/users/create")
def users_create():
    # creates a User-type object
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    sport = data["sport"]
    contests = []
    if not models.User.is_valid_email(email) or models.User.is_email_occupied(email):
        return Response("An invalid email entered", status=HTTPStatus.BAD_REQUEST)
    user = models.User(id, first_name, last_name, email, sport, contests)
    USERS.append(user)
    response = Response(
        json.dumps(user.convert_to_dict()),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_users(user_id):
    # returns the data of a User-type object in json format
    if not models.User.is_valid_id(user_id):
        return Response("An invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(user.convert_to_dict()),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/users/<int:user_id>/assigncont")
def users_assigncont(user_id):
    # assigns a contest to a user
    if not models.User.is_valid_id(user_id):
        return Response("An invalid user id entered", status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    contest_id = int(data["id"])
    if not models.Contest.is_valid_id(contest_id):
        return Response("An invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    contest = CONTESTS[contest_id]
    if user.sport != contest.sport:
        return Response(
            f"{user.sport} sportsman cannot participate in {contest.sport}",
            status=HTTPStatus.BAD_REQUEST,
        )
    if contest.is_finished():
        return Response(
            f"{contest.id} is already finished", status=HTTPStatus.BAD_REQUEST
        )
    if contest_id not in user.contests:
        user.contests.append(contest_id)
        contest.participants.append(user_id)
    response = Response(
        json.dumps(user.convert_to_dict()),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/contests")
def users_contests(user_id):
    # returns the data of the user's contests in json format
    if not models.User.is_valid_id(user_id):
        return Response("An invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user_contests = []
    for cont in CONTESTS:
        if user_id in cont.participants:
            user_contests.append(cont)
    if len(user_contests) == 0:
        return Response(
            f"The user {user_id} has no actual contests", status=HTTPStatus.OK
        )
    response = Response(
        json.dumps(
            {"contests": [contest.convert_to_dict() for contest in user_contests]}
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def users_leaderboard():
    # returns the leaderboard of all users in the requested order and format (list or graph)
    data = request.get_json()
    type = data["type"]
    if type == "list":
        sort = data["sort"]
        if sort in ("asc", "desc"):
            users = USERS.copy()
            if sort == "asc":
                users.sort(key=lambda user: len(user.contests))
            else:
                users.sort(key=lambda user: len(user.contests), reverse=True)
        else:
            return Response(
                "Invalid leaderboard type entered", status=HTTPStatus.BAD_REQUEST
            )

        response = Response(
            json.dumps({"users": [user.convert_to_dict() for user in users]}),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif type == "graph":
        funcs.create_graph(USERS)
        return send_file("leaderboard.png", mimetype="image/gif")
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
