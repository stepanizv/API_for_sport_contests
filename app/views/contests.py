from app import app, CONTESTS, USERS, models
from flask import request, Response
from http import HTTPStatus


@app.post("/contests/create")
def contests_create():
    # creates a Contest-type object
    data = request.get_json()
    name = data["name"]
    if not models.Contest.is_valid_name(name):
        return Response("Contest already created", status=HTTPStatus.BAD_REQUEST)
    sport = data["sport"]
    contest = models.Contest(name, sport)
    CONTESTS.append(contest)
    return contest.get_response_json("CREATED")


@app.get("/contests/<int:contest_id>")
def get_contests(contest_id):
    # returns the data of a Contest-type object in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    return contest.get_response_json("OK")


@app.post("/contests/<int:contest_id>/assignuser")
def contests_assignuser(contest_id):
    # assigns a user to a contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.is_finished():
        return Response("This contest is finished. Try another one", status=HTTPStatus.BAD_REQUEST)
    data = request.get_json()
    user_id = data["id"]
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    if user.sport != contest.sport:
        return Response(
            f"{user.sport} sportsman cannot participate in {contest.sport} contest",
            status=HTTPStatus.BAD_REQUEST,
        )
    if user_id in contest.participants:
        return Response("This user already assigned to this contest", status=HTTPStatus.OK)
    user.contests.append(contest_id)
    contest.participants.append(user_id)
    return contest.get_response_json("CREATED")


@app.post("/contests/<int:contest_id>/finish")
def contests_finish(contest_id):
    # finishes the contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.is_finished():
        return Response("The contest is already finished", status=HTTPStatus.BAD_REQUEST)
    winner_id = request.get_json()["winner"]
    if not contest.is_valid_winner(winner_id):
        return Response("Invalid contest winner", status=HTTPStatus.BAD_REQUEST)
    contest.finish(winner_id)
    return contest.get_response_json("CREATED")


@app.get("/contests/<int:contest_id>/participants")
def contests_participants(contest_id):
    # returns the data of the contest's participants in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    cont_participants = contest.create_list_of_participants()
    if len(cont_participants) == 0:
        return Response(
            f"The contest {contest_id} has no participants yet", status=HTTPStatus.OK
        )
    return contest.get_participants_json()
