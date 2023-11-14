from app import app, CONTESTS, USERS, models, funcs
from flask import request, Response, send_file
import json
from http import HTTPStatus


@app.post("/users/create")
def users_create():
    # creates a User-type object
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    sport = data["sport"]
    if not models.User.is_valid_email(email):
        return Response("Invalid email entered", status=HTTPStatus.BAD_REQUEST)
    if models.User.is_email_occupied(email):
        return Response("This email is already occupied", status=HTTPStatus.BAD_REQUEST)
    user = models.User(first_name, last_name, email, sport)
    USERS.append(user)
    return user.get_response_json("CREATED")


@app.get("/users/<int:user_id>")
def get_users(user_id):
    # returns the data of a User-type object in json format
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return user.get_response_json("OK")


@app.post("/users/<int:user_id>/assigncont")
def users_assigncont(user_id):
    # assigns a contest to a user
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    contest_id = data["id"]
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.is_finished():
        return Response("This contest is finished. Try another one", status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
    if user.sport != contest.sport:
        return Response(
            f"{user.sport} sportsman cannot participate in {contest.sport} contest",
            status=HTTPStatus.BAD_REQUEST,
        )
    if contest_id in user.contests:
        return Response("This user already assigned to this contest", status=HTTPStatus.OK)
    user.contests.append(contest_id)
    contest.participants.append(user_id)
    return user.get_response_json("CREATED")


@app.get("/users/<int:user_id>/contests")
def users_contests(user_id):
    # returns the data of the user's contests in json format
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return user.get_contests_json()


@app.get("/users/leaderboard")
def users_leaderboard():
    # returns the leaderboard of all users in the requested order and format (list or graph)
    data = request.get_json()
    type = data["type"]
    if type == "list":
        sort = data["sort"]

        if sort not in ("asc", "desc"):
            return Response(
                "Invalid leaderboard type entered", status=HTTPStatus.BAD_REQUEST
            )

        users = funcs.get_users_leaderboard(sort)
        response = Response(
            json.dumps({"users": [user.convert_to_dict() for user in users]}),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif type == "graph":
        funcs.create_graph()
        return send_file("leaderboard.png", mimetype="image/gif")
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    # returns the data of a User-type object in json format
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    user.status = models.User_status.DELETED.value
    return user.get_response_json("OK")
