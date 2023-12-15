from app import app, funcs, CONTESTS, USERS, models, ENDPOINT
from flask import request, Response, render_template
from http import HTTPStatus
from app.forms import CreateContestForm
import requests
import random


@app.post("/contests/create")
def contests_create():
    # creates a Contest-type object
    data = request.get_json()
    name = data["name"]
    if not models.Contest.is_valid_name(name):
        return Response("Contest already created", status=HTTPStatus.CONFLICT)
    sport = data["sport"]
    contest = models.Contest(name, sport)
    CONTESTS.append(contest)
    return contest.get_response_json(HTTPStatus.CREATED)


@app.get("/contests/<int:contest_id>")
def get_contests(contest_id):
    # returns the data of a Contest-type object in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    return contest.get_response_json(HTTPStatus.OK)


@app.post("/contests/<int:contest_id>/assignuser")
def contests_assignuser(contest_id):
    # assigns a user to a contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.is_finished():
        return Response("This contest is finished. Try another one", status=HTTPStatus.BAD_REQUEST)
    data = request.get_json()
    user_id = int(data["id"])
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
    return contest.get_response_json(HTTPStatus.CREATED)


@app.route("/contests/<int:contest_id>/finish", methods=["GET", "POST"])
def contests_finish(contest_id):
    # assignes the "Finished" status to the contest
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.is_finished():
        return Response("The contest is already finished", status=HTTPStatus.BAD_REQUEST)
    winner_id = request.get_json()["winner"]
    if not contest.is_valid_winner(winner_id):
        return Response("Invalid contest winner", status=HTTPStatus.BAD_REQUEST)
    contest.finish(winner_id)
    return contest.get_response_json(HTTPStatus.CREATED)


@app.get("/contests/<int:contest_id>/participants")
def contests_participants(contest_id):
    # returns the data of the contest's participants in json format
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    cont_participants = funcs.get_valid_users(USERS=contest.participants)
    if cont_participants == []:
        return Response(
            f"The contest {contest_id} has no participants", status=HTTPStatus.OK
        )
    return contest.get_participants_json()


@app.route('/front/contest/create', methods=['GET', 'POST'])
def front_contests_create():
    contest_data = None
    form = CreateContestForm()
    if form.validate_on_submit():
        contest_data = dict()
        contest_data['name'] = form.name.data
        contest_data['sport'] = form.sport.data
        response = requests.post(
            f'{ENDPOINT}/contests/create', json=contest_data)
        if response.status_code == HTTPStatus.CONFLICT:
            return "This contest already exists! Create a different one"
    return render_template('create_contest_form.html', form=form, contest_data=contest_data, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/contest/<int:contest_id>')
def front_get_contest(contest_id):
    # users_all - is the list of Users WITH deleted ones (as it points to the common USERS list)
    if not models.Contest.is_valid_id(contest_id):
        return Response("Invalid contest id entered", status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    winner_id = contest.winner
    winner = USERS[winner_id] if (contest.is_finished(
    ) and models.User.is_valid_id(winner_id)) else None
    return render_template('get_contest.html', winner=winner, contest=contest,
                           users_all=USERS, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/contest/<int:contest_id>/finish', methods=["GET", "POST"])
def front_contest_finish(contest_id):
    contest = CONTESTS[contest_id]
    if len(contest.participants) == 0:
        return "You cannot finish the contest without any participants! Wait for the action at first!"
    random_winner_id = random.choice(contest.participants)
    winner = USERS[random_winner_id]
    requests.post(f'{ENDPOINT}/contests/{contest_id}/finish',
                  json={"winner": random_winner_id})
    return render_template('contest_finished.html', contest=contest, winner=winner, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)
