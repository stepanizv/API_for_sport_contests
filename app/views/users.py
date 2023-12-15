from app import app, CONTESTS, USERS, models, funcs, ENDPOINT
from flask import request, Response, send_file, render_template
from http import HTTPStatus
import json
from app.forms import CreateUserForm
import requests


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
        return Response("This email is already occupied", status=HTTPStatus.CONFLICT)
    user = models.User(first_name, last_name, email, sport)
    USERS.append(user)
    return user.get_response_json(HTTPStatus.CREATED)


@app.get("/users/<int:user_id>")
def get_users(user_id):
    # returns the data of a User-type object in json format
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return user.get_response_json(HTTPStatus.OK)


@app.post("/users/<int:user_id>/assigncont")
def users_assigncont(user_id):
    # assigns a contest to a user
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    contest_id = int(data["id"])
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
    return user.get_response_json(HTTPStatus.CREATED)


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
        return send_file("static/leaderboard.png", mimetype="image/gif")
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    # returns the data of a User-type object in json format
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    user.status = models.User_status.DELETED.value
    user.remove_from_all_contests()
    return user.get_response_json(HTTPStatus.NO_CONTENT)


@app.route('/front/user/<int:user_id>')
def front_get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return render_template('get_user.html', user=user, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/user/create', methods=['GET', 'POST'])
def front_users_create():
    user_data = None
    form = CreateUserForm()
    if form.validate_on_submit():
        user_data = dict()
        user_data['first_name'] = form.first_name.data
        user_data['last_name'] = form.last_name.data
        user_data['email'] = form.email.data
        user_data['sport'] = form.sport.data
        response = requests.post(f'{ENDPOINT}/users/create', json=user_data)
        if response.status_code == HTTPStatus.CONFLICT:
            return "The entered email is occupied!"
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return "Invalid email entered!"
    return render_template('create_user_form.html', form=form, user_data=user_data, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/user/<int:user_id>/assigncont', methods=['GET', 'POST'])
def front_user_assigncont(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return render_template('user_assigncont.html', user=user, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/user/<int:user_id>/assigned/<int:contest_id>', methods=['GET', 'POST'])
def front_user_assigned(user_id, contest_id):
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    contest = CONTESTS[contest_id]
    requests.post(f'{ENDPOINT}/users/{user_id}/assigncont',
                  json={"id": contest_id})
    return render_template('user_cont_assigned.html', user=user, contest=contest, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/front/users/leaderboard/<type>', methods=['GET', 'POST'])
def front_users_leaderboard(type):
    users_list = funcs.get_users_leaderboard()
    requests.get(f'{ENDPOINT}/users/leaderboard', json={'type': type})
    return render_template('get_leaderboard.html', type=type, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS, users_list=users_list)


@app.route('/front/user/<int:user_id>/delete', methods=["GET", "POST"])
def front_delete_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("Invalid user id entered", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    requests.delete(f"{ENDPOINT}/users/{user_id}")
    return render_template('deleted_user.html', user=user, USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)


@app.route('/temp')
def temp():
    return render_template('index.html', USERS=funcs.get_valid_users(), CONTESTS=CONTESTS)
