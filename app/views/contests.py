from app import app, CONTESTS, USERS, models,funcs
from flask import request, Response,send_file
import json
from http import HTTPStatus


@app.post("/contests/create")
def contests_create():
    # creates a Contest-type object
    data = request.get_json()
    name = data["name"]
    sport = data["sport"]
    participants = []
    status = models.Status.STARTED
    id = len(CONTESTS)
    winner = "not defined"
    contest = models.Contest(id, name, sport, participants, status, winner)
    CONTESTS.append(contest)
    response = Response(
        json.dumps(contest.convert_to_dict()),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response

@app.get("/contests/<int:contest_id>")
def get_contests(contest_id):
    # returns the data of a Contest-type object in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("An invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    response = Response(
        json.dumps(contest.convert_to_dict()),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

@app.post("/contests/<int:contest_id>/assignuser")
def contests_assignuser(contest_id):
    # assigns a user to a contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("An invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    user_id = int(data["id"])
    if not models.User.is_valid_id(user_id):
        return Response("An invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    contest = CONTESTS[contest_id]
    if user.sport != contest.sport:
        return Response(
            f"{user.sport} sportsman cannot participate in {contest.sport} contest",
            status=HTTPStatus.BAD_REQUEST,
        )
    if contest.is_finished():
        return Response(
            f"{contest.id} is already finished", status=HTTPStatus.BAD_REQUEST
        )
    if user_id not in contest.participants:
        user.contests.append(contest_id)
        contest.participants.append(user_id)
    response = Response(
        json.dumps(contest.convert_to_dict()),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response

@app.post("/contests/<int:contest_id>/finish")
def contests_finish(contest_id):
    # finishes the contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("An invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    data = request.get_json()
    winner = data["winner"]
    if not contest.is_valid_winner(winner):
        return Response("Invalid contest winner", status=HTTPStatus.BAD_REQUEST)
    if contest.status != models.Status.FINISHED:
        contest.winner = winner
        contest.status = models.Status.FINISHED
        funcs.remove_finished_contest(USERS, contest_id)
    response = Response(
        json.dumps(contest.convert_to_dict()),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response

@app.get("/contests/<int:contest_id>/participants")
def contests_participants(contest_id):
    # returns the data of the contest's participants in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("An invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest_participants = []
    for user in USERS:
        if contest_id in user.contests:
            contest_participants.append(user)
    if len(contest_participants) == 0:
        return Response(
            f"The contest {contest_id} has no participants yet", status=HTTPStatus.OK
        )
    response = Response(
        json.dumps(
            {
                "participants": [
                    participant.convert_to_dict() for participant in contest_participants
                ]
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response